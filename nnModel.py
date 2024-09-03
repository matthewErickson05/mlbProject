import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


labels_df = pd.read_csv("labels.csv")
y = labels_df.values.flatten()

data_df = pd.read_csv("clean_data.csv")
scaled_df = data_df #scale_column_to_range(data_df)
print(scaled_df.describe())
X = scaled_df.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

