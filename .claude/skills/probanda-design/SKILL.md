---
name: probanda-design
description: Design system of probanda.ai — colours, type, components, page patterns, product mockups, phone layout and wording. Use before adding or restyling any section, page, card, table, mockup or picture on the site, and when the user says "make it look better", "new section", "new page", "more enterprise", "redesign".
---

# probanda.ai design system

Look: calm, editorial, enterprise. Warm paper background, deep ink text, one teal accent, serif headlines,
sans body. Think annual report or audit committee paper, not a startup landing page.
**Reuse what exists.** Before building anything new, find the closest existing block in `src/pages/` and
copy its markup and inline styles. All styles live in `src/probanda.css` (scoped under `.pb.pb`).

## Tokens (use the variables, never new hex values)
| Token | Value | Use |
|---|---|---|
| `--paper` / `--paper2` | #FAF8F3 / #F2EEE5 | page background / alternate band |
| `--ink` / `--ink2` / `--mut` | #16211F / #47524F / #7A8480 | text / secondary text / labels |
| `--line` | #E3DED3 | borders, dividers |
| `--t` / `--t2` | #1F6B67 / #E4EFEC | teal accent (eyebrows, links, "met") / teal tint |
| `--amb` / `--amb2` | #B7791F / #F7ECD9 | needs review, risky, sent back |
| `--red` / `--red2` | #B4472F / #F6E3DD | blocked, breach, exception |
| `--blue` / `--blue2` | #355F8C / #E4EBF3 | frameworks, second panel |
| `--night` | #0F1B1A | top bar, dark panels |
| green (inline) | #2E8A57 on #E3F1E8 | done, allowed, met |

Status colours carry meaning: green = allowed/met, amber = person decides/sent back, red = blocked/
exception. Never use them decoratively.

## Type
- Headlines: `class="serif"` (Newsreader 500, tight letter-spacing). h1 ~64-72px desktop, section h2 ~44-52px.
- Body: Inter 16px/1.55; intro paragraph `class="lead"` (19px, `--ink2`, max 640px).
- Section label above a headline: `class="eyebrow"` (13px caps, teal), e.g. `WHY NOW`, `SERVICES`.
- Numbers in tables and stats: `class="mono"` (Inter with tabular figures).
- Minimum 13px for any text, 16px for running text. Keep lines under ~70 characters.

## Components
- `.wrap` content width 1200px · `.grid` + inline `grid-template-columns` for columns (gap 20px).
- `.card` white, 1px `--line` border, radius 16, padding 26. `.card.dash` = dashed, for partner-led items.
- `.chip` small rounded label; `.btn` dark pill button, `.btn.l` outlined. Buttons are links (`<a class="btn">`).
- `.pl` large coloured panel (radius 18) with serif h3 and ruled `li` list.
- `.flow` / `.n` / `.a` horizontal step flow; `.lvl` level boxes; `.gate` approval gate box.
- Tables: header row with `<th>`; the build turns them into labelled cards on phones automatically.
- Pills (status): inline `span` radius 999, 12px 600 weight, tint background + strong text colour (see home).

## Product mockups ("app" windows)
- Wrapper `.app` with title bar `.tb` (three grey dots + window title in 13px `--mut`).
- Always precede with the yellow chip `ILLUSTRATIVE · fictional data` and one sentence saying who the view is for.
- Content in business language: agent names by function (Accounts payable agent), real system names
  (SAP S/4HANA, Workday, ServiceNow, Salesforce), amounts with currency, named roles (CFO, Finance Manager).
- Every number must add up across the mockup (totals = sum of parts; caught counts = listed outcomes).
- No code, IDs, hashes, JSON, log lines or engineering terms in pictures.

## Phone layout
The site is designed at 1440px; `src/probanda.css` has the 900px media rules (grids to one column, panels
stacked, tables to cards, staircase SVGs to lists). Anything new must survive 390px: no fixed widths
above 340px inside content, no absolute positioning for content, no text inside SVG that matters on phones.
Always run the layout test and look at the `m-*.png` screenshot of the changed page.

## Wording
Calm, precise, senior. Short sentences. Verbs over nouns. Outcomes for the business ("your auditor can
check it offline"), not features. No hype ("revolutionary", "seamless"), no jargon (payload, SDK, eval,
pipeline, API in headlines). Never "certified", "compliant", "guaranteed".

## Before you call it done
1. `python3 build.py`, then the layout test (see `CLAUDE.md`): every page `ok`.
2. Look at desktop and phone screenshots of each changed page; fix overlaps, cramped text, orphan words.
3. Check colours come from tokens and status colours match meaning.
