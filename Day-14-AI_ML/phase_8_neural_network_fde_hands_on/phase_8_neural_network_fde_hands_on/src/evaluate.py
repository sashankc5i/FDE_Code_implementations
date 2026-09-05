def evaluate(model, X, y, threshold=.5):
    import torch
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
    model.eval()
    with torch.no_grad():
        probs = torch.sigmoid(model(torch.tensor(X, dtype=torch.float32))).numpy()
    pred = (probs >= threshold).astype(int)
    return {
        "accuracy": accuracy_score(y, pred),
        "precision": precision_score(y, pred, zero_division=0),
        "recall": recall_score(y, pred, zero_division=0),
        "f1": f1_score(y, pred, zero_division=0),
        "roc_auc": roc_auc_score(y, probs)
    }
