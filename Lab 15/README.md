The Polynomial Trap: Bias-Variance Tradeoff

The link of code: https://colab.research.google.com/drive/15p8-LhXXICOlGfOPiM5gdcfaRE0EyOdu?usp=sharing
This lab explores the central tension in predictive modeling — balancing model complexity against generalization — using both synthetic and real-world data.
On synthetic sine-wave data (n=50 training, n=200 test), I fit polynomial regressions of degree 1 through 15 and tracked training versus test RMSE across the complexity spectrum. The results illustrate the classic U-shaped test error curve: low-degree models underfit (high bias), while high-degree models overfit (high variance). The optimal range fell at degree 3–5, where test RMSE approached the irreducible noise floor. Five-fold cross-validation on the training set alone successfully identified this sweet spot, confirming CV as a reliable proxy for true out-of-sample performance when held-out test data is unavailable.
I then applied these principles to the Ames Housing dataset (1,460 observations, 80 features). A parsimonious 5-feature model selected by correlation ranking achieved lower CV RMSE than a kitchen-sink specification using all numeric predictors — demonstrating that more features do not guarantee better generalization, particularly when the additional variables introduce estimation noise that outweighs their marginal signal.
Tools: Python, NumPy, scikit-learn (PolynomialFeatures, LinearRegression, cross_val_score, KFold), Matplotlib
Concepts applied: bias-variance tradeoff, complexity curves, K-fold cross-validation, overfitting diagnostics, feature selection
