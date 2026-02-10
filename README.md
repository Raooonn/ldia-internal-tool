# Luxury Decision Intelligence Assistant (LDIA)

Internal decision-support tool for luxury businesses
(watches / high-end) to transform raw data into executive insights.

## Project objective
Build a lightweight internal tool that:
- Reads structured business data
- Produces executive-ready metrics
- Evolves into forecasting and decision intelligence

## Target user
Regional Sales Director – Luxury Watches (Europe)

## Initial executive questions
1. What is total and average monthly sales?
2. Which months perform best and worst?
3. How is performance evolving month over month?

## Shipments

### Week 1
- Dataset: `data/sales.csv`
- Script: `hello_decision.py`
- Output evidence: `assets/week1_terminal.png`
- Executive note: `week1_exec_note.md`

Delivered a first end-to-end data-to-insight pipeline.

### Week 2
- Script: `analysis_pandas.py`
- Output evidence: `assets/week2_terminal.png`
- Executive note: `week2_exec_note.md`

Refactored the analysis pipeline using pandas for scalability and robustness.

### Week 3
- Baseline forecasting (naïve + rolling mean)
- Output evidence: `assets/week3_terminal.png`
- Executive note: `week3_exec_note.md`

Introduced a first forward-looking baseline forecast to support planning decisions.
