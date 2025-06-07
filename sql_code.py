import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the dataset
df = pd.read_csv('online_sales_dataset.csv', parse_dates=['InvoiceDate'])

# 2. Filter out invalid rows
df = df[df['Quantity'] > 0]

# 3. Extract year and month (SQL: EXTRACT(MONTH FROM order_date))
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month

# 4. Calculate Revenue
if 'Discount' in df.columns:
    df['Revenue'] = df['Quantity'] * df['UnitPrice'] * (1 - df['Discount'])
else:
    df['Revenue'] = df['Quantity'] * df['UnitPrice']

# 5. GROUP BY year/month, SUM(revenue), COUNT(DISTINCT order_id)
summary = df.groupby(['Year', 'Month']).agg(
    Total_Revenue=('Revenue', 'sum'),
    Sales_Volume=('InvoiceNo', 'nunique')  # equivalent to COUNT(DISTINCT order_id)
).reset_index()

# 6. ORDER BY year/month
summary = summary.sort_values(by=['Year', 'Month'])

# 7. LIMIT to last 6 months (optional)
# Convert to datetime for filtering
summary['YearMonth'] = pd.to_datetime(summary[['Year', 'Month']].assign(DAY=1))
last_6_months = summary.sort_values('YearMonth').tail(6)

# 8. Display result
print("Sales Trend Summary (Last 6 Months):")
print(last_6_months[['Year', 'Month', 'Total_Revenue', 'Sales_Volume']])

# 9. Plot the Revenue Trend
plt.figure(figsize=(10, 5))
plt.plot(last_6_months['YearMonth'], last_6_months['Total_Revenue'], marker='o', color='blue', label='Total Revenue')
plt.title('Monthly Revenue Trend (Last 6 Months)')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
