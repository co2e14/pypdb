import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

f = plt.figure(figsize=(7,5))
ax = f.add_subplot(1,1,1)

columns = ["wavelength", "beamline", "pdbid"]
alldata = pd.read_csv("wl_bl_id_sorted.csv", names=columns, header=None)
i23data = pd.read_csv("wl_bl_id_I23only.csv", names=columns, header=None)
# paperdata = pd.read_csv("wavelengthlistvalues_frompaper.csv", names=columns, header=None)
# alldata = pd.read_csv("wavelengthlistvalues_allfilt_plusneut.csv", names=columns, header=None)


# plot = plt.hist([i23data.wavelength, paperdata.wavelength, alldata.wavelength], color = ["orange", "lime", "grey"], stacked=True, bins=200, log=True)
plot = plt.hist([alldata.wavelength, i23data.wavelength], color=["orange", "lime"], bins=200, log=True, stacked=True)
plt.show()
#plt.savefig("out.png")