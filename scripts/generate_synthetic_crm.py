# /// script
# requires-python = ">=3.11"
# dependencies = ["psycopg[binary]"]
# ///
"""Generate a synthetic Pipedrive-style CRM (no real people, companies or figures) and load it into Postgres.

Usage:
  uv run scripts/generate_synthetic_crm.py --csv-dir data/synthetic            # CSV only
  uv run scripts/generate_synthetic_crm.py --csv-dir data/synthetic --load     # CSV + Postgres (env PG* vars)

The data is random (seeded, so reproducible) but deliberately includes the quirks that made the real pilot hard:
  * messy raw lead sources (blank, 'google', 'google.com', page URLs) next to a clean source/medium group
  * deals that are won in a LATER month than they were created (the creation-month vs won-month trap)
  * two different meanings of "lead": persons (funnel leads) and an inbox table (crm.leads)
  * almost everyone marked Qualified (a weak quality signal)
  * no advertising spend anywhere (so cost questions must be refused)
"""
import argparse
import csv
import datetime as dt
import os
import random
import uuid
from pathlib import Path

SEED = 42
START = dt.datetime(2024, 1, 1, tzinfo=dt.timezone.utc)
MONTHS = 24
END = dt.datetime(2025, 12, 31, 23, 59, tzinfo=dt.timezone.utc)

# (raw source, raw medium, agreed group, share of leads, deal conversion, win share of deals)
CHANNELS = [
    (None, None, "direct / none", 0.20, 0.07, 0.30),
    ("(direct)", "none", "direct / none", 0.10, 0.08, 0.30),
    ("https://example-site.test/contact/", "", "direct / none", 0.08, 0.10, 0.32),
    ("google", "cpc", "google / cpc", 0.22, 0.12, 0.34),
    ("google", "organic", "organic / google", 0.12, 0.10, 0.28),
    ("google.com", "", "organic / google", 0.05, 0.09, 0.27),
    ("bing", "organic", "organic / bing", 0.03, 0.08, 0.25),
    ("chatgpt.com", "referral", "ai / assistant", 0.03, 0.12, 0.20),
    ("newsletter", "email", "email", 0.05, 0.06, 0.25),
    ("partner-referral", "referral", "referral", 0.12, 0.18, 0.45),
]
STAGES = ["New", "Contacted", "Proposal Sent", "Negotiation", "Verbal Yes", "Contract Signed", "Invoiced"]
COUNTRIES = ["USA"] * 9 + ["Canada"] * 4 + ["UK"] * 3 + ["Other"] * 2 + [""] * 2
ARCHIVE_REASONS = ["Trash / Spam", "Timeline too short", "Low Budget", "Test", "Out of scope"]


def month_start(i: int) -> dt.datetime:
    y, m = divmod(START.month - 1 + i, 12)
    return dt.datetime(START.year + y, m + 1, 1, tzinfo=dt.timezone.utc)


def build():
    rng = random.Random(SEED)
    weights = [c[3] for c in CHANNELS]
    persons, deals, leads = [], [], []
    pid = did = 0
    for mi in range(MONTHS):
        lo, hi = month_start(mi), month_start(mi + 1)
        n = int(rng.randint(110, 170) * (1 + 0.025 * mi))  # gentle growth
        for _ in range(n):
            pid += 1
            ch = rng.choices(CHANNELS, weights)[0]
            added = lo + (hi - lo) * rng.random()
            qualified = rng.random() > 0.012
            persons.append(dict(
                id=pid, name=f"Person {pid:05d}", org_id=pid // 3 + 1, add_time=added.isoformat(),
                lead_source=ch[0] or "", lead_medium=ch[1] or "", source_medium_group=ch[2],
                country=rng.choice(COUNTRIES), qualification="Qualified" if qualified else "Not Qualified"))
            if rng.random() < 0.7:  # inbox record, a different thing from a funnel lead
                leads.append(dict(
                    id=str(uuid.UUID(int=rng.getrandbits(128), version=4)), title=f"Inbox item {len(leads)+1:05d}",
                    person_id=pid, add_time=added.isoformat(),
                    archive_reason="" if qualified else rng.choice(ARCHIVE_REASONS), is_archived=not qualified))
            if qualified and rng.random() < ch[4]:
                for _ in range(1 + (rng.random() < 0.12)):
                    did += 1
                    created = min(added + dt.timedelta(days=rng.randint(0, 60), hours=rng.randint(0, 23)), END)
                    value = round(rng.lognormvariate(8.9, 0.7), 2)
                    status, won_time, lost_time = "open", None, None
                    r = rng.random()
                    if r < ch[5]:
                        won_time = created + dt.timedelta(days=rng.randint(10, 120))  # often a later month
                        if won_time <= END:
                            status = "won"
                        else:
                            won_time = None
                    elif r < ch[5] + 0.35:
                        lost_time = created + dt.timedelta(days=rng.randint(5, 150))
                        if lost_time <= END:
                            status = "lost"
                        else:
                            lost_time = None
                    stage = 7 if status == "won" else rng.randint(1, 6)
                    deals.append(dict(
                        id=did, title=f"Project {did:05d}", value_usd=value, status=status, person_id=pid,
                        org_id=pid // 3 + 1, stage_id=stage, add_time=created.isoformat(),
                        won_time=won_time.isoformat() if won_time else "",
                        lost_time=lost_time.isoformat() if lost_time else ""))
    stages = [dict(id=i + 1, name=n, pipeline_name="Sales Pipeline") for i, n in enumerate(STAGES)]
    return dict(persons=persons, deals=deals, leads=leads, stages=stages)


def write_csv(tables: dict, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for name, rows in tables.items():
        with open(out / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"{name}.csv: {len(rows)} rows")


DDL = """
drop schema if exists crm cascade; create schema crm;
create table crm.stages (id int primary key, name text, pipeline_name text);
create table crm.persons (id int primary key, name text, org_id int, add_time timestamptz, lead_source text, lead_medium text,
  source_medium_group text, country text, qualification text);
create table crm.deals (id int primary key, title text, value_usd numeric(12,2), status text, person_id int references crm.persons(id),
  org_id int, stage_id int references crm.stages(id), add_time timestamptz, won_time timestamptz, lost_time timestamptz);
create table crm.leads (id uuid primary key, title text, person_id int references crm.persons(id), add_time timestamptz,
  archive_reason text, is_archived boolean);
"""


def load(tables: dict) -> None:
    import psycopg
    cfg = dict(host=os.getenv("PGHOST", "localhost"), port=int(os.getenv("PGPORT", 5432)), user=os.getenv("PGUSER", "postgres"),
               password=os.environ["PGPASSWORD"])
    db = os.getenv("PGDATABASE", "showcase_demo")
    with psycopg.connect(dbname="postgres", autocommit=True, **cfg) as c:
        if not c.execute("select 1 from pg_database where datname=%s", (db,)).fetchone():
            c.execute(f'create database "{db}"')
    with psycopg.connect(dbname=db, **cfg) as c:
        c.execute(DDL)
        for name in ("stages", "persons", "deals", "leads"):
            rows = tables[name]
            cols = list(rows[0].keys())
            with c.cursor().copy(f"copy crm.{name} ({','.join(cols)}) from stdin") as cp:
                for r in rows:
                    cp.write_row([None if v == "" and k in ("won_time", "lost_time", "archive_reason") else v for k, v in r.items()])
            print(f"loaded crm.{name}: {len(rows)} rows into {db}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv-dir", default="data/synthetic")
    ap.add_argument("--load", action="store_true")
    a = ap.parse_args()
    t = build()
    write_csv(t, Path(a.csv_dir))
    if a.load:
        load(t)
