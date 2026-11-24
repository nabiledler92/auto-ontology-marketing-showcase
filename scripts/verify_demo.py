# /// script
# requires-python = ">=3.11"
# dependencies = ["psycopg[binary]"]
# ///
"""Run the funnel SQL on the synthetic demo database and check it is internally consistent.
Env: PGPASSWORD (required), PGHOST, PGPORT, PGUSER, PGDATABASE (default showcase_demo).
"""
import os
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parent.parent
cfg = dict(host=os.getenv("PGHOST", "localhost"), port=int(os.getenv("PGPORT", 5432)), user=os.getenv("PGUSER", "postgres"),
           password=os.environ["PGPASSWORD"], dbname=os.getenv("PGDATABASE", "showcase_demo"))

with psycopg.connect(**cfg) as c:
    funnel = c.execute((ROOT / "sql" / "monthly_funnel.sql").read_text()).fetchall()
    n_persons = c.execute("select count(*) from crm.persons").fetchone()[0]
    n_qual = c.execute("select count(*) from crm.persons where qualification='Qualified'").fetchone()[0]
    n_deals = c.execute("select count(*) from crm.deals").fetchone()[0]
    n_won = c.execute("select count(*) from crm.deals where status='won'").fetchone()[0]
    # The trap: the same 'won' deals counted by creation month instead of won month
    wrong = c.execute("""select count(*) from crm.deals where status='won'
                          and date_trunc('month', add_time) <> date_trunc('month', won_time)""").fetchone()[0]
    inbox = c.execute("select count(*) from crm.leads").fetchone()[0]

checks = {
    "sum of monthly leads equals persons": sum(r[1] for r in funnel) == n_persons,
    "sum of monthly qualified equals qualified persons": sum(r[2] for r in funnel) == n_qual,
    "sum of monthly SQL deals equals deals": sum(r[3] for r in funnel) == n_deals,
    "sum of monthly won deals equals won deals": sum(r[5] for r in funnel) == n_won,
}
print("month       leads  qual  sql  won   sql->won")
for r in funnel[-6:]:
    print(f"{r[0]:%Y-%m}    {r[1]:5d} {r[2]:5d} {r[3]:4d} {r[5]:4d}   {r[8] if r[8] is not None else '-'}")
print(f"\nwon deals won in a later month than created: {wrong} of {n_won} ({wrong / n_won:.0%}) -> counting won by creation month misstates them")
print(f"persons (funnel leads): {n_persons}  vs inbox table crm.leads: {inbox}  -> two meanings of 'leads'")
for k, v in checks.items():
    print(("PASS " if v else "FAIL ") + k)
raise SystemExit(0 if all(checks.values()) else 1)
