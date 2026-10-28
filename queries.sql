-- Query 1: Calculate average oil rate per well, ordered by highest average
SELECT 
    w.well_name, 
    w.field_name, 
    ROUND(AVG(p.oil_rate), 2) AS avg_oil_rate
FROM project_wells w
JOIN project_production p ON w.well_id = p.well_id
GROUP BY w.well_id
ORDER BY avg_oil_rate DESC;

-- Query 2: Find problematic records (status is Maintenance OR oil_rate is NULL)
SELECT
    pw.well_name,
    pj.production_date,
    pj.status,
    pj.oil_rate
FROM project_production pj
JOIN project_wells pw ON pj.well_id = pw.well_id
WHERE pj.status = 'Maintenance' OR pj.oil_rate IS NULL;