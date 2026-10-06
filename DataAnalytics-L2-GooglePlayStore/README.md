
---

# 3️⃣ `DataAnalytics-L2-GooglePlayStore/README.md`

```markdown
# OASIS INFOBYTE — Unveiling the Android App Market

## 📌 Project Overview

This project analyzes the Google Play Store ecosystem to understand app categories, ratings, installs, pricing, size, revenue potential, and user review sentiment.

The analysis combines app-level data with user review data to generate insights useful for mobile app developers and business decision-makers.

## 🎯 Objectives

- Load and analyze apps and reviews datasets separately.
- Clean missing values and duplicate records.
- Clean and transform installation and pricing data.
- Analyze app categories.
- Study app ratings.
- Analyze app size and installation relationships.
- Compare free and paid applications.
- Analyze paid app pricing.
- Estimate potential revenue.
- Perform sentiment analysis on user reviews.
- Compare sentiment across app categories.
- Generate actionable developer recommendations.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- TextBlob
- Scikit-learn
- Jupyter Notebook

## 📊 Analysis Performed

### 1. Data Loading

Two datasets are analyzed separately:

- Google Play Store Apps dataset
- Google Play Store Reviews dataset

### 2. Data Cleaning

The analysis includes:

- Missing-value handling
- Duplicate detection and removal
- Installation value cleaning
- Rating cleaning
- Price conversion
- App size processing

### 3. Category Analysis

App categories are analyzed to identify:

- Category distribution
- Most represented categories
- Category saturation

### 4. Rating Analysis

The project analyzes:

- Rating distribution
- Average rating by category
- Highest-rated categories

### 5. Size vs Installs

App size is compared with installation volume to understand whether larger applications attract more or fewer installs.

### 6. Free vs Paid Applications

Applications are classified as:

- Free
- Paid

The proportion of free and paid applications is analyzed.

### 7. Price and Revenue Analysis

Paid application prices are analyzed and potential category-level revenue is estimated using price and installation information.

### 8. Review Sentiment Analysis

User reviews are classified using sentiment analysis.

Sentiment categories include:

- Positive
- Neutral
- Negative

Sentiment distribution and sentiment by category are visualized.

## 🔍 Key Insights

| Insight | Result |
|---|---|
| Most saturated category | HEALTH_AND_FITNESS |
| Highest average-rated category | EDUCATION |
| Free apps share | 70.0% |

## 💡 Developer Recommendations

1. Study saturated categories carefully and differentiate the application around a clear user need.

2. Prioritize product quality and user retention because ratings and reviews can strongly influence adoption.

3. Validate monetization opportunities using installation volume, pricing, and category-level revenue potential before launching an application.

## 📁 Project Structure

```text
DataAnalytics-L2-GooglePlayStore/
│
├── Google_Play_Store_Analysis.py
├── Google_Play_Store_Analysis.ipynb
├── README.md
├── requirements.txt
│
├── dataset/
│   ├── apps_sample.csv
│   └── reviews_sample.csv
│
├── outputs/
│   ├── key_insights.csv
│   └── review_sentiment.csv
│
├── visualizations/
│   ├── average_rating_by_category.png
│   ├── category_distribution.png
│   ├── estimated_revenue_by_category.png
│   ├── free_vs_paid.png
│   ├── paid_price_distribution.png
│   ├── rating_distribution.png
│   ├── sentiment_by_category.png
│   ├── sentiment_distribution.png
│   └── size_vs_installs.png
│
└── screenshots/