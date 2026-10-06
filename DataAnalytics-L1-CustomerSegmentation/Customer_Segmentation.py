import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

DATA_PATH="dataset/online_retail.csv"; OUT="visualizations"; os.makedirs(OUT,exist_ok=True)
if not os.path.exists(DATA_PATH):
    rng=np.random.default_rng(7); n=2500
    customers=rng.integers(10001,10501,n); dates=pd.to_datetime("2025-01-01")+pd.to_timedelta(rng.integers(0,365,n),unit="D")
    qty=rng.integers(1,8,n); price=np.round(rng.uniform(5,180,n),2)
    df0=pd.DataFrame({"CustomerID":customers,"InvoiceDate":dates,"Quantity":qty,"UnitPrice":price})
    df0.to_csv(DATA_PATH,index=False)
else: df0=pd.read_csv(DATA_PATH)

df=df0.copy(); df["InvoiceDate"]=pd.to_datetime(df["InvoiceDate"],errors="coerce")
df["CustomerID"]=df["CustomerID"].astype(str); df["Quantity"]=pd.to_numeric(df["Quantity"],errors="coerce"); df["UnitPrice"]=pd.to_numeric(df["UnitPrice"],errors="coerce")
df["Amount"]=df["Quantity"]*df["UnitPrice"]; df=df.dropna(subset=["CustomerID","InvoiceDate","Amount"]); df=df[df["Quantity"]>0]; df=df[df["UnitPrice"]>0]
reference=df["InvoiceDate"].max()+pd.Timedelta(days=1)
rfm=df.groupby("CustomerID").agg(Recency=("InvoiceDate",lambda x:(reference-x.max()).days),Frequency=("InvoiceDate","nunique"),Monetary=("Amount","sum"))
rfm["AveragePurchaseValue"]=rfm["Monetary"]/rfm["Frequency"]
print("RFM summary:\n",rfm.describe())

features=["Recency","Frequency","Monetary"]
X=rfm[features].replace([np.inf,-np.inf],np.nan).dropna()
scaler=StandardScaler(); Xs=scaler.fit_transform(X)
ks=range(2,9); inertias=[]
for k in ks: inertias.append(KMeans(n_clusters=k,random_state=42,n_init=10).fit(Xs).inertia_)
plt.figure(figsize=(8,5)); plt.plot(list(ks),inertias,marker="o"); plt.title("Elbow Method"); plt.xlabel("K"); plt.ylabel("Inertia"); plt.tight_layout(); plt.savefig(f"{OUT}/elbow_method.png",dpi=160); plt.close()

k=4
model=KMeans(n_clusters=k,random_state=42,n_init=10); X["Cluster"]=model.fit_predict(Xs); rfm.loc[X.index,"Cluster"]=X["Cluster"].astype(int)
profile=rfm.groupby("Cluster")[features+['AveragePurchaseValue']].mean().round(2); counts=rfm["Cluster"].value_counts().sort_index()
profile.to_csv("outputs/cluster_profile.csv")
counts.to_csv("outputs/cluster_counts.csv",header=["Customers"])

plt.figure(figsize=(8,5)); counts.plot(kind="bar"); plt.title("Customers per Cluster"); plt.xlabel("Cluster"); plt.ylabel("Customers"); plt.tight_layout(); plt.savefig(f"{OUT}/cluster_customer_counts.png",dpi=160); plt.close()
plt.figure(figsize=(8,6)); sns.scatterplot(data=rfm,x="Recency",y="Monetary",hue="Cluster",palette="tab10"); plt.title("Clusters: Recency vs Monetary"); plt.tight_layout(); plt.savefig(f"{OUT}/recency_monetary_clusters.png",dpi=160); plt.close()
plt.figure(figsize=(8,6)); sns.scatterplot(data=rfm,x="Frequency",y="Monetary",hue="Cluster",palette="tab10"); plt.title("Clusters: Frequency vs Monetary"); plt.tight_layout(); plt.savefig(f"{OUT}/frequency_monetary_clusters.png",dpi=160); plt.close()

# Simple automatic segment labels for marketing discussion.
ranked=profile.copy();
for c,row in ranked.iterrows():
    if row.Monetary>=profile.Monetary.median() and row.Recency<=profile.Recency.median(): label="High-value / Loyal"
    elif row.Recency>profile.Recency.median() and row.Monetary>=profile.Monetary.median(): label="At-risk High Value"
    elif row.Frequency<=profile.Frequency.median() and row.Monetary<profile.Monetary.median(): label="Low-engagement"
    else: label="Regular / Growth"
    ranked.loc[c,"Segment_Label"]=label
ranked.to_csv("outputs/marketing_segments.csv")
print("\nCluster profile:\n",ranked)
print("\nMarketing actions:")
print("High-value / Loyal: VIP rewards, early access, cross-sell.")
print("At-risk High Value: win-back offers and personalized reminders.")
print("Regular / Growth: bundles and loyalty incentives to increase frequency.")
print("Low-engagement: low-cost reactivation campaigns and onboarding offers.")
