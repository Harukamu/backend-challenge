-- Q1: Balances for all restaurants (aggregation)
SELECT
    restaurant_id,
    SUM(amount) AS available,
    MAX(created_at) AS last_event_at
FROM ledger_entries
WHERE currency = 'PEN'
GROUP BY restaurant_id;

-- Q2: Top 10 restaurants by net revenue (last 7 days)
SELECT
    restaurant_id,
    SUM(amount) AS net_amount,
    COUNT(CASE WHEN type='charge_succeeded' THEN 1 END) AS charge_count,
    COUNT(CASE WHEN type='refund_succeeded' THEN 1 END) AS refund_count
FROM ledger_entries
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY restaurant_id
ORDER BY net_amount DESC
LIMIT 10;

-- Q3: Payout eligibility (filter + anti-join)
SELECT r.restaurant_id, SUM(l.amount) AS available
FROM ledger_entries l
JOIN restaurants r ON l.restaurant_id = r.restaurant_id
LEFT JOIN payouts p ON p.restaurant_id = r.restaurant_id AND p.created_at::date = CURRENT_DATE
WHERE l.currency = 'PEN'
GROUP BY r.restaurant_id
HAVING SUM(l.amount) >= 5000
   AND COUNT(p.payout_id) = 0;

-- Q4: Data integrity check (example: duplicate event_id)
SELECT event_id, COUNT(*) as duplicates
FROM processor_events
GROUP BY event_id
HAVING COUNT(*) > 1;
