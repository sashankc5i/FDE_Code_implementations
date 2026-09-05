# Phase 7 Hands-on — Customer Churn Classification

Train and evaluate a binary classification model end-to-end.

## Run
```bash
pip install -r requirements.txt
python train_and_evaluate.py
```

## Tasks
1. Inspect churn rate and class balance.
2. Compare accuracy with precision, recall, F1 and ROC-AUC.
3. Inspect the confusion matrix.
4. Compare thresholds 0.30–0.70.
5. Assume a retention team has limited intervention capacity. Decide how threshold selection changes.
6. Write an FDE findings report: business problem → data/label check → split → baseline → metrics → threshold → business impact → monitoring.

Do not optimize blindly; explain why the model is useful or not.
