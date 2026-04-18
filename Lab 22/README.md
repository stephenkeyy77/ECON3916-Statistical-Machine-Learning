# Clustering World Economies with K-Means & PCA

## Objective

This project applies unsupervised machine learning to classify ~259 countries into development tiers using 10 World Bank indicators, evaluating whether data-driven clustering can recover the World Bank's expert-defined income group taxonomy.

## Methodology

- Retrieved 10 World Development Indicators via the `wbgapi` Python package, covering income (GDP per capita PPP), health (life expectancy, infant mortality, health expenditure per capita), education (primary enrollment), connectivity (internet usage), trade openness (trade % of GDP), labor markets (unemployment rate), urbanization, and demographics (population growth).
- Standardized all features using `StandardScaler` to ensure equal contribution to Euclidean distance calculations in K-Means, preventing high-magnitude variables like GDP per capita from dominating the clustering.
- Fit K-Means with K=4 to mirror the World Bank's four income classifications (Low, Lower-Middle, Upper-Middle, High) and projected the 10-dimensional feature space to 2D using Principal Component Analysis (PCA) for visualization.
- Conducted elbow method (WCSS) and silhouette analysis across K=2 through K=10 to evaluate optimal cluster count.
- Cross-tabulated algorithmic cluster assignments against official World Bank income groups using a confusion-matrix-style heatmap to assess alignment.
- Extended the pipeline to California Housing census tract data (~20,640 tracts, 8 features), applying the same standardization → K-Means → PCA workflow.

## Key Findings

- **High-income economies are the most distinct cluster.** Cluster 0 mapped perfectly to the World Bank's High-income group (46 out of 46 countries), indicating that wealthy nations form a tight, well-separated group in the feature space.
- **Middle-income boundaries are blurry.** Upper-Middle and Lower-Middle income countries showed significant overlap across clusters, suggesting that development is a continuum rather than a set of discrete categories — a finding consistent with development economics literature.
- **Low-income countries cluster cleanly.** The algorithm reliably grouped Low-income economies together, though some were merged with Lower-Middle-income nations.
- **Silhouette analysis** suggested K=2 as the statistically optimal split, but K=4 provides more economically interpretable groupings aligned with established policy frameworks.
- **California Housing extension:** K=2 produced a primarily geographic split (Southern vs. Northern California) rather than an economically meaningful segmentation, highlighting that geographic features can dominate clustering when latitude and longitude are included.

## Tools & Libraries

Python · pandas · NumPy · scikit-learn (KMeans, PCA, StandardScaler, silhouette_score) · wbgapi · matplotlib · seaborn
