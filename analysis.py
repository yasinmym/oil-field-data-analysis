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

print("Data loaded and merged successfully.\n")

# --- 6. Statistical Summary ---
print("--- Statistical Summary ---")
print(df_merged[['depth_m', 'pressure_bar', 'oil_rate']].describe())
print("\n")

# --- 7. Data Visualization (Saving plots as images) ---

# Plot 1: Bar Chart (Average Oil Rate per Well)
avg_oil_rate = df_merged.groupby('well_name')['oil_rate'].mean()
plt.figure(figsize=(8, 5))
avg_oil_rate.plot(kind='bar', color='skyblue')
plt.title('Average Oil Rate per Well')
plt.xlabel('Well Name')
plt.ylabel('Average Oil Rate (bbl/day)')
plt.tight_layout()
plt.savefig('plot1_avg_oil_rate.png')
plt.close()
print("Saved: plot1_avg_oil_rate.png")

# Plot 2: Line Chart (Production Trend for Well-Alpha)
df_merged['production_date'] = pd.to_datetime(df_merged['production_date'])
well_alpha_data = df_merged[df_merged['well_name'] == 'Well-Alpha'].sort_values('production_date')
plt.figure(figsize=(8, 5))
plt.plot(well_alpha_data['production_date'], well_alpha_data['oil_rate'], marker='o', color='green', linestyle='-')
plt.title('Oil Production Trend for Well-Alpha')
plt.xlabel('Date')
plt.ylabel('Oil Rate (bbl/day)')
plt.grid(True)
plt.tight_layout()
plt.savefig('plot2_well_alpha_trend.png')
plt.close()
print("Saved: plot2_well_alpha_trend.png")

# Plot 3: Histogram (Distribution of Oil Rate)
plt.figure(figsize=(8, 5))
plt.hist(df_merged['oil_rate'], bins=5, color='purple', edgecolor='black')
plt.title('Distribution of Oil Rate')
plt.xlabel('Oil Rate (bbl/day)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('plot3_oil_rate_distribution.png')
plt.close()
print("Saved: plot3_oil_rate_distribution.png")

# Plot 4: Scatter Plot (Pressure vs Oil Rate)
plt.figure(figsize=(8, 5))
plt.scatter(df_merged['pressure_bar'], df_merged['oil_rate'], color='red', alpha=0.7)
plt.title('Relationship between Pressure and Oil Rate')
plt.xlabel('Pressure (bar)')
plt.ylabel('Oil Rate (bbl/day)')
plt.grid(True)
plt.tight_layout()
plt.savefig('plot4_pressure_vs_oil_rate.png')
plt.close()
print("Saved: plot4_pressure_vs_oil_rate.png")

# Plot 5: Box Plot (Oil Rate)
plt.figure(figsize=(6, 5))
plt.boxplot(df_merged['oil_rate'], patch_artist=True, boxprops=dict(facecolor='lightblue'))
plt.title('Box Plot of Oil Rate')
plt.ylabel('Oil Rate (bbl/day)')
plt.tight_layout()
plt.savefig('plot5_oil_rate_boxplot.png')
plt.close()
print("Saved: plot5_oil_rate_boxplot.png\n")

# --- 8. Correlation Matrix ---
print("--- Correlation Matrix ---")
correlation_matrix = df_merged[['depth_m', 'pressure_bar', 'oil_rate']].corr()
print(correlation_matrix) 
