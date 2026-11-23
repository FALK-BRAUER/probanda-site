# DESIGN.md — probanda.ai

Mode: **Persuade** (marketing site for senior enterprise buyers). Identity: calm, editorial, enterprise —
annual report / audit committee paper, not a startup landing page. Refinements keep this identity.
Source of truth for styles: `src/probanda.css` (scoped under `.pb.pb`). Reuse existing blocks from
`src/pages/` before inventing new ones.

## Colour tokens (CSS variables; from the Probanda AI brand kit v2, Drive `08-brand`)
| Token | Value | Use |
|---|---|---|
| `--paper` / `--paper2` | #FFFFFF / #EEF2F3 | page background (white, ~80%) / quiet panels (brand `surface`) |
| `--ink` / `--ink2` / `--mut` | #0E1B2D / #5F646A / #5F646A | navy text / secondary / labels (brand `ink`, `ink-muted`) |
| `--line` | #D3DCDB | hairlines (brand `rule`) |
| `--t` / `--t2` | #11786F / #E3F0EE | teal accent on white: eyebrows, links, the square, "met" |
| `--mint` | #2FD3C0 | accent on navy only; never on white |
| `--night` / `--blue` | #0E1B2D | navy: top bar, dark panels, footer (no pure black) |
| `--blue2` | #EEF2F3 | quiet panel (alias of surface) |
| `--amb` / `--amb2` | #B7791F / #F7ECD9 | status only: person decides, sent back, risky |
| `--red` / `--red2` | #B4472F / #F6E3DD | status only: blocked, breach, exception |
| green (inline) | #2E8A57 on #E3F1E8 | status only: done, allowed, met |
Teal on white, mint on navy. One accent per block. Status colours carry meaning only and always with a word.
No gradients, no shadows.

## Type and signature
- Inter only (400/500/600). Headlines 600, tracking -0.02em (`.serif` now maps to this): h1 64-72px, section h2 44-52px.
- Body Inter 16px/1.55; intro `lead` 19px `--ink2`, max 640px. Labels `eyebrow` 14px 600 teal, sentence case.
- Sentence case everywhere; no all-caps headlines or labels.
- The brand square (teal on white, mint on navy) ends the hero title only, once per page.
- Logo: `assets/probanda-lockup-on-light.svg` in the header, `-on-dark` in the footer; favicon from the kit.
  Name is "Probanda AI"; tagline "Proof, complete." once, in the footer.

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
