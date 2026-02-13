# Audit 02: Deconstructing Statistical Lies

## Overview
This analysis investigates three common statistical pitfalls that can distort decision-making in real-world scenarios: latency skew detection, false positive rates in fraud detection, and survivorship bias in financial markets.

## 1. Latency Skew: MAD vs. Standard Deviation

### Context
Network latency monitoring with 1,000 observations: 980 normal requests (20-50ms) and 20 traffic spikes (1,000-5,000ms).

### Key Finding
**MAD (Median Absolute Deviation) remains robust while Standard Deviation explodes:**
- MAD: 8.0ms
- SD: 487.68ms

### Why This Matters
Standard deviation uses squared deviations from the mean, causing extreme outliers to disproportionately inflate the metric. The 20 spike latencies contribute massive squared errors that dominate the variance calculation. In contrast, MAD operates on the median of absolute deviations—with 98% of data points in the normal range, the median barely shifts.

**Practical Implication:** For monitoring systems prone to occasional spikes, MAD provides a more stable baseline for anomaly detection. SD-based alerts would trigger constantly, while MAD-based thresholds correctly identify true operational issues.

## 2. False Positives: The Base Rate Fallacy

### Context
Anti-cheating system with 98% sensitivity and 98% specificity tested across three academic environments with different cheating prevalence rates.

### Results

| Scenario | Prior P(Cheater) | P(Cheater \| Flagged) |
|----------|------------------|----------------------|
| **A: Bootcamp** | 50% | **98.0%** |
| **B: Econ Class** | 5% | **72.1%** |
| **C: Honors Seminar** | 0.1% | **4.7%** |

### Key Insight
Even with 98% accuracy metrics, the **base rate** (prior probability) dramatically affects post-test confidence. In the honors seminar scenario, a flagged student has only a 4.7% chance of actually cheating—meaning 95.3% of flags are false positives.

**Bayesian Formula Applied:**
```
P(Cheater | Flagged) = [P(Flagged | Cheater) × P(Cheater)] / P(Flagged)
```

**Policy Recommendation:** High-stakes decisions (academic penalties, account bans) require context-aware thresholds. Systems deployed in low-prevalence environments need additional verification layers to avoid massive false positive rates.

## 3. Survivorship Bias: The Graveyard Hypothesis

### Context
Simulation of 10,000 cryptocurrency tokens with Pareto-distributed peak market caps (α = 2.0), comparing all tokens versus top 1% survivors.

### Results
- **Mean peak market cap (All tokens):** $1,974,417.82
- **Mean peak market cap (Top 1% survivors):** $18,479,749.42
- **Multiplier effect:** 9.36×

### Visualization Insight
The linear-scale histogram shows an extreme spike near zero—most tokens barely register. The log-scale histogram reveals the heavy-tailed distribution: 99% of tokens achieve minimal market caps while a tiny fraction captures enormous value.

### Economic Interpretation
This demonstrates why **survivor-only analyses grossly overestimate expected returns**. Media coverage, case studies, and investment pitches naturally focus on winners (the top 1%), but the "graveyard" of failed projects represents the modal outcome. An investor evaluating "average crypto returns" based on visible success stories would overestimate returns by nearly 10×.

**Application Beyond Crypto:** This bias affects startup ecosystems, hedge fund performance data (defunct funds aren't reported), and mutual fund rankings (poor performers are merged or closed).

## Technical Implementation

### Sample Ratio Mismatch (SRM) Test
Chi-square test for A/B experiment validity:
```python
observed = [50,250, 49,750]
expected = [50,000, 50,000]
χ² = 2.5 (threshold: 3.84)
```
**Verdict:** Experiment valid—no detectable engineering bias in traffic allocation.

## Methodological Notes

**MAD Calculation:** Implemented from scratch without NumPy shortcuts to demonstrate the algorithm: compute median, calculate absolute deviations, return median of deviations.

**Pareto Distribution:** Power-law model (α = 2.0) generates realistic heavy-tailed outcomes. Lower α values (1.5-1.8) produce even more extreme winner-take-all dynamics.

## Key Takeaways

1. **Metric Selection Matters:** Choose robust statistics (MAD) over traditional ones (SD) when dealing with heavy-tailed distributions or outlier-prone data.

2. **Context Shapes Interpretation:** Statistical accuracy metrics (sensitivity/specificity) mean nothing without base rates. Always apply Bayes' theorem in diagnostic contexts.

3. **Survivorship Bias is Invisible:** The most dangerous statistical lie is the one created by missing data. Always ask: "What am I not seeing?"

---

**Course:** ECON 3916 - Statistical & Machine Learning for Economics  
**Tools Used:** Python (NumPy, Pandas, Matplotlib, Seaborn)  
**Concepts Demonstrated:** Robust statistics, Bayesian inference, power-law distributions, experimental validity testing
