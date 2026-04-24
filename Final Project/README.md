# 🚲 Bike Sharing Demand Prediction

## ECON 3916: ML Prediction Project — Final Project (Spring 2026)

**Author:** Stephen Key  
**Date:** April 26, 2026

### Project Overview

This project predicts hourly bike rental demand in Washington D.C. using weather conditions, time-of-day, and calendar features. A Random Forest Regressor achieves R² = 0.94 with RMSE = 42, enabling bike-share operators to optimize hourly bike allocation.

**Stakeholder:** City transportation planners and bike-share operators (e.g., Capital Bikeshare) who need to decide how many bikes to deploy at each station for each hour.

### Live Dashboard

🔗 [https://econ3916-statistical-machine-learning-bike-demand-estimate.streamlit.app](https://econ3916-statistical-machine-learning-bike-demand-estimate.streamlit.app)

### Dataset

- **Source:** [UCI Bike Sharing Dataset](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset)
- **Observations:** 17,379 (hourly data, 2011–2012)
- **Features:** 11 (season, yr, mnth, hr, holiday, weekday, workingday, weathersit, temp, hum, windspeed)
- **Target:** `cnt` (total bike rentals per hour)

### Repository Structure

```
Final Project/
├── app.py                          # Streamlit dashboard
├── Data/
│   └── hour.csv                    # Dataset
├── ECON 3916: ML Prediction Project — Final Project - deliverble 1.ipynb  # Analysis notebook
└── README.md                       # This file
requirements.txt                    # Python dependencies (root directory)
```

### How to Reproduce

**1. Clone the repository:**
```bash
git clone https://github.com/stephenkeyy77/ECON3916-Statistical-Machine-Learning.git
cd ECON3916-Statistical-Machine-Learning/Final\ Project
```

**2. Install dependencies:**
```bash
pip install -r ../requirements.txt
```

**3. Run the Jupyter notebook:**
Open `ECON 3916: ML Prediction Project — Final Project - deliverble 1.ipynb` in Jupyter or Google Colab to see the full analysis pipeline (EDA, model training, evaluation).

**4. Launch the Streamlit app locally:**
```bash
streamlit run app.py
```
The app will open in your browser at `http://localhost:8501`.

### Model Performance

| Model | RMSE | MAE | R² |
|-------|------|-----|-----|
| Linear Regression (Baseline) | 139.44 | 104.98 | 0.39 |
| **Random Forest (Final)** | **42.10** | **24.68** | **0.94** |

**95% Bootstrap Confidence Intervals (Random Forest):**
- RMSE: [39.17, 45.16]
- MAE: [23.64, 25.83]
- R²: [0.9355, 0.9517]

### Key Findings

- **Hour of day** is the strongest predictor (~60% of feature importance), capturing commuter patterns
- **Temperature** is the second most important feature (~14%)
- Working days show a double-peak commuter pattern (8AM and 5-6PM); weekends show a single midday peak
- Feature importance is **predictive, not causal** — this model forecasts demand, it does not explain what causes people to ride bikes
