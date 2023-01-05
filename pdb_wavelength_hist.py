import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

f = plt.figure(figsize=(7,5))
ax = f.add_subplot(1,1,1)

columns = ["pdbid", "wavelength"]
i23data = pd.read_csv("wavelengthlistvalues_I23.csv", names=columns, header=None)
alldata = pd.read_csv("wavelengthlistvalues_allfilt_plusneut.csv", names=columns, header=None)


plot = plt.hist([i23data.wavelength, alldata.wavelength], color = ["orange", "grey"], stacked=True, bins=200, log=False)
plt.show()