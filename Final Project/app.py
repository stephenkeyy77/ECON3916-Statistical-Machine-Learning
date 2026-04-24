import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# ----------------------------
# Load Data & Train Model
# ----------------------------
@st.cache_resource
def load_and_train():
    url = 'https://raw.githubusercontent.com/stephenkeyy77/ECON3916-Statistical-Machine-Learning/refs/heads/main/Final%20Project/Data/hour.csv'
    df = pd.read_csv(url)
    
    # Feature engineering (same as notebook)
    X = df.drop(columns=['instant', 'dteday', 'casual', 'registered', 'cnt', 'atemp'])
    y = df['cnt']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    
    # Historical averages for the chart
    historical_avg = df.groupby('hr')['cnt'].mean()
    
    return model, historical_avg

model, historical_avg = load_and_train()

# ----------------------------
# App Title & Description
# ----------------------------
st.title("🚲 Bike Sharing Demand Prediction Dashboard")

st.markdown("""
This tool predicts **hourly bike rental demand** using a trained Random Forest model.

**Who is this for?**
- Bike-share operations managers
- City planners
- Logistics teams

**Why it matters:**
- Optimize bike allocation
- Reduce shortages/overcapacity
- Improve customer satisfaction

Adjust the inputs in the sidebar to simulate real-world conditions.
""")

# ----------------------------
# Sidebar Inputs (Real Units)
# ----------------------------
st.sidebar.header("Input Conditions")

hour = st.sidebar.slider("Hour of Day", 0, 23, 12)
temp = st.sidebar.slider("Temperature (°C)", -8, 39, 20)
humidity = st.sidebar.slider("Humidity (%)", 0, 100, 50)
windspeed = st.sidebar.slider("Wind Speed (km/h)", 0, 67, 10)

season = st.sidebar.selectbox("Season", ["Winter", "Spring", "Summer", "Fall"])
weather = st.sidebar.selectbox("Weather", ["Clear", "Mist", "Light Rain", "Heavy Rain"])
workingday = st.sidebar.selectbox("Working Day", ["Yes", "No"])

mnth = st.sidebar.slider("Month", 1, 12, 6)
weekday = st.sidebar.slider("Weekday (0=Sun)", 0, 6, 3)
holiday = st.sidebar.selectbox("Holiday", ["No", "Yes"])

# Fixed default
yr = 1  # assume 2012

# ----------------------------
# Feature Engineering
# ----------------------------

# Normalization using fixed constants from UCI documentation
temp_norm = (temp - (-8)) / (39 - (-8))
humidity_norm = humidity / 100
windspeed_norm = windspeed / 67

# Mappings
season_map = {"Winter": 1, "Spring": 2, "Summer": 3, "Fall": 4}
weather_map = {"Clear": 1, "Mist": 2, "Light Rain": 3, "Heavy Rain": 4}
workingday_map = {"Yes": 1, "No": 0}
holiday_map = {"Yes": 1, "No": 0}

# Build input dataframe (must match training feature order)
input_data = pd.DataFrame({
    "season": [season_map[season]],
    "yr": [yr],
    "mnth": [mnth],
    "hr": [hour],
    "holiday": [holiday_map[holiday]],
    "weekday": [weekday],
    "workingday": [workingday_map[workingday]],
    "weathersit": [weather_map[weather]],
    "temp": [temp_norm],
    "hum": [humidity_norm],
    "windspeed": [windspeed_norm]
})

# ----------------------------
# Prediction
# ----------------------------
prediction = model.predict(input_data)[0]
prediction = np.clip(prediction, 1, 977)

# ----------------------------
# Bootstrap Uncertainty (using individual trees)
# ----------------------------
all_preds = np.array([tree.predict(input_data)[0] for tree in model.estimators_])
lower = np.percentile(all_preds, 5)
upper = np.percentile(all_preds, 95)

# ----------------------------
# Display Metrics
# ----------------------------
st.subheader("📊 Prediction Output")

col1, col2, col3 = st.columns(3)
col1.metric("Predicted Demand", f"{prediction:.0f} bikes")
col2.metric("90% CI Lower", f"{lower:.0f} bikes")
col3.metric("90% CI Upper", f"{upper:.0f} bikes")

st.write(f"**Uncertainty Range (90% interval):** {lower:.0f} — {upper:.0f} bikes/hour")

# ----------------------------
# Interactive Visualization
# ----------------------------
st.subheader("📈 Demand vs. Time of Day")

fig, ax = plt.subplots(figsize=(10, 5))

# Historical average line
ax.plot(historical_avg.index, historical_avg.values, 'o-', color='steelblue', linewidth=2, label="Avg Historical Demand")

# User's prediction point
ax.scatter(hour, prediction, color='red', s=150, zorder=5, label=f"Your Prediction ({prediction:.0f})")

# Uncertainty band at the selected hour
ax.fill_between([hour - 0.3, hour + 0.3], lower, upper, color='red', alpha=0.2, label=f"90% Interval [{lower:.0f}, {upper:.0f}]")

ax.set_xlabel("Hour of Day", fontsize=12)
ax.set_ylabel("Bike Demand", fontsize=12)
ax.set_title("Hourly Bike Demand: Historical Average vs. Your Prediction", fontsize=14, fontweight='bold')
ax.set_xticks(range(0, 24))
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
st.pyplot(fig)

# ----------------------------
# Model Info
# ----------------------------
with st.expander("ℹ️ About This Model"):
    st.markdown("""
    - **Model:** Random Forest Regressor (200 trees)
    - **Test R²:** 0.9440 [0.9355, 0.9517]
    - **Test RMSE:** 42.10 [39.17, 45.16]
    - **Test MAE:** 24.68 [23.64, 25.83]
    - **Data:** UCI Bike Sharing Dataset (17,379 hourly observations, 2011–2012)
    - **Features:** 11 (season, yr, mnth, hr, holiday, weekday, workingday, weathersit, temp, hum, windspeed)
    
    ⚠️ **Caveat:** Feature importance is predictive, not causal. This model forecasts demand — it does not explain what causes people to ride bikes.
    """)

# ----------------------------
# Debug / Validation
# ----------------------------
with st.expander("🔍 Debug / Validation Checks"):
    st.write("Normalized Temperature:", round(temp_norm, 3))
    st.write("Expected: 20°C → ~0.596")
    st.write("Humidity (normalized):", round(humidity_norm, 3))
    st.write("Windspeed (normalized):", round(windspeed_norm, 3))
    st.write("Input Features:", input_data.to_dict())
    st.write("Prediction Range Enforced: 1–977")
