
---

# 2️⃣ `DataAnalytics-L1-CustomerSegmentation/README.md`

```markdown
# OASIS INFOBYTE — Customer Segmentation Analysis

## 📌 Project Overview

This project performs customer segmentation using RFM (Recency, Frequency, Monetary) analysis and K-Means clustering.

The objective is to identify groups of customers with similar purchasing behaviour and develop suitable marketing strategies for each customer segment.

## 🎯 Objectives

- Inspect and clean customer transaction data.
- Calculate Recency, Frequency, and Monetary values.
- Calculate average purchase value.
- Standardize customer behavioural features.
- Determine the appropriate number of clusters using the Elbow Method.
- Apply K-Means clustering.
- Visualize customer segments.
- Profile the identified customer groups.
- Develop marketing strategies for each segment.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

## 📊 Methodology

### 1. Data Inspection and Cleaning

The transaction dataset is inspected for:

- Missing values
- Data types
- Duplicate records
- Invalid transaction values

### 2. RFM Analysis

Three important customer behaviour metrics are calculated:

**Recency**

Measures how recently a customer made a purchase.

**Frequency**

Measures how frequently a customer makes purchases.

**Monetary**

Measures the total amount spent by a customer.

Average Purchase Value is also calculated to understand customer spending behaviour.

### 3. Feature Scaling

RFM features are standardized using `StandardScaler` so that variables with different numerical ranges can be compared fairly.

### 4. Elbow Method

The Elbow Method is used to evaluate different values of K and identify a suitable number of customer clusters.

### 5. K-Means Clustering

K-Means clustering is applied to group customers based on their purchasing behaviour.

### 6. Cluster Visualization

The customer segments are visualized using:

- Recency vs Monetary
- Frequency vs Monetary
- Customer count by cluster

### 7. Customer Profiling

Each cluster is analyzed using:

- Recency
- Frequency
- Monetary value
- Average purchase value

## 📈 RFM Summary

The analysis generated the following overall customer metrics:

| Metric | Result |
|---|---:|
| Customers | 494 |
| Average Recency | 70.46 |
| Average Frequency | 5.03 |
| Average Monetary Value | 1820.63 |
| Average Purchase Value | 357.93 |

## 👥 Customer Segments

The analysis identifies customer groups based on purchasing behaviour.

### High-Value / Loyal Customers

These customers show strong purchasing activity and high monetary value.

**Marketing Action:**
- VIP rewards
- Early access to products
- Cross-selling and personalized offers

### At-Risk High-Value Customers

Customers with valuable historical purchases but declining recent activity can be targeted for re-engagement.

**Marketing Action:**
- Personalized win-back campaigns
- Special offers
- Purchase reminders

### Regular / Growth Customers

These customers show moderate purchasing behaviour and can potentially become high-value customers.

**Marketing Action:**
- Product bundles
- Loyalty incentives
- Cross-selling

### Low-Engagement Customers

These customers have relatively low purchasing activity.

**Marketing Action:**
- Low-cost reactivation campaigns
- Introductory offers
- Personalized reminders

## 📁 Project Structure

```text
DataAnalytics-L1-CustomerSegmentation/
│
├── Customer_Segmentation.py
├── Customer_Segmentation.ipynb
├── README.md
├── requirements.txt
│
├── dataset/
│   └── online_retail.csv
│
├── outputs/
│   ├── cluster_counts.csv
│   ├── cluster_profile.csv
│   └── marketing_segments.csv
│
├── visualizations/
│   ├── cluster_customer_counts.png
│   ├── elbow_method.png
│   ├── frequency_monetary_clusters.png
│   └── recency_monetary_clusters.png
│
└── screenshots/