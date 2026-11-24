-- Single-purpose funnel metrics, one statement each. Each was added to Auto Ontology as a SQL attribute
-- under the matching term (Person or Deal). Keep each one narrow: a metric that states exactly one way to
-- compute a figure steered the answering agent better than long descriptions did.

-- Person term -------------------------------------------------------------
-- Leads: a lead is a person record, counted by persons.add_time month (UTC). Not the crm.leads inbox table.
SELECT COUNT(*) AS leads FROM crm.persons;

-- Qualified Leads: persons marked 'Qualified', by persons.add_time month (UTC).
SELECT COUNT(*) AS qualified_leads FROM crm.persons WHERE qualification = 'Qualified';

-- Deal term ---------------------------------------------------------------
-- SQL (deals created): every deal created, any status, by deals.add_time month (UTC).
SELECT COUNT(*) AS sql_deals FROM crm.deals;

-- SQL Value (USD, provisional): total value of every deal created, by creation month.
SELECT SUM(value_usd) AS sql_value_usd FROM crm.deals;

-- Won Deals: status 'won', by the month of won_time (the WON date), never by creation month.
SELECT COUNT(*) AS won_deals FROM crm.deals WHERE status = 'won';

-- Won Revenue (USD): same rule as Won Deals.
SELECT SUM(value_usd) AS won_revenue_usd FROM crm.deals WHERE status = 'won';

-- Open SQL (current snapshot): not yet won or lost right now. A snapshot, not a monthly figure.
SELECT COUNT(*) AS open_sql FROM crm.deals WHERE status = 'open';

-- Won Deals and Revenue by Won Month: the narrow metric that removed the "won by creation month" error.
SELECT date_trunc('month', won_time AT TIME ZONE 'UTC') AS won_month, COUNT(*) AS won_deals,
       SUM(value_usd) AS won_revenue_usd
FROM crm.deals WHERE status = 'won' GROUP BY 1 ORDER BY 1;

-- Deal-by-channel: use the agreed source/medium group, never the raw lead_source column.
SELECT p.source_medium_group, COUNT(*) AS sql_deals, SUM(d.value_usd) AS sql_value_usd,
       COUNT(*) FILTER (WHERE d.status = 'won') AS won_deals,
       SUM(d.value_usd) FILTER (WHERE d.status = 'won') AS won_value_usd
FROM crm.deals d JOIN crm.persons p ON p.id = d.person_id
GROUP BY p.source_medium_group;
