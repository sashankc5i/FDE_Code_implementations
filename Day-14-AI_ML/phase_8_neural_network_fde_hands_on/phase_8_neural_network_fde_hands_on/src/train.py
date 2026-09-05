import torch
from dataclasses import dataclass
from torch.utils.data import TensorDataset, DataLoader

@dataclass
class History:
    train_loss: list
    val_loss: list
    grad_norms: list

def train_model(model, X_train, y_train, X_val, y_val, lr=1e-3,
                epochs=30, batch_size=128, optimizer_name="adamw"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    positive_weight = torch.tensor(
    len(y_train[y_train == 0]) / len(y_train[y_train == 1]),
    dtype=torch.float32,
    device=device
)

    loss_fn = torch.nn.BCEWithLogitsLoss(
    pos_weight=positive_weight
)
    if optimizer_name.lower() == "sgd":
        opt = torch.optim.SGD(model.parameters(), lr=lr, momentum=.9)
    elif optimizer_name.lower() == "adam":
        opt = torch.optim.Adam(model.parameters(), lr=lr)
    else:
        opt = torch.optim.AdamW(model.parameters(), lr=lr)
    ds = TensorDataset(torch.tensor(X_train, dtype=torch.float32),
                       torch.tensor(y_train, dtype=torch.float32))
    loader = DataLoader(ds, batch_size=batch_size, shuffle=True)
    Xv = torch.tensor(X_val, dtype=torch.float32).to(device)
    yv = torch.tensor(y_val, dtype=torch.float32).to(device)
    h = History([], [], [])
    for _ in range(epochs):
        model.train(); total = 0.; gtotal = 0.
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            if not torch.isfinite(loss):
                raise FloatingPointError("Non-finite loss encountered")
            loss.backward()
            g2 = 0.
            for p in model.parameters():
                if p.grad is not None: g2 += p.grad.detach().norm().item()**2
            gtotal += g2**.5
            opt.step()
            total += loss.item() * len(xb)
        model.eval()
        with torch.no_grad(): vl = loss_fn(model(Xv), yv).item()
        h.train_loss.append(total/len(ds)); h.val_loss.append(vl)
        h.grad_norms.append(gtotal/len(loader))
    return model, h
