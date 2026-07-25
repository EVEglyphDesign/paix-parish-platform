#!/usr/bin/env python3
"""Second half of the translation manifest: parish-page body prose.

These strings used to be hard-coded inside per-language `if parish['lang'] == ...`
branches in build.py. Lifting them into the manifest is what makes the surface
genuinely multilingual instead of five languages with hard-coded exceptions.
"""
import json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = OrderedDict()


def put(key, text, note=""):
    S[key] = {"text": text, "note": note} if note else {"text": text}


# --- parish index page -----------------------------------------------------
put("page.index_blurb",
    "{name}, founded in {founded}, is located in {city}. This site is a non-official "
    "mirror prepared under the EVE Glyph Design doctrine, with the same editorial care "
    "as the parish's official site. The official source remains {source_link}.",
    note="{name} {founded} {city} {source_link} are substituted at build time; keep all four placeholders")
put("page.index_blurb_nofound",
    "{name} is located in {city}. This site is a non-official mirror prepared under the "
    "EVE Glyph Design doctrine, with the same editorial care as the parish's official "
    "site. The official source remains {source_link}.",
    note="variant used when the founding year is unknown; keep all three placeholders")
put("page.card_title", "One parish, one people")
put("page.card_body",
    "Faith lived locally, with a community that prays, celebrates and cares for one another.")

# --- parish life page ------------------------------------------------------
put("page.life_h1", "Parish life")
put("page.life_intro",
    "The active groups in the parish. To learn more or to join a group, contact the parish office.")
for i, item in enumerate([
        "Prayer group",
        "Eucharistic adoration",
        "Choir",
        "Faith formation",
        "Knights of Columbus",
        "Parish pastoral council",
        "Outreach to those in need",
        "Parish volunteering"]):
    put(f"page.life_item.{i}", item, note="short list item, two or three words")

# --- contact page ----------------------------------------------------------
put("page.dt_address", "Address")
put("page.dt_phone", "Phone")
put("page.dt_email", "Email")
put("page.dt_diocese", "Diocese")
put("page.tel_abbrev", "Tel.", note="abbreviation for telephone used in the footer, with trailing period")

# --- Nafplio-specific about-page content -----------------------------------
put("nafplio.location",
    "The church stands in the Old Town of Nafplio, up the steps above the square of "
    "Agios Spyridon. People in Nafplio call it the Frankoklisia — the Frankish church. "
    "It belongs to {diocese}.",
    note="keep the {diocese} placeholder; Frankoklisia and Agios Spyridon are proper nouns")
put("nafplio.history",
    "The building served as a mosque in the years before the Greek War of Independence. "
    "In 1839 the Municipality of Nafplio ceded it to the Catholic Church by royal decree "
    "of King Otto, and in 1840 it was consecrated to the Transfiguration of the Saviour — "
    "a choice of name meant to stand for the transfiguration of the country itself after "
    "the Ottoman period. The mihrab is still there inside.")
put("nafplio.arch_h", "The Touret Arch (1841)")
put("nafplio.arch_p",
    "Inside the church stands a wooden arch shaped like the front of an ancient temple, "
    "paid for by the French philhellene Auguste Hilarion Touret. It carries the inscription "
    "A LA MEMOIRE DES PHILHELLENES MORTS POUR L'INDEPENDANCE and the names of roughly 280 "
    "foreign volunteers, each with the place where he fell written beside it. It is the "
    "oldest monument to the Philhellenes in Greece, and it was restored in 2002.",
    note="the French inscription must be reproduced verbatim in every language, never translated")
put("nafplio.crypt_h", "The crypt")
put("nafplio.crypt_p",
    "Under the floor there is a Venetian cistern about three metres deep. In 1839 the bones "
    "of philhellenes and of Bavarian soldiers lost to typhoid fever in 1833–1834 were moved "
    "into it. In 1990 the relief Philhellenes Fighting for the Greeks, by Nikolaos Dagoulis, "
    "was installed there.")
put("nafplio.card_title", "One parish, one people")
put("nafplio.card_body",
    "Faith lives where it stands, with a community that prays, celebrates and looks after "
    "one another.")

out = ROOT / "i18n" / "_split_pages.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {out} — {len(S)} strings")
