import pypdb as pp
import tqdm
from multiprocessing import Pool, freeze_support
import os
from pypdb.clients.search.search_client import perform_search
from pypdb.clients.search.search_client import ReturnType
from pypdb.clients.search.operators import text_operators
import re

class sContent:
    def __init__(self):
        pass

    def getPDBs(self):
        self.searchOperator = text_operators.ExactMatchOperator(value="X-RAY DIFFRACTION", attribute="exptl.method")
        self.returnType = ReturnType.ENTRY
        self.results = perform_search(self.searchOperator, self.returnType) 
        print(f"Found {len(self.results)} structures")
        #self.results = self.results[:3000]
        return self.results

    def whatPercent(self, structure: str) -> float:
        seqString: str = ""
        fastaSeqs = pp.fasta_client.get_fasta_from_rcsb_entry(structure)
        fastaSeqs = str(fastaSeqs)
        splitSeq = fastaSeqs.split()
        for x in splitSeq:
            if x.startswith("sequence='"):
                seqString += x
            else:
                pass
        sulphurs = seqString.count("C") + seqString.count("M")
        # all_AAs = sulphurs
        all_AAs = sum(1 for c in seqString if c.isupper())
        # for AA in ["A", "R", "N", "D", "E", "Q", "G", "H", "I", "L", "K", "F", "P", "S", "T", "W", "Y", "V"]:
        #     all_AAs += seqString.count(AA)
        try:
            percentage_S = (sulphurs / all_AAs) * 100
            return percentage_S
        except:
            pass

if __name__ == '__main__':
    pool = Pool(os.cpu_count())
    getSContent = sContent()
    torun = getSContent.getPDBs()
    #print(torun)
    sContentList = list(tqdm.tqdm(pool.imap(getSContent.whatPercent, torun), total=len(torun)))
    with open("sContent.csv", "w") as file:
        for value in sContentList:
            file.write(str(value) + "\n")
    #unitCellCheck.writeSaveFile(longCellList)
