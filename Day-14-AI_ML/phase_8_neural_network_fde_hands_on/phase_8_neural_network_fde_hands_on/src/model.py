import torch
from torch import nn

class ChurnMLP(nn.Module):
    def __init__(self, input_dim, hidden=(64, 32), activation="relu"):
        super().__init__()
        act = nn.ReLU() if activation == "relu" else nn.Sigmoid()
        layers = [nn.Linear(input_dim, hidden[0]), act]
        for i in range(1, len(hidden)):
            layers += [nn.Linear(hidden[i-1], hidden[i]), act]
        layers += [nn.Linear(hidden[-1], 1)]
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x).squeeze(-1)
