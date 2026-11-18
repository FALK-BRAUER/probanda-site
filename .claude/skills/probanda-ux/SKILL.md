---
name: probanda-ux
description: UX rules for probanda.ai — who visits, what each page must achieve, page anatomy, calls to action, navigation, accessibility, phone use, SEO and a review checklist. Use when planning a new page or section, reordering content, changing navigation or buttons, when the user asks "is this page good", "improve the page", "review the site", "make it clearer", or before publishing a larger change.
---

# probanda.ai UX

## Who visits and what they need
| Visitor | Arrives from | Needs within 30 seconds | Next step we want |
|---|---|---|---|
| CFO / COO | LinkedIn post, referral | What problem, why now, is this serious | Talk to us |
| Chief risk officer, compliance | Framework search, event | How it maps to frameworks, what evidence exists | Request a sample evidence pack |
| Head of internal audit | Referral from risk | Can I verify it independently | Sample evidence pack |
| CIO / platform owner | Vendor shortlist | Which systems, where it runs, effort | Readiness workshop |
| Partner (SI, consultancy) | Partner outreach | What they deliver, how they earn | Become a partner |

Every page serves one main visitor and one next step. If a section serves no one in this table, cut it.

## Page anatomy (keep this order)
1. **Eyebrow + headline + one-sentence lead**: what this page answers, in the reader's words.
2. **Proof early**: a picture, a number with a source, or a concrete example before long text.
3. **How it works**: 3-5 steps or blocks, never more than 6 items in one group.
4. **Objections answered**: data residency, effort, who does what, frameworks (FAQ or short blocks).
5. **One primary call to action** (dark `.btn`), at most one secondary (outlined `.btn.l`).
Headline scan test: reading only the headlines of a page should tell the whole story.

## Calls to action
- Verb + outcome: "Request a sample evidence pack", "Book a readiness workshop", "Talk to us". Never "Learn more", "Click here", "Submit".
- Every button is a real link (`<a class="btn" href="/contact/">`); no dead buttons.
- Same action = same wording on every page.

## Navigation and links
- Top navigation stays as defined in `build.py` (`nav`); change it only on request and keep ≤ 7 items.
- Internal links end with `/` (`/use-cases/`). Link text says where it goes ("Browse all use cases →").
- New pages must be reachable from at least one existing page, and added to `pages` in `build.py`.

## Accessibility (WCAG 2.2 AA as the bar)
- Contrast ≥ 4.5:1 for text (`--mut` on `--paper` is the lightest allowed for small text; never lighter).
- One `h1` per page; headings in order (h2 under h1, h3 under h2); don't pick headings for size.
- Meaningful images and SVG diagrams need a text equivalent (the phone list, a caption or `aria-label`).
- Status is never colour-only: pills carry words ("Blocked", "Met").
- Tap targets ≥ 44px on phones; no hover-only information.

## Phone
Most first visits come from LinkedIn on a phone. Check the phone screenshot first: headline fits in
3-4 lines, first proof visible within two screen heights, no sideways scroll, tables readable as cards.

## SEO basics
- Each page: unique `<title>` (`build.py` → `pages` titles) and a specific meta description.
  Currently all pages share one description in `build.py`; when touching a page, give it its own (≤ 155 characters).
- Headline and lead use the words buyers search for: "AI agent governance", "AI agent audit trail",
  "human oversight AI agents", "EU AI Act record-keeping".

## Review checklist (run before "publish")
- [ ] Main visitor and next step of the page are obvious from the first screen.
- [ ] Headline scan tells the story; no section without a reader.
- [ ] One primary CTA, working link, standard wording.
- [ ] Contrast, heading order, text equivalents, colour + word for status.
- [ ] Phone screenshot read top to bottom; desktop screenshot read top to bottom.
- [ ] Wording passes `probanda-copy`; visuals pass `probanda-design`.
