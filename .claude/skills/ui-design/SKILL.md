---
name: ui-design
description: "Design, build, review or polish a frontend screen in this repo: new page or component, redesign, layout, typography, colour, motion, UX copy, accessibility, responsive behaviour, dashboards, forms, empty states. Walks mockup first → Falk's yes → build → code check → audit/polish → screenshot check. Use for any UI change that a person will look at, and for 'make this look better', 'audit the UI', 'polish', 'critique', 'is this accessible'. Not for backend-only work."
argument-hint: "[shape · build · critique · audit · polish · layout · typeset · colorize · clarify · harden · adapt · animate · quieter · bolder · distill · onboard · optimize] [target]"
---

# ui-design

The one UI skill. It lives only in repos that build UI (source of truth:
`~/vibe-hq/library/skills/ui/ui-design/`, copied into each repo's `.claude/skills/`).
Design knowledge comes from two vendored, pinned sources, read on demand:

- `reference/impeccable/` — Impeccable v4.7.0 (Paul Bakaus, Apache-2.0): design method, modes,
  craft floor, one playbook per command.
- `reference/vercel/web-interface-guidelines.md` — Vercel web interface guidelines (MIT): MUST/SHOULD/NEVER
  rules for keyboard, forms, focus, targets, motion, performance.

Read only the files the current step names. Never load the whole folder.

## Impeccable without its engine

The references were written for Impeccable's launcher (`scripts/impeccable`), which downloads and runs
a binary. **It is not shipped here and must not be installed.** Wherever a reference says to run
`".../scripts/impeccable" <verb>` (context, detect, comp-spec, live-*, build-phase, critique-storage,
component-review, surface-brief, hooks, pin):

- `context` → read `PRODUCT.md` and `DESIGN.md` at the repo root (or the UI folder) yourself; don't invent
  missing context.
- `detect` → the checks in step 4 and 6 below replace it.
- anything else → skip that step and follow the reference's manual or degraded path
  (`reference/impeccable/degraded/`). Don't mention the missing launcher to Falk each time.

Its live-browser mode, variant generator, hooks and doctor are removed.

## Workflow

Run the steps in order. Small refinements (one component, a spacing fix) start at step 3; anything
new or a redesign starts at step 1.

### 1. Mockup first

1. Read `reference/impeccable/SKILL-impeccable.md` (modes, principles) and, for a new surface,
   `reference/impeccable/new-work.md`; for task discovery `shape.md`.
2. Pick the mode: **Operate** for app UI, dashboards, cockpits, admin (most of these repos);
   Persuade/Read/Experience only when the surface is one.
3. Make a mockup Falk can look at: an Artifact (`Artifact` tool, `action: "quickstart"`,
   `intent: "design"`) with the real data shape and the states that matter (loaded, empty, error,
   loading). No placeholder lorem when real labels are known.
4. If the project has a `DESIGN.md`, the mockup follows it. If none exists and the choice is durable,
   propose one (`reference/impeccable/document.md` / `init.md`).

### 2. Falk's yes

Show the mockup link and ask one yes/no: "Build this? yes/no". Changes → new mockup round. No code before yes.
Skip only for refinements that keep the existing look.

### 3. Build

1. Read `reference/impeccable/craft-floor.md` immediately before the first UI edit (quality floor,
   absolute bans). Read the playbook for the sub-command in play (`layout.md`, `typeset.md`, …).
2. shadcn/ui repos: read `components.json` and the installed components before adding any; use the
   repo's own `shadcn` CLI if it is in its dependencies (`npx shadcn info --json`), add components through it,
   never hand-copy registry code. Reuse existing tokens; no new colours or fonts outside `DESIGN.md`.
3. Follow the repo's own stack and gate (its CLAUDE.md). Build through the `coder` skill when the repo uses it.

### 4. Code check

Go through the diff against `reference/vercel/web-interface-guidelines.md`. Report findings as
`file:line — rule — fix`, fix every MUST/NEVER, list SHOULDs you skip with the reason.

### 5. Audit and polish

Run `reference/impeccable/audit.md` (a11y, performance, responsive, theming) on the changed surface,
then `polish.md`. Use `critique.md` instead of audit when Falk asks for a design review. Fix in one batch.

### 6. Screenshot check

1. Start the app with the repo's dev command (its CLAUDE.md/README); log in only with test accounts
   from the repo's seed or example config.
2. Chrome DevTools MCP: `new_page` → `resize_page` 375, 768, 1440 wide → `take_screenshot` each, in light and dark
   when the app has both. Check the screenshots against the mockup and craft-floor; fix, then look again
   once (batch the fixes, don't screenshot after every tweak).
3. `lighthouse_audit` (accessibility, best practices) on the changed route: accessibility below 95 is a finding to fix
   or to report with the reason.
4. Report: what changed · screenshots (SendUserFile) · Lighthouse scores · open findings.

## Rules

- One lead: this skill. Don't pull in other UI/design skills or plugins — they give conflicting direction.
- The brief wins: what Falk pins (look, font, palette, density) beats the references' taste.
- Refinement keeps the existing identity; redesign replaces it fully — never polish a look you were asked to replace.
- No new runtime dependency, font service or icon set without saying its size and getting a yes.
- Never send app data, screenshots or URLs to an outside service; screenshots go to Falk only.

## Updating the vendored sources

Pinned: Impeccable `skill-v4.7.0` (commit aeeb3d8), Vercel web-interface-guidelines `434b7f9` (2026-10-05).
To update: clone the new tag into the scratchpad, read the diff of `plugin/skills/impeccable/reference/`,
copy it over (keep `live*.md`, `generate.md`, `hooks.md`, `doctor.md` out), update this section, then run
`~/vibe-hq/scripts/deploy-ui-design.sh` to refresh the UI repos.
