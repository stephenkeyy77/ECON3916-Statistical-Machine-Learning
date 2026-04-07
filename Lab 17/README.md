NY Fed Yield Curve Recession Model Replication
Objective: Replicated the Federal Reserve Bank of New York's yield curve recession probability model by fitting logistic regression to FRED macroeconomic data, predicting NBER-dated recessions 12 months ahead using the 10Y–3M Treasury yield spread.
Methodology

Sourced monthly 10-Year minus 3-Month Treasury yield spread (T10Y3M) and NBER recession indicator (USREC) from the FRED API, covering 1970 to present.
Constructed a 12-month lagged yield spread feature as the sole predictor, aligning with the NY Fed's original specification.
Benchmarked a Linear Probability Model (OLS) against logistic regression to illustrate the LPM's well-known boundary violations (predicted probabilities outside [0, 1]) on real data.
Fitted a logistic regression via scikit-learn (unregularized, C = 1e9) and extracted coefficient estimates, odds ratios, and 95% confidence intervals using statsmodels.
Generated the full recession probability time series with NBER recession shading and evaluated model performance across historical episodes.
Extended the baseline model by adding lagged unemployment (UNRATE) as a second predictor to test for omitted variable bias and assess whether a multivariate specification improves forecast accuracy.

Key Findings

The yield spread odds ratio was approximately 0.45 (95% CI: 0.37–0.83), implying that a 1 percentage-point steepening of the curve cuts recession odds by roughly 55% — consistent with the spread's established role as a leading indicator.
During the 2022–2024 yield curve inversion, the model predicted recession probabilities peaking near 40%, yet no NBER recession materialized — a useful case study in interpreting probabilistic forecasts under structural uncertainty.
Adding lagged unemployment shifted the spread's odds ratio toward 1.0 (0.45 → 0.57), but UNRATE itself was not statistically significant (p = 0.15, CI crossing 1.0), supporting the parsimony of the NY Fed's single-predictor design.

Tech Stack
Python · pandas · NumPy · scikit-learn · statsmodels · matplotlib · fredapi
