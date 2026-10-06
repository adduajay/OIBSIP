import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = "dataset/retail_sales.csv"
OUT = "visualizations"
os.makedirs(OUT, exist_ok=True)

# Load / generate a small reproducible dataset if no dataset is supplied.
if not os.path.exists(DATA_PATH):
    rng = np.random.default_rng(42)
    n = 1200
    dates = pd.date_range("2025-01-01", "2025-12-31", periods=n)
    categories = rng.choice(["Electronics","Clothing","Home","Beauty","Sports"], n, p=[.22,.28,.18,.17,.15])
    products = rng.choice(["Laptop","T-Shirt","Sofa","Skincare Kit","Running Shoes","Headphones","Jeans","Coffee Maker","Watch","Yoga Mat"], n)
    age = rng.integers(18, 66, n)
    gender = rng.choice(["Male","Female"], n)
    qty = rng.integers(1, 6, n)
    unit = np.round(rng.uniform(12, 450, n), 2)
    sales = np.round(qty*unit, 2)
    df0 = pd.DataFrame({"Date":dates,"Product":products,"Category":categories,"Age":age,"Gender":gender,"Quantity":qty,"Unit_Price":unit,"Sales":sales})
    df0.to_csv(DATA_PATH,index=False)
else:
    df0 = pd.read_csv(DATA_PATH)

df = df0.copy()
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
for c in ["Age","Quantity","Unit_Price","Sales"]: df[c]=pd.to_numeric(df[c],errors="coerce")
df = df.dropna(subset=["Date","Sales"])

print("Shape:", df.shape)
print("\nDtypes:\n", df.dtypes)
print("\nNulls:\n", df.isna().sum())
num=df.select_dtypes(include=np.number)
print("\nDescriptive statistics:\n", pd.DataFrame({"mean":num.mean(),"median":num.median(),"mode":num.mode().iloc[0],"std":num.std()}))

df["Month"] = df["Date"].dt.to_period("M").astype(str)
df["Quarter"] = df["Date"].dt.to_period("Q").astype(str)
df["Age_Group"] = pd.cut(df["Age"], bins=[17,24,34,44,54,100], labels=["18-24","25-34","35-44","45-54","55+"])

monthly=df.groupby("Month")["Sales"].sum()
plt.figure(figsize=(11,5)); monthly.plot(marker="o"); plt.title("Monthly Sales Trend"); plt.ylabel("Sales"); plt.xticks(rotation=45); plt.tight_layout(); plt.savefig(f"{OUT}/monthly_sales_trend.png",dpi=160); plt.close()
quarterly=df.groupby("Quarter")["Sales"].sum()
plt.figure(figsize=(9,5)); quarterly.plot(marker="o"); plt.title("Quarterly Sales Trend"); plt.ylabel("Sales"); plt.tight_layout(); plt.savefig(f"{OUT}/quarterly_sales_trend.png",dpi=160); plt.close()

plt.figure(figsize=(8,5)); df["Age_Group"].value_counts().sort_index().plot(kind="bar"); plt.title("Customer Age Group Distribution"); plt.xlabel("Age Group"); plt.ylabel("Customers"); plt.tight_layout(); plt.savefig(f"{OUT}/age_group_distribution.png",dpi=160); plt.close()
plt.figure(figsize=(6,5)); df["Gender"].value_counts().plot(kind="bar"); plt.title("Gender Breakdown"); plt.xlabel("Gender"); plt.ylabel("Customers"); plt.tight_layout(); plt.savefig(f"{OUT}/gender_distribution.png",dpi=160); plt.close()

top10=df.groupby("Product")["Quantity"].sum().nlargest(10).sort_values()
plt.figure(figsize=(9,5)); top10.plot(kind="barh"); plt.title("Top 10 Best-Selling Products"); plt.xlabel("Units Sold"); plt.tight_layout(); plt.savefig(f"{OUT}/top_10_products.png",dpi=160); plt.close()
rev=df.groupby("Category")["Sales"].sum().sort_values()
plt.figure(figsize=(9,5)); rev.plot(kind="barh"); plt.title("Revenue by Product Category"); plt.xlabel("Revenue"); plt.tight_layout(); plt.savefig(f"{OUT}/revenue_by_category.png",dpi=160); plt.close()

plt.figure(figsize=(8,6)); sns.heatmap(df[["Age","Quantity","Unit_Price","Sales"]].corr(),annot=True,cmap="coolwarm",fmt=".2f"); plt.title("Correlation Heatmap"); plt.tight_layout(); plt.savefig(f"{OUT}/correlation_heatmap.png",dpi=160); plt.close()

# Non-obvious insight: average order value by gender and category.
pivot=df.pivot_table(index="Category",columns="Gender",values="Sales",aggfunc="mean")
plt.figure(figsize=(9,5)); pivot.plot(kind="bar",ax=plt.gca()); plt.title("Average Sales by Category and Gender"); plt.ylabel("Average Sales"); plt.xticks(rotation=30); plt.tight_layout(); plt.savefig(f"{OUT}/additional_insight.png",dpi=160); plt.close()

summary=pd.DataFrame({"metric":["Total Revenue","Average Transaction","Total Units","Top Category","Top Product"],"value":[df.Sales.sum(),df.Sales.mean(),df.Quantity.sum(),rev.idxmax(),top10.idxmax()]})
summary.to_csv("outputs/eda_summary.csv",index=False)
print("\nKey findings:")
print(summary.to_string(index=False))
print("\nActionable recommendations:")
print("1. Prioritize inventory and promotions for the highest-revenue category.")
print("2. Use age/gender purchase patterns for targeted campaigns rather than one-size-fits-all offers.")
print("3. Monitor monthly/quarterly peaks and plan stock and marketing budgets ahead of high-demand periods.")
