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
        self.searchOperator = text_operators.ExactMatchOperator(
            value="X-RAY DIFFRACTION", attribute="exptl.method"
        )
        self.returnType = ReturnType.ENTRY
        self.results = perform_search(self.searchOperator, self.returnType)
        print(f"Found {len(self.results)} structures")
        # self.results = self.results[8500:9000]
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
    toRun = getWavelengths.getPDBs()
    wavelengthList = list(
        tqdm.tqdm(pool.imap(getWavelengths.getWavelength, toRun), total=len(toRun))
    )
    print(wavelengthList)
    with open("wavelengthlistvalues_all.csv", "w") as file:
        for value in wavelengthList:
            if value != None:
                for wave_val in range(0, len(value[1])):
                    pdb_wave_pair = str(value[0] + ", " + str(value[1][wave_val]))
                    file.write(pdb_wave_pair + "\n")
                    print(pdb_wave_pair)
            else:
                pass
            # getWavelengths = wavelength()
    # for x in ["6tkd", "1IXG", "6qng", "6fax", "1IYQ"]:
    #     getWavelengths.getWavelength(x)
