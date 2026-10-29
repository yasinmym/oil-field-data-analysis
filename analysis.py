import sqlite3

try:
    # 1. Connect to the database
    connection = sqlite3.connect('oil_field_project.db')
    cursor = connection.cursor()

    # 2. Secure query with parameterized inputs (preventing SQL injection)
    min_pressure = 100
    query = """
        SELECT w.well_name, p.oil_rate 
        FROM project_production p 
        JOIN project_wells w ON p.well_id = w.well_id 
        WHERE p.pressure_bar > ?;
    """
    
    # 3. Execute the query
    cursor.execute(query, (min_pressure,))
    results = cursor.fetchall()

    print(f"--- Wells with pressure > {min_pressure} bar ---")
    for row in results:
        print(f"Well: {row[0]}, Oil Rate: {row[1]}")

except sqlite3.Error as e:
    print(f"Database error: {e}")
    
finally:
    # 4. Always close the connection
    if 'connection' in locals():
        connection.close()