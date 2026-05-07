# 📊 RFM Customer Segmentation Analysis

> Advanced customer segmentation using RFM scoring, K-Means clustering,
> and an interactive Streamlit dashboard — built on 1M+ real retail transactions.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.8-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Status](https://img.shields.io/badge/Status-Complete-green)

---

## 🎯 Project Overview

This project performs end-to-end customer segmentation on the
**UCI Online Retail II dataset** (~1 million transactions, 2009–2011).

The goal: identify distinct customer groups based on their purchase behaviour
and generate actionable business recommendations for each segment.

---

## 🏗️ Project Structure

```
rfm-analysis/
├── data/
│   ├── raw/                    # Original UCI dataset (not tracked)
│   └── processed/              # Cleaned data & RFM scores
├── notebooks/
│   ├── 01_eda.ipynb            # Exploratory data analysis
│   ├── 02_cleaning.ipynb       # Data cleaning pipeline
│   ├── 03_rfm_scoring.ipynb    # RFM calculation & scoring
│   ├── 04_clustering.ipynb     # K-Means clustering
│   ├── 05_insights_storytelling.ipynb  # Business insights
│   └── 07_report_generator.ipynb      # Automated HTML report
├── src/
│   ├── cleaning.py             # Reusable cleaning pipeline
│   ├── rfm.py                  # RFM scoring module
│   ├── segmentation.py         # K-Means clustering module
│   └── report_generator.py     # Report generation module
├── dashboard/
│   └── app.py                  # Streamlit interactive dashboard
├── reports/
│   ├── rfm_report.html         # Auto-generated HTML report
│   └── *.png                   # All visualizations
├── requirements.txt
└── README.md
```

---

## 🔬 Methodology

### 1. Data Cleaning
- Loaded **1,067,371** raw transactions across 2 years
- Removed missing Customer IDs (22.77%), duplicates (3.22%),
  cancellations (1.83%), and invalid prices/quantities
- Final clean dataset: **~750,000+ valid transactions**

### 2. RFM Scoring
- **Recency** — days since last purchase
- **Frequency** — number of unique invoices
- **Monetary** — total revenue generated
- Quantile-based scoring (1–5 scale) with Winsorization for outliers

### 3. Customer Segmentation
- Rule-based segmentation → 10 business segments
- K-Means clustering with elbow method + silhouette score validation
- PCA visualization of clusters in 2D and 3D RFM space

### 4. Business Insights
- Pareto analysis — revenue concentration
- Segment profiling with actionable recommendations
- Cohort revenue heatmap showing seasonality
- RFM correlation matrix

---

## 📊 Key Findings

| Segment | Action Priority |
|---|---|
| Champions | Reward & retain — highest value |
| Loyal Customers | Upsell to Champions |
| At Risk | Immediate win-back campaign |
| Cannot Lose Them | Personal outreach within 30 days |
| Lost | Low-cost re-engagement or sunset |

---

## 💡 Business Recommendations

| Segment | Action | Metric to Track |
|---|---|---|
| **Champions** | VIP rewards, early product access | Retention rate |
| **Loyal Customers** | Upsell campaigns, loyalty tiers | Upgrade rate |
| **At Risk** | Win-back emails + discount | Reactivation rate |
| **Cannot Lose Them** | Personal outreach immediately | Recovery rate |
| **Lost** | Low-cost email or sunset | Cost per reactivation |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.14 | Core language |
| Pandas | Data manipulation |
| NumPy | Numerical computing |
| Scikit-learn | K-Means clustering, PCA, scaling |
| Matplotlib / Seaborn | Static visualizations |
| Plotly | Interactive charts |
| Streamlit | Interactive dashboard |
| Jupyter | Analysis notebooks |

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/Dallenrich/RFM-analysis.git
cd RFM-analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download dataset
Download from [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
and place `online_retail_II.xlsx` in `data/raw/`

### 4. Run notebooks in order
```
01_eda → 02_cleaning → 03_rfm_scoring → 04_clustering → 05_insights
```

### 5. Launch dashboard
```bash
streamlit run dashboard/app.py
```

---

## 🌐 Live Demo

👉 **[Live Streamlit Dashboard](https://rfm-analysis-46m5xy4bhkcrftbuau5al9.streamlit.app)**

---

## 📁 Dataset

- **Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
- **Period:** December 2009 – December 2011
- **Records:** 1,067,371 transactions
- **Countries:** 40+
- **Features:** Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country

---

## 👤 Author

**Dallenrich**
- GitHub: [@Dallenrich](https://github.com/Dallenrich)

---

*Built as a portfolio project demonstrating end-to-end data analytics
from raw data to business insights.*