---
name: probanda-copy
description: Writing rules for probanda.ai — voice, enterprise B2B wording, words to avoid, how to state claims, numbers and frameworks safely. Use whenever writing or rewriting any text on the site (headlines, intros, buttons, mockup labels, use cases), for "rewrite", "shorter", "less technical", "more enterprise", "make it sound better".
---

# probanda.ai copy

## Voice
Calm, precise, senior: a trusted risk adviser writing to a CFO. Confident without selling.
- Short sentences (≤ 20 words). One idea per sentence. Active voice, present tense.
- Concrete over abstract: "The CFO approves any purchase order above EUR 250,000" beats "configurable approval workflows".
- Reader first: "your auditor", "your systems", "your rules".
- British/Singapore spelling consistently (organisation, programme, authorise).

## Vocabulary
| Use | Avoid |
|---|---|
| check before it runs, stop, send to a person | intercept, middleware, gate (in headlines) |
| decision record, evidence pack, signed record | log line, payload, hash chain, ledger entry |
| rules, limits, delegation of authority, segregation of duties | policies-as-code, guardrails config |
| test on past cases, quality check | eval, back-test, regression suite, red team (except in services detail) |
| agent for accounts payable / procurement / close | bot, copilot, autonomous system |
| mapped to, supports your assessment | compliant, certified, guaranteed, approved by |
Never: revolutionary, seamless, cutting-edge, game-changing, unlock, empower, leverage, AI-powered.

## Claims
- Regulations and frameworks: name them exactly (EU AI Act Art. 12 record-keeping, Art. 14 human oversight;
  ISO/IEC 42001; IMDA Model AI Governance Framework for Agentic AI; MLCommons Agent Reliability Profile, **draft**).
  Say what Probanda provides evidence for, never that the customer becomes compliant. MAS "expects", not "requires",
  unless quoting a requirement.
- Numbers: real numbers need a named source and date (e.g. "Gartner forecast, Aug 2025"). Example numbers
  live only inside mockups labelled `ILLUSTRATIVE · fictional data`.
- No customer, partner or employer names, no logos we have no permission for, no prices ("on request").
- No promises of speed or results ("in days", "100% safe").

## Patterns
- Headline: outcome or tension in ≤ 8 words ("Agents are arriving faster than proof that they work.").
- Lead: who it's for + what changes, ≤ 2 sentences.
- Card: bold label of 2-4 words + one sentence.
- Button: verb + outcome (see `probanda-ux`).

## Rewrite procedure
1. Show the current text and the proposed text side by side (a short list), then apply.
2. Read the page's headlines alone afterwards: the story must still hold.
3. Grep the changed pages for the avoid-list words and for "compliant|certified|guarantee".
