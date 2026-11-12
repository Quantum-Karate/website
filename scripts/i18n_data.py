"""Locale list, token fill, and the per-locale copy catalogs."""

from __future__ import annotations

import html
import re

LOCALES = (
    ("en", "", "ltr", "English"),
    ("es", "es", "ltr", "Español"),
    ("pt-BR", "pt-BR", "ltr", "Português (Brasil)"),
    ("fr", "fr", "ltr", "Français"),
    ("de", "de", "ltr", "Deutsch"),
    ("it", "it", "ltr", "Italiano"),
    ("zh-Hans", "zh-Hans", "ltr", "中文（简体）"),
    ("ja", "ja", "ltr", "日本語"),
    ("ko", "ko", "ltr", "한국어"),
    ("hi", "hi", "ltr", "हिन्दी"),
    ("ar", "ar", "rtl", "العربية"),
    ("ru", "ru", "ltr", "Русский"),
    ("id", "id", "ltr", "Bahasa Indonesia"),
)

PAGES = ("index.html", "seduma.html", "facts.html", "contact.html")
ORIGIN = "https://quantum-karate.github.io/website/"
PAYHIP = "https://payhip.com/b/K7UaW"

_TOKENS = {
    "seduma_tm": "Seduma\u2122",
    "seduma": "Seduma",
    "trade": "Seduma Trade",
    "qk_plain": "Quantum Karate",
    "qk": "Quantum Karate\u2122",
    "nae": "Neural Agency Engine",
    "practice": "Practice",
    "paper": "Paper",
    "live_token": "LIVE",
    "live": "Live",
    "dojo": "Dojo",
    "payhip": "Payhip",
    "pnl": "P&L",
    "price": "$49",
    "hold": "HOLD",
    "example": "EXAMPLE",
}
_TOKEN_ORDER = sorted(_TOKENS, key=len, reverse=True)
_PLACE = re.compile(r"\{[a-z0-9_]+\}")


def page_url(folder: str, page: str) -> str:
    if folder:
        return f"{ORIGIN}{folder}/{page}"
    return f"{ORIGIN}{page}"


def utm_content(folder: str, page: str) -> str:
    """Button id: the page on English, and locale plus page on a translation."""
    stem = page[:-5] if page.endswith(".html") else page
    if folder:
        return f"{folder}-{stem}"
    return stem


def payhip_button_url(folder: str, page: str) -> str:
    """Tracked buy button. JSON-LD and prose links stay on the bare listing URL."""
    return (
        f"{PAYHIP}?utm_source=quantumkarate_site"
        f"&utm_medium=referral"
        f"&utm_campaign=seduma_trade"
        f"&utm_content={utm_content(folder, page)}"
    )


def allowed_urls() -> frozenset[str]:
    urls = {PAYHIP}
    for _code, folder, _direction, _name in LOCALES:
        for page in PAGES:
            urls.add(page_url(folder, page))
            if page != "facts.html":
                urls.add(payhip_button_url(folder, page))
    return frozenset(urls)


def email_link(locale: str) -> str:
    visible = "v-nat@outlook.com"
    if locale == "ar":
        visible = "<bdi>v-nat@outlook.com</bdi>"
    return f'<a class="support-address" href="mailto:v-nat@outlook.com">{visible}</a>'


def fill(text: str, locale: str, *, html_mode: bool, extras: dict[str, str] | None = None) -> str:
    if extras:
        for key, value in extras.items():
            text = text.replace("{" + key + "}", value)
    wrap = html_mode and locale == "ar"
    for key in _TOKEN_ORDER:
        token = _TOKENS[key]
        if key == "pnl" and html_mode:
            token = "P&amp;L"
        if wrap:
            token = f"<bdi>{token}</bdi>"
        text = text.replace("{" + key + "}", token)
    leftover = _PLACE.search(text)
    if leftover:
        raise ValueError(f"unfilled placeholder {leftover.group(0)} for {locale}: {text[:200]}")
    return text


def _walk(obj, locale: str, *, html_mode: bool, extras: dict[str, str]):
    if isinstance(obj, str):
        return fill(obj, locale, html_mode=html_mode, extras=extras)
    if isinstance(obj, list):
        return [_walk(item, locale, html_mode=html_mode, extras=extras) for item in obj]
    if isinstance(obj, tuple):
        return tuple(_walk(item, locale, html_mode=html_mode, extras=extras) for item in obj)
    raise TypeError(type(obj))


class Copy:
    def __init__(self, locale: str, data: dict):
        self.locale = locale
        self.data = data
        self.extras_html = {
            "promise": fill(data["promise"], locale, html_mode=True),
            "step_ready": fill(data["step_ready"], locale, html_mode=True),
            "email_link": email_link(locale),
        }
        self.extras_text = {
            "promise": fill(data["promise"], locale, html_mode=False),
            "step_ready": fill(data["step_ready"], locale, html_mode=False),
        }

    def html(self, key: str) -> str:
        return fill(self.data[key], self.locale, html_mode=True, extras=self.extras_html)

    def text(self, key: str) -> str:
        return html.escape(self.raw(key), quote=True)

    def raw(self, key: str) -> str:
        return fill(self.data[key], self.locale, html_mode=False, extras=self.extras_text)

    def rows(self, key: str):
        return _walk(self.data[key], self.locale, html_mode=True, extras=self.extras_html)


def same_shape(left, right, path: str = "") -> list[str]:
    if isinstance(left, str):
        if isinstance(right, str):
            return []
        return [f"{path}: expected text"]
    if isinstance(left, list):
        if not isinstance(right, list) or len(left) != len(right):
            return [f"{path}: expected {len(left) if isinstance(left, list) else '?'} items"]
        problems: list[str] = []
        for index, (item, other) in enumerate(zip(left, right)):
            problems.extend(same_shape(item, other, f"{path}[{index}]"))
        return problems
    if isinstance(left, tuple):
        if not isinstance(right, tuple) or len(left) != len(right):
            return [f"{path}: expected a pair"]
        problems = []
        for index, (item, other) in enumerate(zip(left, right)):
            problems.extend(same_shape(item, other, f"{path}[{index}]"))
        return problems
    if isinstance(left, dict):
        problems = []
        for key in left:
            if key not in right:
                problems.append(f"{path}.{key}: missing")
            else:
                problems.extend(same_shape(left[key], right[key], f"{path}.{key}"))
        for key in right:
            if key not in left:
                problems.append(f"{path}.{key}: unexpected")
        return problems
    return [f"{path}: unsupported"]


def load_strings() -> dict[str, dict]:
    from i18n_ar import DATA as AR
    from i18n_de import DATA as DE
    from i18n_en import DATA as EN
    from i18n_es import DATA as ES
    from i18n_fr import DATA as FR
    from i18n_hi import DATA as HI
    from i18n_id import DATA as ID
    from i18n_it import DATA as IT
    from i18n_ja import DATA as JA
    from i18n_ko import DATA as KO
    from i18n_pt import DATA as PT
    from i18n_ru import DATA as RU
    from i18n_zh import DATA as ZH

    strings = {
        "en": EN,
        "es": ES,
        "pt-BR": PT,
        "fr": FR,
        "de": DE,
        "it": IT,
        "zh-Hans": ZH,
        "ja": JA,
        "ko": KO,
        "hi": HI,
        "ar": AR,
        "ru": RU,
        "id": ID,
    }
    problems: list[str] = []
    for code, _folder, _direction, _name in LOCALES:
        if code not in strings:
            problems.append(f"{code}: missing catalog")
            continue
        problems.extend(f"{code}{item}" for item in same_shape(EN, strings[code]))
    if problems:
        raise ValueError("locale catalogs do not match English:\n" + "\n".join(problems))
    return strings
