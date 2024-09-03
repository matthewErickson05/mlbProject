from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import RadiusNeighborsClassifier
import numpy as np
import pandas as pd


def scale_column_to_range(column, new_min=0, new_max=10) :
    old_min = column.min()
    old_max = column.max()
    scaled_column = (column - old_min) / (old_max - old_min) * (new_min + new_max) + new_min
    return scaled_column

#Using the clean data and labels csv files, we need to make the training variables
labels_df = pd.read_csv("labels.csv")
y = labels_df.values.flatten()

data_df = pd.read_csv("clean_data.csv")
scaled_df = data_df #scale_column_to_range(data_df)
print(scaled_df.describe())
X = scaled_df.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Create the model and train it
classifier = KNeighborsClassifier(n_neighbors = 70)
classifier.fit(X_train, y_train)
print(classifier.score(X_test, y_test))
