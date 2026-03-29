import streamlit as st
from src.engine import compute_outputs

st.set_page_config(page_title="LDIA – Decision Intelligence", layout="wide")

st.title("LDIA – Internal Decision Intelligence (MVP UI)")
st.caption("Week 5: first executive-facing UI layer (Streamlit)")

st.markdown(
    """
**Executive brief:** This internal tool converts monthly sales data into a decision-ready signal
using baseline forecasting, deviation benchmarking, and confidence guardrails.
"""
)

# Sidebar controls (config surface)
st.sidebar.header("Controls")
csv_path = st.sidebar.text_input("CSV path", "data/sales.csv")

deviation_threshold = st.sidebar.slider("Deviation threshold (%)", 3, 30, 8)
rolling_window = st.sidebar.slider("Rolling window (months)", 2, 6, 3)

high_conf = st.sidebar.slider("High confidence threshold", 60, 95, 75)
medium_conf = st.sidebar.slider("Medium confidence threshold", 30, 80, 55)

st.sidebar.subheader("Scenario Simulation")

marketing_uplift = st.sidebar.slider("Marketing uplift (%)", 0, 20, 0)
supply_shock = st.sidebar.slider("Supply shock (%)", 0, 20, 0)
# Auto-run when any parameter changes

outputs = compute_outputs(
    csv_path=csv_path,
    deviation_threshold=float(deviation_threshold),
    rolling_window=int(rolling_window),
    high_conf_threshold=int(high_conf),
    medium_conf_threshold=int(medium_conf),
    marketing_uplift=marketing_uplift,
    supply_shock=supply_shock,
)
k = outputs["kpis"]
f = outputs["forecast"]
c = outputs["confidence"]
d = outputs["decision"]



# --- Top: Decision Panel ---
colA, colB = st.columns([2.2, 1])

with colA:
    st.subheader("Decision Panel")

    if "positive" in d['signal'].lower():
        st.success(d['signal'])
    elif "negative" in d['signal'].lower():
        st.error(d['signal'])
    else:
        st.warning(d['signal'])

    st.info(d['action'])

with colB:
    st.subheader("Risk & Confidence")
    st.metric("Confidence", f"{c['score']}/100", c["label"])
    st.metric("Deviation vs Hist. Avg", f"{f['deviation_pct']:.1f}%")
    st.caption(f"Volatility: {c['volatility']:.2f} | Disagreement: {c['agreement_gap_pct']:.1f}%")

with st.expander("Assumptions & Guardrails"):
    st.write("- Baseline models only (naïve + rolling mean).")
    st.write("- Confidence is heuristic (data coverage, volatility, model agreement).")
    st.write("- Low confidence blocks operational actions.")

st.divider()

# --- Executive KPIs ---
st.subheader("Executive KPIs (Descriptive)")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total sales", f"€{k['total_sales']:,.0f}")
k2.metric("Avg monthly sales", f"€{k['avg_sales']:,.0f}")
k3.metric("Best month", k["best_month"], f"€{k['best_sales']:,.0f}")
k4.metric("Worst month", k["worst_month"], f"€{k['worst_sales']:,.0f}")

st.write(f"**Last MoM change:** €{k['mom_change']:,.0f} ({k['mom_pct']:.1f}%)")

st.divider()

# --- Forecast panel ---
st.subheader("Baseline Forecast (Planning)")
f1, f2, f3 = st.columns(3)
f1.metric("Naïve forecast", f"€{f['naive']:,.0f}")
f2.metric(f"Rolling ({rolling_window}m) forecast", f"€{f['rolling']:,.0f}")
f3.metric("Historical average", f"€{f['historical_avg']:,.0f}")

st.caption(f"Last observed month: {f['last_month'].date()} | Forecast month: {f['next_month'].date()}")

st.divider()

# --- Data preview ---
st.subheader("Raw data preview")
st.dataframe(outputs["df_raw"], use_container_width=True)
st.subheader("Scenario Impact")

st.write(f"Marketing uplift: +{marketing_uplift}%")
st.write(f"Supply shock: -{supply_shock}%")
st.write(f"Adjusted forecast: €{outputs['simulation']['adjusted_forecast']:,.0f}")