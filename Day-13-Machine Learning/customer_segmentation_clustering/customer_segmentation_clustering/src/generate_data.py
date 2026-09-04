from pathlib import Path
import numpy as np, pandas as pd

rng=np.random.default_rng(42); n=1200
seg=rng.choice(["high_value","regular","at_risk","low_engagement"],n,p=[.18,.42,.20,.20])
rows=[]
for i,s in enumerate(seg,1):
    if s=="high_value": v=[rng.normal(28,7),rng.normal(18,4),rng.normal(52000,9000),rng.normal(2900,450),rng.normal(2,1),rng.normal(8,4)]
    elif s=="regular": v=[rng.normal(18,6),rng.normal(9,3),rng.normal(19000,4500),rng.normal(2100,350),rng.normal(3,1.5),rng.normal(18,7)]
    elif s=="at_risk": v=[rng.normal(15,7),rng.normal(3,1.5),rng.normal(7500,2500),rng.normal(1800,400),rng.normal(6,2),rng.normal(55,15)]
    else: v=[rng.normal(7,4),rng.normal(2,1),rng.normal(3000,1300),rng.normal(1500,300),rng.normal(2,1.5),rng.normal(45,18)]
    rows.append([f"C{i:05d}",max(1,v[0]),max(0,v[1]),max(100,v[2]),max(200,v[3]),max(0,v[4]),max(1,v[5])])
cols=["customer_id","tenure_months","orders_last_90_days","total_spend_last_90_days","avg_order_value","support_tickets_last_90_days","days_since_last_order"]
df=pd.DataFrame(rows,columns=cols)
df["orders_last_90_days"]=df["orders_last_90_days"].round().astype(int)
df["support_tickets_last_90_days"]=df["support_tickets_last_90_days"].round().astype(int)
for c in cols[1:]: df[c]=df[c].round(2)
out=Path(__file__).resolve().parents[1]/"data/raw/customers.csv"; out.parent.mkdir(parents=True,exist_ok=True)
df.to_csv(out,index=False); print(out)
