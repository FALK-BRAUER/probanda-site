# Product Marketing Context — Probanda (probanda.ai)

**Document version:** v1 · **Last updated:** 2026-11-18
Read by the `ui-design` skill (as PRODUCT.md) and the marketing skills (via `.agents/product-marketing.md`).

## Product Overview
**One-liner:** Reliable, provable AI agents for business-critical work.
**What it does:** Probanda checks every action an AI agent wants to take in enterprise systems (SAP, Workday,
ServiceNow, Salesforce) before it runs: is it correct, is it risky, is it within the company's rules, is the output
good enough. Risky actions go to a named person; rule breaches are blocked. Every decision is written to a signed
record an auditor can check independently, mapped to the frameworks the company reports on.
**Product category:** AI agent governance and assurance (control layer + evidence for AI agents).
**Product type:** Software that runs in the customer's environment, plus services (workshop, gap check, pilot, evidence support, managed reliability) delivered with partners.
**Business model:** Enterprise sales; packages "on request" (no public prices).

## Target Audience
**Target companies:** Large and regulated enterprises, Singapore and APAC first, also EU (finance, insurance, shared services, supply chain).
**Decision-makers:** CFO / COO (sponsor), chief risk officer and compliance, head of internal audit, CIO / platform owner, business process owners.
**Primary use case:** Letting AI agents act in finance and operations processes (payments, procurement, financial close, HR, IT access, refunds) with control and proof.
**Jobs to be done:**
- Let agents do real work without losing control of money, data and access.
- Show the board, auditors and regulators that agents act within mandate.
- Widen what an agent may do step by step, based on evidence.

## Personas
| Persona | Cares about | Challenge | Value we promise |
|---|---|---|---|
| CFO / COO | Productivity without new risk | Agents are coming faster than controls | Agents act only within limits; every exception reaches a person |
| Chief risk officer / compliance | Frameworks, accountability | No evidence format for agent actions | Control-by-control status mapped to EU AI Act, ISO/IEC 42001, IMDA |
| Head of internal audit | Independent verification | Logs are owned by the system being audited | Signed records checked offline, without access to the vendor |
| CIO / platform owner | Integration effort, security | Many agents, many systems | One checkpoint in front of SAP, Workday, ServiceNow, Salesforce, in your environment |
| Partner (SI, consultancy) | Delivery revenue | Clients ask for agent governance | A method and product they deliver around |

## Problems & Pain Points
**Core problem:** AI agents now write into core systems, but nobody can prove what they did, why, and who allowed it.
**Why alternatives fall short:**
- Monitoring and observability show what happened after it happened; they don't stop it.
- Governance platforms document policies; they don't sit in the path of each action.
- The agent's own logs are not independent evidence.
**What it costs them:** Stalled agent programmes, audit findings, payment and data errors, regulatory exposure.
**Emotional tension:** "We are told to use AI agents, but we will be accountable when one goes wrong."

## Competitive Landscape
**Direct:** AI governance / agent security platforms — strong on inventories and policies, weak on per-action evidence an auditor can verify.
**Secondary:** GRC tools — track controls, don't enforce them at runtime.
**Indirect:** Build it in-house with workflow approvals and logs — slow, not independent, breaks with each new agent.

## Differentiation
**Key differentiators:**
- Checks each action before it runs (not after).
- Independent, signed record; the auditor verifies it offline.
- Mapped to frameworks control by control, without claiming compliance.
- Autonomy widened step by step on evidence (progressive autonomy).
**Why customers choose us:** They can say yes to agents and still answer the auditor.

## Objections
| Objection | Response |
|---|---|
| Where does our data go? | Nowhere. Probanda runs in your environment; your keys, your records. |
| Will this slow agents down? | Routine actions pass automatically; only risky or rule-breaking ones stop. |
| We have no partner / integrator | We work inside your integrator's programme or introduce one. |
| Do you make us compliant? | No one can. We provide evidence that supports your own assessment. |
**Anti-persona:** Teams experimenting with chatbots that never act in a system of record.

## Customer Language
**Words to use:** check before it runs · stop · send to a person · decision record · evidence pack · signed record ·
rules · limits · delegation of authority · segregation of duties · tested on past cases · quality check ·
mapped to · supports your assessment · within mandate.
**Words to avoid:** payload, SDK, eval, back-test, red team (outside service detail), hash chain, middleware,
guardrails config, bot, copilot; revolutionary, seamless, cutting-edge, game-changing, unlock, empower, leverage,
AI-powered; **compliant, certified, guaranteed, approved by**.
**Glossary:**
| Term | Meaning |
|---|---|
| Evidence pack | Export of signed decision records for an auditor, checked offline |
| Autonomy level | How far an agent may act alone (suggests · each step approved · within limits · alone) |
| Gap | A system change made outside Probanda, shown instead of hidden |

## Brand Voice
**Tone:** Calm, precise, senior — a trusted risk adviser writing to a CFO. **Style:** Short sentences (≤ 20 words),
active voice, concrete examples, reader first ("your auditor"). British/Singapore spelling.
**Personality:** credible, exact, unhurried, independent.

## Proof Points
**Metrics:** "40% of enterprise apps will have task-specific AI agents by end of 2026" (Gartner forecast, Aug 2025).
**Customers / testimonials:** none published yet. Never invent any.
**Frameworks referenced:** EU AI Act (Art. 12 record-keeping, Art. 14 human oversight), ISO/IEC 42001, IMDA Model AI
Governance Framework for Agentic AI, AI Verify, MLCommons Agent Reliability Profile (**draft**), Agent Reliability Engineering.

## Goals
**Business goal:** Pilots with regulated enterprises that lead to production use.
**Conversion actions:** Talk to us · Request a sample evidence pack · Book a readiness workshop · Become a partner (all → /contact/).

## Site rules (public)
- Mockups carry `ILLUSTRATIVE · fictional data`; every number in a mockup adds up.
- No customer, partner or employer names; no logos without permission; no prices; no internal notes, costs, team or equity.
- Regulators and standards bodies: no claim of endorsement; MAS "expects", not "requires", unless quoting.
- Real numbers need a named source and date. No promises of speed or results.
