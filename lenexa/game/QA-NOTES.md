# The Lantern Room — QA notes (25 July 2026)

File: `lenexa/game/index.html` (single file, vanilla HTML/CSS/JS, no build step, no dependencies).
Only external request: Google Fonts (Cormorant Garamond + Source Sans 3), same as the dashboard.
Stylesheet: `../../assets/style.css` + page-scoped `<style>`.

## Playthrough verified with Playwright
- Title → Begin → 5 scenarios in sequence → consequence + principle on each → end screen. Ran three full passes (choice A path, B path, C path) plus one keyboard-only pass (Tab to Begin, Enter through every step).
- Teacher view toggle verified on all three screens (title, play, end); `aria-pressed` flips and label reads "Teacher view: on/off".
- "Play again" resets the in-memory `path` array and returns to the title screen.
- No console/page errors.

## Privacy verification
- Source searched for `localStorage`, `sessionStorage`, `document.cookie`, `fetch(`, `XMLHttpRequest`, `sendBeacon`, `indexedDB`, `WebSocket`, `gtag`, `<script src` — zero code matches (only prose in the no-data panel).
- Runtime check after a full playthrough: `localStorage.length === 0`, `sessionStorage.length === 0`, `document.cookie === ""`.
- Network log during a full playthrough: only the page itself and two Google Fonts files.

## Layout
- `document.documentElement.scrollWidth === 390` at 390×844 on the title, play and end screens — zero horizontal overflow.
- 1440×1000 verified, `scrollWidth === 1440`.
- Focus ring: 3px gold `:focus-visible` outline with 2px offset on every interactive element.
- Fixed during QA: base `main { background:#fffdf7; min-height:60vh }` from `assets/style.css` was creating a white dead zone under the title panel — overridden with `main.g-stage { background: transparent; min-height: 0 }`.

## Screenshots

## Honest labelling
Wireframe banner is on the title screen and immediately under the masthead on every screen. "What is wireframed, and what is real" section sits above the footer. ARK block and the Donat Omer Thériault founder credit are in the footer verbatim.

Screenshots were reviewed during QA and kept out of the repository so the public
surface stays to the artifact itself. Re-run the checks against a local server
(`python3 -m http.server` from the repository root, then `/lenexa/game/`).

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
