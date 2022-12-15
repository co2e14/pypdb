import ast
import pypdb as pp
import tqdm
from multiprocessing import Pool, freeze_support
import os
from pypdb.clients.search.search_client import perform_search
from pypdb.clients.search.search_client import ReturnType
from pypdb.clients.search.operators import text_operators

class wavelength:
    def __init__(self):
        pass

    def getPDBs(self,):
        self.searchOperator = text_operators.ExactMatchOperator(value="X-RAY DIFFRACTION", attribute="exptl.method")
        self.returnType = ReturnType.ENTRY
        self.results = perform_search(self.searchOperator, self.returnType) 
        print(f"Found {len(self.results)} structures")
        self.results = self.results[7000:9000]
        return self.results

    def getI23PDBs(self,):
        self.searchOperator = text_operators.ExactMatchOperator(value="I23", attribute="diffrn_source.pdbx_synchrotron_beamline")
        self.returnType = ReturnType.ENTRY
        self.results = perform_search(self.searchOperator, self.returnType)
        return self.results

    def getWavelength(self, structure):
        info = pp.get_info(structure)
        try:
            wavelength = str(info["diffrn_source"])
            for char in "[]": wavelength = wavelength.replace(char, "")
            wavelength = ast.literal_eval(wavelength)
            multi_wavelength_out = []
            if len(wavelength) > 1:
                for dif_id in range(0, len(wavelength), 1):
                    multi_wavelength = wavelength[dif_id]
                    multi_wavelength_ = float(multi_wavelength["pdbx_wavelength_list"])
                    multi_wavelength_out += [multi_wavelength_]
            else:
                pass
        except:
            wavelength = None
        if wavelength == None or multi_wavelength_out == []:
            pass
        else:
            print(structure, multi_wavelength_out) 
            return structure, multi_wavelength_out

if __name__ == '__main__':
    pool = Pool(os.cpu_count())
    getWavelengths = wavelength()
    toRun = getWavelengths.getI23PDBs()
    wavelengthList = list(tqdm.tqdm(pool.imap(getWavelengths.getWavelength, toRun), total=len(toRun)))
    with open("wavelengthlistvalues_I23.csv", "w") as file:
        for value in wavelengthList:
            if value != None:
                for wave_val in range(0, len(value[1])):
                    pdb_wave_pair = str(value[0] + ", " + str(value[1][wave_val]))
                    file.write(pdb_wave_pair + "\n")
                    print(pdb_wave_pair)
            else:
                pass