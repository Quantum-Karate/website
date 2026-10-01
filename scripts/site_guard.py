#!/usr/bin/env python3
"""Check the Quantum Karate static site for claim and link rules, and re-check docs/ against the manifest."""

from __future__ import annotations

import hashlib
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
MANIFEST_PATH = ROOT / ".github" / "site-manifest.sha256"

TEXT_SUFFIXES = {".html", ".css", ".js", ".svg"}

# Files that may live under docs/ without a manifest entry.
# CNAME is allowlisted here but still scanned when it is present.
MANIFEST_ALLOWLIST = {
    ".nojekyll",
    "CNAME",
}

# Locked sentences the pages must keep. Apostrophe is U+2019; the dash is U+2014.
STEP_TITLE = "You\u2019re set \u2014 setup stays Paper"
PROMISE = "We don\u2019t fake Practice. We don\u2019t trade until you say so."
DISCLAIMER = "Seduma is not a broker or an investment adviser."
REQUIRED_PAGES = ("index.html", "seduma.html", "facts.html", "contact.html")

# The delivered pages do not use "autonomous" at all, so there is no
# exact-sentence exemption. A negated sentence is still a match.
_SENTENCE_ALLOWLIST: frozenset[str] = frozenset()

_NAE_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:N\.A\.E\.?|NAE)(?![A-Za-z0-9])",
    re.IGNORECASE,
)
# Standalone entity suffix, with or without a following period.
_ENTITY_RE = re.compile(r"\bLLC\b|\bInc\b", re.IGNORECASE)
_PHRASES = (
    "auto-run",
    "autopilot",
    "set-and-forget",
    "set and forget",
    "trades for you",
    "guaranteed",
    "expected edge",
    "autonomous",
)
_PHRASE_RES = tuple(re.compile(re.escape(phrase), re.IGNORECASE) for phrase in _PHRASES)
# Boundaries keep these from matching nearby words such as "hands offset".
_BOUNDED_PHRASES = (
    "hands-off",
    "hands off",
)
_BOUNDED_PHRASE_RES = tuple(
    re.compile(r"(?<![A-Za-z0-9])" + re.escape(phrase) + r"(?![A-Za-z0-9])", re.IGNORECASE)
    for phrase in _BOUNDED_PHRASES
)
_ARR_RE = re.compile(r"(?<![A-Za-z0-9])ARR(?![A-Za-z0-9])", re.IGNORECASE)
_PERCENT_RETURN_RE = re.compile(
    r"\d+(?:\.\d+)?%\s*(?:return|gain|profit|apy|apr)\b",
    re.IGNORECASE,
)
_RETURN_OF_RE = re.compile(r"\breturns?\s+of\b", re.IGNORECASE)
_COUNT_RE = re.compile(
    r"\d[\d,]*\+?\s*(?:customers|users|traders|clients)\b",
    re.IGNORECASE,
)

_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
_BR_RE = re.compile(r"<br\b[^>]*>", re.IGNORECASE)
_INLINE_TAG_RE = re.compile(
    r"</?(?:a|abbr|b|bdi|bdo|cite|code|data|dfn|em|i|kbd|mark|q|s|samp|small|span|strong|sub|sup|time|u|var)\b[^>]*>",
    re.IGNORECASE,
)
_TAG_RE = re.compile(r"<[^>]*>", re.DOTALL)
_SCRIPT_BLOCK_RE = re.compile(r"<script\b[^>]*>(.*?)</script>", re.IGNORECASE | re.DOTALL)
_STYLE_BLOCK_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.IGNORECASE | re.DOTALL)
_WS_RE = re.compile(r"\s+")

_CLAIM_ATTRS = {"content", "title", "aria-label", "alt", "placeholder"}
_ATTR_RE = re.compile(
    r"""(?P<name>[\w:-]+)\s*=\s*(?:"(?P<dq>[^"]*)"|'(?P<sq>[^']*)'|(?P<uq>[^\s"'=<>`]+))""",
    re.IGNORECASE,
)
_REF_ATTR_RE = re.compile(
    r"""(?<![\w-])(?P<name>srcset|href|src|action)\s*=\s*(?:"(?P<dq>[^"]*)"|'(?P<sq>[^']*)'|(?P<uq>[^\s"'=<>`]+))""",
    re.IGNORECASE,
)
_STYLE_ATTR_RE = re.compile(
    r"""(?<![\w-])style\s*=\s*(?:"([^"]*)"|'([^']*)')""",
    re.IGNORECASE,
)
_CSS_URL_RE = re.compile(
    r"""url\(\s*(?:'(?P<sq>[^']*)'|"(?P<dq>[^"]*)"|(?P<uq>[^)\s]*))\s*\)""",
    re.IGNORECASE,
)
_CSS_IMPORT_RE = re.compile(r"@import\b([^;]*)", re.IGNORECASE | re.DOTALL)
_JS_FETCH_RE = re.compile(r"""\bfetch\s*\(\s*(['"`])(.*?)\1""", re.DOTALL)
_JS_IMPORT_RE = re.compile(r"""\bimport\s*\(\s*(['"`])(.*?)\1""", re.DOTALL)
_JS_XHR_RE = re.compile(
    r"""\.open\s*\(\s*(['"`])[^'"`]*\1\s*,\s*(['"`])(.*?)\2""",
    re.DOTALL,
)
_HOSTNAME_RE = re.compile(
    r"(?=.{1,253}\Z)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\Z",
    re.IGNORECASE,
)


def strip_html_comments(text: str) -> str:
    return _HTML_COMMENT_RE.sub(" ", text)


def strip_css_comments(text: str) -> str:
    return _CSS_COMMENT_RE.sub(" ", text)


def collapse_ws(text: str) -> str:
    return _WS_RE.sub(" ", text).strip()


def _attr_value(match: re.Match[str]) -> str:
    return next(group for group in (match.group("dq"), match.group("sq"), match.group("uq")) if group is not None)


def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def normalize_html_text(raw: str) -> str:
    """Visible text: inline tags collapse, entities decode, whitespace collapses."""
    text = html.unescape(raw)
    text = _INLINE_TAG_RE.sub("", text)
    text = _BR_RE.sub(" ", text)
    text = _TAG_RE.sub(" ", text)
    text = html.unescape(text)
    return collapse_ws(text)


def normalize_plain(text: str) -> str:
    return collapse_ws(html.unescape(text))


def claim_attribute_values(raw: str) -> list[str]:
    values: list[str] = []
    for match in _ATTR_RE.finditer(raw):
        name = match.group("name").lower()
        if name in _CLAIM_ATTRS or name.startswith("og:"):
            values.append(_attr_value(match))
    return values


def html_claim_texts(raw: str) -> list[str]:
    style_blocks = [match.group(1) for match in _STYLE_BLOCK_RE.finditer(raw)]
    scripts = [match.group(1) for match in _SCRIPT_BLOCK_RE.finditer(raw)]
    body = _STYLE_BLOCK_RE.sub(" ", raw)
    body = _SCRIPT_BLOCK_RE.sub(" ", body)
    texts = [normalize_html_text(body)]
    texts.extend(normalize_plain(value) for value in claim_attribute_values(raw))
    for block in style_blocks:
        texts.append(normalize_plain(strip_css_comments(block)))
    for match in _STYLE_ATTR_RE.finditer(raw):
        value = next(group for group in match.groups() if group is not None)
        texts.append(normalize_plain(strip_css_comments(value)))
    texts.extend(normalize_plain(script) for script in scripts)
    return texts


def reference_problem(value: str) -> str | None:
    value = html.unescape(value).strip()
    if not value or value.startswith("#") or value.lower().startswith("mailto:"):
        return None
    lowered = value.lower()
    if lowered.startswith(("http://", "https://", "//")):
        return "external"
    if value.startswith("/"):
        return "root-relative"
    return None


def _srcset_urls(value: str) -> list[str]:
    urls: list[str] = []
    for part in html.unescape(value).split(","):
        token = part.strip().split()
        if token:
            urls.append(token[0])
    return urls


def _css_urls(css: str) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for match in _CSS_URL_RE.finditer(css):
        url = next(group for group in match.groups() if group is not None)
        found.append(("url", url))
    for match in _CSS_IMPORT_RE.finditer(css):
        body = match.group(1)
        url_match = _CSS_URL_RE.search(body)
        if url_match:
            url = next(group for group in url_match.groups() if group is not None)
            found.append(("@import", url))
            continue
        quoted = re.search(r"""['"]([^'"]+)['"]""", body)
        if quoted:
            found.append(("@import", quoted.group(1)))
    return found


def _reference_findings(kind: str, value: str) -> list[str]:
    problem = reference_problem(value)
    if problem is None:
        return []
    shown = html.unescape(value).strip()
    return [f"{problem} {kind} value: {shown}"]


def html_reference_findings(raw: str) -> list[str]:
    findings: list[str] = []
    for match in _REF_ATTR_RE.finditer(raw):
        name = match.group("name").lower()
        value = _attr_value(match)
        if name == "srcset":
            for url in _srcset_urls(value):
                findings.extend(_reference_findings("srcset", url))
        else:
            findings.extend(_reference_findings(name, value))
    return findings


def css_reference_findings(css: str) -> list[str]:
    findings: list[str] = []
    for kind, url in _css_urls(strip_css_comments(css)):
        findings.extend(_reference_findings(kind, url))
    return findings


def js_reference_findings(source: str) -> list[str]:
    findings: list[str] = []
    for match in _JS_FETCH_RE.finditer(source):
        findings.extend(_reference_findings("fetch", match.group(2)))
    for match in _JS_IMPORT_RE.finditer(source):
        findings.extend(_reference_findings("import", match.group(2)))
    for match in _JS_XHR_RE.finditer(source):
        findings.extend(_reference_findings("XMLHttpRequest", match.group(3)))
    return findings


def embedded_reference_findings(raw: str) -> list[str]:
    findings: list[str] = []
    for match in _STYLE_BLOCK_RE.finditer(raw):
        findings.extend(css_reference_findings(match.group(1)))
    for match in _STYLE_ATTR_RE.finditer(raw):
        value = next(group for group in match.groups() if group is not None)
        findings.extend(css_reference_findings(html.unescape(value)))
    for match in _SCRIPT_BLOCK_RE.finditer(raw):
        findings.extend(js_reference_findings(match.group(1)))
    return findings


def _sentence_allowed(text: str, start: int, end: int) -> bool:
    if not _SENTENCE_ALLOWLIST:
        return False
    left = max(text.rfind(".", 0, start), text.rfind("!", 0, start), text.rfind("?", 0, start))
    right_candidates = [pos for pos in (text.find(".", end), text.find("!", end), text.find("?", end)) if pos != -1]
    right = min(right_candidates) if right_candidates else len(text)
    sentence = text[left + 1 : right + 1].strip()
    return sentence in _SENTENCE_ALLOWLIST


def phrase_findings(text: str) -> list[str]:
    findings: list[str] = []
    for match in _NAE_RE.finditer(text):
        if not _sentence_allowed(text, match.start(), match.end()):
            findings.append(f"standalone abbreviation: {match.group(0)}")
    for match in _ENTITY_RE.finditer(text):
        if not _sentence_allowed(text, match.start(), match.end()):
            findings.append(f"entity suffix: {match.group(0)}")
    for phrase, pattern in zip(_PHRASES, _PHRASE_RES):
        for match in pattern.finditer(text):
            if not _sentence_allowed(text, match.start(), match.end()):
                findings.append(f"banned phrase: {phrase}")
                break
    for phrase, pattern in zip(_BOUNDED_PHRASES, _BOUNDED_PHRASE_RES):
        for match in pattern.finditer(text):
            if not _sentence_allowed(text, match.start(), match.end()):
                findings.append(f"banned phrase: {phrase}")
                break
    for match in _ARR_RE.finditer(text):
        if not _sentence_allowed(text, match.start(), match.end()):
            findings.append("banned phrase: ARR")
            break
    for match in _PERCENT_RETURN_RE.finditer(text):
        if not _sentence_allowed(text, match.start(), match.end()):
            findings.append(f"banned phrase: {match.group(0)}")
            break
    for match in _RETURN_OF_RE.finditer(text):
        if not _sentence_allowed(text, match.start(), match.end()):
            findings.append(f"banned phrase: {match.group(0)}")
            break
    for match in _COUNT_RE.finditer(text):
        if not _sentence_allowed(text, match.start(), match.end()):
            findings.append(f"banned phrase: {match.group(0)}")
            break
    return findings


def findings_for_text(suffix: str, content: str) -> list[str]:
    """Return claim and link findings for one deployable text file's contents."""
    suffix = suffix.lower()
    findings: list[str] = []
    if suffix in {".html", ".svg"}:
        raw = strip_html_comments(content)
        findings.extend(html_reference_findings(raw))
        findings.extend(embedded_reference_findings(raw))
        for text in html_claim_texts(raw):
            findings.extend(phrase_findings(text))
    elif suffix == ".css":
        raw = strip_css_comments(content)
        findings.extend(css_reference_findings(raw))
        findings.extend(phrase_findings(normalize_plain(raw)))
    elif suffix == ".js":
        findings.extend(js_reference_findings(content))
        findings.extend(phrase_findings(normalize_plain(content)))
    else:
        findings.extend(phrase_findings(normalize_plain(content)))
    return _unique(findings)


def cname_findings(content: str) -> list[str]:
    """CNAME must be one bare hostname, and that hostname is still claim-checked."""
    body = content[:-1] if content.endswith("\n") else content
    if body.endswith("\r"):
        body = body[:-1]
    if (
        not body
        or "\n" in body
        or "\r" in body
        or re.search(r"[A-Za-z]", body) is None
        or _HOSTNAME_RE.fullmatch(body) is None
    ):
        return ["CNAME: must be a single bare hostname line"]
    return [f"CNAME: {item}" for item in phrase_findings(normalize_plain(body))]


def required_findings(pages: dict[str, str]) -> list[str]:
    findings: list[str] = []
    seduma = pages.get("seduma.html", "")
    if STEP_TITLE not in seduma:
        findings.append(f"seduma.html: missing required text: {STEP_TITLE}")
    if PROMISE not in seduma:
        findings.append(f"seduma.html: missing required text: {PROMISE}")
    for name in REQUIRED_PAGES:
        if DISCLAIMER not in pages.get(name, ""):
            findings.append(f"{name}: missing required text: {DISCLAIMER}")
    return findings


def check_required(docs_dir: Path) -> list[str]:
    pages: dict[str, str] = {}
    for name in REQUIRED_PAGES:
        path = docs_dir / name
        if path.is_file():
            try:
                pages[name] = path.read_text(encoding="utf-8")
            except UnicodeError:
                pages[name] = ""
        else:
            pages[name] = ""
    return required_findings(pages)


def scan_docs(docs_dir: Path) -> list[str]:
    findings: list[str] = []
    if not docs_dir.is_dir():
        return [f"missing docs directory: {docs_dir}"]
    for path in sorted(p for p in docs_dir.rglob("*") if p.is_file()):
        rel = path.relative_to(docs_dir).as_posix()
        if path.name == "CNAME":
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeError:
                findings.append(f"{rel}: not valid utf-8")
                continue
            for item in cname_findings(content):
                findings.append(f"{rel}: {item}")
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeError:
            findings.append(f"{rel}: not valid utf-8")
            continue
        for item in findings_for_text(path.suffix, content):
            findings.append(f"{rel}: {item}")
    return findings


def _manifest_entries(manifest_text: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for line_no, raw in enumerate(manifest_text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) != 2 or len(parts[0]) != 64:
            entries.append(("", f"malformed manifest line {line_no}"))
            continue
        digest, rel = parts
        if rel.startswith("*"):
            rel = rel[1:]
        if rel.startswith("./"):
            rel = rel[2:]
        entries.append((digest.lower(), rel))
    return entries


def check_manifest(docs_dir: Path, manifest_path: Path) -> list[str]:
    """Re-check docs/ against the manifest. Allowlisted extras may be absent from it."""
    findings: list[str] = []
    if not manifest_path.is_file():
        return [f"missing manifest: {manifest_path}"]
    if not docs_dir.is_dir():
        return [f"missing docs directory: {docs_dir}"]

    listed: set[str] = set()
    for digest, rel in _manifest_entries(manifest_path.read_text(encoding="utf-8")):
        if not digest:
            findings.append(rel)
            continue
        listed.add(rel)
        path = docs_dir / rel
        if not path.is_file():
            findings.append(f"manifest file missing: {rel}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest:
            findings.append(f"manifest hash mismatch: {rel}")

    for path in sorted(p for p in docs_dir.rglob("*") if p.is_file()):
        rel = path.relative_to(docs_dir).as_posix()
        if rel not in listed and rel not in MANIFEST_ALLOWLIST:
            findings.append(f"file not in manifest or allowlist: {rel}")
    return findings


def run_guard(docs_dir: Path = DOCS_DIR, manifest_path: Path = MANIFEST_PATH) -> list[str]:
    return scan_docs(docs_dir) + check_required(docs_dir) + check_manifest(docs_dir, manifest_path)


def main(argv: list[str] | None = None) -> int:
    del argv  # paths are fixed to this repository
    findings = run_guard()
    if findings:
        print("site guard: failed")
        for item in findings:
            print(item)
        return 1
    print("site guard: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
