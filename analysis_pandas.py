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

# ==========================
# CONFIGURATION PARAMETERS
# ==========================

from config import (
    DEVIATION_THRESHOLD,
    HIGH_CONFIDENCE_THRESHOLD,
    MEDIUM_CONFIDENCE_THRESHOLD,
    ROLLING_WINDOW,
)

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
rolling_3m = df["sales_eur"].rolling(window=ROLLING_WINDOW).mean()
rolling_forecast = rolling_3m.iloc[-1]
# Define next month
last_month = df.index[-1]
next_month = last_month + pd.offsets.MonthBegin(1)
print("\n=== LDIA – Week 3 Baseline Forecast ===")
print(f"Last observed month: {last_month.date()}")
print(f"Forecast month: {next_month.date()}")

print(f"Naïve forecast: €{naive_forecast:,.0f}")
print(f"Rolling 3-month average forecast: €{rolling_forecast:,.0f}")

# Historical average (structural benchmark)
historical_avg = df["sales_eur"].mean()
deviation_pct = ((rolling_forecast - historical_avg) / historical_avg) * 100

# --- Confidence heuristics (explainable) ---

n_months = len(df)

# Volatility proxy: coefficient of variation (std/mean)
volatility = df["sales_eur"].std() / df["sales_eur"].mean()

# Agreement proxy: how far naive is from rolling (as % of rolling)
agreement_gap_pct = abs(naive_forecast - rolling_forecast) / rolling_forecast * 100
# Score components (0..100) - simple, explainable
data_score = min(100, (n_months / 24) * 100)  # 24 mesos = "ideal" per tenir estabilitat

# Volatility score: <10% vol = molt bé; >30% vol = malament
if volatility <= 0.10:
    vol_score = 100
elif volatility >= 0.30:
    vol_score = 20
else:
    # linear interpolation between 0.10 and 0.30
    vol_score = 100 - ((volatility - 0.10) / (0.20)) * 80

# Agreement score: si naive i rolling difereixen molt, baixa confiança
if agreement_gap_pct <= 3:
    agree_score = 100
elif agreement_gap_pct >= 12:
    agree_score = 30
else:
    # linear interpolation between 3% and 12%
    agree_score = 100 - ((agreement_gap_pct - 3) / 9) * 70

confidence_score = round(0.4 * data_score + 0.35 * vol_score + 0.25 * agree_score)
if confidence_score >= HIGH_CONFIDENCE_THRESHOLD:
    confidence_label = "High"
elif confidence_score >= MEDIUM_CONFIDENCE_THRESHOLD:
    confidence_label = "Medium"
else:
    confidence_label = "Low"

print("\n=== Forecast Confidence (heuristic) ===")
print(f"Deviation vs historical average: {deviation_pct:.1f}%")
print(f"Data points (months): {n_months}")
print(f"Volatility (std/mean): {volatility:.2f}")
print(f"Baseline disagreement (naive vs rolling): {agreement_gap_pct:.1f}%")
print(f"Confidence: {confidence_score}/100 ({confidence_label})")


print("\n=== Decision Signal ===")
if confidence_label == "Low":
    print("Signal: Low confidence")
    print("Action: Do not trigger operational changes. Validate data quality and gather more history.")

else:
    if deviation_pct > DEVIATION_THRESHOLD:
        print("Signal: Strong positive deviation")

        if confidence_label == "Medium":
            print("Action: Review stock coverage of top SKUs and validate demand drivers (no operational changes yet).")
        else:  # High
            print("Action: Review stock coverage of top SKUs and validate supply readiness.")

    elif deviation_pct < -DEVIATION_THRESHOLD:
        print("Signal: Negative deviation")

        if confidence_label == "Medium":
            print("Action: Trigger commercial review (pipeline + campaign timing) before any promotional measures.")
        else:  # High
            print("Action: Trigger commercial review and prepare a targeted commercial response plan.")

    else:
        print("Signal: Within normal range")
        print("Action: Maintain current commercial plan.")
    if deviation_pct > DEVIATION_THRESHOLD * 2:
       deviation_level = "Strong"
    elif deviation_pct > DEVIATION_THRESHOLD:
       deviation_level = "Moderate"
    elif deviation_pct < -DEVIATION_THRESHOLD * 2:
       deviation_level = "Strong"
    elif deviation_pct < -DEVIATION_THRESHOLD:
       deviation_level = "Moderate"
    else:
       deviation_level = "Normal"