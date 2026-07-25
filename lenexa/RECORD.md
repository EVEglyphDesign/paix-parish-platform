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
