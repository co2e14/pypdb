import pypdb as pp
import tqdm
from multiprocessing import Pool, freeze_support
import os
from pypdb.clients.search.search_client import perform_search
from pypdb.clients.search.search_client import ReturnType
from pypdb.clients.search.operators import text_operators
import re

class reflectionsperscatterer:
    def __init__(self):
        pass

    def removeUC(self, string):
        regex = "[^A-Z]"
        return (re.sub(regex, "", string))

    def getPDBs(self,):
        self.searchOperator = text_operators.ExactMatchOperator(value="X-RAY DIFFRACTION", attribute="exptl.method")
        self.returnType = ReturnType.ENTRY
        self.results = perform_search(self.searchOperator, self.returnType) 
        print(f"Found {len(self.results)} structures")
        #self.results = self.results[:3000]
        return self.results

    def grabMillerIndices(self, structure):
        seqString = ""
        info = pp.get_info(structure)
        fastaSeqs = pp.fasta_client.get_fasta_from_rcsb_entry(structure)
        fastaSeqs = str(fastaSeqs)
        splitSeq = fastaSeqs.split()
        for x in splitSeq:
            if x.startswith("sequence='"):
                seqString += x
            else:
                pass
        sulphurs = seqString.count("C") + seqString.count("M")
        try:
            millerInd = int(info["pdbx_vrpt_summary"]["num_miller_indices"])
        except:
            millerInd = 1
        try:
            refPerScat = int(millerInd / sulphurs)
        except:
            refPerScat = 1
        if millerInd == 1:
            pass
        else:
            infoOut = f"{structure}, {sulphurs}, {millerInd}, {refPerScat}"
            return infoOut

    def printCode(self, structure):
        print(structure)

    def writeSaveFile(self, toSave):
        if not os.path.exists("refScaRat.csv"):
            with open("refScaRat.csv", "a") as file:
                for val in toSave:
                    file.write(str(val) + "\n")
        else:
            print("File already exists, remove it before starting\n")

if __name__ == '__main__':
    pool = Pool(os.cpu_count())
    getRefScatRatio = reflectionsperscatterer()
    torun = getRefScatRatio.getPDBs()
    #print(torun)
    refScatRatioList = list(tqdm.tqdm(pool.imap(getRefScatRatio.grabMillerIndices, torun), total=len(torun)))
    with open("refScatRatio.csv", "w") as file:
        for value in refScatRatioList:
            file.write(str(value) + "\n")
    #unitCellCheck.writeSaveFile(longCellList)
