# LDIA – Week 3 Executive Note

## What was delivered
A baseline monthly sales forecast was added to the analytics pipeline,
providing a forward-looking view based on recent performance.

Two standard baseline methods were implemented:
- Naïve forecast (last observed month)
- 3-month rolling average forecast

## Business interpretation
Assuming no major changes in commercial conditions, baseline projections
suggest next-month sales within a bounded range defined by recent volatility.

The naïve forecast reflects short-term momentum, while the rolling average
smooths recent fluctuations to provide a more stable expectation.

## Business value
This establishes a first decision-ready forward-looking signal that can be
used for planning discussions, budget alignment, and early risk detection.

## Limitations
- No seasonality modeling
- No external drivers included
- Short historical window

## Next steps
- Extend the time series with additional historical data
- Introduce simple accuracy tracking (backtesting)
- Integrate forecasts into an internal UI for non-technical users
