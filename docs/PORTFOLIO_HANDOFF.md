# Portfolio handoff: Auto Ontology for marketing and CRM

For any Claude session (including one on a different account) that is building a portfolio page or repo entry from this work.
Read this first. It is safe to publish: it contains no client details.

## What this project is

A pilot that tested whether an ontology layer (shared, governed business definitions on top of CRM data) lets marketers ask
funnel questions in plain English and get answers that match the agreed definitions, with the SQL shown.
Tool: NVIDIA Auto Ontology (open source, Apache-2.0). Data in this repo is synthetic; the pilot used a real CRM export from an
anonymous B2B services company.

## Copy you can use

**One line:** I tested an AI ontology layer on CRM data to see if marketing funnel questions could get consistent, auditable answers.

**Three sentences:** Marketing funnel numbers often live in pivot sheets where "leads" means different things in different tabs.
I loaded a CRM export into Postgres, let NVIDIA Auto Ontology build a business-term map of it, and added the agreed funnel
definitions as SQL metrics. Then I measured how often the AI gave the right answer to the same question: from 3 of 8 correct to 8 of 8,
and the big jump came from building the rules into database views and hiding the tables that confused it, not from a bigger model.

**Skills shown:** data modeling, SQL, metric definition, LLM evaluation (repeat-run scoring), debugging an open-source tool
against a hosted API, writing up honest limits.

## Facts that are safe to state

| Fact | Notes |
|---|---|
| 8 CRM tables loaded; 10 funnel metrics written as SQL attributes | Counts only, no client figures |
| 5 batches of 8 runs on one funnel question: 3, 2, 4, 6 and 8 correct (B1 to B5) | B5 = rules built into database views plus 2 confusing tables hidden. The first scoring script was wrong and was corrected; scores are the corrected ones |
| Median answer time 59.5 s (B4) to 21 s (B5) | Standard median of 8 runs |
| Real pilot data, 17 plain-language questions: 15/17 with views and a win-rate metric, 17/17 after a person-level channel view | One run per question |
| Synthetic demo: explicit set 19/20 before and after views; plain-language set 15/17 to 16/17 | One run per question |
| Answering models: Nemotron 3.5 Lightning (tool default) for B1 and B2, Nemotron Ultra from B3 | Hosted by NVIDIA; database, ontology and agent ran locally in Docker |
| Defaults failed: 9 model calls rejected by the hosted endpoint, so the first compile was thin (104 of 130 columns described, 1 table link); a ~6 line patch fixed it; after the rebuild 156 of 156 columns described | Patch is in `patches/` |
| 7 hosted models tested for structured output; the 5 that responded all failed the same way | Cause was the client library and endpoint, not the models |
| The agent refused to invent ad spend when the data had none | Once returned empty cost columns instead of a clean refusal |
| Metrics matched the client's own reference sheet exactly when run directly | Say "reference figures", never quote them |
| Kumo Engine (synthetic data, local CPU): lead-scoring AUROC 0.52 to 0.58 across runs vs 0.589 for a per-channel rate, ceiling 0.606 | Synthetic data whose only signal is the channel; not a verdict on Kumo Engine |

## Claims NOT to make

- That it is reliable, production-ready or "always right" (8 of 8 is on one question; 8 runs per batch and one run per question in the larger sets are small samples).
- That Kumo Engine is bad in general, or any Kumo result on real data: it was tested on synthetic data only.
- Any real figure, count, date range, channel result or company detail from the pilot.
- That the certification (human review) step was done: it was not.

## Never include (checklist before publishing anything new)

- The client's name, domain, people, deal titles, IDs, stage names, or country mix.
- Links to the client's spreadsheet, the raw export, or screenshots of the real data.
- Any `.env`, API keys, passwords, or connection strings.
- The internal test log and the real loader scripts (they use the client's column names): these stay out of the public repo.
- Screenshots of the real ontology graph or chat answers. Make new ones from the synthetic database only.

## Repo contents

| Path | What it is |
|---|---|
| `README.md` | Public write-up with results, marketing and CRM value, limits |
| `docs/test-log.md` | Anonymized test tables |
| `docs/PORTFOLIO_ENTRY_DRAFT.md` | Short CV and LinkedIn versions. The case study itself is live as CS-08 in the portfolio repo (`content/projects.ts`), which is now the source of truth |
| `docs/ARTICLE_HANDOFF.md`, `docs/article-data/` | Findings, safe facts and chart data for the long-form article |
| `docs/images/` | Four screenshots of the synthetic demo (graph, terms, metrics, chat answer with SQL) |
| `scripts/generate_synthetic_crm.py` | Synthetic Pipedrive-style CRM, seeded |
| `scripts/verify_demo.py` | Checks the funnel SQL totals add up on the synthetic data |
| `sql/` | Canonical monthly funnel and single-purpose metrics |
| `patches/` | Local patch to Auto Ontology (diff of NVIDIA code, Apache-2.0) |

## Suggested case-study outline

1. The problem: one word, many meanings, funnel numbers nobody can audit.
2. The approach: CRM export, Postgres, Auto Ontology, metrics.
3. How I measured it: same question, 8 runs, scored by value.
4. What worked and what did not (table of the five batches; views plus hidden tables gave 8 of 8).
5. What this means for marketing and for CRM hygiene.
6. Limits and next steps (cohort funnel, certification, ad spend as a data source, more questions).
7. Reproduce it on synthetic data.

## Still open (Nabil to decide)

| Decision | Options |
|---|---|
| Repo visibility | Public. Commits use the GitHub no-reply email, not a personal email |
| Licence for my own code | Decided: MIT (see `LICENSE`). The patch in `patches/` stays under NVIDIA's Apache-2.0 licence |
| How to describe the client | Currently "an anonymous B2B services company". Do not mention the agency or employer unless Nabil agrees |
| Screenshots on the portfolio | Decided: the four demo screenshots are on the article page, not the case page |

## Status

This repo (`nabiledler92/auto-ontology-marketing-showcase`) is **public** as of 2026-11-25, at Nabil's request. Anything added to it from now on is visible to everyone, so apply the never-include checklist above to every change.

On the portfolio (nabil-takiyuddin.dev) as of 2026-11-25:

| Page | State |
|---|---|
| Case study CS-08, `/projects/auto-ontology-marketing-crm` | Live with B1 to B4. Update to B5 (3 to 8 of 8), question sets and the Kumo note is in portfolio PR #30, awaiting merge |
| Article, `/articles/auto-ontology-marketing-crm` | Live with B1 to B4. Rewrite to the `ARTICLE_HANDOFF.md` outline (charts 1 to 5, architecture diagram, model names) is in the same PR |
