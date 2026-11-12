#!/usr/bin/env python3
"""Check the Quantum Karate static site for claim and link rules, and re-check docs/ against the manifest."""

from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from pathlib import Path

from i18n_data import (
    LOCALES,
    PAGES as LOCALE_PAGES,
    allowed_urls,
    fill,
    load_strings,
    page_url,
    payhip_button_url,
)

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
# Unicode letters keep this off words such as French "arrêt".
_ARR_RE = re.compile(r"(?<!\w)ARR(?!\w)", re.IGNORECASE)
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


# Payhip, plus each locale page. Every other absolute URL stays blocked.
_ALLOWED_EXTERNAL_REFS = allowed_urls()
_PAYHIP = "https://payhip.com/b/K7UaW"


def reference_problem(value: str) -> str | None:
    value = html.unescape(value).strip()
    if not value or value.startswith("#") or value.lower().startswith("mailto:"):
        return None
    if value in _ALLOWED_EXTERNAL_REFS:
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


_JSONLD_RE = re.compile(
    r"""<script\b[^>]*type\s*=\s*["']application/ld\+json["'][^>]*>(.*?)</script>""",
    re.IGNORECASE | re.DOTALL,
)
_JSONLD_CONTEXT = "https://schema.org"
_SCHEMA_TYPES = frozenset({
    "Organization",
    "Product",
    "SoftwareApplication",
    "Offer",
})
_RATING_KEYS = frozenset({"aggregaterating", "review", "ratingvalue", "reviewcount"})
_ORG_DESCRIPTION = (
    "Quantum Karate\u2122 builds technology the way a martial artist trains: "
    "with precision, discipline, and attention to the smallest detail."
)
_PRODUCT_DESCRIPTION = (
    "Practice your own trading rules in a paper trading simulator on your own computer. "
    "$49 once, no subscription. Simulated results only. Not a broker."
)
_OPERATING_SYSTEM = "Windows, macOS, Linux"
_LLM_FILES = ("llms.txt", "llms-full.txt")


def parse_jsonld(raw: str) -> list[object]:
    """Parse every JSON-LD block. Raises json.JSONDecodeError if one does not parse."""
    return [json.loads(match.group(1)) for match in _JSONLD_RE.finditer(raw)]


def _type_set(node: object) -> set[str] | None:
    if not isinstance(node, dict):
        return None
    raw_type = node.get("@type")
    if isinstance(raw_type, str):
        return {raw_type}
    if isinstance(raw_type, list) and raw_type and all(isinstance(item, str) for item in raw_type):
        return set(raw_type)
    return set()


def _rating_keys(node: object) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key.lower() in _RATING_KEYS:
                found.append(key)
            found.extend(_rating_keys(value))
    elif isinstance(node, list):
        for item in node:
            found.extend(_rating_keys(item))
    return found


def _used_types(node: object) -> set[str]:
    found: set[str] = set()
    if isinstance(node, dict):
        types = _type_set(node)
        if types:
            found.update(types)
        for value in node.values():
            found.update(_used_types(value))
    elif isinstance(node, list):
        for item in node:
            found.update(_used_types(item))
    return found


def jsonld_findings(pages: dict[str, str]) -> list[str]:
    """Organization on Home, Product and SoftwareApplication with an Offer on Seduma."""
    findings: list[str] = []
    parsed: dict[str, list[object]] = {}
    for name in REQUIRED_PAGES:
        try:
            parsed[name] = parse_jsonld(pages.get(name, ""))
        except json.JSONDecodeError:
            findings.append(f"{name}: JSON-LD does not parse")
            parsed[name] = []

    for name in ("facts.html", "contact.html"):
        if parsed[name]:
            findings.append(f"{name}: unexpected JSON-LD")

    home = parsed["index.html"]
    if len(home) != 1 or not isinstance(home[0], dict):
        findings.append("index.html: expected one Organization JSON-LD object")
    else:
        org = home[0]
        if org.get("@context") != _JSONLD_CONTEXT:
            findings.append("index.html: JSON-LD @context must be https://schema.org")
        if _type_set(org) != {"Organization"}:
            findings.append("index.html: JSON-LD @type must be Organization")
        if org.get("name") != "Quantum Karate":
            findings.append("index.html: Organization name must be Quantum Karate")
        if org.get("url") != "https://quantum-karate.github.io/website/index.html":
            findings.append("index.html: Organization url must be the Home page")
        if org.get("slogan") != "Precision is Power":
            findings.append("index.html: Organization slogan must be Precision is Power")
        if org.get("description") != _ORG_DESCRIPTION:
            findings.append("index.html: Organization description must match the Home page")
        if org.get("logo") != "https://quantum-karate.github.io/website/assets/logo-horizontal-transparent.svg":
            findings.append("index.html: Organization logo must be the site logo")
        expected_keys = {"@context", "@type", "name", "url", "slogan", "description", "logo"}
        if set(org) != expected_keys:
            findings.append("index.html: Organization JSON-LD has unexpected fields")
        if _rating_keys(org):
            findings.append("index.html: JSON-LD must not include ratings or reviews")
        unknown = _used_types(org) - _SCHEMA_TYPES
        if unknown:
            findings.append(f"index.html: JSON-LD uses unknown schema.org types: {', '.join(sorted(unknown))}")

    product_blocks = parsed["seduma.html"]
    if len(product_blocks) != 1 or not isinstance(product_blocks[0], dict):
        findings.append("seduma.html: expected one Product JSON-LD object")
    else:
        product = product_blocks[0]
        if product.get("@context") != _JSONLD_CONTEXT:
            findings.append("seduma.html: JSON-LD @context must be https://schema.org")
        if _type_set(product) != {"Product", "SoftwareApplication"}:
            findings.append("seduma.html: JSON-LD @type must be Product and SoftwareApplication")
        if product.get("name") != "Seduma Trade":
            findings.append("seduma.html: product name must be Seduma Trade")
        if product.get("operatingSystem") != _OPERATING_SYSTEM:
            findings.append("seduma.html: operatingSystem must be Windows, macOS, Linux")
        if product.get("description") != _PRODUCT_DESCRIPTION:
            findings.append("seduma.html: product description must match the page")
        if product.get("url") != "https://quantum-karate.github.io/website/seduma.html":
            findings.append("seduma.html: product url must be the Seduma page")
        expected_keys = {"@context", "@type", "name", "operatingSystem", "description", "url", "offers"}
        if set(product) != expected_keys:
            findings.append("seduma.html: product JSON-LD has unexpected fields")
        offer = product.get("offers")
        offer_keys = {"@type", "price", "priceCurrency", "url", "availability"}
        if not isinstance(offer, dict) or set(offer) != offer_keys:
            findings.append("seduma.html: Offer must be one object with price, currency, url, and availability")
        elif (
            offer.get("@type") != "Offer"
            or offer.get("price") != "49.00"
            or offer.get("priceCurrency") != "USD"
            or offer.get("url") != "https://payhip.com/b/K7UaW"
            or offer.get("availability") != "https://schema.org/InStock"
        ):
            findings.append("seduma.html: Offer must be 49.00 USD, InStock, at the Payhip listing")
        if _rating_keys(product):
            findings.append("seduma.html: JSON-LD must not include ratings or reviews")
        unknown = _used_types(product) - _SCHEMA_TYPES
        if unknown:
            findings.append(f"seduma.html: JSON-LD uses unknown schema.org types: {', '.join(sorted(unknown))}")
    return findings


def check_jsonld(docs_dir: Path) -> list[str]:
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
    return jsonld_findings(pages)


def llm_copy_findings(docs_dir: Path) -> list[str]:
    """The plain-language summaries stay inside the same claim rules as the pages."""
    findings: list[str] = []
    if not docs_dir.is_dir():
        return [f"missing docs directory: {docs_dir}"]
    for name in _LLM_FILES:
        path = docs_dir / name
        if not path.is_file():
            findings.append(f"missing {name}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            findings.append(f"{name}: not valid utf-8")
            continue
        for item in findings_for_text(".txt", text):
            findings.append(f"{name}: {item}")
        if "Seduma Trade Dojo" in text:
            findings.append(f"{name}: old product name")
    return findings


def check_i18n(docs_dir: Path) -> list[str]:
    """Lang, direction, hreflang, disclaimer, and the single Payhip CTA for every locale."""
    findings: list[str] = []
    try:
        strings = load_strings()
    except ValueError as exc:
        return [str(exc)]
    expected_links = len(LOCALES) + 1
    for code, folder, direction, _name in LOCALES:
        data = strings[code]
        disclaimer = fill(data["disclaimer"], code, html_mode=True)
        promise = fill(data["promise"], code, html_mode=True)
        step_ready = fill(data["step_ready"], code, html_mode=True)
        for page in LOCALE_PAGES:
            rel = f"{folder}/{page}" if folder else page
            path = docs_dir / rel
            if not path.is_file():
                findings.append(f"missing locale page: {rel}")
                continue
            text = path.read_text(encoding="utf-8")
            if f'<html lang="{code}"' not in text:
                findings.append(f"{rel}: html lang must be {code}")
            if f'dir="{direction}"' not in text:
                findings.append(f"{rel}: html dir must be {direction}")
            if text.count('<link rel="alternate" hreflang="') != expected_links:
                findings.append(f"{rel}: hreflang alternate count")
            if 'hreflang="x-default"' not in text:
                findings.append(f"{rel}: missing x-default")
            for alt, alt_folder, _alt_dir, _alt_name in LOCALES:
                href = page_url(alt_folder, page)
                if f'hreflang="{alt}"' not in text or href not in text:
                    findings.append(f"{rel}: missing hreflang {alt}")
            if disclaimer not in text:
                findings.append(f"{rel}: missing translated disclaimer")
            if "Neural Agency Engine" not in text:
                findings.append(f"{rel}: Neural Agency Engine must stay spelled out")
            if "Seduma Trade Dojo" in text:
                findings.append(f"{rel}: old product name")
            if page == "seduma.html":
                if promise not in text:
                    findings.append(f"{rel}: missing translated promise")
                if step_ready not in text:
                    findings.append(f"{rel}: missing translated setup line")
            button = payhip_button_url(folder, page)
            button_count = text.count(f'href="{button}"')
            bare_count = text.count(f'href="{_PAYHIP}"')
            if page == "facts.html":
                if button_count or bare_count:
                    findings.append(f"{rel}: facts page must not link to Payhip")
            elif button_count != 1 or bare_count:
                findings.append(f"{rel}: Payhip button must be the tracked listing link, once")
            title = re.search(r"<title>([^<]*)</title>", text)
            og_title = re.search(r'<meta property="og:title" content="([^"]*)"', text)
            for kind, match in (("title", title), ("og:title", og_title)):
                if match and "Dojo" in match.group(1):
                    findings.append(f"{rel}: {kind} still names the product as a Dojo")
            if page == "seduma.html":
                if not title or not title.group(1).startswith("Seduma Trade"):
                    findings.append(f"{rel}: title must use the Seduma Trade: form")
                if f'"operatingSystem": "{_OPERATING_SYSTEM}"' not in text:
                    findings.append(f"{rel}: operatingSystem must be {_OPERATING_SYSTEM}")
            mails = text.lower().count("mailto:")
            if page == "contact.html" and mails != 1:
                findings.append(f"{rel}: contact must publish one support address")
            if page != "contact.html" and mails != 0:
                findings.append(f"{rel}: email must stay on the contact page")
            if "waitlist" in text.lower():
                findings.append(f"{rel}: waitlist is not allowed")
    sitemap = docs_dir / "sitemap.xml"
    if sitemap.is_file():
        sm = sitemap.read_text(encoding="utf-8")
        if "xmlns:xhtml" not in sm:
            findings.append("sitemap.xml: missing xhtml namespace")
        for page in LOCALE_PAGES:
            for code, folder, _direction, _name in LOCALES:
                loc = page_url(folder, page)
                if f"<loc>{loc}</loc>" not in sm:
                    findings.append(f"sitemap.xml: missing {loc}")
                if f'hreflang="{code}"' not in sm or loc not in sm:
                    findings.append(f"sitemap.xml: missing alternate {code} for {page}")
        if 'hreflang="x-default"' not in sm:
            findings.append("sitemap.xml: missing x-default")
    else:
        findings.append("missing sitemap.xml")
    return findings


_OLD_PRODUCT_NAME = "Seduma Trade Dojo"


def old_product_name_findings(docs_dir: Path) -> list[str]:
    """The product name is Seduma Trade. The old compound listing name must not appear."""
    findings: list[str] = []
    if not docs_dir.is_dir():
        return [f"missing docs directory: {docs_dir}"]
    for path in sorted(item for item in docs_dir.rglob("*") if item.is_file()):
        if path.suffix.lower() not in {".html", ".txt", ".md", ".xml"} and path.name != "robots.txt":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            findings.append(f"{path.name}: not valid utf-8")
            continue
        if _OLD_PRODUCT_NAME in text:
            rel = path.relative_to(docs_dir).as_posix()
            findings.append(f"{rel}: old product name")
    readme = docs_dir.parent / "README.md"
    if readme.is_file() and _OLD_PRODUCT_NAME in readme.read_text(encoding="utf-8"):
        findings.append("README.md: old product name")
    return findings


def run_guard(docs_dir: Path = DOCS_DIR, manifest_path: Path = MANIFEST_PATH) -> list[str]:
    return (
        scan_docs(docs_dir)
        + check_required(docs_dir)
        + check_jsonld(docs_dir)
        + llm_copy_findings(docs_dir)
        + check_i18n(docs_dir)
        + old_product_name_findings(docs_dir)
        + check_manifest(docs_dir, manifest_path)
    )


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
