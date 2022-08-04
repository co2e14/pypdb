import pandas as pd
import matplotlib.pyplot as plt

columns = ["PDBID", "Scat", "Refs", "Ratio"]
df = pd.read_csv("refScatRatio.csv", names=columns, header=None)
df = df[df.PDBID != "None"]
df = df[df.Ratio < 100000]
#df = df[df.Ratio > 1]
print(df)
plt.xkcd()
plot = plt.hist(df.Ratio, bins=100, log=True)
plt.plot([1000, 1000], [0, 100000])
plt.ylabel("# Structures (log)")
plt.xlabel("Unique Reflections / Scatterer (S) Ratio")
plt.title("S-SAD Solvability on I23 Based on Unique Reflections per Scatterer Ratio")
plt.show()
