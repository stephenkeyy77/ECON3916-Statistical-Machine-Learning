# FedSpeak Analysis — NLP on FOMC Minutes

## Objective

This project applies natural language processing techniques to 26 years of Federal Open Market Committee (FOMC) meeting minutes to quantify shifts in monetary policy sentiment and identify distinct communication regimes across major macroeconomic events.

## Methodology

- Loaded 462 FOMC documents (statements and minutes) spanning February 2000 to March 2026 via the HuggingFace `vtasca/fomc-statements-minutes` dataset
- Preprocessed raw text through a five-stage NLP pipeline: lowercasing, non-alphabetic character removal, tokenization (NLTK), stop word filtering, and WordNet lemmatization
- Constructed a TF-IDF document-term matrix (462 × 5,000) with unigram and bigram features, applying minimum document frequency (5) and maximum document frequency (85%) thresholds to filter noise
- Computed document-level sentiment scores using a simplified Loughran-McDonald financial dictionary, measuring net sentiment (positive − negative word share) and uncertainty (hedging language share)
- Visualized sentiment and uncertainty time series with 12-month rolling averages, annotated against key policy events (Lehman collapse, Taper Tantrum, COVID-19, 2022 tightening cycle)
- Reduced the TF-IDF feature space to 50 dimensions via Truncated SVD (77.8% variance retained), then applied K-Means clustering (K=3) to discover latent language regimes
- Evaluated cluster quality with silhouette score and projected clusters into 2D PCA space for visualization
- Conducted a comparative distributional analysis of pre-COVID vs. post-COVID sentiment patterns

## Key Findings

- **Sentiment tracks macroeconomic conditions:** Net sentiment dropped sharply during the 2008 financial crisis and again following COVID-19, with the most negative document corresponding to the December 2025 meeting and the most positive to September 2012 (QE3 announcement).
- **Uncertainty reflects communication strategy:** Uncertainty language was highest in early 2000s documents, declined during the post-GFC forward guidance era as the Fed adopted more decisive language, and rose again post-2020 amid inflation and policy rate uncertainty.
- **Three distinct language regimes emerged from K-Means clustering:** Cluster 0 (81 documents, 2000–2010) captured crisis-era vocabulary; Cluster 1 (240 documents, spanning the full period) represented the Fed's default policy-normalization language; Cluster 2 (141 documents, 2009–2026) corresponded to accommodative and pandemic-response communication. Silhouette score: 0.242.
- **Post-COVID sentiment shift:** Mean net sentiment declined approximately 70% from 0.0101 (pre-COVID) to 0.0030 (post-COVID), while uncertainty remained stable (0.0216 vs. 0.0227), indicating the Fed adopted a more negative tone without substantially increasing hedging language.
