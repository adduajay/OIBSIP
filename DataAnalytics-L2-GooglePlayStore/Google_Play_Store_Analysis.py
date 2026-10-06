import os, re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
try:
    from textblob import TextBlob
except Exception:
    TextBlob=None

APP_PATH="dataset/apps_sample.csv"; REV_PATH="dataset/reviews_sample.csv"; OUT="visualizations"; os.makedirs(OUT,exist_ok=True)
apps=pd.read_csv(APP_PATH); reviews=pd.read_csv(REV_PATH)
apps=apps.drop_duplicates(subset="App").copy()
apps["Rating"]=pd.to_numeric(apps["Rating"],errors="coerce")
apps["Reviews"]=pd.to_numeric(apps["Reviews"],errors="coerce")
apps["Size_MB"]=apps["Size"].astype(str).str.extract(r"([0-9.]+)")[0].astype(float)
apps["Installs_num"]=apps["Installs"].astype(str).str.replace(",","",regex=False).str.replace("+","",regex=False).astype(float)
apps["Price_num"]=apps["Price"].astype(str).str.replace("$","",regex=False).astype(float)

plt.figure(figsize=(10,6)); apps["Category"].value_counts().sort_values().plot(kind="barh"); plt.title("Apps by Category"); plt.xlabel("Number of Apps"); plt.tight_layout(); plt.savefig(f"{OUT}/category_distribution.png",dpi=160); plt.close()
plt.figure(figsize=(8,5)); apps["Rating"].dropna().plot(kind="hist",bins=10); plt.title("Distribution of App Ratings"); plt.xlabel("Rating"); plt.tight_layout(); plt.savefig(f"{OUT}/rating_distribution.png",dpi=160); plt.close()
cat_rating=apps.groupby("Category")["Rating"].mean().sort_values()
plt.figure(figsize=(10,6)); cat_rating.plot(kind="barh"); plt.title("Average Rating by Category"); plt.xlabel("Average Rating"); plt.tight_layout(); plt.savefig(f"{OUT}/average_rating_by_category.png",dpi=160); plt.close()
plt.figure(figsize=(8,6)); sns.scatterplot(data=apps,x="Size_MB",y="Installs_num",hue="Type"); plt.title("App Size vs Installs"); plt.tight_layout(); plt.savefig(f"{OUT}/size_vs_installs.png",dpi=160); plt.close()

plt.figure(figsize=(6,5)); apps["Type"].value_counts().plot(kind="bar"); plt.title("Free vs Paid Apps"); plt.ylabel("Apps"); plt.tight_layout(); plt.savefig(f"{OUT}/free_vs_paid.png",dpi=160); plt.close()
paid=apps[apps.Type=="Paid"].copy(); plt.figure(figsize=(7,5)); paid["Price_num"].plot(kind="hist",bins=8); plt.title("Paid App Price Distribution"); plt.xlabel("Price"); plt.tight_layout(); plt.savefig(f"{OUT}/paid_price_distribution.png",dpi=160); plt.close()
apps["Estimated_Revenue"]=apps["Installs_num"]*apps["Price_num"]; revenue=apps.groupby("Category")["Estimated_Revenue"].sum().sort_values(); plt.figure(figsize=(10,6)); revenue.plot(kind="barh"); plt.title("Estimated Revenue by Category"); plt.xlabel("Estimated Revenue"); plt.tight_layout(); plt.savefig(f"{OUT}/estimated_revenue_by_category.png",dpi=160); plt.close()

# TextBlob sentiment; fallback to simple lexical baseline if TextBlob is unavailable.
pos={"great","excellent","good","useful","love","fast","easy"}; neg={"bad","slow","crash","crashes","ads","not"}
def sentiment(text):
    if TextBlob:
        p=TextBlob(str(text)).sentiment.polarity
        return "positive" if p>0.1 else "negative" if p<-0.1 else "neutral"
    words=set(re.findall(r"\b[a-z]+\b",str(text).lower())); score=len(words&pos)-len(words&neg)
    return "positive" if score>0 else "negative" if score<0 else "neutral"
reviews["Sentiment"]=reviews["Translated_Review"].map(sentiment)
reviews.to_csv("outputs/review_sentiment.csv",index=False)
plt.figure(figsize=(6,5)); reviews["Sentiment"].value_counts().plot(kind="bar"); plt.title("Review Sentiment Distribution"); plt.ylabel("Reviews"); plt.tight_layout(); plt.savefig(f"{OUT}/sentiment_distribution.png",dpi=160); plt.close()
sent=reviews.merge(apps[["App","Category"]],on="App",how="left").groupby(["Category","Sentiment"]).size().unstack(fill_value=0)
sent.plot(kind="bar",figsize=(10,6)); plt.title("Sentiment by Category"); plt.ylabel("Review Count"); plt.xticks(rotation=35); plt.tight_layout(); plt.savefig(f"{OUT}/sentiment_by_category.png",dpi=160); plt.close()

insights=pd.DataFrame({"Insight":["Most saturated category","Highest average-rated category","Free apps share"],"Value":[apps.Category.value_counts().idxmax(),cat_rating.idxmax(),f"{(apps.Type.eq('Free').mean()*100):.1f}%"]})
insights.to_csv("outputs/key_insights.csv",index=False)
print(insights.to_string(index=False))
print("\nDeveloper recommendations:")
print("1. Study saturated categories carefully and differentiate on a clear user need.")
print("2. Prioritize product quality and retention because ratings and reviews strongly influence adoption.")
print("3. Validate monetization using install volume, price and category-level revenue potential before launch.")
