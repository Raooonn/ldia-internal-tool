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
