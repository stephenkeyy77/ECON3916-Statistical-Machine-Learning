
# Architecting the Prediction Engine: Multivariate OLS for Real Estate Valuation

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)
![statsmodels](https://img.shields.io/badge/statsmodels-Patsy_API-4DABCF?style=flat)
![pandas](https://img.shields.io/badge/pandas-numpy-150458?style=flat&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive_Viz-3F4F75?style=flat&logo=plotly&logoColor=white)
![Course](https://img.shields.io/badge/ECON_3916-Statistical_ML-1F4E79?style=flat)

## Objective

Engineered a multivariate hedonic pricing OLS model on cross-sectional Zillow ZHVI 2026 micro-data to operationalize a transition from explanatory econometrics to predictive valuation, benchmarking out-of-sample performance via a dollar-denominated RMSE loss function.

---

## Dataset

**Zillow ZHVI 2026 Micro Dataset** — 1,000 cross-sectional residential observations ingested directly from a hosted GitHub source via `pandas.read_csv()`, ensuring full reproducibility without local file dependency.

| Feature | Type | Range / Values | Description |
|---|---|---|---|
| `Home_Value` | Continuous | $21,653 – $584,771 | Target variable — property valuation (USD) |
| `Square_Footage` | Continuous | 236 – 4,366 sq ft | Interior living area |
| `Property_Age` | Continuous | 0 – 80 years | Age of property in years |
| `Distance_to_Transit` | Continuous | 0.12 – 14.99 miles | Distance to nearest transit node |
| `School_District_Rating` | Categorical | Poor / Average / Good / Excellent | Ordinal quality rating (dummy-encoded by Patsy; baseline: *Average*) |

---

## Methodology

**Step 1 — Data Ingestion**
- Pulled raw CSV from a public GitHub URL via `pandas.read_csv()`, producing a clean 1,000-row DataFrame with five hedonic features.

**Step 2 — Model Specification via Patsy Formula API**
- Leveraged `statsmodels.formula.api` (`smf`) to declaratively specify the OLS functional form using R-style syntax. Patsy automatically dummy-encoded `School_District_Rating` with *Average* as the baseline category:
  ```
  Home_Value ~ Square_Footage + Property_Age + Distance_to_Transit + School_District_Rating
  ```

**Step 3 — OLS Estimation**
- Fit the model via `smf.ols(formula=formula, data=df).fit()`, extracting the full coefficient table, standard errors, t-statistics, p-values, and goodness-of-fit diagnostics from the `results` object.

**Step 4 — Prediction Extraction**
- Called `results.predict(df)` to generate the in-sample fitted values vector ŷ, transitioning the `results` object from a tool of statistical inference to a deployable prediction instrument.

**Step 5 — Loss Function Evaluation**
- Computed RMSE using `statsmodels.tools.eval_measures.rmse()` between actuals and predictions, formatted as a nominal USD figure to produce a financially interpretable, dollar-denominated error margin.

**Step 6 — Residual Forensics Dashboard**
- Built a 4-panel interactive diagnostic suite in Plotly (`graph_objects`) to audit model assumptions post-estimation:
  - **Panel 1 — Residuals vs. Fitted:** primary heteroscedasticity detector; outliers exceeding ±2σ flagged in crimson
  - **Panel 2 — Residual Distribution:** normality check overlaid with reference normal curve
  - **Panel 3 — Scale–Location plot:** LOWESS smoothing reveals variance trend across the fitted value range
  - **Panel 4 — Residuals over Index:** structural break scanner for regime shifts across observation order

---

## Results

### Model Performance

| Metric | Value |
|---|---|
| Observations | 1,000 |
| R² | 0.766 |
| Adjusted R² | 0.765 |
| F-statistic | 542.5 (p ≈ 2.81e-309) |
| **RMSE** | **$42,316.69** |

### Coefficient Summary

| Predictor | Coefficient | Std Err | t-stat | p-value |
|---|---|---|---|---|
| Intercept | +$89,840 | 6,448 | 13.93 | 0.000 *** |
| `Square_Footage` | +$120.79 / sq ft | 2.19 | 55.25 | 0.000 *** |
| `Property_Age` | −$814.60 / yr | 57.37 | −14.20 | 0.000 *** |
| `Distance_to_Transit` | −$997.71 / mile | 317.2 | −3.15 | 0.002 ** |
| `School_District_Rating [Excellent]` | −$1,085 | 3,956 | −0.27 | 0.784 n.s. |
| `School_District_Rating [Good]` | −$3,104 | 3,679 | −0.84 | 0.399 n.s. |
| `School_District_Rating [Poor]` | +$534 | 3,858 | +0.14 | 0.890 n.s. |

*`***` p < 0.001 · `**` p < 0.01 · `n.s.` not significant*

---

## Key Findings

**Statistically significant predictors:**
- `Square_Footage` (+$120.79/sq ft) is the dominant valuation driver — each additional square foot carries a measurable, precisely estimated price premium.
- `Property_Age` (−$814.60/yr) imposes the strongest per-unit penalty, consistent with physical depreciation and obsolescence effects.
- `Distance_to_Transit` (−$997.71/mile) confirms that accessibility is meaningfully priced into residential market values.

**Notable non-finding:**
- `School_District_Rating` dummies were statistically insignificant across all categories (p > 0.39). After controlling for square footage, property age, and transit access, school quality carries no residual explanatory power in this cross-section. This is a substantive econometric finding — not a data flaw — suggesting that school quality effects may be fully mediated by the physical and locational attributes already in the model.

**Dollar-denominated loss framing:**
- The RMSE of **$42,316.69** represents the model's average prediction error in nominal US dollars — a direct measure of algorithmic business risk interpretable against real-world underwriting tolerances and appraisal confidence thresholds. This framing positions the OLS engine not merely as a statistical tool, but as a deployable valuation instrument with a quantifiable confidence cost.

---

## Tech Stack

`Python` · `pandas` · `numpy` · `statsmodels` · `Patsy Formula API` · `Plotly` · `Google Colab`
```
