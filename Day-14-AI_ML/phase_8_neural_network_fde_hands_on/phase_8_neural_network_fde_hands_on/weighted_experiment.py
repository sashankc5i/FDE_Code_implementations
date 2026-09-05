from src.data import make_data, split_scale
from src.model import ChurnMLP
from src.train import train_model
from src.evaluate import evaluate

df = make_data()

Xtr, Xv, Xt, ytr, yv, yt = split_scale(df)

model = ChurnMLP(
    input_dim=Xtr.shape[1],
    hidden=(64, 32),
    activation="relu"
)

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

print("\nWeighted Model")
print("=" * 60)

print("\nValidation @ 0.50:")
print(evaluate(model, Xv, yv, threshold=0.50))

print("\nTest @ 0.50:")
print(evaluate(model, Xt, yt, threshold=0.50))

print("\nThreshold Analysis")
print("-" * 60)

for threshold in [0.01, 0.02, 0.05, 0.10, 0.20, 0.30, 0.50]:
    metrics = evaluate(model, Xv, yv, threshold=threshold)

    print(
        f"Threshold={threshold:.2f} | "
        f"Precision={metrics['precision']:.3f} | "
        f"Recall={metrics['recall']:.3f} | "
        f"F1={metrics['f1']:.3f} | "
        f"AUC={metrics['roc_auc']:.3f}"
    )

print("\nTraining loss:", history.train_loss[-1])
print("Validation loss:", history.val_loss[-1])