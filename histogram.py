from tkinter.tix import COLUMN
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("refScatRatio.csv", names=["PDBID", "S", "RESIDUES", "RATIO"], header=None)
df = df.dropna()
print(df.describe())
print(df["RATIO"].max())
#plot = plt.hist(df2, bins=100)
#plt.show()

sns.distplot(df["RATIO"], hist=True, kde=True, rug=False)
plt.show()