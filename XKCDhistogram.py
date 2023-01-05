import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_style("whitegrid")
df = pd.read_csv("refScatRatioDROPNA.csv")

print(df["RATIO"].max())
df.drop("Unnamed: 0", axis=1, inplace=True)
a = np.array(df['RATIO'].values.tolist())
df["RATIO"] = np.where(a < 2.0, 0.0, a).tolist()
sns.kdeplot(df["RATIO"], shade=True, bw=0.05, color="#13C113", log_scale=True)
plt.xlabel("Reflections per Sulphur Atom", fontsize=15)
plt.ylabel("Density of Total X-Ray PDB Structures", fontsize=15)
plt.savefig("refscatrat.png", format="png", bbox_inches="tight", dpi=600, alpha=0.5)
plt.show()