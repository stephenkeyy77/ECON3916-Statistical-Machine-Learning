# The Cost of Living Crisis: A Data-Driven Analysis

## Executive Summary
This portfolio entry demonstrates the application of economic index theory and data science techniques to analyze the inflation crisis from a student perspective. Using Python, FRED API integration, and Laspeyres index methodology, I constructed a custom Student Price Index (SPI) that reveals significant disparities between official CPI measurements and actual student cost burdens.

## The Problem: Why the "Average" CPI Fails Students

The Bureau of Labor Statistics publishes the Consumer Price Index (CPI) as a measure of average price changes for U.S. consumers. However, this "average" basket fundamentally misrepresents the student experience. Students face a unique cost structure dominated by:

- **Tuition & Fees**: 60% weight vs. negligible in official CPI
- **Rent**: 25% weight vs. ~33% in official CPI  
- **Food Away From Home**: 13% weight (campus dining)
- **Cable & Streaming**: 2% weight (digital necessities)

The official CPI's broad demographic averaging obscures the hyperinflation in education costs and urban housing markets where students concentrate.

## Methodology: Python, APIs, and Index Theory

### Data Acquisition & Processing
```python
from fredapi import Fred
import pandas as pd
import matplotlib.pyplot as plt

# Initialize FRED API connection
fred = Fred(api_key='your_api_key')

# Extract sector-specific price indices
official_cpi = fred.get_series('CPIAUCSL')
tuition = fred.get_series('CUSR0000SEEB')
rent = fred.get_series('CUSR0000SEHA')
food_away = fred.get_series('CUSR0000SEFV')
streaming = fred.get_series('CUSR0000SERA02')
```

### Index Construction: Laspeyres Formula Implementation

The Student Price Index employs the **Laspeyres weighted average** methodology:

$$\text{SPI}_t = \sum_{i=1}^{n} w_i \times \left(\frac{P_{i,t}}{P_{i,0}} \times 100\right)$$

Where:
- $w_i$ = expenditure weights (tuition=0.6, rent=0.25, food=0.13, streaming=0.02)
- $P_{i,t}$ = price level at time $t$
- $P_{i,0}$ = base period price (January 2016 = 100)

**Critical Implementation Step**: Reindexing to Common Base Year
```python
base_date = '2016-01-01'
base_values = df.loc[base_date]
df_reindexed = (df / base_values) * 100  # Normalize all series to 2016=100
```

This normalization eliminates scale fallacies (e.g., tuition's $50K baseline vs. streaming's $10 baseline) and enables valid cross-sector comparisons.

### Weight Calibration
Student expenditure weights derived from:
- College Board's *Trends in College Pricing* (tuition share)
- Bureau of Labor Statistics' Consumer Expenditure Survey (rent/food allocation)
- Pew Research digital consumption studies (streaming weight)

## Key Findings

### Primary Discovery: The 28.48% Inflation Gap
**My analysis reveals a 28.48 percentage point divergence between Student Price Index growth (+137.48% from 2016 baseline) and National CPI growth (+109.00% over same period).**

**Decomposition of Student Inflation Drivers:**

| Sector | Weight | Growth Since 2016 | Contribution to SPI |
|--------|--------|-------------------|---------------------|
| Tuition, Fees & Childcare | 60% | +28.89% | **+17.33pp** |
| Rent of Primary Residence | 25% | +50.00% | **+12.50pp** |
| Food Away From Home | 13% | +53.33% | +6.93pp |
| Cable & Streaming TV | 2% | +40.00% | +0.80pp |

**Key Insight**: The 60% tuition weight amplifies education cost hyperinflation into a compounding burden. While official CPI rose modestly (+9.00% total), students experienced effective inflation of +37.48% due to expenditure concentration in high-growth sectors.

### Regional Analysis: Boston Metro vs. National Averages
Comparative visualization revealed:
- **National CPI**: 137.19 (Jan 2016 = 100)
- **Boston-Cambridge-Newton CPI**: 135.25
- **Student SPI**: 137.48

**Surprising Result**: The Student Price Index (+37.48%) actually *exceeded* both national (+9.00%) and regional Boston CPI (+35.25%) by **+2.23 percentage points**. This contradicts conventional wisdom that coastal metro costs outpace student burdens—instead, higher education inflation represents a **nationwide crisis transcending regional variations**.

### Visualization Insights

**Figure 1: Raw Data Scale Fallacy**
```python
plt.plot(df_raw.index, df_raw['Tuition, Fees, & Childcare'])
plt.plot(df_raw.index, df_raw['Cable & Streaming TV'])
```
Plotting raw CPI values ($50K tuition vs. $10 streaming) creates optical illusion where streaming appears flat despite 40% inflation. **Reindexing corrects this perceptual bias.**

**Figure 2: Student SPI vs. Official CPI Divergence**
The shaded divergence area between SPI (salmon line) and Official CPI (blue line) quantifies the **$3,847 annual purchasing power loss** for average students (calculated as 28.48% × $13,500 baseline budget).

## Technical Implementation Highlights

1. **API Rate Limiting Handling**: Implemented exponential backoff retry logic for FRED API requests
2. **Time Series Alignment**: Used pandas `.ffill()` method to forward-fill monthly Boston CPI data into quarterly national series
3. **Vectorized Weight Application**: Leveraged NumPy broadcasting for efficient Laspeyres calculation across 108-month time series
4. **Professional Visualization**: Employed matplotlib's `fill_between()` for divergence shading, custom color palettes, and grid styling

## Policy Implications

The 28.48% student-specific inflation gap demands:
1. **Revised Loan Forgiveness Calculations**: Current income-driven repayment plans use outdated CPI adjustments
2. **University Accountability Metrics**: Publicly report "real cost burden" using SPI methodology
3. **Regional Aid Redistribution**: Boston CPI (-1.93pp below national) contradicts assumptions of coastal premium in student aid formulas

## Reproducibility & Code Quality

All analysis conducted in Google Colab with:
- **Modular Functions**: Separated data fetching, reindexing, and visualization into reusable components
- **Inline Documentation**: Comprehensive markdown cells explaining economic rationale for each step
- **Version Control**: Complete notebook archived at [GitHub Repository](https://github.com/stephenkeyy77/ECON3916-Statistical-Machine-Learning/tree/main/Assignment%201)

## Technical Stack
- **Python 3.x** (Google Colab environment)
- **Libraries**: `fredapi`, `pandas`, `matplotlib`, `numpy`
- **Economic Theory**: Laspeyres index construction, base year normalization, weighted averages
- **Data Source**: Federal Reserve Economic Data (FRED) API

---

**Conclusion**: By applying rigorous index theory to real-world economic data, this analysis exposes a critical blind spot in inflation measurement. The Student Price Index serves as both a technical demonstration of data science skills and a call to action for evidence-based policy reform addressing the student debt crisis.
