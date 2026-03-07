# ECON 3916 — Assignment 3: Causal Inference & Non-Parametric Methods
> Statistical & Machine Learning for Economics · Northeastern University

This notebook applies three non-parametric causal inference techniques to synthetic SwiftCart operational data, demonstrating why classical parametric assumptions (normality, homoscedasticity, no selection bias) systematically fail in real-world gig economy contexts.

---

## Problem Structure

### Part 1 — The Zero-Inflated Gig Economy Tip Distribution
**Business context:** A labor union is challenging SwiftCart's public claim about "Median Driver Compensation." Tip data is notoriously zero-inflated (40% of drivers receive $0) and right-skewed by generous outliers, making the Central Limit Theorem unreliable at small audit sample sizes.

**Method: Manual Bootstrap Engine**
- Simulates an audit sample of 250 driver tips: 100 zero-tips + 150 draws from `Exponential(scale=5.0)`
- Resamples with replacement 10,000 times, computing the median on each resample
- Extracts the 95% Confidence Interval via `np.percentile` at the 2.5th and 97.5th quantiles

**Key insight:** The bootstrap CI is asymmetric — the lower arm is compressed toward $0 (hard floor from the zero-mass spike) while the upper arm is wider (exponential tail has no ceiling). A parametric CI would impose false symmetry and misrepresent the true uncertainty.

---

### Part 2 — The Algorithmic Routing Crash
**Business context:** The engineering division claims their new "Batch Routing" algorithm significantly reduces delivery times. An A/B test on 1,000 deliveries was conducted, but the treatment group contains extreme upper-bound outliers from software crash loops, violating the homoscedasticity assumption of a standard T-test.

**Method: Manual Permutation Test**
- Control group: `Normal(mean=35, sd=5)`, n=500
- Treatment group: `LogNormal(mean=3.4, sigma=0.4)`, n=500
- Concatenates all 1,000 deliveries, shuffles 5,000 times via `np.random.permutation`, and computes a simulated null distribution of mean differences
- Computes an exact empirical p-value: the proportion of permutations yielding a difference ≥ the observed difference

**Key insight:** Unlike a T-test, the permutation test makes zero distributional assumptions. It constructs the null distribution directly from the data, making it robust to the heteroscedasticity introduced by crash-loop outliers.

---

### Part 3 — The Loyalty Program Paradox
**Business context:** The marketing team claims SwiftPass premium subscribers spend 300% more per month, and requests a doubled acquisition budget. However, high-volume "power users" self-select into the program to save on cumulative delivery fees — a textbook case of Selection Bias.

**Method: Propensity Score Matching (PSM)**

The analysis proceeds in three steps:

**Step 3.1 — Naive SDO**
Computes the raw Simple Difference in Means between subscribers (`D=1`) and non-subscribers (`D=0`) on `post_spend`. This is the biased, unadjusted estimate.

**Step 3.2 — PSM Architecture**
- Estimates each user's propensity to subscribe using `LogisticRegression(solver='liblinear')` on pre-treatment covariates only: `pre_spend`, `account_age`, `support_tickets`
- Uses `NearestNeighbors(n_neighbors=1)` to match each subscriber to the single non-subscriber with the closest propensity score

**Step 3.3 — ATT & Love Plot**
- Computes the Average Treatment Effect on the Treated (ATT) using only the matched control group
- Generates a **Love Plot** (Standardized Mean Differences) to visually verify covariate balance before and after matching. All covariates falling within the ±0.1 SMD threshold band confirms that selection bias has been successfully mitigated

---

## Repository Structure

```
.
├── Econ_3916_Assignment_3_Causal.ipynb   # Main analysis notebook
├── swiftcart_loyalty.csv                 # Input dataset (Part 3)
└── README.md
```

---

## Dependencies

```python
numpy
pandas
scipy
matplotlib
seaborn
scikit-learn
```

Install all dependencies with:
```bash
pip install numpy pandas scipy matplotlib seaborn scikit-learn
```

---

## Methods Summary

| Part | Problem | Classical Failure | Method Used |
|------|---------|-------------------|-------------|
| 1 | Median tip CI | CLT breaks on zero-inflated data | Bootstrap (B=10,000) |
| 2 | A/B test on delivery times | Homoscedasticity violated by crash outliers | Permutation Test (B=5,000) |
| 3 | Loyalty program spend effect | Selection bias from power-user self-selection | Propensity Score Matching |

---

## Key Concepts

**Bootstrap CI Asymmetry** — When the sampling distribution of an estimator is non-Gaussian (as with medians on zero-inflated data), `np.percentile`-based CIs correctly capture the true shape of uncertainty, unlike symmetric parametric intervals.

**Permutation Test** — Constructs an empirical null distribution by randomly reassigning group labels. The p-value is the exact proportion of random permutations that produce a test statistic as extreme as the observed one.

**Selection Bias vs. Treatment Effect** — The Naive SDO conflates correlation with causation. PSM isolates the causal ATT by ensuring the treated and control groups are statistically comparable on all observable pre-treatment characteristics, making the assignment to treatment "as good as random" within matched pairs.

**Love Plot** — The standard diagnostic for PSM. Successful bias removal requires all covariates' post-matching SMD to fall within ±0.1 (Rubin, 2001).
