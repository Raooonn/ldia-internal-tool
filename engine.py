import pandas as pd


def compute_outputs(
    csv_path: str,
    deviation_threshold: float,
    rolling_window: int,
    high_conf_threshold: int,
    medium_conf_threshold: int,
):
    df_raw = pd.read_csv(csv_path)

    # Week 2 KPIs (raw)
    total_sales = df_raw["sales_eur"].sum()
    avg_sales = df_raw["sales_eur"].mean()
    best_row = df_raw.loc[df_raw["sales_eur"].idxmax()]
    worst_row = df_raw.loc[df_raw["sales_eur"].idxmin()]

    last_sales_raw = df_raw["sales_eur"].iloc[-1]
    prev_sales_raw = df_raw["sales_eur"].iloc[-2]
    mom_change = last_sales_raw - prev_sales_raw
    mom_pct = (mom_change / prev_sales_raw) * 100

    # Week 3 time series prep
    df = df_raw.copy()
    df["month"] = pd.to_datetime(df["month"])
    df = df.sort_values("month").set_index("month")

    # Forecasts
    naive_forecast = df["sales_eur"].iloc[-1]
    rolling_series = df["sales_eur"].rolling(window=rolling_window).mean()
    rolling_forecast = rolling_series.iloc[-1]

    last_month = df.index[-1]
    next_month = last_month + pd.offsets.MonthBegin(1)

    # Benchmarks
    historical_avg = df["sales_eur"].mean()
    deviation_pct = ((rolling_forecast - historical_avg) / historical_avg) * 100

    # Confidence heuristics
    n_months = len(df)
    volatility = df["sales_eur"].std() / df["sales_eur"].mean()
    agreement_gap_pct = abs(naive_forecast - rolling_forecast) / rolling_forecast * 100

    data_score = min(100, (n_months / 24) * 100)

    if volatility <= 0.10:
        vol_score = 100
    elif volatility >= 0.30:
        vol_score = 20
    else:
        vol_score = 100 - ((volatility - 0.10) / 0.20) * 80

    if agreement_gap_pct <= 3:
        agree_score = 100
    elif agreement_gap_pct >= 12:
        agree_score = 30
    else:
        agree_score = 100 - ((agreement_gap_pct - 3) / 9) * 70

    confidence_score = round(0.4 * data_score + 0.35 * vol_score + 0.25 * agree_score)

    if confidence_score >= high_conf_threshold:
        confidence_label = "High"
    elif confidence_score >= medium_conf_threshold:
        confidence_label = "Medium"
    else:
        confidence_label = "Low"

    # Decision signal w/ guardrails
    if confidence_label == "Low":
        signal = "Low confidence"
        action = "Do not trigger operational changes. Validate data quality and gather more history."
    else:
        if deviation_pct > deviation_threshold:
            signal = "Strong positive deviation"
            if confidence_label == "Medium":
                action = "Review stock coverage of top SKUs and validate demand drivers (no operational changes yet)."
            else:
                action = "Review stock coverage of top SKUs and validate supply readiness."
        elif deviation_pct < -deviation_threshold:
            signal = "Negative deviation"
            if confidence_label == "Medium":
                action = "Trigger commercial review (pipeline + campaign timing) before any promotional measures."
            else:
                action = "Trigger commercial review and prepare a targeted commercial response plan."
        else:
            signal = "Within normal range"
            action = "Maintain current commercial plan."

    return {
        "kpis": {
            "total_sales": total_sales,
            "avg_sales": avg_sales,
            "best_month": str(best_row["month"]),
            "best_sales": float(best_row["sales_eur"]),
            "worst_month": str(worst_row["month"]),
            "worst_sales": float(worst_row["sales_eur"]),
            "mom_change": float(mom_change),
            "mom_pct": float(mom_pct),
        },
        "forecast": {
            "last_month": last_month,
            "next_month": next_month,
            "naive": float(naive_forecast),
            "rolling": float(rolling_forecast),
            "historical_avg": float(historical_avg),
            "deviation_pct": float(deviation_pct),
        },
        "confidence": {
            "score": int(confidence_score),
            "label": confidence_label,
            "n_months": int(n_months),
            "volatility": float(volatility),
            "agreement_gap_pct": float(agreement_gap_pct),
        },
        "decision": {"signal": signal, "action": action},
        "df_raw": df_raw,
    }