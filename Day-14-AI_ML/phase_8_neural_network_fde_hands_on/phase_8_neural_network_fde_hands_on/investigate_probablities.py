import torch
from src.data import make_data, split_scale
from src.model import ChurnMLP
from src.train import train_model

df = make_data()

Xtr, Xv, Xt, ytr, yv, yt = split_scale(df)

model = ChurnMLP(Xtr.shape[1])
model, history = train_model(
    model, Xtr, ytr, Xv, yv,
    lr=1e-3,
    epochs=30,
    batch_size=128,
    optimizer_name="adamw"
)

model.eval()

with torch.no_grad():
    logits = model(torch.tensor(Xv, dtype=torch.float32))
    probs = torch.sigmoid(logits)

print("Min probability:", probs.min().item())
print("Max probability:", probs.max().item())
print("Mean probability:", probs.mean().item())

print("\nChurner probabilities:")
print(probs[yv == 1].numpy()[:20])

print("\nRetained probabilities:")
print(probs[yv == 0].numpy()[:20])