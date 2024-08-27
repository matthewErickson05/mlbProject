import os
import torch
from torch import nn
import csv
import numpy as np

#First we need to convert the csv to a numpy array
#Then convert the numpy array to a tensor
data = np.genfromtxt('clean_data.csv', delimiter=',')
x_data = torch.from_numpy(data)



device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device} device")

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(11, 10),
            nn.ReLU(),
            nn.Linear(10, 10),
            nn.ReLU(),
            nn.Linear(10, 6),
        )
    
    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits
    
model = NeuralNetwork().to(device)
print(model)

X = torch.rand(1, 11, device=device)
logits = model(X)
pred_probab = nn.Softmax(dim=1)(logits)
y_pred = pred_probab.argmax(1)
print(f"Predicted class: {y_pred}")


input_vector = torch.rand(11)
print(input_vector.size())

layer1 = nn.Linear(in_features=11, out_features=10)
hidden1 = nn.Linear(x_data)
print(hidden1.size())

