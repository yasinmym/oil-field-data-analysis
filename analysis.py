import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 1. Connect to the SQLite database
connection = sqlite3.connect('oil_field_project.db')

# 2. Read data from both tables
query_wells = "SELECT * FROM project_wells;"
df = pd.read_sql_query(query_wells, connection)

query_prod = "SELECT * FROM project_production;"
df_prod = pd.read_sql_query(query_prod, connection)

# 3. Merge the tables based on the well_id
df_merged = pd.merge(df, df_prod, on='well_id')

# 4. Handle missing values in the oil_rate column
df_merged['oil_rate'] = df_merged['oil_rate'].fillna(0)

# 5. Close the database connection
connection.close()

# 6. Calculate average oil rate per well
avg_oil_rate = df_merged.groupby('well_name')['oil_rate'].mean()

# 7. Create the bar chart
plt.figure(figsize=(8, 5))
avg_oil_rate.plot(kind='bar', color='skyblue')

# 8. Set labels and title
plt.title('Average Oil Rate per Well')
plt.xlabel('Well Name')
plt.ylabel('Average Oil Rate (bbl/day)')

# plt.xticks(rotation=45) # Commented out due to compatibility issue with Python 3.14

# 9. Adjust layout and display the plot
plt.tight_layout()
plt.show()