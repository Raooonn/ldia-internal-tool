import pandas as pd
DATA_PATH = "data/sales.csv"
df = pd.read_csv(DATA_PATH)
print(df.head())
total_sales = df["sales_eur"].sum()
avg_sales = df["sales_eur"].mean()
best_row = df.loc[df["sales_eur"].idxmax()]
worst_row = df.loc[df["sales_eur"].idxmin()]
last_sales = df["sales_eur"].iloc[-1]
prev_sales = df["sales_eur"].iloc[-2]

mom_change = last_sales - prev_sales
mom_pct = (mom_change / prev_sales) * 100
print("=== LDIA – Week 2 Executive Snapshot (pandas) ===")
print(f"Total sales: €{total_sales:,.0f}")
print(f"Average monthly sales: €{avg_sales:,.0f}")
print(f"Best month: {best_row['month']} (€{best_row['sales_eur']:,})")
print(f"Worst month: {worst_row['month']} (€{worst_row['sales_eur']:,})")
print(f"Last MoM change: €{mom_change:,} ({mom_pct:.1f}%)")
# Convert month to datetime
df["month"] = pd.to_datetime(df["month"])

# Sort by time (important!)
df = df.sort_values("month")

# Set month as index (time index)
df = df.set_index("month")
print(df.head())
print(df.index)
# Baseline 1: Naïve forecast (next month = last observed value)
naive_forecast = df["sales_eur"].iloc[-1]
# Baseline 2: Rolling mean forecast (last 3 months)
rolling_3m = df["sales_eur"].rolling(window=3).mean()
rolling_forecast = rolling_3m.iloc[-1]
# Define next month
last_month = df.index[-1]
next_month = last_month + pd.offsets.MonthBegin(1)
print("\n=== LDIA – Week 3 Baseline Forecast ===")
print(f"Last observed month: {last_month.date()}")
print(f"Forecast month: {next_month.date()}")

print(f"Naïve forecast: €{naive_forecast:,.0f}")
print(f"Rolling 3-month average forecast: €{rolling_forecast:,.0f}")
