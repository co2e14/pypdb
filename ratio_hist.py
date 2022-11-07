import pandas as pd
import matplotlib.pyplot as plt
from pypdb.clients.search.search_client import perform_search
from pypdb.clients.search.search_client import ReturnType
from pypdb.clients.search.operators import text_operators

columns = ["PDBID", "Scat", "Refs", "Ratio"]
df = pd.read_csv("refScatRatio.csv", names=columns, header=None)

searchOperator = text_operators.ExactMatchOperator(value="X-RAY DIFFRACTION", attribute="exptl.method")
returnType = ReturnType.ENTRY
results = perform_search(searchOperator, returnType)
total = len(results)

df = df[df.PDBID != "None"]
successful = len(df.index)

df = df[df.Ratio < 100000]
sensible = len(df.index)

df_over1000 = df[df.Ratio > 1000]
possible = len(df_over1000.index)

print(f"A total of {total} structures were found, of which {successful} were successfully parsed. Of these, {sensible} are below 100000 (the 'sensible' limit) and finally, {possible} are over 1000 and therefore possible")
#df = df[df.Ratio > 1]
print(df)
plt.xkcd()
plot = plt.hist(df.Ratio, bins=100, log=True)
plt.plot([1000, 1000], [0, 100000])
plt.ylabel("# Structures (log)")
plt.xlabel("Unique Reflections / Scatterer (S) Ratio")
plt.title("S-SAD Solvability on I23 Based on Unique Reflections per Scatterer Ratio")
#plt.show()
