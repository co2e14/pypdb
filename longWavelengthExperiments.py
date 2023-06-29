from pypdb.clients.search.search_client import perform_search
from pypdb.clients.search.search_client import ReturnType
from pypdb.clients.search.operators import text_operators
from multiprocessing import Pool
import pypdb as pp
import os
import pandas as pd
import tqdm
import ast


class wavelength:
    def __init__(self):
        pass

    def getPDBs(self,):
        self.searchOperator = text_operators.ExactMatchOperator(
            value="X-RAY DIFFRACTION", attribute="exptl.method"
        )
        self.returnType = ReturnType.ENTRY
        self.results = perform_search(self.searchOperator, self.returnType)
        return self.results

    def getI23PDBs(self,):
        self.searchOperator = text_operators.ExactMatchOperator(value="I23", attribute="diffrn_source.pdbx_synchrotron_beamline")
        self.returnType = ReturnType.ENTRY
        self.results = perform_search(self.searchOperator, self.returnType)
        return self.results

    def getNeutronDiffractionPDBs(self,):
        self.searchOperator = text_operators.ExactMatchOperator(
            value="NEUTRON DIFFRACTION", attribute="exptl.method"
        )        
        self.returnType = ReturnType.ENTRY
        self.results = perform_search(self.searchOperator, self.returnType)
        return self.results

    def getWavelength(self, structure):
        info = pp.get_info(structure)
        try:
            wavelength = str(info["diffrn_source"])
            for char in "[]":
                wavelength = wavelength.replace(char, "")
            length = wavelength.count("pdbx_wavelength_list")
            if length <= 1:
                multi = False
            elif length >= 2:
                multi = True
            wavelength = ast.literal_eval(wavelength)
            if multi:
                multi_wavelength_out = []
                for dif_id in range(0, len(wavelength), 1):
                    multi_wavelength = wavelength[dif_id]
                    multi_wavelength_ = float(multi_wavelength["pdbx_wavelength_list"])
                    multi_wavelength_out += [multi_wavelength_]
                wavelength = multi_wavelength_out
            else:
                pass
            if length == 1:
                wavelength = [float(wavelength["pdbx_wavelength_list"])]
            elif length == 0:
                wavelength = None
            else:
                pass
        except:
            wavelength = None
        if wavelength == None:
            pass
        else:
            return structure, wavelength
        
if __name__ == "__main__":
    pool = Pool(os.cpu_count())
    getWavelengths = wavelength()
    toRun = getWavelengths.getNeutronDiffractionPDBs()
    wavelengthList = list(
        tqdm.tqdm(pool.imap(getWavelengths.getWavelength, toRun), total=len(toRun)))
    with open("longWavelengthExperiments_neutron.csv", "w") as file:
        for value in wavelengthList:
            if value != None:
                for wave_val in range(0, len(value[1])):
                    pdb_wave_pair = str(value[0] + ", " + str(value[1][wave_val]))
                    file.write(pdb_wave_pair + "\n")
                    print(pdb_wave_pair)
            else:
                pass
    toRun = getWavelengths.getI23PDBs()
    wavelengthList = list(
        tqdm.tqdm(pool.imap(getWavelengths.getWavelength, toRun), total=len(toRun)))
    with open("longWavelengthExperiments_I23.csv", "w") as file:
        for value in wavelengthList:
            if value != None:
                for wave_val in range(0, len(value[1])):
                    pdb_wave_pair = str(value[0] + ", " + str(value[1][wave_val]))
                    file.write(pdb_wave_pair + "\n")
                    print(pdb_wave_pair)
            else:
                pass
    toRun = getWavelengths.getPDBs()
    wavelengthList = list(
        tqdm.tqdm(pool.imap(getWavelengths.getWavelength, toRun), total=len(toRun)))
    with open("longWavelengthExperiments_all.csv", "w") as file:
        for value in wavelengthList:
            if value != None:
                for wave_val in range(0, len(value[1])):
                    pdb_wave_pair = str(value[0] + ", " + str(value[1][wave_val]))
                    file.write(pdb_wave_pair + "\n")
                    print(pdb_wave_pair)
            else:
                pass


    df = pd.read_csv("longWavelengthExperiments_I23.csv", names=["pdbid", "wavelength"], header=None)
    df = df.pdbid
    df.drop_duplicates(inplace=True)
    i23pdbids = df.values.tolist()
    i23pdbids = tuple(i23pdbids)
    df = pd.read_csv("longWavelengthExperiments_neutron.csv", names=["pdbid", "wavelength"], header=None)
    df = df.pdbid
    df.drop_duplicates(inplace=True)
    neutronpdbids = df.values.tolist()
    neutronpdbids = tuple(neutronpdbids)
    allpdbidstoremove = neutronpdbids + i23pdbids

    with open("longWavelengthExperiments_all.csv", "r") as fileIn:
        with open("longWavelengthExperiments_filtererd.csv", "w") as fileOut:
            for line in fileIn:
                if line.startswith(allpdbidstoremove):
                    pass
                else:
                    fileOut.write(line)
