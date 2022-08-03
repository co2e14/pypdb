import pandas as pd
import matplotlib.pyplot as plt

columns = ["PDBID", "Scat", "Refs", "Ratio"]
df = pd.read_csv("refScatRatio.csv", names=columns, header=None)
df = df[df.PDBID != "None"]
df = df[df.Ratio < 50000]
df = df[df.Ratio > 1000]
print(df)

plot = plt.hist(df.Ratio, bins=1000)
plt.show()
