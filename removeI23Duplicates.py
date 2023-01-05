import pandas as pd

df = pd.read_csv("wavelengthlistvalues_I23.csv", names=["pdbid", "wavelength"], header=None)
df = df.pdbid
df.drop_duplicates(inplace=True)
i23pdbids = df.values.tolist()
i23pdbids = tuple(i23pdbids)
df = pd.read_csv("wavelengthlistvalues_neutron.csv", names=["pdbid", "wavelength"], header=None)
df = df.pdbid
df.drop_duplicates(inplace=True)
neutronpdbids = df.values.tolist()
neutronpdbids = tuple(neutronpdbids)
allpdbidstoremove = neutronpdbids + i23pdbids

with open("wavelengthlistvalues_all.csv", "r") as fileIn:
    with open("wavelengthlistvalues_allfilt_plusneut.csv", "w") as fileOut:
        for line in fileIn:
            if line.startswith(allpdbidstoremove):
                pass
            else:
                fileOut.write(line)
