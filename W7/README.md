# Week 7 — Customer Segmentation via Clustering
**Fusemachines AI Fellowship 2026 | Phase 2**

## Overview
End-to-end clustering pipeline on the [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii) dataset (~500k transactions → 4 customer segments).

## Setup
```bash
pip install pandas numpy scikit-learn scipy matplotlib seaborn openpyxl
```
Place `online_retail_II.xlsx` in the same directory as the notebook, then **Run All**.

## Pipeline
```
Raw transactions → Clean → RFM + extended features → Scale → Cluster → Validate → Business narrative
```

| Step | Decision | Reason |
|------|----------|--------|
| Outlier handling | Winsorize at P99 | Keeps VIP customers, limits distance distortion |
| Scaler | RobustScaler | RFM data is right-skewed; median/IQR > mean/std |
| K selection | k = 4 | Elbow + silhouette agree; maps to Champion/Loyal/At-Risk/New |
| Best method | K-Means (k-means++) | Stable, scalable, interpretable centroids |

## Features Engineered
- **Recency** — days since last purchase  
- **Frequency** — unique invoice count  
- **Monetary** — total spend  
- **AvgBasketSize** — revenue per invoice  
- **UniqueProducts** — catalog breadth  
- **AvgPurchaseGap** — mean days between orders  
- **ReturnRate** — cancelled / total quantity  

## Segments Found

| Cluster | Name | RFM Pattern | Action |
|---------|------|-------------|--------|
| A | Champion | Low R, High F, High M | VIP rewards |
| B | Loyal Regular | Mid across all | Cross-sell bundles |
| C | At-Risk | High R, Low F, Low M | Win-back + discount |
| D | New/One-Time | Very Low F, Low M | Onboarding nurture |

## Key Findings
- K-Means and Ward hierarchical clustering independently produced the same 4-cluster structure — strong evidence these segments are real.
- DBSCAN "noise" customers had the *highest* monetary value — flag as VIP, not outliers.
- k-means++ initialization reduced inertia variance across runs vs random init.

## Structure
```
Week_7_Clustering_Assignment_Complete_Solution.ipynb
├── Section 0  — Environment setup
├── Section 1  — Data loading & first look
├── Section 2  — Data cleaning
├── Section 3  — Feature engineering
├── Section 4  — Preprocessing (outliers + scaling)
├── Section 5  — K-Means clustering
├── Section 6  — Hierarchical clustering
├── Section 7  — DBSCAN clustering
├── Section 8  — Cluster validation & comparison
├── Section 9  — Business narrative
├── Section 10 — Failure log (4 entries)
└── Section 11 — K-Means from scratch (extension)
```

## Author
Swopnim Ghimire | Kathmandu University 
