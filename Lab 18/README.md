# Fraud Detection Model Evaluation — Metrics that Matter

## Objective

Evaluate a logistic regression fraud classifier beyond headline accuracy by deploying confusion matrices, Precision-Recall analysis, ROC/PR-AUC curves, threshold optimization, and a capacity-constrained operating-point selection on the severely imbalanced Kaggle Credit Card Fraud dataset (284,807 transactions, 0.172% positive class).

## Methodology

- **Data & preprocessing:** Loaded 284,807 European credit card transactions with PCA-anonymized features V1–V28, scaled the raw `Amount` feature via `StandardScaler`, dropped `Time`, and performed a stratified 80/20 train-test split to preserve the 0.172% fraud prevalence in both sets.
- **Accuracy paradox baseline:** Constructed a naïve all-negative classifier to demonstrate that predicting "not fraud" for every transaction yields 99.83% accuracy with zero fraud recall — a textbook illustration of why accuracy is misleading under extreme class imbalance.
- **Logistic regression training:** Fit `sklearn.linear_model.LogisticRegression` on the training set and extracted predicted fraud probabilities P(Class = 1 | X) for threshold analysis.
- **Confusion matrix & classification report:** Computed TP, FP, FN, TN at the default τ = 0.5 threshold; reported per-class Precision, Recall, and F1-Score to isolate fraud-class performance from the majority-class noise.
- **ROC & Precision-Recall curves:** Plotted the full ROC curve (FPR vs. TPR) with AUC as a threshold-free discrimination summary, then plotted the Precision-Recall curve with PR-AUC — a more informative metric when the positive class is rare, since it is not inflated by the massive True Negative count.
- **Multi-threshold comparison:** Evaluated confusion matrices side by side at τ ∈ {0.5, 0.3, 0.1} to visualize the precision-recall tradeoff as the decision boundary shifts.
- **F1-optimal threshold search:** Swept τ from 0.01 to 0.99 and identified the threshold that maximizes the fraud-class F1-Score, showing that the optimal operating point deviates substantially from the default 0.5.
- **Capacity-constrained threshold selection:** Simulated a real-world constraint (≤ 500 daily investigations) by finding the lowest threshold at which total flagged transactions stay within budget, then reported the achievable Recall at that operating point.

## Key Findings

- **Accuracy paradox confirmed:** A zero-skill baseline achieves 99.83% accuracy but detects no fraud, underscoring that accuracy is an unreliable metric for imbalanced classification.
- **Strong discrimination:** The logistic regression model achieved high ROC-AUC, confirming that it ranks most fraudulent transactions above most legitimate ones in predicted probability.
- **PR-AUC as the harder test:** The Precision-Recall curve revealed that maintaining high Precision while pushing Recall upward is substantially more difficult than the ROC curve suggests — a direct consequence of the 0.172% base rate diluting the FPR denominator.
- **Threshold ≠ 0.5:** The F1-maximizing threshold was well below the default 0.5, reflecting the asymmetry inherent in fraud detection — missing a fraud is costlier than a false alarm.
- **Business-relevant operating point:** Under the 500-investigation capacity constraint, the selected threshold achieved meaningful Recall while respecting operational limits, demonstrating that model deployment decisions are ultimately driven by business context rather than a single summary statistic.

## Tech Stack

Python · pandas · NumPy · scikit-learn (LogisticRegression, confusion_matrix, classification_report, roc_curve, roc_auc_score, precision_recall_curve, auc, f1_score, precision_score, recall_score) · Matplotlib · Seaborn
