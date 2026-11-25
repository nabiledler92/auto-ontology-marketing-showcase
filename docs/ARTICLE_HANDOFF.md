# Article handoff: findings and graphs

For a Claude session on Nabil's personal account that will write an article (with graphs) about this project.
Everything in this file and in `docs/article-data/` is safe to publish: tool results only, no client data.
Read `docs/PORTFOLIO_HANDOFF.md` too; its never-include checklist applies to the article.

**Status (2026-11-25):** written. The article at `/articles/auto-ontology-marketing-crm` on the portfolio was rewritten to this
outline, with charts 1 to 5, an architecture diagram and the answering models named (Nemotron 3.5 Lightning for B1 and B2,
Nemotron Ultra from B3). It is in portfolio PR #30, awaiting merge. Chart 4 uses only the lead-scoring rows of
`kumo_auroc_synthetic.csv`; nothing from `kumo-pilot/` was used.

## The story in one paragraph

Marketing funnel numbers usually live in pivot sheets where "leads" means different things in different tabs. I tested whether
an AI ontology layer (NVIDIA Auto Ontology) could answer funnel questions in plain English, correctly and every time, on a real
CRM export from an anonymous B2B services company. Defaults failed, longer descriptions and a bigger model only helped partly,
and the big jump came from **removing choices from the AI**: building the business rules into database views and hiding the
tables that confused it. The same funnel question went from 3 of 8 correct to 8 of 8, and a 17-question plain-language set
reached 17 of 17. A side test of Kumo Engine for lead scoring showed a simple per-channel rate was already as good as the model
on that data.

## Suggested outline

1. **The problem.** One word, many meanings; funnel numbers nobody can audit.
2. **The setup.** CRM export into Postgres, NVIDIA Auto Ontology builds the business map, agreed funnel rules written as SQL metrics.
3. **How I measured.** Same question asked 8 times per setup; every answer scored by value against a known-correct result.
4. **What did not work.** Default setup (thin build, 9 failed model calls); descriptions alone; one big canonical query the AI ignored.
5. **What worked.** Narrow single-purpose metrics; then views that build the rules in, plus hiding two confusing tables.
6. **The results.** Charts 1 to 3.
7. **The side quest: predictions with Kumo Engine.** Chart 4. A strong simple baseline is hard to beat on small data.
8. **Lessons for marketing and CRM teams.** See below.
9. **Limits.** See below.

## Graphs (data in `docs/article-data/`)

| # | File | Chart | Title idea | The point it makes |
|---|---|---|---|---|
| 1 | `funnel_question_batches.csv` | Bar or step line of `correct` (out of 8) for B1 to B5, each bar labelled with its `setup` | "Same question, 8 tries each: from 3 to 8 correct" | Accuracy came from removing choices, not from a bigger model alone |
| 2 | `question_sets.csv` | Grouped bars, before vs after, per dataset and wording | "Plain-language questions: 15 to 17 of 17 on the real data" | The fix carried over beyond one question |
| 3 | `compile_quality.csv` | Two small bars: failed model calls (9 to 0) and share of columns described (80% to 100%) | "Check what was built, not the success message" | The first build reported success while skipping steps |
| 4 | `kumo_auroc_synthetic.csv` | Dot plot with confidence intervals, one row per model, a vertical line at 0.5 (random) | "The simple channel rate already wins" | On small data, a per-channel rate is a tough baseline |
| 5 (optional) | `funnel_question_batches.csv`, `median_seconds` | Two bars, B4 vs B5 | "Faster too: 59.5 s to 21 s" | Views made answers faster as well as correct |

Chart notes: say "8 runs per batch" and "one run per question" on the charts or captions, because the samples are small.
Medians use the standard median; an earlier write-up quoted 61 s for B4 and 56 s for B3 (upper middle value).

## Facts that are safe to state

| Fact | Source file |
|---|---|
| Same funnel question, 8 runs per setup: 3, 2, 4, 6, 8 correct (B1 to B5) | `funnel_question_batches.csv` |
| Median answer time 59.5 s (B4) to 21 s (B5) | same |
| Synthetic demo: explicit set 19/20 before and after views; plain-language set 15/17 to 16/17 | `question_sets.csv` |
| Real pilot data, 17 plain-language questions: 15/17 with views and a win-rate metric, 17/17 after a person-level channel view | same |
| First build: 9 failed model calls, 104 of 130 columns described, 1 table link; after a 6-line patch 0 failures; after the rebuild 156 of 156 columns described | `compile_quality.csv` |
| 7 hosted models tested for the failing request; the 5 that responded failed the same way | `test-log.md` |
| The AI refused to invent ad spend when the data had none (once returned empty cost columns instead of a clean refusal) | `test-log.md` |
| Kumo Engine (synthetic data, local CPU): lead scoring AUROC 0.52 to 0.58 across runs vs 0.589 for the per-channel rate, ceiling 0.606 | `kumo_auroc_synthetic.csv` |

## Lessons to draw (marketing and CRM)

| Lesson | Evidence |
|---|---|
| Remove choices instead of adding words | Descriptions and a bigger model gave 4 to 6 of 8; views plus hidden tables gave 8 of 8 |
| Every ambiguous business word needs one stated definition | "SQL" and "win rate" were guessed differently until a metric stated them |
| Raw columns compete with agreed groupings | Referral leads were wrong from the raw source column until a view carried the agreed channel group |
| Check what the tool actually built | The first build said "success" with 9 failed steps |
| Measure with repeats and score by value | Single answers looked fine; repeats showed a coin flip before the fix |
| A simple baseline first, then a model | The per-channel rate matched Kumo Engine on this data |

## Claims to keep out

- That it is production-ready or "always right". Samples are small (8 runs per batch, one run per question in the larger sets).
- Any real figure from the pilot: counts, revenue, dates, channel results, table or column names, stage names, the client's name or industry.
- That a human certified the metrics (not done).
- That Kumo Engine is bad in general. It was tested on synthetic data whose only signal is the channel, so there was nothing extra to learn.
- Naming an agency or employer, unless Nabil agrees.

## Where things are

| What | Where |
|---|---|
| Public repo (code, synthetic data, SQL, test log, screenshots) | https://github.com/nabiledler92/auto-ontology-marketing-showcase |
| Chart data | `docs/article-data/*.csv` in that repo |
| Screenshots for the article | `docs/images/` in that repo (synthetic demo only) |
| Kumo Engine findings (synthetic only, not in the public repo) | On Nabil's laptop: `BusinessOntology-Client/kumo-pilot/FINDINGS.md`, mockup hand-off in `kumo-pilot/mockup/README.md`. Ask Nabil before publishing any of it |
| Internal files with client details | Never use: `docs/auto-ontology-test-log.md`, `loader/`, `data/`, `backups/` in the local project folder |
