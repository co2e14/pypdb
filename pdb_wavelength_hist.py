import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

f = plt.figure(figsize=(7,5))
ax = f.add_subplot(1,1,1)

columns = ["pdbid", "wavelength"]
df = pd.read_csv("wavelengthlistvalues_I23.csv", names=columns, header=None)

plot = plt.hist(df.wavelength, bins=50, log=False)
plt.show()