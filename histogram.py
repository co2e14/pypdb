import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("longcellvalues.csv")

df2 = df[df <= 300]

plot = plt.hist(df2, bins=100)
plt.show()
