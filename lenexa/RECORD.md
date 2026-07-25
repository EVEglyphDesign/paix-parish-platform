# Record of transmission — Lenexa lane

Append-only. Entries are added, never edited and never removed. A correction is a new
entry that references the one it corrects. This file is the ledger side of GLOBAL doctrine
§2 (*watermarks only — the proof lives outside the artifact, in the Git ledger and the
public hash index*) and §4 (*tokenized history is canonical*).

Nothing in this repository is ever force-pushed and no history is ever rewritten
(§5, the golden rule). The commit that introduces each entry below is the time stamp.

---

## EGD-LNX-2026-0725-01 — ARK Stewardship Brief, Lenexa Police Department (School Resource Unit)

| Field | Value |
| --- | --- |
| Artifact | `lenexa/ARK-Stewardship-Brief-Lenexa-PD-2026-07-25.pdf` |
| Title | ARK Stewardship Brief — Lenexa Police Department, School Resource Unit |
| Author | Dany Theriault, EVE Glyph Design |
| Design founder | Donat Omer Thériault — credit irrevocable, travels with the work |
| Date of record | 25 July 2026 |
| Pages | 3 |
| Bytes | 67076 |
| SHA-256 | `32dd3676562f4916fe082c137ac82548af2ca23afcaef6ea0419271bc33ba393` |
| MD5 | `cb068a9f3d0875a72b1cd48be12adbb4` |
| Permanent URL | https://eveglyphdesign.github.io/paix-parish-platform/lenexa/ARK-Stewardship-Brief-Lenexa-PD-2026-07-25.pdf |
| Companion surface | https://eveglyphdesign.github.io/paix-parish-platform/lenexa/ |
| Intended recipient | Lenexa Police Department, School Resource Unit, Special Operations Division |
| Purpose | To place the ARK copyright and stewardship framework before a local institution, in the guest-teacher context of the School Resource Officer role |

### Verify it

```
sha256sum ARK-Stewardship-Brief-Lenexa-PD-2026-07-25.pdf
# 32dd3676562f4916fe082c137ac82548af2ca23afcaef6ea0419271bc33ba393
```

Any file presenting itself as this brief and producing a different digest is not this
document. Compare against the digest published here and in the commit history.

### Canon conformance

| Check | Status |
| --- | --- |
| §1 Universal copyright footer, verbatim, unaltered | Present on page 3, machine-verified against the canonical string |
| §2 Watermarks only — no payload modification | No steganography, no hidden metadata, no embedded proof, no tracker, no remote asset. The footer is the only watermark and it is plain text. Fonts are embedded subsets of Cormorant Garamond and Source Sans 3 (SIL Open Font License). |
| §2 Hash the file as-is | Digest above is of the delivered bytes, unmodified after generation |
| §4 Tokenized history is canonical | Committed to `EVEglyphDesign/paix-parish-platform`, public history |
| §5 Reverse history / no force-push | No rewrite. This entry is append-only. |
| §6 Inheritor-operable | Plain PDF/1.4, no DRM, no password, no expiry, no vendor dependency. Regenerable from `make_brief.py` in the workspace lineage. |
| §7 No vendor lock-in | Open format, open fonts, open repository, open hash |
| §9 Safety rank 1, betterment rank 2 | The document's operative doctrine is "no profiling of individuals, ever" |
| Founder credit | Donat Omer Thériault, stated in the running foot of every page |
| TERM-INDEX | "Dany Theriault" without accent in the copyright line; "Donat Omer Thériault" with accents as design-founder name; "PAIX" all caps; "Pacific Utilities Design Council" written in full |

### Standing on transmission

The brief is published before it is sent. Transmission does not create the record — the
commit does. Once this entry exists, the document is fixed: any later version is a new
artifact with a new identifier and a new digest, and this one remains readable and
verifiable at the URL above for as long as the repository exists.

Reading, quoting and citing are permitted and encouraged, per `LICENSE-NOTICE.md`.
Re-implementation or adaptation of the methodology is governed by the umbrella
instrument at
[`EVEglyphDesign/umbrella-copyright-proof`](https://github.com/EVEglyphDesign/umbrella-copyright-proof/blob/main/LICENSE).

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.

Pour le bien-être du peuple.


---

## EGD-LNX-2026-0725-02 — ARK Extract, sealed

| Field | Value |
| --- | --- |
| Record | `EGD-LNX-2026-0725-02` |
| Key ID | `EVEGLYPH-LNX-2026-0725` |
| Artifact | `ARK-EXTRACT-LENEXA-PD-2026-0725.pdf` |
| Manifest | `ARK-EXTRACT-LENEXA-PD-2026-0725-manifest.txt` |
| Form | Sealed extract + verification manifest — the form used for *Pour Ève — extrait scellé* |
| Pages | 2, US Letter |
| Bytes | 70244 |
| SHA-256, extract | `bb165f871854c82046ee17a86cc68989f4be833e2fb9faa98d012b20c5bb2745` |
| SHA-256, manifest | `5e26edacaa63ac81edeca050ae3d674e49832420f9e943c4ff70740eea7a1007` |
| SHA-256, content payload | `dbe59c6c9a885f0575f64cd14f652469c5b1b80ea6bbc8f0d8c539b38aa84632` |
| Author | Dany Theriault |
| Steward | Pacific Utilities Design Council |
| Issued | 25 July 2026, Lenexa, Kansas |
| Prepared for | Lenexa Police Department — School Resource Unit, Special Operations Division |
| Status | Watermarked extract. Extract, not integral. |

### What this is, and how it differs from the brief

`EGD-LNX-2026-0725-01` is the **brief** — the argument, three pages, written to persuade a
reader who has not yet decided anything. This record is the **extract** — the instrument
itself, lifted out of the corpus, watermarked, fingerprinted and published before it is
transmitted. It carries the copyright paragraph verbatim, the reserved / assignable /
granted split, the binding doctrine, the digest of every artifact in the lane, the
verification procedure, and a three-party signature block. The institution's signature
line is deliberately left blank: the extract does not presume who signs for the City.

### Canon conformance

| Point | How it is met |
| --- | --- |
| §1 Universal copyright footer | Verbatim in the closing band and in the running foot of both pages |
| §2 Watermarks only | Visible diagonal plain-text watermark, "SEALED EXTRACT · EVEGLYPH-LNX-2026-0725". No steganography, no hidden metadata, no embedded proof payload. Proof lives here and in the manifest, outside the artifact |
| §3 Public stays public | Committed to a public repository, reachable without an account |
| §4 Tokenized history canonical | The commit, not the transmission, is the time stamp |
| §5 No history rewrite | Appended below the previous entry. Nothing above this line was altered |
| §6 Inheritor-operable | Verification is one `sha256sum` command; no tooling, no account, no dependency on us |
| §7 No vendor lock-in | Open format, open fonts, open repository, open digest |
| §9 Safety rank 1, betterment rank 2 | Stated as binding doctrine on the face of the extract |
| Founder credit | Donat Omer Thériault, in the running foot of both pages |
| TERM-INDEX | "Dany Theriault" unaccented in the copyright line; "Donat Omer Thériault" accented as design-founder name; "Pacific Utilities Design Council" in full |

### Note on the digest table

The digest table inside the extract covers the brief, the dashboard and the game
wireframe. It deliberately does **not** cover `RECORD.md`: this ledger is append-only by
design, so its digest is expected to change and hashing it inside a sealed artifact would
publish a value guaranteed to go stale. The extract's own digest cannot appear inside
itself and is published in the companion manifest and in the table above.

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.

Pour le bien-être du peuple.


---

## EGD-LNX-2026-0725-03 — ARK Command Briefing, printable

| Field | Value |
| --- | --- |
| Record | `EGD-LNX-2026-0725-03` |
| Document | `EGD-CMD-LNX-2026-0725` |
| Artifact | `ARK-Command-Briefing-LNX-2026-07-25.pdf` |
| Pages | 4, US Letter, print-first |
| Bytes | 87863 |
| SHA-256 | `38862e840939374d95fb4c3a5fcb7c1f8fde3d9b360da3e09edbc20ff2419e1d` |
| Generator | `make_command_brief.py`, department-parameterised |
| Author | Dany Theriault |
| Issued | 25 July 2026, Lenexa, Kansas |
| Purpose | A leave-behind that can be printed on a station printer and carried up the chain of command |
| Routing | Sgt. Jason Hinkle → Major Brett Rushton → Chief Eric Schmitz |

### Why a third document

`-01` is the brief: the argument, for a reader deciding whether the idea has merit. `-02`
is the extract: the instrument itself, sealed and fingerprinted. Neither is written for a
commander with four minutes. This one is. Page one is the entire ask and can be read
standing up; pages two to four are the evidence, the law and the risks. It carries a
three-option decision box and a routing table, and one of the three options is *not at this
time* — stated on the page, with no reply required.

It is print-first by construction: no full-bleed dark pages, no reversed body text, no
large solid fills that a station printer turns into a toner slick. Navy is confined to
rules, headings and two small bands.

### Reusable for the next department

The generator carries a `DEPARTMENTS` registry. A `template` entry sits beside the Lenexa
entry with the department name, unit, city, chain of command, districts and state statutes
left blank. Filling those and running `DEPT=<key> python3 make_command_brief.py` produces
the same document for the next department, with its own document identifier and its own
digest. Nothing about the argument is Lenexa-specific except the facts that should be.

### Also published in this commit

| Surface | Path | What it is |
| --- | --- | --- |
| The public record | `lenexa/evidence/index.html` | Every one of the 26 public repositories under `github.com/EVEglyphDesign`, each linked to its source and, for the 19 that have one, to its live site. The 7 without a published site say so rather than linking a dead address. Carries the SHA-256 of every document in this lane and the commands to check them. |

### A note on point-in-time digests

The sealed extract `-02` records a SHA-256 for `lenexa/index.html` as it stood at the moment
of sealing. That page has since gained links to this briefing and to the public record, so
its digest has moved. This is expected and is not a defect: a sealed extract is a snapshot,
and its value is that it fixes what was true at a stated time. The extract has **not** been
reissued and its own digest is unchanged. Living surfaces — the dashboard, the evidence
index, this ledger — are not the thing the seal is protecting.

---

## EGD-LNX-2026-0725-04 — audit findings, corrections, and the errata sheet

**Filed** 25 July 2026. Append-only. Nothing above this line was edited to produce it.

An accessibility audit, a full link check and a footer sweep were run against this lane and
against the wider estate after publication. What they found, and what was done, is below.

### Documents

| Document | SHA-256 | Status |
| --- | --- | --- |
| `ARK-Errata-LNX-2026-07-25.pdf` (1 page) | `e93e122b75904cd8a9aefe6ddad681bc03d033fe20b75e76c4d68e3d7e89148a` | New. The correction of record. |
| `ARK-Command-Briefing-LNX-2026-07-25.pdf` (4 pages) | `b64fe592b9eb703b9c8be023f9b12508e5fbbc8b98a366ca9b7b614a143d29f8` | Reissued. In force. |
| ↳ first issue, superseded | `38862e840939374d95fb4c3a5fcb7c1f8fde3d9b360da3e09edbc20ff2419e1d` | Superseded same day, before delivery. |
| `ARK-Stewardship-Brief-Lenexa-PD-2026-07-25.pdf` (3 pages) | `32dd3676562f4916fe082c137ac82548af2ca23afcaef6ea0419271bc33ba393` | **Unchanged.** Corrected by errata, not by edit. |
| `ARK-EXTRACT-LENEXA-PD-2026-0725.pdf` (2 pages) | `bb165f871854c82046ee17a86cc68989f4be833e2fb9faa98d012b20c5bb2745` | **Unchanged.** Sealed. Corrected by errata, not by edit. |

### Findings and disposition

| # | Finding | Severity | Disposition |
| --- | --- | --- | --- |
| 1 | Brief page 3, source item 8: labelled K.S.A. 38-2309, link resolved to the text of 38-2310. | Material for counsel | Errata 1. Generator corrected — both statutes now carried and separately linked in every future department brief. Published brief not reissued; its digest stands. |
| 2 | The umbrella copyright instrument is cited to `EVEglyphDesign/umbrella-copyright-proof`, which is private. An external reader following the citation gets a 404. | High | Errata 2. `LICENSE-NOTICE.md` in this repository is named as the operative public statement of terms. Whether to make the canonical instrument public is an Operator decision and has not been made. |
| 3 | The dashboard cited both Kansas statutes but linked only one. | Medium | Fixed in `lenexa/index.html`. Both now linked separately. |
| 4 | One axe-core violation on `lenexa/index.html`. | Medium | Fixed. Re-run: 0 violations on the dashboard, 0 on the evidence page, 0 on the game across all six states. Keyboard-only playthrough of the game passes. No tracking of any kind present. |
| 5 | Two repository descriptions named private individuals. | Medium | Rewritten. Neither now names a person who did not ask to be named. |
| 6 | Estate-wide footer sweep of all 19 live GitHub Pages sites: only 4 carried the canonical footer verbatim, 1 carried a non-verbatim variant, 14 carried none. | High — canon §1 | Filed as `SIN-EGD-2026-0725-Q-FOOTERGAP-high-16` in the truth-ledger. Remediation dispatched across the estate; commits are recorded in each repository's own history. |
| 7 | The canonical footer is stored with curly quotes in HTML and PDF and straight quotes in markdown, so a byte-exact comparison across formats fails by design. | Medium | Filed as `SIN-EGD-2026-0725-Q-GLYPHQUOTE-med-17`. Awaiting Operator ratification of a single canonical form. Recommendation on file: curly canonical, with a documented markdown transliteration. |
| 8 | `registry/INDEX.csv` in the truth-ledger was missing entries 11–17. | Medium | Repaired. |

### On method

Canon §12 requires that a defect be filed and corrected in the same motion, or the filing is
theatre. Findings 1 and 2 concern documents whose digests are already published and one of
which is sealed. Editing those files would break a fingerprint a reader may already hold, so
they were not edited. The errata sheet is the correction, and it is linked from both the
dashboard and the public record page with its own digest.

Findings 3–8 concern living surfaces, which carry no seal, and were fixed in place.

### Still open, and owed to the Operator

1. Ratification of the canonical quote character (SIN-17).
2. Whether `umbrella-copyright-proof` should be made public, which would close Erratum 2 at
   the source rather than by substitution.
3. An unterminated CSS comment in `paroisse-sainte-anne-des-pays-bas` that breaks that site's
   styling entirely. Found during the footer sweep, left untouched as out of scope, and
   recorded here so it is not lost.

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.

Pour le bien-être du peuple.
