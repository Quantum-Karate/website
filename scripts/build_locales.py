#!/usr/bin/env python3
"""Write docs locale pages, sitemap.xml, and the site manifest from the catalogs."""

from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from pathlib import Path

from i18n_data import (
    LOCALES,
    ORIGIN,
    PAYHIP,
    PAGES,
    Copy,
    fill,
    load_strings,
    page_url,
    payhip_button_url,
)

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MANIFEST = ROOT / ".github" / "site-manifest.sha256"
OG_IMAGE = f"{ORIGIN}assets/og-seduma.png"
ALLOWLIST = {".nojekyll", "CNAME"}

CHECK = (
    '<svg viewBox="0 0 12 12" aria-hidden="true" focusable="false">'
    '<path d="M2.5 6.2l2.3 2.3 4.7-5" fill="none" stroke="currentColor" '
    'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)
XMARK = (
    '<svg viewBox="0 0 12 12" aria-hidden="true" focusable="false">'
    '<path d="M3 3l6 6M9 3l-6 6" fill="none" stroke="currentColor" '
    'stroke-width="1.5" stroke-linecap="round"/></svg>'
)
FOOTER_MARK = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><g fill="none" '
    'stroke="currentColor" stroke-width="1.25"><rect x="1.5" y="1.5" width="21" height="21" rx="1"/>'
    '<circle cx="12" cy="12" r="5.75"/><path d="M12 1.5v4M12 18.5v4M1.5 12h4M18.5 12h4"/></g>'
    '<circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>'
)
ARROW = '<span class="arrow" aria-hidden="true">\u2192</span>'
INFO = {code: (folder, direction, native) for code, folder, direction, native in LOCALES}


def asset(folder: str, path: str) -> str:
    return f"../{path}" if folder else path


def rel_page(from_folder: str, to_folder: str, page: str) -> str:
    if from_folder == to_folder:
        return page
    if not from_folder:
        return f"{to_folder}/{page}"
    if not to_folder:
        return f"../{page}"
    return f"../{to_folder}/{page}"


def latin(locale: str, text: str) -> str:
    return f"<bdi>{text}</bdi>" if locale == "ar" else text


def delay(index: int) -> str:
    return f' style="--d:{index}"' if index else ""


def payhip(folder: str, page: str, label: str) -> str:
    href = payhip_button_url(folder, page)
    return (
        f'<a class="btn btn--primary" href="{href}" rel="noopener">{label} {ARROW}</a>'
    )


def lights() -> str:
    return '<div class="console__lights" aria-hidden="true"><i></i><i></i><i></i></div>'


def chip(kind: str, label: str) -> str:
    return f'<span class="chip chip--{kind}"><span class="chip__dot"></span>{label}</span>'


def head(L: Copy, folder: str, page: str, title_key: str, desc_key: str, og_title_key: str, og_desc_key: str, schema: str = "") -> str:
    canonical = page_url(folder, page)
    title = L.text(title_key)
    desc = L.text(desc_key)
    og_title = L.text(og_title_key)
    og_desc = L.text(og_desc_key)
    alt = L.text("og_alt")
    links = [
        f'<link rel="alternate" hreflang="{code}" href="{page_url(loc_folder, page)}">'
        for code, loc_folder, _direction, _name in LOCALES
    ]
    links.append(f'<link rel="alternate" hreflang="x-default" href="{page_url("", page)}">')
    links.append(
        f'<link rel="alternate" href="{asset(folder, "llms.txt")}" type="text/plain" title="Plain-language summary for AI tools">'
    )
    schema_block = f'<script type="application/ld+json">\n{schema}\n</script>\n' if schema else ""
    return f"""<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{chr(10).join(links)}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Quantum Karate\u2122">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{og_desc}">
<meta name="twitter:image" content="{OG_IMAGE}">
<meta name="twitter:image:alt" content="{alt}">
{schema_block}<meta name="theme-color" content="#0B0F14">
<meta name="color-scheme" content="dark">
<link rel="icon" href="{asset(folder, "assets/favicon.svg")}" type="image/svg+xml">
<link rel="icon" href="{asset(folder, "assets/favicon.ico")}" sizes="16x16 32x32 48x48">
<link rel="preload" href="{asset(folder, "fonts/Geist-Variable.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{asset(folder, "site.css")}">
<script src="{asset(folder, "site.js")}" defer></script>
</head>"""


def header(L: Copy, folder: str, page: str) -> str:
    nav_label = L.text("nav_label")
    lang_label = L.text("lang_label")
    links = [
        ("index.html", L.html("nav_home")),
        ("seduma.html", latin(L.locale, "Seduma\u2122")),
        ("facts.html", L.html("nav_facts")),
        ("contact.html", L.html("nav_contact")),
    ]
    items = []
    for href, label in links:
        current = ' aria-current="page"' if href == page else ""
        items.append(f'<li><a href="{href}"{current}>{label}</a></li>')
    lang_items = []
    for code, to_folder, _direction, native in LOCALES:
        href = rel_page(folder, to_folder, page)
        current = ' aria-current="true"' if code == L.locale else ""
        name = html.escape(native, quote=True)
        lang_items.append(
            f'<li><a href="{href}" lang="{code}" hreflang="{code}"{current}>{name}</a></li>'
        )
    current_name = html.escape(INFO[L.locale][2], quote=True)
    logo = asset(folder, "assets/logo-horizontal-transparent.svg")
    return f"""<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="index.html"><img class="brand-logo" src="{logo}" alt="Quantum Karate" width="202" height="34"></a>
    <nav class="nav" aria-label="{nav_label}"><ul role="list">{"".join(items)}</ul></nav>
    <nav class="lang" aria-label="{lang_label}">
      <details class="lang-switch">
        <summary class="lang-switch__summary"><span class="lang-switch__name">{current_name}</span></summary>
        <ul class="lang-switch__menu" role="list">{"".join(lang_items)}</ul>
      </details>
    </nav>
  </div>
</header>"""


def footer(L: Copy, page: str) -> str:
    brand = latin(L.locale, "Quantum Karate\u2122")
    links = [
        ("index.html", L.html("nav_home")),
        ("seduma.html", latin(L.locale, "Seduma\u2122")),
        ("facts.html", L.html("nav_facts")),
        ("contact.html", L.html("nav_contact")),
    ]
    items = []
    for href, label in links:
        current = ' aria-current="page"' if href == page else ""
        items.append(f'<li><a href="{href}"{current}>{label}</a></li>')
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="site-footer__grid">
      <div>
        <a class="brand" href="index.html">{FOOTER_MARK}<span>{brand}</span></a>
        <p class="tag">{L.html("footer_tag")}</p>
      </div>
      <nav aria-label="{L.text("footer_nav_label")}">
        <p class="label">{L.html("footer_pages")}</p>
        <ul role="list">{"".join(items)}</ul>
      </nav>
      <div>
        <p class="label">{L.html("footer_disclaimer_label")}</p>
        <p class="disclaimer">{L.html("disclaimer")}</p>
      </div>
    </div>
    <div class="site-footer__base">
      <p class="label label--case">{L.html("footer_base")}</p>
    </div>
  </div>
</footer>"""


def document(L: Copy, folder: str, page: str, main: str, head_html: str, theme: str = "") -> str:
    _folder, direction, _native = INFO[L.locale]
    body = f' data-theme="{theme}"' if theme else ""
    prefix = "../" if folder else ""
    return f"""<!doctype html>
<html lang="{L.locale}" dir="{direction}">
{head_html}
<body{body}>
<a class="skip-link" href="#main">{L.html("skip")}</a>
{header(L, folder, page)}
<main id="main" tabindex="-1">
{main}
</main>
{footer(L, page)}
<script data-goatcounter="https://quantumkarate.goatcounter.com/count" async src="{prefix}assets/count.js"></script>
</body>
</html>
"""


def get_band(L: Copy, folder: str, page: str, indexed: bool) -> str:
    index = ""
    if indexed:
        index = (
            '<p class="index label" data-reveal><span class="index__num">04</span>'
            f'<span>{L.html("get_label")}</span></p>'
        )
    return f"""<section class="section section--tight" aria-labelledby="get-seduma-title">
    <div class="container">
      {index}
      <div class="band" data-reveal>
        <div>
          <h2 id="get-seduma-title" class="h2">{L.html("get_h")}</h2>
          <p class="lead" style="margin-top:var(--s-4)">{L.html("get_lead")}</p>
        </div>
        {payhip(folder, page, L.html("get_btn"))}
      </div>
    </div>
  </section>"""


def render_home(L: Copy, folder: str, reticle: str) -> str:
    trade = fill("{trade}", L.locale, html_mode=True)
    qk = fill("{qk}", L.locale, html_mode=True)
    pillars = []
    for index, (title, paragraph) in enumerate(L.rows("pillars")):
        pillars.append(
            f'<article class="pillar" data-reveal{delay(index)}><span class="label">{index + 1:02d}</span>'
            f"<h3 class=\"h3\">{title}</h3><p>{paragraph}</p></article>"
        )
    practice = chip("practice", L.html("chip_practice"))
    live_off = chip("off", L.html("chip_live_off"))
    main = f"""<section class="hero hero--home" aria-labelledby="hero-title">
    <div class="hero__bg" aria-hidden="true"></div>
    <div class="container hero__inner">
      <div class="hero__eyebrow"><span class="label">{qk}</span><span class="label">{L.html("eyebrow_tag")}</span></div>
      <h1 id="hero-title" class="display"><span class="line">{trade}</span></h1>
      <p class="hero__tagline">{L.html("tagline")}</p>
      <p class="hero__amp">{L.html("amp")}</p>
      <div class="hero__grid">
        <div>
          <p class="hero__offer"><strong>{L.html("offer")}</strong></p>
          <p class="hero__note">{L.html("note")}</p>
          <p class="hero__sub">{L.html("sub")}</p>
          <div class="actions">
            <a class="btn btn--primary" href="seduma.html">{L.html("btn_meet")} {ARROW}</a>
            <a class="btn btn--ghost" href="facts.html">{L.html("btn_what")}</a>
          </div>
        </div>
        {reticle}
      </div>
    </div>
    <div class="ruler" aria-hidden="true"></div>
  </section>
  <section class="section" aria-labelledby="philosophy-title">
    <div class="container">
      <p class="index label" data-reveal><span class="index__num">01</span><span>{L.html("phil_label")}</span></p>
      <div class="section__head section__head--split">
        <h2 id="philosophy-title" class="h2" data-reveal>{L.html("phil_h")}</h2>
        <p class="lead" data-reveal style="--d:1">{L.html("phil_lead")}</p>
      </div>
      <div class="pillars">
        {"".join(pillars)}
      </div>
    </div>
  </section>
  <section class="section feature--seduma" aria-labelledby="seduma-title">
    <div class="container">
      <p class="index label" data-reveal><span class="index__num">02</span><span>{L.html("prod_label")}</span></p>
      <div class="feature">
        <div data-reveal>
          <div class="hero__eyebrow" style="margin:0"><span class="label">{latin(L.locale, "Seduma\u2122")}</span><span class="chip chip--honest">{L.html("chip_honest")}</span></div>
          <h2 id="seduma-title" class="h2 feature__title">{L.html("prod_h")}</h2>
          <div class="prose">
            <p>{L.html("prod_p1")}</p>
            <p>{L.html("prod_p2")}</p>
          </div>
          <div class="actions">
            <a class="btn btn--primary" href="seduma.html">{L.html("btn_explore")} {ARROW}</a>
            <a class="btn btn--ghost" href="facts.html">{L.html("btn_what")}</a>
          </div>
        </div>
        <figure class="mini" data-reveal style="--d:1">
          <div role="img" aria-label="{L.text("mini_aria")}">
            <div class="console__bar">
              {lights()}
              <span class="console__title">{L.html("console_paper")}</span>
            </div>
            <div class="mini__body">
              <div class="trust">
                <div class="trust__card"><span class="trust__title">{L.html("trust_practice")}</span>{practice}</div>
                <div class="trust__card"><span class="trust__title">{L.html("trust_live")}</span>{live_off}</div>
                <div class="trust__card"><span class="trust__title">{L.html("trust_stop")}</span><span class="trust__meta">{L.html("stop_available")}</span></div>
              </div>
              <div><span class="chip chip--sim">{L.html("chip_sim")}</span></div>
            </div>
          </div>
          <figcaption class="shot__caption label label--case">{L.html("caption_stop")}</figcaption>
        </figure>
      </div>
    </div>
  </section>
  <section class="section section--tight" aria-labelledby="band-title">
    <div class="container">
      <p class="index label" data-reveal><span class="index__num">03</span><span>{L.html("talk_label")}</span></p>
      <div class="band" data-reveal>
        <div>
          <h2 id="band-title" class="h2">{L.html("talk_h")}</h2>
          <p class="lead" style="margin-top:var(--s-4)">{L.html("talk_p")}</p>
        </div>
        <a class="link-arrow" href="facts.html">{L.html("talk_link")} {ARROW}</a>
      </div>
    </div>
  </section>
  {get_band(L, folder, "index.html", indexed=True)}
"""
    head_html = head(
        L,
        folder,
        "index.html",
        "home_title",
        "home_desc",
        "home_title",
        "home_desc" if L.locale == "en" else "listing_og_desc",
        organization_schema(L, folder),
    )
    return document(L, folder, "index.html", main, head_html)


def organization_schema(L: Copy, folder: str) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Quantum Karate",
        "url": page_url(folder, "index.html"),
        "slogan": L.raw("eyebrow_tag"),
        "description": L.raw("phil_lead"),
        "logo": f"{ORIGIN}assets/logo-horizontal-transparent.svg",
    }
    if L.locale != "en":
        payload["inLanguage"] = L.locale
    return json.dumps(payload, ensure_ascii=False, indent=2)


def schema_block(L: Copy, folder: str) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": ["Product", "SoftwareApplication"],
        "name": "Seduma Trade",
        "operatingSystem": L.raw("os_name"),
        "description": L.raw("se_desc"),
        "url": page_url(folder, "seduma.html"),
        "offers": {
            "@type": "Offer",
            "price": "49.00",
            "priceCurrency": "USD",
            "url": PAYHIP,
            "availability": "https://schema.org/InStock",
        },
    }
    if L.locale != "en":
        payload["inLanguage"] = L.locale
    return json.dumps(payload, ensure_ascii=False, indent=2)


def render_seduma(L: Copy, folder: str) -> str:
    practice = chip("practice", L.html("chip_practice"))
    live_off = chip("off", L.html("chip_live_off"))
    honest = f'<span class="chip chip--honest">{L.html("chip_honest")}</span>'
    defs = "".join(
        f"<div><dt>{term}</dt><dd>{definition}</dd></div>" for term, definition in L.rows("defs")
    )
    compare_rows = []
    skip_label = L.text("col_skip")
    get_label = L.text("col_get")
    for header, skipped, got in L.rows("compare"):
        compare_rows.append(
            "<tr>"
            f'<th scope="row">{header}</th>'
            f'<td data-label="{skip_label}">{skipped}</td>'
            f'<td data-label="{get_label}">{got}</td>'
            "</tr>"
        )
    steps = []
    for index, (title, body) in enumerate(L.rows("steps")):
        steps.append(
            f'<li class="step" data-reveal{delay(index)}><span class="step__num label">{L.html("step_word")} {index + 1:02d}</span>'
            f"<h3 class=\"h3\">{title}</h3>{body}</li>"
        )
    wizard = []
    for index, (title, sub) in enumerate(L.rows("wizard"), start=1):
        if index < 4:
            wizard.append(
                '<li class="is-done"><span class="wizard__mark">'
                f'{CHECK}</span><div><div class="wizard__title">{title}</div>'
                f'<div class="wizard__sub">{sub}</div></div></li>'
            )
        else:
            wizard.append(
                '<li class="is-current"><span class="wizard__mark">04</span><div>'
                f'<div class="wizard__title">{title}</div>'
                f'<div class="wizard__card"><span>{CHECK}{L.html("wiz_card")}</span>'
                f'<span class="mono">{L.html("wiz_status")}</span></div></div></li>'
            )
    checks = "".join(f"<li>{item}</li>" for item in L.rows("checks"))
    honesty = "".join(
        f'<li data-reveal><span class="label">{index:02d}</span><p>{line}</p></li>'
        for index, line in enumerate(L.rows("honesty"), start=1)
    )
    cards = []
    for index, (label, heading, paragraph) in enumerate(L.rows("connections")):
        cards.append(
            f'<article class="card" data-reveal{delay(index)}><span class="label">{label}</span>'
            f"<h3 class=\"h3\">{heading}</h3><p>{paragraph}</p></article>"
        )
    feet = "".join(f"<p>{item}</p>" for item in L.rows("conn_foot"))
    nav = "".join(
        f'<span class="{cls}">{label}</span>'
        for cls, label in (
            ("is-active", L.html("c_home")),
            ("", L.html("c_conn")),
            ("", L.html("c_act")),
            ("", L.html("c_safe")),
        )
    )
    main = f"""<section class="hero hero--page" aria-labelledby="hero-title">
    <div class="hero__bg" aria-hidden="true"></div>
    <div class="container hero__inner">
      <div class="hero__eyebrow"><span class="label">{L.html("se_eyebrow")}</span>{honest}</div>
      <h1 id="hero-title" class="h1"><span class="line">{L.html("h1_1")}</span> <span class="line">{L.html("h1_2")}</span> <span class="line">{L.html("h1_3")}</span></h1>
      <p class="hero__sub">{L.html("se_sub")}</p>
      <div class="actions">
        <a class="btn btn--primary" href="#how">{L.html("btn_how")} <span class="arrow" aria-hidden="true">\u2193</span></a>
        <a class="btn btn--ghost" href="facts.html">{L.html("btn_what")}</a>
      </div>
      <dl class="defs">{defs}</dl>
      <figure class="shot" data-reveal>
      <div class="console" role="img" aria-label="{L.text("console_aria")}">
        <div class="console__bar">
          {lights()}
          <span class="console__title">{L.html("console_paper")}</span>
          <div class="console__chips">
            {practice}
            {live_off}
            {honest}
          </div>
        </div>
        <div class="console__body">
          <div class="console__nav">
            {nav}
            <div class="console__navfoot"><span class="label label--case">{L.html("c_foot")}</span></div>
          </div>
          <div class="console__main">
            <div class="console__banner">
              <strong>{L.html("promise")}</strong>
              {honest}
              <span class="dim">{L.html("fills_line")}</span>
            </div>
            <div class="trust">
            <div class="trust__card"><span class="trust__title">{L.html("trust_practice")}</span>{practice}<span class="trust__meta">{L.html("trust_meta_practice")}</span></div>
            <div class="trust__card"><span class="trust__title">{L.html("trust_live")}</span>{live_off}<span class="trust__meta">{L.html("trust_meta_live")}</span></div>
            <div class="trust__card"><span class="trust__title">{L.html("trust_stop")}</span><span class="trust__meta">{L.html("stop_available")}</span><span class="stop-btn">{L.html("trust_stop")}</span></div>
          </div>
            <div class="activity">
              <div class="activity__head"><span class="h-sm">{L.html("act_title")}</span><span class="chip chip--sim">{L.html("chip_sim")}</span></div>
              <div class="cycle">{L.html("cycle_line")}<span class="cycle__track"></span></div>
              <ul class="rows">
                <li class="row"><span class="mono">14:32:08</span><span class="sym">{fill("{example}", L.locale, html_mode=True)}</span><span class="evt">{L.html("row1_evt")}</span><span class="state">{L.html("row1_state")}</span></li>
                <li class="row"><span class="mono">14:30:12</span><span class="sym">\u2014</span><span class="evt">{L.html("row2_evt")}</span><span class="state state--stop">{L.html("row2_state")}</span></li>
              </ul>
            </div>
            <div class="locks"><span>{CHECK}{L.html("lock_practice")}</span></div>
          </div>
        </div>
      </div>
      <figcaption class="shot__caption label label--case">{L.html("caption_stop")}</figcaption>
    </figure>
    </div>
  </section>
  <section class="section" id="why-dojo" aria-labelledby="why-dojo-title">
    <div class="container">
      <p class="index label" data-reveal><span class="index__num">01</span><span>{L.html("comp_label")}</span></p>
      <div class="section__head">
        <h2 id="why-dojo-title" class="h2" data-reveal>{L.html("comp_h")}</h2>
      </div>
      <div class="compare-wrap" data-reveal>
        <table class="compare">
          <caption class="visually-hidden">{L.html("comp_caption")}</caption>
          <thead>
            <tr>
              <th scope="col"><span class="visually-hidden">{L.html("comp_label")}</span></th>
              <th scope="col">{L.html("col_skip")}</th>
              <th scope="col">{L.html("col_get")}</th>
            </tr>
          </thead>
          <tbody>
            {"".join(compare_rows)}
          </tbody>
        </table>
      </div>
    </div>
  </section>
  <section class="section" id="source" aria-labelledby="source-title">
    <div class="container">
      <p class="index label" data-reveal><span class="index__num">02</span><span>{L.html("source_label")}</span></p>
      <div class="section__head section__head--split" style="margin-bottom:0">
        <h2 id="source-title" class="h2" data-reveal>{L.html("source_h")}</h2>
        <div class="prose" data-reveal style="--d:1">
          <p>{L.html("source_p1")}</p>
          <p>{L.html("source_p2")}</p>
        </div>
      </div>
    </div>
  </section>
  <section class="section" id="how" aria-labelledby="how-title">
    <div class="container">
      <p class="index label" data-reveal><span class="index__num">03</span><span>{L.html("how_label")}</span></p>
      <div class="section__head section__head--split">
        <h2 id="how-title" class="h2" data-reveal>{L.html("how_h")}</h2>
        <p class="lead" data-reveal style="--d:1">{L.html("how_lead")}</p>
      </div>
      <ol class="steps" role="list">
        {"".join(steps)}
      </ol>
      <div class="duo">
        <div data-reveal>
          <p class="label">{L.html("first_label")}</p>
          <h3 class="h2" style="margin-top:var(--s-3)">{L.html("first_h")}</h3>
          <div class="prose">
            <p>{L.html("first_p1")}</p>
            <p>{L.html("first_p2")}</p>
          </div>
        </div>
        <figure data-reveal>
        <div class="panel" role="img" aria-label="{L.text("wizard_aria")}">
          <div class="panel__head">{chip("practice", fill("{paper} {practice}", L.locale, html_mode=True))}{live_off}</div>
          <div class="panel__body">
            <ol class="wizard">
              {"".join(wizard)}
            </ol>
          </div>
          <div class="panel__foot">{L.html("wiz_foot")}</div>
        </div>
        <figcaption class="shot__caption label label--case">{L.html("caption_plain")}</figcaption>
      </figure>
      </div>
      <div class="duo duo--flip">
        <div data-reveal>
          <p class="label">{L.html("live_label")}</p>
          <h3 class="h2" style="margin-top:var(--s-3)">{L.html("live_h")}</h3>
          <div class="prose">
            <p>{L.html("live_p1")}</p>
            <p>{L.html("live_p2")}</p>
          </div>
        </div>
        <figure data-reveal>
        <div class="modal-demo" role="img" aria-label="{L.text("modal_aria")}">
          <div class="modal">
            <div class="modal__head"><span class="modal__title">{L.html("modal_title")}</span></div>
            <div class="modal__body">
              <ul class="checks">{checks}</ul>
              <div class="field"><span class="label label--case">{L.html("type_live")}</span><span class="field__input"></span></div>
            </div>
            <div class="modal__foot"><span class="mbtn mbtn--primary">{L.html("btn_live_on")}</span><span class="mbtn">{L.html("btn_stay")}</span></div>
          </div>
        </div>
        <figcaption class="shot__caption label label--case">{L.html("caption_plain")}</figcaption>
      </figure>
      </div>
    </div>
  </section>
  <section class="section" id="honesty" aria-labelledby="honesty-title">
    <div class="container">
      <p class="index label" data-reveal><span class="index__num">04</span><span>{L.html("hon_label")}</span></p>
      <div class="section__head"><h2 id="honesty-title" class="h2" data-reveal>{L.html("hon_h")}</h2></div>
      <ol class="honesty" role="list">{honesty}</ol>
      <p class="note" data-reveal>{L.html("hon_note")}</p>
      <p class="note" data-reveal>{L.html("pnl_note")}</p>
    </div>
  </section>
  <section class="section" id="connections" aria-labelledby="conn-title">
    <div class="container">
      <p class="index label" data-reveal><span class="index__num">05</span><span>{L.html("conn_label")}</span></p>
      <div class="section__head section__head--split">
        <h2 id="conn-title" class="h2" data-reveal>{L.html("conn_h")}</h2>
        <p class="lead" data-reveal style="--d:1">{L.html("conn_lead")}</p>
      </div>
      <div class="conn">{"".join(cards)}</div>
      <div class="conn-foot" data-reveal>{feet}</div>
    </div>
  </section>
  <section class="section" id="research" aria-labelledby="research-title">
    <div class="container">
      <p class="index label" data-reveal><span class="index__num">06</span><span>{L.html("res_label")}</span></p>
      <div class="section__head section__head--split" style="margin-bottom:0">
        <h2 id="research-title" class="h2" data-reveal>{L.html("res_h")}</h2>
        <div class="prose" data-reveal style="--d:1">
          <p>{L.html("res_p1")}</p>
          <p>{L.html("res_p2")}</p>
        </div>
      </div>
    </div>
  </section>
  <section class="section section--tight" aria-labelledby="facts-cta">
    <div class="container">
      <div class="band" data-reveal>
        <div>
          <h2 id="facts-cta" class="h2">{L.html("facts_cta_h")}</h2>
          <p class="lead" style="margin-top:var(--s-4)">{L.html("facts_cta_p")}</p>
        </div>
        <a class="link-arrow" href="facts.html">{L.html("facts_cta_link")} {ARROW}</a>
      </div>
    </div>
  </section>
  {get_band(L, folder, "seduma.html", indexed=False)}
"""
    head_html = head(
        L,
        folder,
        "seduma.html",
        "se_title",
        "se_desc",
        "listing_og_title",
        "listing_og_desc",
        schema_block(L, folder),
    )
    return document(L, folder, "seduma.html", main, head_html, theme="seduma")


def render_facts(L: Copy, folder: str) -> str:
    def facts(pairs):
        return "".join(
            f"<li><div><strong>{strong}</strong><span>{detail}</span></div></li>"
            for strong, detail in pairs
        )

    glossary = "".join(
        f"<div data-reveal><dt>{term}</dt><dd>{definition}</dd></div>"
        for term, definition in L.rows("glossary")
    )
    main = f"""<section class="hero hero--page" aria-labelledby="hero-title">
    <div class="hero__bg" aria-hidden="true"></div>
    <div class="container hero__inner">
      <div class="hero__eyebrow"><span class="label">{L.html("facts_eyebrow")}</span></div>
      <h1 id="hero-title" class="h1">{L.html("facts_h")}</h1>
      <p class="hero__sub">{L.html("facts_sub")}</p>
    </div>
  </section>
  <section class="section" aria-label="{L.text("facts_region")}">
    <div class="container">
      <div class="facts">
        <div class="facts__col" data-reveal>
          <div class="facts__head"><h2 class="h2" style="margin:0">{L.html("facts_is_h")}</h2><span class="mark">{CHECK}</span></div>
          <ol class="fact-list" role="list">{facts(L.rows("facts_is"))}</ol>
        </div>
        <div class="facts__col" data-reveal style="--d:1">
          <div class="facts__head"><h2 class="h2" style="margin:0">{L.html("facts_isnt_h")}</h2><span class="mark">{XMARK}</span></div>
          <ol class="fact-list" role="list">{facts(L.rows("facts_isnt"))}</ol>
        </div>
      </div>
    </div>
  </section>
  <section class="section" aria-labelledby="gloss-title">
    <div class="container">
      <p class="index label" data-reveal><span class="index__num">\u2014</span><span>{L.html("gloss_label")}</span></p>
      <div class="section__head"><h2 id="gloss-title" class="h2" data-reveal>{L.html("gloss_h")}</h2></div>
      <dl class="glossary">{glossary}</dl>
    </div>
  </section>
"""
    head_html = head(L, folder, "facts.html", "facts_title", "facts_desc", "facts_og_title", "facts_og_desc")
    return document(L, folder, "facts.html", main, head_html)


def render_contact(L: Copy, folder: str) -> str:
    main = f"""<section class="hero hero--page" aria-labelledby="hero-title">
    <div class="hero__bg" aria-hidden="true"></div>
    <div class="container hero__inner">
      <div class="hero__eyebrow"><span class="label">{L.html("contact_eyebrow")}</span></div>
      <h1 id="hero-title" class="h1">{L.html("contact_h")}</h1>
      <p class="hero__sub">{L.html("contact_sub")}</p>
    </div>
  </section>
  {get_band(L, folder, "contact.html", indexed=False)}
  <section class="section section--tight" aria-label="{L.text("support_label")}">
    <div class="container">
      <p class="lead" data-reveal>{L.html("support")}</p>
    </div>
  </section>
"""
    head_html = head(
        L, folder, "contact.html", "contact_title", "contact_desc", "contact_og_title", "contact_og_desc"
    )
    return document(L, folder, "contact.html", main, head_html)


def load_reticle() -> str:
    text = (DOCS / "index.html").read_text(encoding="utf-8")
    match = re.search(r'<svg class="reticle"[\s\S]*?</svg>', text)
    if not match:
        raise SystemExit("reticle svg missing from docs/index.html")
    return match.group(0)


def sitemap() -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    def emit(page: str, folder: str) -> None:
        loc = page_url(folder, page)
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        for alt, alt_folder, _direction, _name in LOCALES:
            lines.append(
                f'    <xhtml:link rel="alternate" hreflang="{alt}" href="{page_url(alt_folder, page)}"/>'
            )
        lines.append(
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{page_url("", page)}"/>'
        )
        lines.append("  </url>")

    for page in PAGES:
        emit(page, "")
    for page in PAGES:
        for _code, folder, _direction, _name in LOCALES:
            if folder:
                emit(page, folder)
    for name in ("llms.txt", "llms-full.txt"):
        lines.append("  <url>")
        lines.append(f"    <loc>{ORIGIN}{name}</loc>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def manifest_text() -> str:
    lines = []
    for path in sorted(item for item in DOCS.rglob("*") if item.is_file()):
        rel = path.relative_to(DOCS).as_posix()
        if rel in ALLOWLIST or path.name in ALLOWLIST:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  ./{rel}")
    return "\n".join(lines) + "\n"


def render_pages(strings: dict[str, dict], reticle: str) -> dict[str, str]:
    pages: dict[str, str] = {}
    for code, folder, _direction, _name in LOCALES:
        L = Copy(code, strings[code])
        rendered = {
            "index.html": render_home(L, folder, reticle),
            "seduma.html": render_seduma(L, folder),
            "facts.html": render_facts(L, folder),
            "contact.html": render_contact(L, folder),
        }
        for page, content in rendered.items():
            verify(code, page, content)
            rel = f"{folder}/{page}" if folder else page
            pages[rel] = content
    pages["sitemap.xml"] = sitemap()
    return pages


def verify(locale: str, page: str, content: str) -> None:
    if "Seduma Trade Dojo" in content:
        raise SystemExit(f"{locale}/{page} contains Seduma Trade Dojo")
    lowered = content.lower()
    if "waitlist" in lowered or "thoth" in lowered or "phisher" in lowered:
        raise SystemExit(f"{locale}/{page} contains a banned name")
    if "Neural Agency Engine" not in content:
        raise SystemExit(f"{locale}/{page} does not spell Neural Agency Engine")
    if content.count('<link rel="alternate" hreflang="') != len(LOCALES) + 1:
        raise SystemExit(f"{locale}/{page} hreflang count is wrong")
    if f'<html lang="{locale}"' not in content:
        raise SystemExit(f"{locale}/{page} lang attribute missing")
    direction = INFO[locale][1]
    if f'dir="{direction}"' not in content:
        raise SystemExit(f"{locale}/{page} dir attribute missing")
    folder = INFO[locale][0]
    button = payhip_button_url(folder, page)
    button_count = content.count(f'href="{button}"')
    bare_count = content.count(f'href="{PAYHIP}"')
    if page == "facts.html":
        if button_count or bare_count:
            raise SystemExit(f"{locale}/{page} should not link to Payhip")
    elif button_count != 1 or bare_count:
        raise SystemExit(f"{locale}/{page} should link to the tracked Payhip button once")
    title = re.search(r"<title>([^<]*)</title>", content)
    og_title = re.search(r'<meta property="og:title" content="([^"]*)"', content)
    for kind, match in (("title", title), ("og:title", og_title)):
        if match and "Dojo" in match.group(1):
            raise SystemExit(f"{locale}/{page} {kind} still names the product as a Dojo")
    if page == "seduma.html":
        if not title or not title.group(1).startswith("Seduma Trade"):
            raise SystemExit(f"{locale}/{page} title must use the Seduma Trade: form")
        if '"operatingSystem": "Windows, macOS, Linux"' not in content:
            raise SystemExit(f"{locale}/{page} operatingSystem must be Windows, macOS, Linux")
    mails = lowered.count("mailto:")
    if page == "contact.html" and mails != 1:
        raise SystemExit(f"{locale}/{page} should have one mailto")
    if page != "contact.html" and mails != 0:
        raise SystemExit(f"{locale}/{page} should not publish email")
    if 'role="list"' not in content:
        raise SystemExit(f"{locale}/{page} missing role=list")
    if locale == "en":
        verify_english(page, content)


def verify_english(page: str, content: str) -> None:
    required = {
        "index.html": [
            "<title>Quantum Karate: Seduma Trade Practice Trading Simulator, $49 Once</title>",
            'content="Quantum Karate: $49 once, no subscription, nothing to cancel. The source includes the Neural Agency Engine, on your own computer. Simulated results only."',
            "Get Seduma Trade.",
            "Seduma Trade is the $49 Practice eval.",
            "The Neural Agency Engine researches. Seduma is the front door.",
            "Get Seduma Trade on Payhip",
            "Buyers get the source, including the Neural Agency Engine, and run it on their own computer.",
            "Simulated results only. No passive-income promise, and no profit promise.",
            "$49 once, no subscription, nothing to cancel",
            "What Seduma is and isn\u2019t",
        ],
        "seduma.html": [
            "<title>Seduma Trade: Practice Trading Simulator, $49 Once | Quantum Karate</title>",
            'content="Practice your own trading rules in a paper trading simulator on your own computer. $49 once, no subscription. Simulated results only. Not a broker."',
            '"SoftwareApplication"',
            '"price": "49.00"',
            '"priceCurrency": "USD"',
            '"availability": "https://schema.org/InStock"',
            f'"url": "{PAYHIP}"',
            "Why a one-time Dojo",
            "You get the source.",
            "Honest Practice. Simulated results only. No passive-income promise, and no profit promise.",
            "We don\u2019t fake Practice. We don\u2019t trade until you say so.",
            "You\u2019re set \u2014 setup stays Paper",
        ],
        "facts.html": [
            "<title>What Seduma is and isn\u2019t | Quantum Karate</title>",
            'content="Plain facts: $49 once, no subscription. Simulated results only. Live stays off unless you choose it. Not a broker."',
            "<strong>A one-time Dojo.</strong>",
            "No passive-income promise, and no profit promise.",
        ],
        "contact.html": [
            "<title>Contact | Quantum Karate</title>",
            'content="Product questions about Seduma Trade go through the Payhip listing. $49 once, no subscription, nothing to cancel. Simulated results only."',
            'Support: <a class="support-address" href="mailto:v-nat@outlook.com">v-nat@outlook.com</a>, replies within 2 business days.',
        ],
    }
    for snippet in required[page]:
        if snippet not in content:
            raise SystemExit(f"English {page} missing exact snippet: {snippet}")
    if page == "index.html" and "What it is and isn\u2019t" in content:
        raise SystemExit("English home still has the short facts button")
    if page == "index.html" and "SoftwareApplication" in content:
        raise SystemExit("English home must not include SoftwareApplication")


def write_outputs(pages: dict[str, str]) -> None:
    for rel, content in pages.items():
        path = DOCS / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    MANIFEST.write_text(manifest_text(), encoding="utf-8")


def check_outputs(pages: dict[str, str]) -> list[str]:
    problems = []
    for rel, content in pages.items():
        path = DOCS / rel
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            problems.append(rel)
    if not MANIFEST.is_file() or MANIFEST.read_text(encoding="utf-8") != manifest_text():
        problems.append(".github/site-manifest.sha256")
    return problems


def main(argv: list[str]) -> int:
    strings = load_strings()
    pages = render_pages(strings, load_reticle())
    # Import after catalogs load so the guard sees the same URL allow-list.
    sys.path.insert(0, str(ROOT / "scripts"))
    import site_guard

    for rel, content in pages.items():
        if not rel.endswith(".html"):
            continue
        findings = site_guard.findings_for_text(".html", content)
        if findings:
            print(f"{rel}: claim scan failed")
            for item in findings:
                print(item)
            return 1
    if "--check" in argv:
        problems = check_outputs(pages)
        if problems:
            print("locale build is stale:")
            for item in problems:
                print(item)
            return 1
        print("locale build: ok")
        return 0
    write_outputs(pages)
    print(f"wrote {len(pages) - 1} pages and sitemap.xml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
