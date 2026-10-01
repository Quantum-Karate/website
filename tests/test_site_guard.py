"""In-memory cases for the site claim guard."""

import hashlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import site_guard


def test_spelled_out_engine_name_is_allowed():
    text = "<p>The Neural Agency Engine researches. Seduma is the front door.</p>"
    assert site_guard.findings_for_text(".html", text) == []


def test_standalone_abbreviation_fails_and_comments_are_ignored():
    assert site_guard.findings_for_text(".html", "<p>The NAE researches.</p>")
    assert site_guard.findings_for_text(".html", "<p>See N.A.E today.</p>")
    assert site_guard.findings_for_text(".html", "<p>See N.A.E. today.</p>")
    assert site_guard.findings_for_text(".html", "<!-- NAE -->\n<p>Hello</p>") == []
    css_comment = "/* Tokens derive from Lockframe (/nae-seduma-ds/tokens.css) */\nbody { color: black; }"
    assert site_guard.findings_for_text(".css", css_comment) == []
    assert site_guard.findings_for_text(".css", "body { content: 'NAE'; }")


def test_attribute_values_are_scanned():
    safe = "The Neural Agency Engine researches."
    for snippet in (
        f'<meta name="description" content="{safe}">',
        f'<meta property="og:title" content="{safe}">',
        f'<meta property="og:description" content="{safe}">',
        f'<p title="{safe}">Hello</p>',
        f'<img alt="{safe}">',
        f'<input placeholder="{safe}">',
        f'<div aria-label="{safe}">Hello</div>',
        "<title>The Neural Agency Engine</title>",
    ):
        assert site_guard.findings_for_text(".html", snippet) == []
    for snippet in (
        '<meta name="description" content="The NAE researches.">',
        '<meta property="og:title" content="NAE">',
        '<meta property="og:description" content="See N.A.E today.">',
        '<p title="NAE">Hello</p>',
        '<img alt="NAE">',
        '<input placeholder="N.A.E.">',
        '<div aria-label="The NAE">Hello</div>',
        "<title>NAE</title>",
    ):
        assert site_guard.findings_for_text(".html", snippet)


def test_inline_tags_entities_and_whitespace_are_normalised():
    assert site_guard.findings_for_text(".html", "<p>N<b>A</b>E</p>")
    assert site_guard.findings_for_text(".html", '<p>N<span class="x">A</span>E</p>')
    assert site_guard.findings_for_text(".html", "<p>N&#65;E</p>")
    assert site_guard.findings_for_text(".html", "<p>&#78;&#65;&#69;</p>")
    assert site_guard.findings_for_text(".html", "<p>set   and\n\tforget</p>")
    assert site_guard.findings_for_text(".html", "<meta name=\"description\" content=\"N&#65;E\">")
    # Block tags stay separated, and spaced letters are not an abbreviation.
    assert site_guard.findings_for_text(".html", "<p>N</p><p>AE</p>") == []
    assert site_guard.findings_for_text(".html", "<p>N A E</p>") == []
    assert site_guard.findings_for_text(".html", "<p>The Neural Agency Engine</p>") == []


def test_entity_suffix_and_nearby_words():
    assert site_guard.findings_for_text(".html", "<p>Quantum Karate LLC</p>")
    assert site_guard.findings_for_text(".html", "<p>Hello, Inc. welcomes you.</p>")
    assert site_guard.findings_for_text(".html", "<p>Quantum Karate Inc</p>")
    assert site_guard.findings_for_text(".html", "<p>Quantum Karate Inc.</p>")
    assert site_guard.findings_for_text(".html", "<p>including the smallest details since yesterday.</p>") == []
    assert site_guard.findings_for_text(".html", "<p>include income</p>") == []


def test_banned_phrases_are_case_insensitive_and_near_misses_pass():
    for phrase in ("Auto-run", "AUTOPILOT", "Set-and-forget", "Set and forget", "Trades for you", "Guaranteed", "Expected edge"):
        assert site_guard.findings_for_text(".html", f"<p>{phrase}</p>")
    near = "<p>Auto-trading off. An auto-close. Seduma does not pick trades for me. No promise of results.</p>"
    assert site_guard.findings_for_text(".html", near) == []


def test_new_banned_terms_and_near_misses():
    for phrase in ("autonomous", "This is not autonomous.", "hands-off", "hands   off", "ARR", "12% return", "3.5% APY", "10%profit", "return of", "returns of", "1,000+ customers", "12 users", "3 traders", "40 clients"):
        assert site_guard.findings_for_text(".html", f"<p>{phrase}</p>"), phrase
    near = """
    <p>Auto-trading off. An auto-close.</p>
    <script>
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      var margin = '0px 0px -8% 0px';
      var vh = document.documentElement.clientHeight;
    </script>
    <p>The arrow marks a link. An array of steps. 100% of the layout. Users bring their own rules. Hands offset.</p>
    """
    assert site_guard.findings_for_text(".html", near) == []
    assert site_guard.findings_for_text(".js", "if (ok) return;\nvar margin = '0px 0px -8% 0px';\nvar vh = d.clientHeight;\n") == []


def test_href_and_src_rules_allow_mailto_hash_and_relative():
    ok = '<a href="index.html"></a><a href="#main"></a><a href="mailto:{{CONTACT_EMAIL}}"></a><img src="assets/favicon.svg">'
    assert site_guard.findings_for_text(".html", ok) == []
    assert site_guard.findings_for_text(".html", '<a href="https://example.com">x</a>')
    assert site_guard.findings_for_text(".html", '<a href="http://example.com">x</a>')
    assert site_guard.findings_for_text(".html", '<script src="//cdn.example/lib.js"></script>')
    assert site_guard.findings_for_text(".html", '<a href="/index.html">x</a>')
    svg = '<svg xmlns="http://www.w3.org/2000/svg"></svg>'
    assert site_guard.findings_for_text(".svg", svg) == []


def test_references_beyond_href_and_src():
    assert site_guard.findings_for_text(".html", '<img srcset="a.png 1x, b.png 2x">') == []
    assert site_guard.findings_for_text(".html", '<form action="contact.html"></form>') == []
    assert site_guard.findings_for_text(".html", '<form action="#main"></form>') == []
    assert site_guard.findings_for_text(".html", '<div style="background:url(assets/a.png)"></div>') == []
    assert site_guard.findings_for_text(".html", "<style>@import 'site.css';</style>") == []
    assert site_guard.findings_for_text(".css", 'body { background: url("fonts/Geist-Variable.woff2"); }') == []
    assert site_guard.findings_for_text(".css", '@import "local.css";') == []
    assert site_guard.findings_for_text(".js", 'fetch("data.json"); import("./mod.js"); xhr.open("GET", "local.json");') == []
    assert site_guard.findings_for_text(".css", '/* @import "https://example.com/a.css"; */\nbody { color: black; }') == []

    assert site_guard.findings_for_text(".html", '<img srcset="/a.png 1x, b.png 2x">')
    assert site_guard.findings_for_text(".html", '<img srcset="https://cdn.example/a.png 2x">')
    assert site_guard.findings_for_text(".html", '<form action="/submit"></form>')
    assert site_guard.findings_for_text(".html", '<form action="https://example.com/post"></form>')
    assert site_guard.findings_for_text(".html", '<div style="background:url(https://example.com/a.png)"></div>')
    assert site_guard.findings_for_text(".html", '<div style="background:url(/a.png)"></div>')
    assert site_guard.findings_for_text(".html", '<style>@import "https://example.com/a.css";</style>')
    assert site_guard.findings_for_text(".html", "<style>@import url(/abs.css);</style>")
    assert site_guard.findings_for_text(".css", 'body { background: url(//cdn.example/a.png); }')
    assert site_guard.findings_for_text(".css", '@import "/abs.css";')
    assert site_guard.findings_for_text(".js", 'fetch("https://example.com/a");')
    assert site_guard.findings_for_text(".js", 'fetch("/api");')
    assert site_guard.findings_for_text(".js", 'import("//cdn.example/mod.js");')
    assert site_guard.findings_for_text(".html", '<script>var x = new XMLHttpRequest(); x.open("GET", "/api");</script>')
    assert site_guard.findings_for_text(".js", 'xhr.open("GET", "https://example.com/a");')


def test_required_sentences():
    good = {
        "index.html": f"<p>{site_guard.DISCLAIMER}</p>",
        "facts.html": f"<p>{site_guard.DISCLAIMER}</p>",
        "contact.html": f"<p>{site_guard.DISCLAIMER}</p>",
        "seduma.html": f"<h3>{site_guard.STEP_TITLE}</h3><strong>{site_guard.PROMISE}</strong><p>{site_guard.DISCLAIMER}</p>",
    }
    assert "\u2019" in site_guard.STEP_TITLE and "\u2014" in site_guard.STEP_TITLE
    assert "\u2019" in site_guard.PROMISE
    assert site_guard.required_findings(good) == []

    missing_title = dict(good)
    missing_title["seduma.html"] = f"<strong>{site_guard.PROMISE}</strong><p>{site_guard.DISCLAIMER}</p>"
    assert any("seduma.html" in item and site_guard.STEP_TITLE in item for item in site_guard.required_findings(missing_title))

    missing_promise = dict(good)
    missing_promise["seduma.html"] = f"<h3>{site_guard.STEP_TITLE}</h3><p>{site_guard.DISCLAIMER}</p>"
    assert any(site_guard.PROMISE in item for item in site_guard.required_findings(missing_promise))

    missing_disclaimer = dict(good)
    missing_disclaimer["facts.html"] = "<p>Hello</p>"
    assert any(item.startswith("facts.html") and site_guard.DISCLAIMER in item for item in site_guard.required_findings(missing_disclaimer))


def test_cname_must_be_one_hostname():
    assert site_guard.cname_findings("example.com\n") == []
    assert site_guard.cname_findings("www.example.com") == []
    assert site_guard.cname_findings("https://example.com\n")
    assert site_guard.cname_findings("example.com\nwww.example.com\n")
    assert site_guard.cname_findings("not a host\n")
    assert site_guard.cname_findings("")
    assert site_guard.cname_findings("/quantumkarate\n")


def test_manifest_allowlist_and_hash_mismatch(tmp_path: Path):
    docs = tmp_path / "docs"
    docs.mkdir()
    page = docs / "index.html"
    page.write_text("<p>Hello</p>", encoding="utf-8")
    (docs / ".nojekyll").write_bytes(b"")
    (docs / "CNAME").write_text("example.com\n", encoding="utf-8")
    digest = hashlib.sha256(page.read_bytes()).hexdigest()
    manifest = tmp_path / "site-manifest.sha256"
    manifest.write_text(f"{digest}  ./index.html\n", encoding="utf-8")

    assert site_guard.check_manifest(docs, manifest) == []

    (docs / "extra.html").write_text("<p>extra</p>", encoding="utf-8")
    extra_findings = site_guard.check_manifest(docs, manifest)
    assert extra_findings == ["file not in manifest or allowlist: extra.html"]

    page.write_text("<p>Changed</p>", encoding="utf-8")
    (docs / "extra.html").unlink()
    mismatch = site_guard.check_manifest(docs, manifest)
    assert mismatch == ["manifest hash mismatch: index.html"]


def test_delivered_docs_pass():
    if not site_guard.DOCS_DIR.is_dir():
        pytest.skip("docs/ is not present")
    assert site_guard.run_guard() == []
