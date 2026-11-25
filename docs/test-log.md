# Test log (anonymized)

Pilot of NVIDIA Auto Ontology on a CRM export (Pipedrive-style) from a B2B services company. The client, its people, its stages
and all its figures are left out. Only what the tool did is recorded. *Verified* means checked directly against the database or the
client's own reference figures.

## 1. Setup and build tests

| # | What I tested | Result | What I learned | Why it matters |
|---|---|---|---|---|
| S1 | Install and run the stack with Docker | Worked after two fixes: scripts had Windows line endings and failed inside Linux containers; one image build failed on a network error and passed after restarting Docker | Heavy on memory and build time | Run it on a server or spare machine, not a daily laptop |
| S2 | Load the CRM export into Postgres | 8 tables loaded; totals checked directly. Contact details (email, phone) dropped before loading | A spreadsheet export works as a stand-in warehouse, but needs a scheduled refresh for real use | Fine for a pilot; plan the data pipeline for ongoing use |
| S3 | First compile with the default model | **Thin result.** 9 model calls failed with HTTP 400. Result: 8 terms, most columns described, 1 table link, 0 metrics. It still reported "success" | A compile can report success while skipping steps | Check what was built, not the status message |
| S4 | Try 7 hosted models against the failing request type | The 5 that responded all rejected the same field, so the cause is the endpoint and the client library, not the model | Changing model would not fix it | Open-source tools can break against hosted services; budget engineering time |
| S5 | Patch the model client (about 6 lines) and recompile | **Fixed.** 0 failures; 8 terms with clearer names; 125 of 126 columns described; 5 table links; still 0 metrics | The automatic build gives a good map but writes no business rules on its own | People still have to add the definitions that matter |

## 2. Metric definition tests

| # | What I tested | Result | Verified |
|---|---|---|---|
| M1 | My SQL for leads, qualified leads, SQLs, won deals, won revenue against the client's reference sheet for two months | Exact match on every figure | Yes |
| M2 | Conversion rates in the canonical monthly query | Matched the reference sheet | Yes |
| M3 | Later months from the same query | Produced figures; no reference to compare. One month showed SQL-to-won above 1 because rates are ratios of monthly totals, not cohort rates | Computed only |

## 3. Chat answer tests

| # | Kind of question | Verdict | What I learned |
|---|---|---|---|
| C1 | Single-table total (won deals and value) | Correct | Simple questions work |
| C2 | Win rate by lead source | Right method, poor grouping | Raw lead source is unusable (blank, `google`, `google.com`, URLs); the agreed group is the one to use |
| C3 | Leads per month and how many have a deal | Probably wrong | "Lead" means two things: funnel leads (persons) and an inbox table. The agent picked the wrong one, and a join can count a person twice |
| C4 | Ad spend | Correct refusal | Said the data has no spend column instead of inventing one |
| C5 | One-month funnel question, first attempt after adding metrics | Partly wrong | Leads from the wrong table; won deals counted by creation month |
| C6 | Most SQLs by channel, and how many won | Correct | Used the agreed channel grouping once it existed as a metric |
| C7 | One-month funnel question after editing a term description and a metric wording | One run correct, the next wrong with SQL made only of typed-in numbers | Inconsistent |

## 4. Repeat test: same question, 8 runs per setup

Scored by value, not by column name (my first scoring script used column names and wrongly failed two correct runs; corrected).

| Batch | Setup | Correct | Wrong | No answer | Constants-only SQL |
|---|---|---|---|---|---|
| B1 | Default model, descriptions edited | 3 | 4 | 1 | 0 |
| B2 | Default model, canonical monthly query added | 2 | 5 | 1 | 1 |
| B3 | Nemotron Ultra for answering | 4 | 4 | 0 | 0 |
| B4 | Ultra plus a narrow won-by-won-month metric | **6** | 2 | 0 | 0 |

| Takeaway | Meaning |
|---|---|
| Narrow single-purpose metrics steered the agent better than long descriptions or one big query | Write one metric per way of computing one figure |
| A bigger model removed no-answer and constants-only failures | Fewer answers whose SQL cannot be checked |
| Fixing one error did not stop the agent making different ones | Expect to add a metric per recurring error, or keep a human check |
| 8 runs per batch is a small sample | Treat 6 of 8 as encouraging, not proven |

### 4d. Views plus a hidden table, measured on the synthetic demo (2026-11-25)

Setup: synthetic demo stack (no client data), Ultra model for answering, the same 8 metrics before and after.
Change: three database views that build the rules in (`crm.funnel_monthly`, `crm.won_deals` with a ready `won_month`,
`crm.deals_with_channel` with the agreed channel group), and the `leads` inbox table hidden with a connection table filter
(`table_deny_regex = '^leads$'`, which needs an app-managed connection, not `CONNECTION_STRINGS`). Metrics re-pointed at the views.
Each question asked once per setup; expected answers computed by SQL directly on the database; scored by value.

| Question set | Before | After | Answers that queried a view (after) |
|---|---|---|---|
| Explicit wording, rules spelled out in the question (20) | 19/20 | 19/20 | 12/20 (0 before) |
| Plain wording, how a marketer would ask (17) | 15/17 | **16/17** | 12/17 (0 before) |

| Miss | Before | After | Why |
|---|---|---|---|
| "How many SQLs in November 2025?" (plain) | Wrong: invented a stage-based SQL definition (8 instead of 18) | **Fixed** | The agent used the stated metric/view instead of guessing |
| "What is our win rate for Google Ads?" (plain) | won / (won + lost) = 0.58 | Same | Two common definitions; the expected answer used won / all deals (0.32). The question is ambiguous, not the data |
| "Deals lost during 2025, by the date lost" (explicit) | Grouped by day instead of one total | Same | Wording, not wrong data |

| Takeaway | Meaning |
|---|---|
| The synthetic demo was already accurate before the change (19/20, 15/17) | Ceiling effect: this set cannot show a big gain. The clean synthetic schema (no duplicate deal table, no ambiguous lead table) may be most of why. *Later tested on the pilot's real CRM data: the same approach lifted the 8-run funnel test from 6 to 8 of 8, and a 17-question plain-language set reached 17 of 17 after a person-level channel view was added* |
| The agent adopted the views quickly (0 to 12 answers per set) | Views are an easy, deterministic way to fix rules such as "won counts by won date" |
| Remaining misses are definition questions (win rate) | Add a stated metric for every ambiguous business word (win rate, SQL), not more plumbing |
| One run per question | Small sample; a repeat would show run-to-run variation |

Next: apply the same approach to a real CRM schema that has duplicate and ambiguous tables, add a stated win-rate metric, and re-run the 8-run funnel test there.

## 5. What I understand about Auto Ontology

| Part | What it does | My experience |
|---|---|---|
| Automatic ontology build | Reads metadata, samples values, uses a model to name terms, describe columns and find table links | Good map in minutes; no business rules |
| Metrics (SQL attributes) | Named SQL definitions attached to a term | Not created automatically here; I wrote 10 by hand |
| Chat agent | Searches the ontology, tests queries, submits a final SQL, shows SQL and rows | Fast and honest about missing data; not yet consistent |
| Certification | Human review marks a definition as approved | Not done |
| Predictions (Kumo) | Optional hosted prediction service | Not tested |
| Data leaving the machine | Sampled values, questions and embeddings go to NVIDIA's hosted models | Review before using real client data |

## 6. Marketing and CRM takeaways

| Area | Finding | Why it matters |
|---|---|---|
| One funnel definition | Agreed rules reproduce the reference figures in SQL | Removes version drift between pivot tabs |
| Channel reporting | Raw lead source is messy; an agreed source/medium group works | Always report by the agreed group |
| Untagged traffic | A large share of deals had no lead source and fell into "direct" | "Direct" is partly untagged paid or organic traffic; better tagging sharpens channel results |
| Lead quality signal | A tiny share of people were marked not qualified | The flag barely separates leads, so qualified-to-SQL is close to leads-to-SQL |
| Date quality | Won dates were concentrated in recent months | If won dates were recorded late, trend and win rates for earlier months are unreliable |
| Rates | Ratios of monthly totals can exceed 100% | A cohort view is fairer for campaigns |
| Spend, CAC, ROAS | No spend data in the export; the agent said so | Needs ad platform spend as another source |
| Predictions | Not tested | Possible later, after a data review |
