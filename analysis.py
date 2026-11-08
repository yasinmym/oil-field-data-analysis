import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Connect to the SQLite database
conn = sqlite3.connect('oil_field_project.db')

# Read tables into DataFrames
wells_df = pd.read_sql_query("SELECT * FROM project_wells", conn)
prod_df = pd.read_sql_query("SELECT * FROM project_production", conn)

# Close connection after loading data
conn.close()

# Merge the two tables on well_id
df = pd.merge(wells_df, prod_df, on='well_id')

# Fill missing oil rates with 0 (e.g., wells under maintenance)
df['oil_rate'] = df['oil_rate'].fillna(0)

print("--- Statistical Summary ---")
print(df[['depth_m', 'pressure_bar', 'oil_rate']].describe())

# Calculate basic metrics for oil rate
mean_oil = df['oil_rate'].mean()
median_oil = df['oil_rate'].median()
std_oil = df['oil_rate'].std()

print(f"\nMean: {mean_oil:.2f} | Median: {median_oil:.2f} | Std Dev: {std_oil:.2f}")

# T-test comparing North vs South fields
north = df[df['field_name'] == 'North Field']['oil_rate']
south = df[df['field_name'] == 'South Field']['oil_rate']
t_stat, p_val = stats.ttest_ind(north, south, nan_policy='omit')

print(f"\nHypothesis Test - T-stat: {t_stat:.2f}, P-value: {p_val:.4f}")
if p_val < 0.05:
    print("Conclusion: Significant difference in production.")
else:
    print("Conclusion: No significant difference between fields.")

# --- Plotting ---

# 1. Average oil rate per well
avg_rate = df.groupby('well_name')['oil_rate'].mean()
plt.figure(figsize=(8, 5))
avg_rate.plot(kind='bar', color='skyblue')
plt.title('Average Oil Rate by Well')
plt.ylabel('Oil Rate (bbl/day)')
plt.tight_layout()
plt.savefig('plot1_avg_oil_rate.png')
plt.close()

# 2. Production trend over time for Well-Alpha
df['production_date'] = pd.to_datetime(df['production_date'])
alpha_data = df[df['well_name'] == 'Well-Alpha'].sort_values('production_date')
plt.figure(figsize=(8, 5))
plt.plot(alpha_data['production_date'], alpha_data['oil_rate'], marker='o', color='green')
plt.title('Well-Alpha Production Trend')
plt.ylabel('Oil Rate (bbl/day)')
plt.grid(True)
plt.tight_layout()
plt.savefig('plot2_well_alpha_trend.png')
plt.close()

# 3. Distribution of oil rates
plt.figure(figsize=(8, 5))
plt.hist(df['oil_rate'], bins=5, color='purple', edgecolor='black')
plt.title('Oil Rate Distribution')
plt.xlabel('Oil Rate (bbl/day)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('plot3_oil_rate_distribution.png')
plt.close()

# 4. Pressure vs Oil Rate scatter plot
plt.figure(figsize=(8, 5))
plt.scatter(df['pressure_bar'], df['oil_rate'], color='red', alpha=0.7)
plt.title('Pressure vs Oil Rate')
plt.xlabel('Pressure (bar)')
plt.ylabel('Oil Rate (bbl/day)')
plt.grid(True)
plt.tight_layout()
plt.savefig('plot4_pressure_vs_oil_rate.png')
plt.close()

# 5. Box plot to find outliers
plt.figure(figsize=(6, 5))
plt.boxplot(df['oil_rate'], patch_artist=True, boxprops=dict(facecolor='lightblue'))
plt.title('Box Plot of Oil Rate')
plt.ylabel('Oil Rate (bbl/day)')
plt.tight_layout()
plt.savefig('plot5_oil_rate_boxplot.png')
plt.close()

print("\nAll plots saved successfully.")