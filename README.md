> **⚑ Arrivals register at the front door.**
> If you were sent here from a public post, a mention, or a professional referral, please [register your arrival](https://github.com/EVEglyphDesign/eveglyph-arrivals/issues/new?template=arrival.yml) at [github.com/EVEglyphDesign](https://github.com/EVEglyphDesign) before continuing. Ninety seconds. Public. Timestamped. Screeners, agents, publicists, journalists, engineers, and principals all use the same door.
>
> *Compelled engagement, not asked engagement.*

---
# PAIX Parish Platform

A Parish Sovereign Gateway reference build under the **EVE Glyph Design** doctrine.

Front-page portal + **twelve mirrored parish sites across five regions**, each published in **nine languages**, all in one editorial canon:

**United States**
- **Holy Trinity Catholic Parish** — Lenexa, Kansas
- **Cathedral Basilica of St. Augustine** — St. Augustine, Florida

**Montréal**
- **Oratoire Saint-Joseph du Mont-Royal** — Montréal, Québec

**Atlantic Canada**
- **St. Dunstan's Church** — Fredericton, New Brunswick. The founding Catholic parish of Fredericton (1827) and the first cathedral of New Brunswick; Bishop William Dollard was consecrated here on 11 June 1843. The Great Fire of 11 November 1850 spared it — parishioners stood on the roof and beat out the embers. It incubated Sainte-Anne-des-Pays-Bas, which became an independent French-language parish on 2 September 1981. Today part of St. Mary Magdalene Parish.
- **Paroisse Sainte-Anne-des-Pays-Bas** — Fredericton, Nouveau-Brunswick
- **Église Saint-Augustin de Paquetville** — Paquetville, Nouveau-Brunswick
- **St. Dunstan's Basilica Parish** — Charlottetown, Prince Edward Island
- **Saint Catherine of Siena Church** — Halifax, Nouvelle-Écosse
- **Saint Mary's Cathedral Basilica** — Halifax, Nouvelle-Écosse

**México**
- **Cuasiparroquia de la Sagrada Familia** — Las Jarretaderas, Nayarit
- **Parroquia de La Santa Cruz** — La Cruz de Huanacaxtle, Nayarit

**Ελλάδα · Greece**
- **Ιερός Καθολικός Ναός Μεταμορφώσεως του Σωτήρος** — Ναύπλιο, Αργολίδα. The «Frankoklisia» of the Old Town: a mosque ceded to the Catholic Church in 1839 and consecrated in 1840, holding the 1841 Touret Arch — the oldest Philhellene monument in Greece, inscribed with the names of some 280 foreign volunteers who died for Greek independence.

## Languages — Latin is the pivot

Nine languages: **Latina · English · Français · Español · Italiano · Português · Română · Ελληνικά · Kiswahili**.

The template is not a hub-and-spoke translation of English. Every string is first carried into **Latin** (`i18n/la.json`, the pivot), and every other language is rendered *from the Latin*, never from a sibling. That gives symmetrical alignment across the whole set — the Greek and the Swahili stand at the same distance from the centre as the French does.

- `i18n/source.json` — the extraction manifest (266 keys)
- `i18n/la.json` — the pivot
- `i18n/{en,fr,es,it,pt,ro,el,sw}.json` — the leaves, each rendered from the pivot
- `i18n_runtime.py` — resolution order `<lang> → la → source`, with placeholder-integrity fallback and a coverage report printed on every build

Each parish's own language stays at the bare URL so no existing link breaks; the other eight sit under `/<code>/`. `hreflang` is emitted for all nine plus `x-default`. Proper nouns, street addresses, telephone numbers and clock times are never translated. The 1841 Touret arch inscription is reproduced byte-for-byte in all nine.

## Heritage

[`heritage/LIGNEE-ACADIENNE.md`](heritage/LIGNEE-ACADIENNE.md) — **La lignée / The Line.** Bilingual FR/EN. Poitou → Port-Royal → Grand-Pré → l'exil → la Louisiane → Sainte-Anne-des-Pays-Bas. Every dated claim marked **[R]** record, **[I]** inference, or **[L]** lore. Carries the correction that the family does not claim the oldest Roman Catholic site in North America, and the claim that is actually ours: the parish register the people carried out of Grand-Pré through the deportation.

## What this is

Static HTML/CSS. No tracking. No cookies. No analytics. No third-party scripts other than Google Fonts. `noindex, nofollow` throughout.

Reference build for the **Knights of Columbus Council of Palms #6673** (Holy Trinity, Lenexa) — showing how quickly a diocesan-scale parish platform can be stood up without disrupting existing IT relationships.

## Doctrine

- **No profiling.** No parishioner is scored, categorized or targeted.
- **Safety first, betterment second.** Content and identity safety before growth.
- **Founder credit.** Design founder: **Donat Omer Thériault**, EVE Glyph Design. Irrevocable.
- **Parish sovereignty.** Each parish owns its content, domain, and exit path.

## Build

```
python3 build.py
```

All content is generated from `PARISHES` in `build.py` plus the `i18n/` manifests. Adding a parish is one dict entry; adding a language is one `i18n/<code>.json` rendered from the Latin pivot.

*Pour le bien-être du peuple. For the good of the people.*
