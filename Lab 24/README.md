# Causal ML — Double Machine Learning for 401(k) Policy Evaluation

## Objective

This project applies Double Machine Learning (Chernozhukov et al., 2018) to estimate the causal effect of 401(k) eligibility on household net financial assets, addressing selection bias and high-dimensional confounding with cross-fitted Random Forest nuisance learners.

## Methodology

- **Regularization bias demonstration:** Simulated a known data-generating process (TRUE ATE = 5.0) and showed that naive LASSO shrinks the treatment coefficient toward zero, producing biased causal estimates due to indiscriminate penalization of treatment and nuisance variables alike.
- **DoubleML Partially Linear Regression (PLR):** Constructed a PLR model on the Chernozhukov & Hansen 401(k) dataset (n ≈ 9,915), using `net_tfa` (net total financial assets) as the outcome and `e401` (401(k) eligibility) as the binary treatment, with income, age, education, family size, and marital status as covariates.
- **Random Forest nuisance learners:** Employed two Random Forest regressors (500 trees, max depth 7) for the outcome model (Y | X) and the treatment model (D | X), with 5-fold cross-fitting to eliminate overfitting bias in the orthogonal score.
- **Conditional ATE (CATE) analysis:** Estimated subgroup treatment effects by income quartile, fitting separate DML models on each subset to detect heterogeneity in the 401(k) effect across the income distribution.
- **Sensitivity analysis:** Assessed robustness to potential unmeasured confounders using the DoubleML `sensitivity_analysis()` method with confounding bounds cf_y = 0.03 and cf_d = 0.03.

## Key Findings

- **Average Treatment Effect:** The estimated ATE of 401(k) eligibility on net financial assets is approximately −$643, suggesting no meaningful positive effect after controlling for income, age, education, family size, and other covariates.
- **Treatment effect heterogeneity:** CATE analysis by income quartile revealed mixed and statistically insignificant results across all subgroups — Q1: +$492, Q2: −$1,633, Q3: −$827, Q4: −$1,433 — with all 95% confidence intervals spanning zero, indicating insufficient evidence of a differential treatment effect by income level.
- **Regularization bias:** Naive LASSO underestimated the true ATE by approximately 5–10% on simulated data, confirming that standard ML regularization is inappropriate for causal coefficient estimation without orthogonalization.
- **Robustness:** The sensitivity analysis yielded a robustness value of 0.0124, indicating that an omitted confounder explaining just 1.2% of the residual variation in both Y and D could nullify the estimate. This suggests the causal estimate is fragile and sensitive to potential unmeasured confounding.

## Tools & Libraries

Python · DoubleML · scikit-learn (Random Forest, LassoCV) · pandas · NumPy · Matplotlib
