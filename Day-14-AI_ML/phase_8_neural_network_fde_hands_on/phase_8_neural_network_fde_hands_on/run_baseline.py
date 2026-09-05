from src.data import make_data, split_scale
from src.model import ChurnMLP
from src.train import train_model
from src.evaluate import evaluate

df = make_data()
Xtr, Xv, Xt, ytr, yv, yt = split_scale(df)
model = ChurnMLP(Xtr.shape[1])
model, history = train_model(model, Xtr, ytr, Xv, yv)
print("Validation:", evaluate(model, Xv, yv))
print("Test:", evaluate(model, Xt, yt))
print("Final train loss:", history.train_loss[-1])
print("Final validation loss:", history.val_loss[-1])

from src.data import make_data

df = make_data()

print(df["churn"].value_counts())
print(df["churn"].value_counts(normalize=True))