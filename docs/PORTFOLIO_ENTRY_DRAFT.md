# Portfolio entry: Auto Ontology for marketing and CRM

Short versions for CV and LinkedIn. No client details; the pilot company is anonymous.

## 1. Case study (now live)

The case study is published as **CS-08** in `nabil-takiyuddin-portfolio` (`content/projects.ts`, slug
`auto-ontology-marketing-crm`), with a long-form article at `/articles/auto-ontology-marketing-crm`.
That repo is the source of truth; the draft object that used to be here is retired so the two cannot drift apart.

As of 2026-11-25 the live pages show B1 to B4 (3 to 6 of 8). The update to B5 (3 to 8 of 8), the question sets and the
Kumo Engine note is in portfolio PR #30, awaiting merge.

## 2. Short versions

**CV bullet:** Piloted NVIDIA Auto Ontology on CRM funnel data: wrote 10 governed metrics as SQL, scored the AI's answers over five 8-run test batches, and raised correct answers from 3 to 8 of 8 by building the rules into database views; also fixed a hosted-API incompatibility with a small patch.

**LinkedIn post (about 130 words):**
Marketing funnel numbers often live in pivot sheets where "leads" means different things in different tabs. I tested whether an ontology layer could fix that: shared definitions on top of CRM data, so people can ask in plain English and see the SQL behind each answer.

What I did: loaded a CRM export into Postgres, let NVIDIA Auto Ontology draft the model, wrote the funnel rules as SQL metrics, then asked the same question 8 times per setup and scored every answer.

Result: 3, 2, 4, 6, then 8 of 8 correct. Longer descriptions and a bigger model only helped partly; the jump came from removing choices: database views that build the rules in, and hiding the tables that confused it. Small samples, so not production-ready. The demo runs on synthetic data, with no client details.

## 3. Before you publish anything new

| Check | Why |
|---|---|
| Apply the never-include checklist in `PORTFOLIO_HANDOFF.md` | This repo and the portfolio are public |
| Use only the facts listed as safe in `PORTFOLIO_HANDOFF.md` and `ARTICLE_HANDOFF.md` | Keeps every page consistent |
| Do not mention the agency or employer unless Nabil agrees | Client relationship |

## 4. Claims to keep out

Reliability, production readiness or "always right"; any real figure from the pilot; any suggestion that a human certified
the metrics; and any claim that Kumo Engine is bad in general (it was tested on synthetic data only).
