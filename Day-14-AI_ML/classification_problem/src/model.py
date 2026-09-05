from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,confusion_matrix,log_loss

ROOT=Path(__file__).resolve().parents[1]
def load_data(): return pd.read_csv(ROOT/'data/raw/customer_churn.csv')
def build_model():
    f=['age','tenure_months','orders_last_6m','monthly_spend','support_tickets','late_payments','discount_pct']
    prep=ColumnTransformer([('num',StandardScaler(),f)])
    return Pipeline([('prep',prep),('model',LogisticRegression(max_iter=1000))])
def evaluate(y,p,t=.5):
    pred=(p>=t).astype(int)
    return {'threshold':t,'accuracy':accuracy_score(y,pred),'precision':precision_score(y,pred,zero_division=0),
            'recall':recall_score(y,pred,zero_division=0),'f1':f1_score(y,pred,zero_division=0),
            'roc_auc':roc_auc_score(y,p),'log_loss':log_loss(y,p),'confusion_matrix':confusion_matrix(y,pred).tolist()}
