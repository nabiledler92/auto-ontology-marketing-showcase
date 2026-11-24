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
definitions as SQL metrics. Then I measured how often the AI gave the right answer to the same question: from 3 of 8 correct up to 6 of 8
by writing narrower metrics and using a larger model.

**Skills shown:** data modeling, SQL, metric definition, LLM evaluation (repeat-run scoring), debugging an open-source tool
against a hosted API, writing up honest limits.

## Facts that are safe to state

| Fact | Notes |
|---|---|
| 8 CRM tables loaded; 10 funnel metrics written as SQL attributes | Counts only, no client figures |
| 4 batches of 8 runs on one funnel question: 3, 2, 4 and 6 correct | The first scoring script was wrong and was corrected; scores are the corrected ones |
| Defaults failed: 9 model calls rejected by the hosted endpoint, so the first compile was thin; a ~6 line patch fixed it | Patch is in `patches/` |
| 7 hosted models tested for structured output; the 5 that responded all failed the same way | Cause was the client library and endpoint, not the models |
| The agent refused to invent ad spend when the data had none | Observed |
| Metrics matched the client's own reference sheet exactly when run directly | Say "reference figures", never quote them |

## Claims NOT to make

- That it is reliable or production-ready (best was 6 of 8 on one question, 8 runs per batch is a small sample).
- Anything about predictions or Kumo: not tested.
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
| `docs/PORTFOLIO_ENTRY_DRAFT.md` | Ready-to-paste case study object (CS-08 schema for `content/projects.ts`), short CV and LinkedIn versions, and a pre-publish checklist. Not yet added to the portfolio repo; start here when building the portfolio page |
| `docs/images/` | Four screenshots of the synthetic demo (graph, terms, metrics, chat answer with SQL) |
| `scripts/generate_synthetic_crm.py` | Synthetic Pipedrive-style CRM, seeded |
| `scripts/verify_demo.py` | Checks the funnel SQL totals add up on the synthetic data |
| `sql/` | Canonical monthly funnel and single-purpose metrics |
| `patches/` | Local patch to Auto Ontology (diff of NVIDIA code, Apache-2.0) |

## Suggested case-study outline

1. The problem: one word, many meanings, funnel numbers nobody can audit.
2. The approach: CRM export, Postgres, Auto Ontology, metrics.
3. How I measured it: same question, 8 runs, scored by value.
4. What worked and what did not (table of the four batches).
5. What this means for marketing and for CRM hygiene.
6. Limits and next steps (cohort funnel, certification, ad spend as a data source, more questions).
7. Reproduce it on synthetic data.

## Still open (Nabil to decide)

| Decision | Options |
|---|---|
| Repo visibility | Private now. Public after review. Commits use the GitHub no-reply email, not a personal email |
| Licence for my own code | MIT or Apache-2.0 (none added yet) |
| How to describe the client | Currently "an anonymous B2B services company". Do not mention the agency or employer unless Nabil agrees |
| Screenshots on the portfolio case page | The four demo screenshots exist in `docs/images/`. How images attach to a case-study page in the portfolio site was not checked, so decide that when pasting the entry |

## Status

This repo (`nabiledler92/auto-ontology-marketing-showcase`) was created as **private** for review. It is not public yet. Make it public only after Nabil has read the README and this file and agrees.
