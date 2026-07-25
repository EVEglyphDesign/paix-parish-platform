#!/usr/bin/env python3
"""Extract every translatable string on the surface into i18n/source.json.

The manifest is the single source of truth for translation. Latin (la.json) is
authored from this manifest and every other language is translated FROM Latin,
so all languages sit symmetrically the same distance from one pivot.

Keys never carry markup. Proper nouns, street addresses, clock times and
telephone numbers are deliberately NOT in this manifest -- they are rendered
verbatim from PARISHES in every language.
"""
import importlib.util
import json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("b", ROOT / "build.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

S = OrderedDict()


def put(key, text, note=""):
    S[key] = {"text": text, "note": note} if note else {"text": text}


# ---------------------------------------------------------------------------
# 1. Parish-site chrome (the 30 keys that used to live in STRINGS)
# ---------------------------------------------------------------------------
UI = OrderedDict([
    ("home", "Home"),
    ("about", "Our parish"),
    ("pastors", "Clergy"),
    ("church", "Our church"),
    ("mass", "Mass schedule"),
    ("bulletin", "Bulletin"),
    ("life", "Parish life"),
    ("catechesis", "Faith formation"),
    ("events", "Events"),
    ("links", "Links"),
    ("contact", "Contact"),
    ("welcome", "Welcome"),
    ("mass_h1", "Mass schedule"),
    ("mass_day", "Day"),
    ("mass_time", "Time"),
    ("contact_h1", "Get in touch"),
    ("about_h1", "Our parish"),
    ("reach_us", "Reach us"),
    ("on_this_site", "On this site"),
    ("doctrine", "Doctrine"),
    ("no_profile", "No profiling"),
    ("register", "Language register"),
    ("founder", "Founder credit"),
    ("portal_back", "Back to the portal"),
    ("official_source", "Official source"),
    ("mirror_note", "Non-official mirror, prepared with care. Parish content: the parish holds all rights."),
    ("no_tracking", "No tracking. No cookies. No analytics. No third-party scripts other than Google Fonts."),
    ("tribute_line", "Site built under the EVE Glyph Design doctrine. Design founder:"),
    ("for_people", "For the good of the people."),
    ("welcome_lead", "Welcome to the parish website."),
    ("photo_pending", "Photograph pending. This mirror will not publish an image it does not have the right to publish."),
    ("commitment_h", "Our commitment"),
    ("commitment_p", "Locally hosted, no tracking, no ads. The parish owns its content and may take over this mirror at any time."),
    ("about_founded", "Founded in {year}, {name} serves the community of {city}. It is part of {diocese}."),
    ("about_official", "This page introduces the parish. For the full history, clergy biographies and church story, please visit the parish's official site:"),
    ("lang_label", "Language"),
    ("lang_pivot_note", "Every language on this surface is translated from a single Latin baseline, so no language is a second-class citizen of another."),
])
for k, v in UI.items():
    put("ui." + k, v)

# ---------------------------------------------------------------------------
# 2. Portal chrome
# ---------------------------------------------------------------------------
P = OrderedDict([
    ("title", "PAIX Parish Platform"),
    ("subtitle", "Parish Sovereign Gateway — a community-first alternative to predatory hosting"),
    ("meta_desc", "A parish-owned platform template. Locally hosted, no tracking, no ads. Under the EVE Glyph Design doctrine."),
    ("nav_parishes", "Parishes"),
    ("nav_ledger", "Charitable Ledger"),
    ("nav_about", "About the platform"),
    ("nav_kofc", "For the Knights"),
    ("nav_doctrine", "Doctrine"),
    ("hero_h1", "A parish website belongs to the parish."),
    ("hero_lead", "{count} parishes across four countries, one design canon, nine languages. Locally hosted. No tracking. No ads. No third-party predators. Every dollar stays in the community."),
    ("hero_p", "Select a parish to enter its site. Every parish site shares the same EVE Glyph Design canon, so navigation and typography stay familiar. Each parish's official site remains the source of truth — this is a mirror prepared with care, ready to be handed over to the parish's existing IT volunteer whenever they want it."),

    ("ledger_badge", "Paired with the parish sites"),
    ("ledger_h2", "The Charitable Ledger"),
    ("ledger_lead", "A running tally of what the people already do around here — the shopping, the hour of help, the favour from someone with a trade — so it adds up somewhere and the parish can see it."),
    ("ledger_li1", "Shop through the parish code, the savings go to the parish."),
    ("ledger_li2", "An hour of help, one witness signs off, it goes on the ledger."),
    ("ledger_li3", "Someone with a trade — plumber, accountant, nurse — can put an hour in at their real rate."),
    ("ledger_li4", "One page, the whole parish can read it."),
    ("ledger_cta1", "See how it works"),
    ("ledger_cta2", "Letter to the Knights"),

    ("about_h2", "What this is"),
    ("about_p", "{count} Catholic parishes, each with a mirrored site under a shared editorial template. Same header, same footer, same navigation — but each parish keeps its own crest, mass times, contact information and diocesan link. If a parish already has an IT volunteer, this is not a replacement; it is an option they can inspect, fork, or ignore."),
    ("pillar1_h", "Locally hosted"),
    ("pillar1_p", "Static site on GitHub Pages or the parish's own hosting. No third-party dashboards, no vendor lock-in."),
    ("pillar2_h", "Zero surveillance"),
    ("pillar2_p", "No cookies. No analytics. No third-party scripts other than Google Fonts. Marked noindex, nofollow until the parish approves publication."),
    ("pillar3_h", "Full parish ownership"),
    ("pillar3_p", "The parish owns its content, its domain, and its exit. Fork the repository, take it home, keep going."),
    ("pillar4_h", "Consistent design"),
    ("pillar4_p", "Shared EVE Glyph Design canon so parishioners moving between parish sites feel at home."),

    ("lang_h2", "Nine languages, one baseline"),
    ("lang_p1", "This surface is not English with translations bolted on. Every string is carried to a single Latin baseline first, and every other language is rendered from that baseline. Latin is the pivot because it is the language the Church already shares, and because a pivot means no living language is subordinate to another living language."),
    ("lang_p2", "Latin, English, French, Spanish, Italian, Portuguese, Romanian, Greek and Swahili. Greek is rendered from the Latin baseline like every other tongue. Swahili is here because the platform is for all people, not only the wealthy ones — a person should be able to show this to their mother and their sister in the language they actually think in, and be understood."),
    ("lang_p3", "Proper names, street addresses, telephone numbers and clock times are never translated. They are rendered exactly as the parish publishes them, in every language."),

    ("kofc_h2", "For the Knights of Columbus"),
    ("kofc_lead", "This is what scale in a week looks like — with no hurt feelings."),
    ("kofc_p", "If the Knights want to standardize parish web presence across a diocese, this template can spin up a new parish site in about an hour. But that is not the offer. The offer is a choice:"),
    ("kofc_li1_b", "Existing IT volunteer stays put."),
    ("kofc_li1", "If a Brother Knight or parishioner is already running the parish site, nothing is disrupted. This platform is available if they want to switch or fork; otherwise it sits alongside their existing work as a reference."),
    ("kofc_li2_b", "Money stays in the parish."),
    ("kofc_li2", "No annual hosting invoices, no website subscriptions, no advertising credits. Static hosting is free, and every dollar the parish saves stays in the community."),
    ("kofc_li3_b", "Parishioners stay safe."),
    ("kofc_li3", "No surveillance, no engagement-optimized feeds, no algorithmic exposure of children, women, or vulnerable people. The parish site is a parish site — not a data-extraction surface for a distant platform."),
    ("kofc_li4_b", "The Knights stay in charge."),
    ("kofc_li4", "Ownership, doctrine and exit rights belong to the parish and its Council. The design canon is a shared reference, not a vendor contract."),
    ("kofc_note", "Council of Palms #6673 (Holy Trinity, Lenexa) is the reference council for this build."),
    ("kofc_xref", "The Charitable Ledger above pairs with the parish sites — that is the other half of what is on offer."),

    ("doctrine_h2", "Doctrine"),
    ("doc1_h", "No profiling"),
    ("doc1_p", "No parishioner is scored, categorized or targeted by this platform. Ever."),
    ("doc2_h", "Safety first, betterment second"),
    ("doc2_p", "Content and identity safety comes before growth, engagement, or monetization."),
    ("doc3_h", "Founder credit"),
    ("doc3_p", "Design founder: {founder}, EVE Glyph Design. This credit is irrevocable."),
    ("doc4_h", "Parish sovereignty"),
    ("doc4_p", "The parish binds the platform, receives a governance receipt, and may exit with full content export at any time."),

    ("related_h2", "Related surface"),
    ("rel1_h", "PAIX Educational Game"),
    ("rel1_p", "The parishioner-facing educational video game — the game surface of the EVE Glyph Design education program, distributed through the parish and Church portal. Education first; catechetical outputs stay disabled until Church review is complete. Safety first, betterment second."),
    ("rel2_h", "Holy Trinity Charitable Ledger (Lenexa pilot)"),
    ("rel2_p", "The Holy Trinity Lenexa mutual-aid economy pilot. One good deed. One witness. One hour. One token."),

    ("foot_col1_h", "PAIX Parish Platform"),
    ("foot_col1_p", "A Parish Sovereign Gateway reference build. Under the EVE Glyph Design doctrine. Contact the parish directly — see each parish page for details."),
    ("foot_col2_h", "Parishes"),
    ("foot_col3_h", "Reference"),
    ("foot_ref1", "Sainte-Anne source repository"),
    ("foot_ref2", "KofC #6673 outreach"),
    ("foot_ref3", "GoDaddy-Killer migration kit"),
    ("foot_tribute1", "Platform designed under the doctrine EVE Glyph Design. Design founder:"),
    ("foot_tribute2", "Every parish retains full ownership of its own content, domain and exit path. This is a mirror prepared with care, not a takeover."),
    ("foot_photos", "Church photographs:"),
])
for k, v in P.items():
    put("portal." + k, v)

# ---------------------------------------------------------------------------
# 3. Regions
# ---------------------------------------------------------------------------
for rid, name, sub in b.REGIONS:
    put(f"region.{rid}.name", name)
    put(f"region.{rid}.sub", sub)

# ---------------------------------------------------------------------------
# 4. The 1613 footnote
# ---------------------------------------------------------------------------
F = OrderedDict([
    ("h2", "Footnote — and who were the Acadians, anyway?"),
    ("aside", "Down here at the bottom, because it is a footnote and not a sales pitch."),
    ("p1", "Long before any of the parishes above, there was one at Port-Royal, in what is now Nova Scotia: Saint-Jean-Baptiste, founded 1613. Capuchin friars ran the mission from 1632. First Catholic parish in what eventually became Canada."),
    ("p2", "Then most of the paperwork stopped existing. In 1654 a New England force under Robert Sedgwick took Port-Royal, killed the Capuchin superior Léonard de Chartres and shipped his confrères out — against the terms of the capitulation they had just signed. Two registers survive: 1702–1728 and 1727–1755, now at the Centre acadien of Université Sainte-Anne. Everything before 1702 is gone."),
    ("p3", "The Greek card above is the other half of the same idea. In Nafplio, a wooden arch put up in 1841 carries the names of roughly 280 foreigners who died for somebody else's country, each one with the place he fell written beside it. Somebody decided those names were worth keeping. In Port-Royal, somebody decided ours were not."),
    ("p4", "People ask whether Rome kept a copy. Rome does governance, not sacraments — there is no central baptismal register in the Vatican. Baptisms are written down in the parish, full stop. When the parish burns, that is the end of it."),
    ("p5", "One set did travel. The Saint-Charles-des-Mines registers from Grand-Pré went with the deported Acadians to Maryland, then to Louisiana, and were handed to the priest at Fort San Gabriel in 1767. They sit in the Diocese of Baton Rouge vaults today."),
    ("p6", "And no, this is not a claim to being the oldest Catholic anything in North America. St. Augustine, Florida has 1565 — it is the second card at the top of this page. San Miguel Chapel in Santa Fe is around 1610. Port-Royal is just the first one that is ours, and the one whose paperwork got burned."),
    ("more", "Full write-up — the Acadian lineage page"),
])
for k, v in F.items():
    put("footnote." + k, v)

# ---------------------------------------------------------------------------
# 5. Per-parish prose + schedule day labels
# ---------------------------------------------------------------------------
PROSE = ["tagline", "portal_blurb", "city_line", "status_note", "schedule_note",
         "founded_line", "diocese"]
for p in b.PARISHES:
    for f in PROSE:
        if p.get(f):
            put(f"parish.{p['slug']}.{f}", p[f], note=f"source language: {p['lang']}")
    for i, (day, _time) in enumerate(p.get("schedule", [])):
        put(f"parish.{p['slug']}.sched.{i}", day,
            note=f"day/occasion label only; the clock time is never translated (source: {p['lang']})")

out = ROOT / "i18n" / "source.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {out} — {len(S)} strings")
