import pandas as pd

df = pd.read_csv("wavelengthlistvalues_I23.csv", names=["pdbid", "wavelength"], header=None)
df = df.pdbid
df.drop_duplicates(inplace=True)
i23pdbids = df.values.tolist()
i23pdbids = tuple(i23pdbids)

with open("wavelengthlistvalues_all.csv", "r") as fileIn:
    with open("wavelengthlistvalues_allfilt.csv", "w") as fileOut:
        for line in fileIn:
            if line.startswith(i23pdbids):
                pass
            else:
                fileOut.write(line)
