from pathlib import Path
import pandas as pd, matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/"data/raw/customers.csv"
CHARTS=ROOT/"outputs/charts"; REPORTS=ROOT/"outputs/reports"
CHARTS.mkdir(parents=True,exist_ok=True); REPORTS.mkdir(parents=True,exist_ok=True)
FEATURES=["tenure_months","orders_last_90_days","total_spend_last_90_days","avg_order_value","support_tickets_last_90_days","days_since_last_order"]
df=pd.read_csv(DATA)
X=SimpleImputer(strategy="median").fit_transform(df[FEATURES]); X=StandardScaler().fit_transform(X)

inertia=[]; sil=[]
for k in range(2,9):
    m=KMeans(n_clusters=k,random_state=42,n_init=20); lab=m.fit_predict(X)
    inertia.append(m.inertia_); sil.append(silhouette_score(X,lab))
plt.figure(figsize=(8,5)); plt.plot(range(2,9),inertia,marker="o")
plt.xlabel("Number of clusters (k)"); plt.ylabel("Inertia"); plt.title("Elbow Curve")
plt.tight_layout(); plt.savefig(CHARTS/"elbow_curve.png",dpi=150); plt.close()

k=4; model=KMeans(n_clusters=k,random_state=42,n_init=20); df["cluster"]=model.fit_predict(X)
score=silhouette_score(X,df["cluster"])
profile=df.groupby("cluster")[FEATURES].mean().round(2); profile["customer_count"]=df.groupby("cluster").size()
profile["customer_pct"]=(profile["customer_count"]/len(df)*100).round(2); profile.to_csv(REPORTS/"cluster_profiles.csv")
df.to_csv(REPORTS/"customer_segments.csv",index=False)

coords=PCA(n_components=2,random_state=42).fit_transform(X)
plt.figure(figsize=(8,6))
for c in sorted(df["cluster"].unique()):
    p=coords[df["cluster"].to_numpy()==c]; plt.scatter(p[:,0],p[:,1],s=12,alpha=.6,label=f"Cluster {c}")
plt.xlabel("Principal Component 1"); plt.ylabel("Principal Component 2"); plt.title("Customer Clusters — PCA Projection")
plt.legend(); plt.tight_layout(); plt.savefig(CHARTS/"customer_clusters.png",dpi=150); plt.close()

(REPORTS/"interpretation_notes.md").write_text(
"# Interpretation Notes\n\nSelected k: "+str(k)+"\nSilhouette score: "+f"{score:.3f}"+
"\n\nCluster IDs are arbitrary. Profile each cluster before naming it.\n",encoding="utf-8")
print("Outputs:",ROOT/"outputs")
