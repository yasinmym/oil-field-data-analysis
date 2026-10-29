# Oil Field Data Analysis (SQL + Python)

A data analysis project focusing on petroleum engineering datasets using SQLite and Python.

## Features
- Database Design: Created a relational SQLite database (`oil_field_project.db`) with wells and production tables.
- Advanced SQL: Implemented queries using JOIN, GROUP BY, CTE, and Window Functions (for ranking).
- Python Integration: Connected to the database using sqlite3 for automated data extraction and secure parameterized queries.

## Files
- queries.sql: Contains all the analytical SQL queries used for reporting.
- analysis.py: Python script to connect, query, and output data.
- oil_field_project.db: The SQLite database file.

## How to Run
1. Ensure Python is installed.
2. Run the script:
```bash
python analysis.py