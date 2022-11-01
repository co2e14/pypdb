# pdbx_wavelength_list
import ast
import pypdb as pp
import tqdm
from multiprocessing import Pool, freeze_support
import os
from pypdb.clients.search.search_client import perform_search
from pypdb.clients.search.search_client import ReturnType
from pypdb.clients.search.operators import text_operators
import re

class wavelength:
    def __init__(self):
        pass

    def getPDBs(self,):
        self.searchOperator = text_operators.ExactMatchOperator(value="X-RAY DIFFRACTION", attribute="exptl.method")
        self.returnType = ReturnType.ENTRY
        self.results = perform_search(self.searchOperator, self.returnType) 
        print(f"Found {len(self.results)} structures")
        #self.results = self.results[:3000]
        return self.results

    def getWavelength(self, structure):
        info = pp.get_info(structure)
        try:
            wavelength = str(info["diffrn_source"])
            for char in "[]": wavelength = wavelength.replace(char, "")
            wavelength = ast.literal_eval(wavelength)
            wavelength = float(wavelength["pdbx_wavelength_list"])
        except:
            wavelength = None
        if wavelength == None:
            pass
        else:
            print(f"{structure}: {wavelength}")
            return wavelength

if __name__ == '__main__':
    pool = Pool(os.cpu_count())
    getWavelengths = wavelength()
    toRun = getWavelengths.getPDBs()
    wavelengthList = list(tqdm.tqdm(pool.imap(getWavelengths.getWavelength, toRun), total=len(toRun)))
