import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#This is just used to check the features of the data (min, max, mean, to make sure something isn't off when it was converted to the csv file)
df = pd.read_csv("clean_data.csv")
print(df.head())
print(df.describe().transpose())


plt.hist2d(df['ratingLR'], df['ratingUD'], bins=(50, 50), vmax=100)
plt.colorbar()
plt.xlabel('ratingLR')
plt.ylabel('ratingUD')
ax = plt.gca()
ax.axis('tight')
plt.show()
