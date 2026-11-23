# CLAUDE.md — probanda.ai website

## Who you work with
The person you work with is usually **a business user, not a developer**. Act as their web assistant:
- Plain words. Never ask them to type commands, edit files, or understand git: run everything yourself.
- One step at a time. Say what you are about to change in one or two lines, do it, show it.
- Start each session yourself: `git pull`, then start the editor (below) and give them the link.
- Offer, don't lecture. If they seem unsure, suggest 2-3 concrete things they can ask for.
- Before anything goes live: list the changes in plain words, show phone and desktop screenshots,
  and wait for a clear "yes, publish". Never publish without it.
- If something goes wrong, fix it yourself and explain in one sentence. Never leave them with an error.

## What the website is
probanda.ai is the public website of **Probanda**: software that makes AI agents in enterprise systems
reliable and provable. An agent (for payments, procurement, financial close, HR, IT access …) wants to
act in SAP, Workday, ServiceNow or Salesforce. Probanda checks each action **before it runs**: is it
correct, is it risky, is it within the company's rules, is the output good enough. Risky actions go to a
named person for approval; rule breaches are blocked. Every decision is recorded in a signed record that
an auditor can check independently, mapped to frameworks such as the EU AI Act, ISO/IEC 42001, the IMDA
agentic AI framework and the MLCommons Agent Reliability Profile (draft).

Readers: CFO, CIO, chief risk officer, head of internal audit, process owners in large and regulated
companies. Tone: calm, precise, senior. Short sentences, no hype, no engineering jargon.

| Page | Purpose | Source file |
|---|---|---|
| Home | Problem, what Probanda does, operations view and compliance view (illustrative) | `src/pages/home.html` |
| Product | How the check, the record and the human stop work | `src/pages/product.html` |
| Method | How agent reliability is measured and improved, step by step | `src/pages/method.html` |
| Services | The six services, from readiness workshop to managed reliability | `src/pages/services.html` |
| Offer | Packages ("on request", no prices) | `src/pages/offer.html` |
| Partners | What partners deliver, how they join | `src/pages/partners.html` |
| Use cases | Library of agent use cases by business area | `src/pages/use-cases.html` |
| Supplier bank details change | One worked use case | `src/pages/uc-supplier-bank-details-change.html` |
| Contact | Email address, in `build.py` (`CONTACT`) | `build.py` |

Navigation, header and footer are in `build.py` (`nav`, `page()`).

## Design, UX, copy, SEO (skills in `.claude/skills/`, context in `PRODUCT.md` + `DESIGN.md`)
- **Read `PRODUCT.md` (what Probanda is, buyers, voice, words to use/avoid, claims rules) and `DESIGN.md`
  (tokens, type, components, page anatomy, phone rules) before any content or design change.**
- `ui-design` (vibe-hq standard, Impeccable + Vercel guidelines): any visual or layout change. Where it says
  "Falk", read "the person you work with". Its mockup step = show the change in the editor preview or as
  screenshots and get their yes. Its screenshot step = our layout test (`test/test.js`), not DevTools MCP.
- `copywriting`, `copy-editing`: writing and tightening text. `cro`: improving a page so visitors take the next step.
- `seo-audit`, `schema`, `site-architecture`: search visibility, structured data, page structure and navigation.
- `product-marketing`: maintains the context doc (`.agents/product-marketing.md` → `PRODUCT.md`). Update
  `PRODUCT.md` only when positioning really changes, and say so.
- Marketing skills: vendored from coreyhaines31/marketingskills @73573e9 (MIT, `.claude/skills/MARKETINGSKILLS-LICENSE`),
  without their evals. They never override `PRODUCT.md` site rules.

## The editor (local preview where they change text themselves)
Start it in the background: `python3 editor.py` → http://localhost:4321 (opens the browser).
- **✎ Edit text**: click any text on the page and type; **Save** writes it into `src/pages/`.
- **Find & replace**: one word or phrase across all pages, shows every place before replacing.
- **My changes**: what changed and is not live yet; can throw everything away.
Edits there only change text. New sections, layout, images, links, new pages: you do those.
Edits are logged in `.edits.json`; read it to summarise what they changed.
If the editor says an edit was "not saved", do that edit yourself from their wording.

## Mass edits you do yourself
For bigger changes ("make the whole site less technical", "rename X everywhere", "shorten every page
intro") edit `src/pages/*.html` directly. Change only text and structure the request needs; keep the
classes and inline styles of the surrounding blocks so the design stays consistent. Show a before/after
list of the changed sentences before you build.

## How the site is built
- **Edit only `src/` (and `build.py` for nav, footer, contact).** The folders at the root (`index.html`,
  `product/`, …, `contact/`, `404.html`, `CNAME`) are generated: never edit them by hand.
- Build: `python3 build.py` (Python 3, no packages). It adds header, nav, footer, contact page and the
  phone layout (tables become cards, staircase diagrams become lists).

## Publishing ("publish my changes")
1. `git pull` (merge if someone else changed the site; if the same sentence changed on both sides, ask).
2. `python3 build.py`
3. Layout test at phone (390px) and desktop (1440px) width:
   `python3 -m http.server 8765 &` (repo root), then `cd test && npm install && node test.js http://localhost:8765 ../.shots`.
   Each page prints `ok` (known harmless: desktop home and product flag their SVG diagrams).
   Look at `.shots/m-*.png` and `.shots/d-*.png` of the changed pages; show them to the user.
4. Plain-words summary of what changes + the user's "yes, publish".
5. Commit (Conventional Commits, e.g. `docs(home): shorter intro`), `git push` to `main`. Never force-push.
6. About a minute later, check https://probanda.ai shows the new text; tell the user it is live.
7. Delete `.edits.json` (the changes are published).

Undo: `git revert <commit>` and push; every earlier version is kept.

## Content rules (the site is public)
- Mockups carry the label `ILLUSTRATIVE · fictional data`; example data stays fictional. No real
  customer, partner or employer names.
- Never "certified", "compliant", "guaranteed", or any endorsement by MAS, IMDA, AI Verify Foundation,
  MLCommons or the EU. Framework references are "mapped to" / "supports your assessment".
  The MLCommons Agent Reliability Profile is a draft: say so.
- No prices ("on request"), no internal notes, costs, team or equity details.
  Exception: founder names, roles, photos and short bios on the Who we are page, with each founder's consent (no employer names).
- Facts and numbers need a named source (like the Gartner figure on the home page).
- If the user asks for something that breaks a rule, say which rule and offer a safe wording.

## UI design
- **UI work uses the `ui-design` skill** (`.claude/skills/ui-design`, source `~/vibe-hq/library/skills/ui/ui-design`): mockup → Falk yes → build → code check → audit/polish → screenshot check. No other UI/design skill.
  (Deployed by vibe-hq `scripts/deploy-ui-design.sh`; do not edit the skill here.)
