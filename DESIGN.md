# DESIGN.md — probanda.ai

Mode: **Persuade** (marketing site for senior enterprise buyers). Identity: calm, editorial, enterprise —
annual report / audit committee paper, not a startup landing page. Refinements keep this identity.
Source of truth for styles: `src/probanda.css` (scoped under `.pb.pb`). Reuse existing blocks from
`src/pages/` before inventing new ones.

## Colour tokens (CSS variables; no new hex values)
| Token | Value | Use |
|---|---|---|
| `--paper` / `--paper2` | #FAF8F3 / #F2EEE5 | page background / alternate band |
| `--ink` / `--ink2` / `--mut` | #16211F / #47524F / #7A8480 | text / secondary / labels (lightest allowed for small text) |
| `--line` | #E3DED3 | borders, dividers |
| `--t` / `--t2` | #1F6B67 / #E4EFEC | teal accent: eyebrows, links, "met" |
| `--amb` / `--amb2` | #B7791F / #F7ECD9 | person decides, sent back, risky |
| `--red` / `--red2` | #B4472F / #F6E3DD | blocked, breach, exception |
| `--blue` / `--blue2` | #355F8C / #E4EBF3 | frameworks, second panel |
| `--night` | #0F1B1A | top bar, dark panels |
| green (inline) | #2E8A57 on #E3F1E8 | done, allowed, met |
Status colours carry meaning only; status is never colour-only (pills always carry a word).

## Type
- Headlines `serif` (Newsreader 500, tight tracking): h1 64-72px desktop, section h2 44-52px.
- Body Inter 16px/1.55; intro `lead` 19px `--ink2`, max 640px. Labels `eyebrow` 13px caps teal.
- Numbers `mono` (Inter, tabular figures). Minimum 13px anywhere, 16px running text, lines ≤ ~70 characters.

## Components
`.wrap` 1200px · `.grid` + inline columns, gap 20 · `.card` white, 1px `--line`, radius 16, padding 26 ·
`.card.dash` partner-led · `.chip` · `.btn` dark pill (primary), `.btn.l` outlined (secondary), always `<a>` ·
`.pl` large coloured panel · `.flow`/`.n`/`.a` step flow · `.lvl` level boxes · `.gate` approval box ·
tables with `<th>` header (become labelled cards on phones) · status pills (radius 999, 12px 600).

## Product mockups
`.app` window with `.tb` title bar (three dots + title). Preceded by the yellow `ILLUSTRATIVE · fictional data`
chip and one sentence saying who the view is for. Business content only: agents by function, real system
names, amounts with currency, named roles. Totals add up. No code, IDs, hashes or logs.

## Page anatomy
Eyebrow + headline + one-sentence lead → proof early (picture, sourced number, example) → how it works
(3-5 blocks, never > 6) → objections → one primary CTA (+ max one secondary). Reading only the headlines
tells the story. CTA wording: verb + outcome, same action = same words on every page.

## Responsive
Designed at 1440px; 900px media rules in `src/probanda.css` stack grids/panels, turn tables into cards and
staircase SVGs into lists. New content must work at 390px: no fixed widths > 340px in content, no absolutely
positioned content, no essential text only inside SVG. Tap targets ≥ 44px.

## Accessibility
WCAG 2.2 AA: contrast ≥ 4.5:1, one h1, headings in order, text equivalents for diagrams, no hover-only info.
