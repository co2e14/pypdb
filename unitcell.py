import pypdb as pp
import tqdm

xrcStructures = pp.Query("X-RAY DIFFRACTION", query_type="ExpTypeQuery").search()
num = 20583 + 32681 + 2568
xrcStructures = xrcStructures[num:]


print(f"Found {len(xrcStructures)} structures")

longCell_db = []

with tqdm.tqdm(total=len(xrcStructures)) as pbar, open("longcellvalues.csv", "a") as file:
    for structure in xrcStructures:
        info = pp.get_info(structure)
        a = info["cell"]["length_a"]
        b = info["cell"]["length_b"]
        c = info["cell"]["length_c"]
        longCell = max(a, b, c)
        longCell_db += [longCell]
        file.write(str(longCell) + "\n")
        pbar.update(1)

# with open("longcellvalues.csv", "w") as file:
#     for val in longCell_db:
#         file.write(str(val) + "\n")
