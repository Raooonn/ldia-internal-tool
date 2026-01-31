# LDIA – Week 1 Executive Note

## What was delivered
A first working internal prototype that converts a raw monthly sales file
into an executive-ready snapshot.

The tool reads a structured CSV file and automatically produces:
- total sales
- average monthly sales
- best and worst performing months
- last month-over-month change

## Business value
This establishes a repeatable baseline to transform raw operational data
into decision-ready insights with no manual Excel work.

The output is designed to be immediately readable by a regional sales director.

## Current limitations
- Static dataset (single CSV)
- No database persistence
- No forecasting beyond last month comparison

## Next steps
- Replace raw CSV logic with pandas for scalability
- Prepare data structure for time-series forecasting
- Move toward an internal UI for non-technical users
