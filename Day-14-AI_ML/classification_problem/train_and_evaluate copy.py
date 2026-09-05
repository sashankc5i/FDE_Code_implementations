import sys
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
sys.path.insert(0,str(Path(__file__).resolve().parent))
from src.model import load_data,build_model,evaluate
df=load_data(); X=df.drop(columns='churn'); y=df.churn
Xtr,Xtmp,ytr,ytmp=train_test_split(X,y,test_size=.30,random_state=42,stratify=y)
Xv,Xte,yv,yte=train_test_split(Xtmp,ytmp,test_size=.50,random_state=42,stratify=ytmp)
m=build_model(); m.fit(Xtr,ytr)
pv=m.predict_proba(Xv)[:,1]; pt=m.predict_proba(Xte)[:,1]
rows=[evaluate(yv, pv, threshold) for threshold in [0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05]]
for row in rows:
    print(row['threshold'], row)
out=Path('outputs'); out.mkdir(exist_ok=True)
pd.DataFrame(rows).to_csv(out/'validation_threshold_analysis.csv',index=False)
pd.Series(evaluate(yte,pt,.50),dtype='object').to_json(out/'test_metrics.json',indent=2)
print(pd.DataFrame(rows).to_string(index=False))
print("Min probability:", pv.min())
print("Max probability:", pv.max())
print("Mean probability:", pv.mean())

print("\nChurn probabilities:")
print(
    "min:", pv[yv == 1].min(),
    "max:", pv[yv == 1].max(),
    "mean:", pv[yv == 1].mean()
)

print("\nRetained probabilities:")
print(
    "min:", pv[yv == 0].min(),
    "max:", pv[yv == 0].max(),
    "mean:", pv[yv == 0].mean()
)