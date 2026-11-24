-- Canonical monthly funnel. One row per UTC month.
-- Leads            = persons by add date (NOT the crm.leads inbox table)
-- Qualified leads  = persons marked 'Qualified'
-- SQL deals        = every deal created, any status, by creation month
-- Won deals        = status 'won', by WON date (won_time), never by creation month
-- Rates are ratios of the month's totals, not cohort rates, so SQL-to-won can exceed 1.
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
) f
ORDER BY month_start
