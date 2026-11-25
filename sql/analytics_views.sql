-- Views that build the funnel rules into the database, so the AI cannot pick the wrong date or table.
-- Applied on top of the crm tables. Pair with a connection table filter that hides crm.leads (the inbox
-- table that is not the funnel's "leads"): table_deny_regex = '^leads$'.

-- One row per UTC month: leads, qualified leads, SQLs, SQL value, won deals and won revenue (won by WON date).
CREATE OR REPLACE VIEW crm.funnel_monthly AS
SELECT month_start, leads, qualified_leads, sql_deals, sql_value_usd, won_deals, won_revenue_usd,
       ROUND(sql_deals::numeric / NULLIF(qualified_leads, 0), 4) AS qualified_to_sql_rate,
       ROUND(won_deals::numeric / NULLIF(sql_deals, 0), 4) AS sql_to_won_rate
FROM (
  SELECT m.month_start,
    (SELECT COUNT(*) FROM crm.persons p
       WHERE date_trunc('month', p.add_time AT TIME ZONE 'UTC') = m.month_start) AS leads,
    (SELECT COUNT(*) FROM crm.persons p
       WHERE p.qualification = 'Qualified'
         AND date_trunc('month', p.add_time AT TIME ZONE 'UTC') = m.month_start) AS qualified_leads,
    (SELECT COUNT(*) FROM crm.deals d
       WHERE date_trunc('month', d.add_time AT TIME ZONE 'UTC') = m.month_start) AS sql_deals,
    (SELECT SUM(d.value_usd) FROM crm.deals d
       WHERE date_trunc('month', d.add_time AT TIME ZONE 'UTC') = m.month_start) AS sql_value_usd,
    (SELECT COUNT(*) FROM crm.deals d
       WHERE d.status = 'won'
         AND date_trunc('month', d.won_time AT TIME ZONE 'UTC') = m.month_start) AS won_deals,
    (SELECT SUM(d.value_usd) FROM crm.deals d
       WHERE d.status = 'won'
         AND date_trunc('month', d.won_time AT TIME ZONE 'UTC') = m.month_start) AS won_revenue_usd
  FROM (
    SELECT date_trunc('month', add_time AT TIME ZONE 'UTC') AS month_start FROM crm.persons
    UNION
    SELECT date_trunc('month', add_time AT TIME ZONE 'UTC') FROM crm.deals
    UNION
    SELECT date_trunc('month', won_time AT TIME ZONE 'UTC') FROM crm.deals WHERE status = 'won'
  ) m
) f;

-- Won deals only, with the month they were WON already worked out.
CREATE OR REPLACE VIEW crm.won_deals AS
SELECT d.id, d.title, d.value_usd, d.person_id, d.stage_id, d.add_time, d.won_time,
       date_trunc('month', d.won_time AT TIME ZONE 'UTC') AS won_month
FROM crm.deals d
WHERE d.status = 'won';

-- Every deal with its lead's agreed channel group and country, and the month it was created.
CREATE OR REPLACE VIEW crm.deals_with_channel AS
SELECT d.id, d.title, d.value_usd, d.status, d.stage_id, d.add_time, d.won_time, d.lost_time,
       date_trunc('month', d.add_time AT TIME ZONE 'UTC') AS created_month,
       p.id AS person_id, p.source_medium_group, p.country
FROM crm.deals d
JOIN crm.persons p ON p.id = d.person_id;
