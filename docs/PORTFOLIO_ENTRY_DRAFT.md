# Portfolio entry draft: Auto Ontology for marketing and CRM

Draft for `content/projects.ts` in `nabil-takiyuddin-portfolio`. Nothing here has been added to that repo.
Written to the site's existing schema (CS-08 is the next free code after CS-07). No client details; the pilot company is anonymous.

## 1. Case study object (paste into `caseStudies`)

```ts
  {
    slug: "auto-ontology-marketing-crm",
    code: "CS-08",
    updated: "2026-11-25",
    title: "Governed Marketing Funnel Metrics on CRM Data with NVIDIA Auto Ontology, Tested for Answer Accuracy",
    shortTitle: "Auto Ontology for marketing and CRM",
    schemaType: "CreativeWork",
    course: { code: "Independent project", name: "Marketing and CRM analytics" },
    format: "Individual",
    formatLabel: "Independent pilot",
    date: "November 2026",
    context: { label: "Setting", value: "Pilot on an anonymized CRM export, repeated on synthetic data" },
    // links: [{ label: "Source code on GitHub", href: "https://github.com/nabiledler92/auto-ontology-marketing-showcase" }],
    // ^ add once the repo is public; it is private today and the link would 404.
    metaTitle: "Auto Ontology for Marketing and CRM | Nabil Takiyuddin",
    metaDescription:
      "Tested an AI ontology layer on CRM funnel data: agreed metrics written as SQL, the same question asked 8 times per setup. Correct answers rose from 3 to 6 of 8.",
    summary:
      "A pilot that tests whether shared, governed funnel definitions let marketers ask CRM questions in plain English and get auditable answers. Correct answers rose from 3 to 6 of 8 as the metrics got narrower and the model got larger.",
    highlight: { value: "3 to 6 of 8", label: "correct funnel answers across four test batches" },
    problem: [
      "Marketing funnel numbers often live in pivot sheets, where the word \"leads\" means different things in different tabs, raw lead sources are messy, and nobody can say which version is right.",
      "The question was whether an ontology layer, a shared set of business definitions on top of the CRM data, could give consistent answers to plain-English questions and show the SQL behind each one. The pilot used a CRM export from an anonymous B2B services company that had no data warehouse yet.",
    ],
    approach: [
      {
        title: "Load the CRM data",
        text: "Copied the CRM export (persons, deals, leads, stages) into Postgres as 8 tables. Dropped email and phone columns first, because the tool sends sampled values to hosted models.",
      },
      {
        title: "Let the tool draft the ontology",
        text: "Used NVIDIA Auto Ontology to build business terms, column descriptions and table links automatically, then checked what it had actually built instead of trusting the success message.",
      },
      {
        title: "Write the funnel as SQL metrics",
        text: "Added 10 metrics for leads, qualified leads, SQLs, won deals, won revenue and channel results. Run directly, the SQL reproduced the client's own reference figures exactly.",
      },
      {
        title: "Measure accuracy, not impressions",
        text: "Asked the same funnel question 8 times per setup and scored every run by value against the known-correct answer. A first scoring script matched column names and wrongly failed two correct runs, so I rescored by value.",
      },
      {
        title: "Debug the tool",
        text: "The first compile reported success while 9 model calls had failed. Seven hosted models were tested; the five that responded all rejected the same request field. A small local patch fixed it, and the recompile had no failed calls.",
      },
      {
        title: "Rebuild the demo on synthetic data",
        text: "Wrote a seeded generator for a fake Pipedrive-style CRM with the same quirks (messy sources, deals won months after creation, two meanings of \"lead\") and recompiled it, so the work can be shown with no client data.",
      },
    ],
    results: {
      metrics: [
        { value: "6 of 8", label: "Best batch", note: "Larger model plus a narrow won-by-month metric" },
        { value: "3, 2, 4, 6", label: "Correct per batch of 8", note: "Four setups, same question" },
        { value: "10", label: "Funnel metrics as SQL" },
        { value: "9 to 0", label: "Failed model calls", note: "Before and after the patch" },
      ],
      notes: [
        "Narrow, single-purpose metrics steered the answering agent better than long descriptions or one large query. The creation-month error for won deals disappeared once one metric stated the won-date rule.",
        "A larger model removed the worst failures (no answer, and SQL made only of typed-in numbers) but not the wrong-date error.",
        "Asked for ad spend, which the data does not contain, the agent said so instead of inventing a number.",
        "Not production-ready: 8 runs per batch is a small sample, nothing is certified by a human reviewer yet, and new errors appeared as old ones were fixed. Funnel answers still need their SQL read.",
        "Building the layer exposed CRM data-quality issues worth fixing: untagged traffic landing in \"direct\", a qualification flag that barely separates leads, and won dates that look recorded late.",
      ],
    },
    tools: ["Python", "SQL", "PostgreSQL", "Docker", "NVIDIA Auto Ontology", "NVIDIA Nemotron", "Pipedrive data"],
    role: "Independent pilot: data loading, metric definitions, evaluation design and scoring, debugging the tool against a hosted API, and building the synthetic demo.",
    tags: ["BI", "Data Engineering"],
    keywords: [
      "ontology",
      "semantic layer",
      "marketing analytics",
      "CRM",
      "funnel metrics",
      "text-to-SQL",
      "LLM evaluation",
      "NVIDIA Auto Ontology",
    ],
  },
```

## 2. Short versions

**CV bullet:** Piloted NVIDIA Auto Ontology on CRM funnel data: wrote 10 governed metrics as SQL, scored the AI's answers over four 8-run test batches (3 to 6 of 8 correct), and fixed a hosted-API incompatibility with a small patch.

**LinkedIn post (about 120 words):**
Marketing funnel numbers often live in pivot sheets where "leads" means different things in different tabs. I tested whether an ontology layer could fix that: shared definitions on top of CRM data, so people can ask in plain English and see the SQL behind each answer.

What I did: loaded a CRM export into Postgres, let NVIDIA Auto Ontology draft the model, wrote the funnel rules as SQL metrics, then asked the same question 8 times per setup and scored every answer.

Result: 3, 2, 4, then 6 of 8 correct. Narrow metrics beat long descriptions, a bigger model removed the worst failures, and it is not production-ready yet. I rebuilt the demo on synthetic data so it can be shared with no client details.

## 3. Before you publish

| Check | Why |
|---|---|
| Make `auto-ontology-marketing-showcase` public, then uncomment the `links` line | The repo is private today, so the link would 404 |
| Read the repo README on GitHub first | I have not seen it rendered |
| Confirm `CS-08` is still free and `updated` is today's date | Taken from the repo as it was on 2026-11-25 |
| Decide whether "anonymous B2B services company" is enough | Do not name the client or mention an agency or employer unless you agree |
| Add screenshots if you want them on the case page | The existing entries do not show how images are attached, so I did not guess; the four demo images are in the showcase repo |
| Run `npm run typecheck` in the portfolio repo after pasting | I have not compiled this against the site |

## 4. Claims to keep out

Reliability or production readiness, anything about predictions (Kumo was not tested), real figures from the pilot, and any suggestion that a human certified the metrics.
