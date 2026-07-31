#!/usr/bin/env python3
"""Latin-pivot translation runtime for the PAIX Parish Platform.

Doctrine
--------
Every string on this surface is carried to a single **Latin** baseline first,
and every other language is rendered from that baseline. Latin is the pivot
because it is the language the Church already shares, and because routing
through a pivot means no living language is subordinate to another living
language. English is a leaf like every other leaf.

Proper nouns, street addresses, telephone numbers and clock times are never
translated. They are rendered exactly as the parish publishes them, in every
language.

Resolution order for a key in language X:
    i18n/X.json  ->  i18n/la.json  ->  i18n/source.json (the raw source text)

A missing key is never fatal and never renders an empty element; it falls back
up the chain so a half-finished translation degrades to Latin rather than to a
blank page.
"""
from __future__ import annotations

import json
from pathlib import Path

I18N_DIR = Path(__file__).resolve().parent / "i18n"

# code, endonym (what speakers call it), html lang attribute, text direction
LANGS = [
    ("la", "Latina",     "la", "ltr"),
    ("en", "English",    "en", "ltr"),
    ("fr", "Français",   "fr", "ltr"),
    ("es", "Español",    "es", "ltr"),
    ("it", "Italiano",   "it", "ltr"),
    ("pt", "Português",  "pt", "ltr"),
    ("ro", "Română",     "ro", "ltr"),
    ("el", "Ελληνικά",   "el", "ltr"),
    ("sw", "Kiswahili",  "sw", "ltr"),
]
LANG_CODES = [c for c, _, _, _ in LANGS]
PIVOT = "la"
DEFAULT = "en"

# Reading order for the language rail. Latin remains the pivot in the runtime,
# but a reader arriving at the rail should descend through the living Romance
# languages first, reach Latin as their common root, then Greek, then the rest.
# This is presentation order only; it never changes resolution or fallback.
DISPLAY_ORDER = ["en", "fr", "es", "it", "pt", "ro", "la", "el", "sw"]
LANGS_DISPLAY = sorted(LANGS, key=lambda r: DISPLAY_ORDER.index(r[0])
                       if r[0] in DISPLAY_ORDER else len(DISPLAY_ORDER))

# Which of the nine each parish's own community actually speaks. The native
# copy is what lives at the parish's bare URL, so an existing link never breaks.
NATIVE_OF = {
    "en-US": "en", "en-CA": "en", "fr-CA": "fr", "es-MX": "es", "el-GR": "el",
}

_cache: dict[str, dict] = {}


def _load(name: str) -> dict:
    if name in _cache:
        return _cache[name]
    path = I18N_DIR / f"{name}.json"
    if not path.exists():
        _cache[name] = {}
        return _cache[name]
    raw = json.loads(path.read_text(encoding="utf-8"))
    # source.json wraps values as {"text": ..., "note": ...}; leaves are flat.
    flat = {}
    for k, v in raw.items():
        flat[k] = v["text"] if isinstance(v, dict) and "text" in v else v
    _cache[name] = flat
    return flat


class Translator:
    """Callable string table for one language, with pivot and source fallback."""

    def __init__(self, code: str):
        self.code = code
        self.endonym = dict((c, n) for c, n, _, _ in LANGS)[code]
        self.html_lang = dict((c, h) for c, _, h, _ in LANGS)[code]
        self._own = _load(code)
        self._pivot = _load(PIVOT)
        self._source = _load("source")
        self.missing: set[str] = set()

    def __call__(self, key: str, **fmt) -> str:
        for table in (self._own, self._pivot, self._source):
            if key in table and table[key]:
                s = table[key]
                break
        else:
            self.missing.add(key)
            return ""
        if table is not self._own:
            self.missing.add(key)
        if fmt:
            try:
                s = s.format(**fmt)
            except (KeyError, IndexError, ValueError):
                # A translator dropped or mangled a placeholder. Fall back to
                # the pivot rather than emitting a broken brace to a reader.
                alt = self._pivot.get(key) or self._source.get(key) or ""
                try:
                    s = alt.format(**fmt)
                except Exception:
                    s = alt
                self.missing.add(key + " [placeholder]")
        return s

    def has(self, key: str) -> bool:
        return bool(self._own.get(key))


def translator(code: str) -> Translator:
    return Translator(code)


def coverage() -> dict[str, tuple[int, int]]:
    """(translated, total) per language, measured against the source manifest."""
    total = len(_load("source"))
    out = {}
    for code in LANG_CODES:
        t = _load(code)
        out[code] = (sum(1 for k in _load("source") if t.get(k)), total)
    return out
