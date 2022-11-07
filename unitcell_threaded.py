import pypdb as pp
import tqdm
from multiprocessing import Pool, freeze_support
import os


class unitCell:
    def __init__(self):
        self.longCell_db = []
        pass

    def getPDBs(self,):
        self.xrcStructures = pp.Query("X-RAY DIFFRACTION", query_type="ExpTypeQuery").search()
        print(f"Found {len(self.xrcStructures)} structures")
        return self.xrcStructures

    def grabLongUnitCellThreaded(self, structure):
        info = pp.get_info(structure)
        a = info["cell"]["length_a"]
        b = info["cell"]["length_b"]
        c = info["cell"]["length_c"]
        longCell = max(a, b, c)
        return longCell

    def printCode(self, structure):
        print(structure)

    def writeSaveFile(self, toSave):
        if not os.path.exists("all_longcellvalues.csv"):
            with open("all_longcellvalues.csv", "w") as file:
                for val in toSave:
                    file.write(str(val) + "\n")
        else:
            print("File already exists, remove it before starting\n")

if __name__ == '__main__':
    pool = Pool(os.cpu_count())
    unitCellCheck = unitCell()
    torun = unitCellCheck.getPDBs()
    longCellList = list(tqdm.tqdm(pool.imap(unitCellCheck.grabLongUnitCellThreaded, torun), total=len(torun)))
    with open("longcellvalues.csv", "w") as file:
        for cell in longCellList:
            file.write(str(cell) + "\n")
    #unitCellCheck.writeSaveFile(longCellList)


    

