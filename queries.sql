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

-- Query 3: Rank wells by pressure within their field (using Window Functions) 
SELECT 
    w.well_name, 
    w.field_name, 
    p.pressure_bar, 
    Rank() OVER(PARTITION BY w.field_name  ORDER BY p.pressure_bar DESC) AS pressure_rank 
    FROM project_wells w 
    JOIN project_production p ON w.well_id = p.well_id; 

-- Query 4: Find wells producing below their field's average (using CTE) 
WITH FieldAvg AS ( 
    SELECT w.field_name, AVG(p.oil_rate) AS field_avg_rate 
    FROM project_wells w 
    JOIN project_production p ON w.well_id = p.well_id 
    GROUP BY w.field_name 
) 
SELECT 
    w.well_name, 
    w.field_name, 
    p.oil_rate, 
    fa.field_avg_rate 
FROM project_production p 
JOIN project_wells w ON p.well_id = w.well_id 
JOIN FieldAvg fa ON w.field_name = fa.field_name 
WHERE p.oil_rate < fa.field_avg_rate; 
