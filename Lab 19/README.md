# Random Forest vs. OLS — California Housing

## Objective

Compare a single decision tree, Ridge regression, and Random Forest on the California Housing dataset (20,640 observations, 8 features) to quantify the predictive gains from ensemble non-linear modeling, then tune hyperparameters via cross-validation and interpret feature importance through both MDI and permutation methods.

## Methodology

- **Data & setup:** Loaded the scikit-learn California Housing dataset with 8 features (MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude) and performed a stratified 80/20 train-test split with a fixed random seed for reproducibility.
- **Three-model comparison:** Trained an unrestricted Decision Tree (high variance baseline), Ridge Regression (linear, high bias baseline), and a 100-tree Random Forest on the same split, then compared Train/Test RMSE and R² to map each model onto the bias-variance tradeoff.
- **Feature importance analysis:** Extracted MDI (Mean Decrease in Impurity) importance from the trained Random Forest and computed permutation importance on the test set, then compared rankings to identify where the two methods agree and diverge — particularly around high-cardinality features like Latitude and Longitude.
- **Hyperparameter tuning:** Ran GridSearchCV over `n_estimators` ∈ {50, 100, 200}, `max_depth` ∈ {10, 20, None}, and `max_features` ∈ {sqrt, 0.5, None} with 5-fold cross-validation, selecting the configuration that minimized CV RMSE.
- **Classification extension:** Created a binary target (price > median) and compared a Random Forest classifier against Logistic Regression using ROC-AUC, demonstrating the RF's superior discrimination on non-linear decision boundaries.
- **Partial dependence plots:** Visualized the marginal effect of MedInc and AveOccup on predicted housing prices, revealing non-linear relationships that Ridge regression structurally cannot capture.

## Key Findings

- **Bias-variance tradeoff in action:** The single Decision Tree achieved a perfect Train R² of 1.0 but only 0.6221 on test data (severe overfitting), Ridge scored a modest 0.5759 test R² (underfitting due to linearity), and the Random Forest landed at 0.8051 — the best bias-variance tradeoff of the three.
- **Non-linearity confirmed:** The RF's substantial advantage over Ridge (R² 0.8051 vs. 0.5759) indicates that the feature-price relationship is fundamentally non-linear, corroborated by the partial dependence plots showing diminishing returns in MedInc and a sharp threshold effect in AveOccup.
- **Feature importance divergence:** Both MDI and permutation methods agreed that MedInc dominates, but MDI overstated Latitude/Longitude importance due to their high cardinality providing more split opportunities — a known bias in Gini-based importance.
- **Tuning yields modest gains:** GridSearchCV selected `{n_estimators: 200, max_depth: None, max_features: sqrt}`, improving Test RMSE from 0.5053 → 0.4921 and Test R² from 0.8051 → 0.8152 — confirming that the ensemble structure drives most of the performance, not hyperparameter tuning.
- **Classification:** The RF classifier (AUC = 0.9611) substantially outperformed Logistic Regression (AUC = 0.9010), a practically significant 6-point gap attributable to the RF's ability to model non-linear decision boundaries.

## Tech Stack

Python · NumPy · pandas · Matplotlib · scikit-learn (DecisionTreeRegressor, Ridge, RandomForestRegressor, RandomForestClassifier, GridSearchCV, PartialDependenceDisplay, permutation_importance)
