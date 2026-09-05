import torch

from src.data import make_data, split_scale
from src.model import ChurnMLP
from src.train import train_model
from src.evaluate import evaluate

df = make_data()

Xtr, Xv, Xt, ytr, yv, yt = split_scale(df)

model = ChurnMLP(Xtr.shape[1])

model, history = train_model(
    model,
    Xtr,
    ytr,
    Xv,
    yv,
    lr=1e-3,
    epochs=30,
    batch_size=128,
    optimizer_name="adamw"
)

print("\nThreshold Analysis")
print("-" * 70)

for threshold in [0.01, 0.02, 0.03, 0.04, 0.05, 0.10, 0.20, 0.30, 0.50]:

    metrics = evaluate(
        model,
        Xv,
        yv,
        threshold=threshold
    )

    print(
        f"Threshold={threshold:.2f} | "
        f"Precision={metrics['precision']:.3f} | "
        f"Recall={metrics['recall']:.3f} | "
        f"F1={metrics['f1']:.3f} | "
        f"AUC={metrics['roc_auc']:.3f}"
    )