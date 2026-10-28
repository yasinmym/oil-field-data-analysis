import sqlite3 
connection = sqlite3.connect('oil_field_project.db') 
cursor= connection.cursor() 
query= "SELECT * FROM project_wells LIMIT 3;" 
cursor.execute(query) 
results = cursor.fetchall() 
print("Data from Python:") 
for row in results: 
    print(row) 
connection.close() 
