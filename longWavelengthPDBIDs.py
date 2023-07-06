from pypdb.clients.search.search_client import (
    perform_search,
    ReturnType,
)
from pypdb.clients.search.operators import text_operators
import pypdb as pp
from collections import Counter
import ast

def search(limit):
    returnType = ReturnType.ENTRY

    searchOperator = text_operators.ExactMatchOperator(
        value="X-RAY DIFFRACTION", attribute="exptl.method"
    )
    results = perform_search(searchOperator, returnType)

    pdbids = results

    searchOperator = text_operators.ExactMatchOperator(
        value="SYNCHROTRON", attribute="diffrn_source.source"
    )
    results = perform_search(searchOperator, returnType)

    pdbids = list(set(pdbids).intersection(results))

    searchOperator = text_operators.ExactMatchOperator(
        value="I23", attribute="diffrn_source.pdbx_synchrotron_beamline"
    )
    results = perform_search(searchOperator, returnType)

    pdbids = [x for x in pdbids if x not in results]

    searchOperator = text_operators.ExactMatchOperator(
        value="NEUTRON DIFFRACTION", attribute="exptl.method"
    )
    results = perform_search(searchOperator, returnType)

    pdbids = [x for x in pdbids if x not in results]

    searchOperator = text_operators.ComparisonOperator(
        value=limit,
        attribute="rcsb_entry_info.diffrn_radiation_wavelength_minimum",
        comparison_type=text_operators.ComparisonType.GREATER_OR_EQUAL,
    )
    results = perform_search(searchOperator, returnType)

    pdbids = list(set(pdbids).intersection(results))

    return limit, pdbids

def getinfo(pdbid):
    try:
        pdbinfo = pp.get_info(pdb)
        pdbinfo = str(pdbinfo["diffrn_source"])
        for char in "[]":
            info = pdbinfo.replace(char, "")
        pdbinfo = ast.literal_eval(pdbinfo)
        wavelenghts = [d['pdbx_wavelength_list'] for d in pdbinfo]
        beamline = [d['type'] for d in pdbinfo]
        return wavelenghts, beamline
    except:
        print('error')
    # try:
    #     diffrn_source = str(pdbinfo["diffrn_source"])
    #     print(diffrn_source)
    #     for char in "[]":
    #         diffrn_source = diffrn_source.replace(char, "")
    #     length = diffrn_source.count("source")
    #     print(length)
    #     diffrn_source = ast.literal_eval(diffrn_source)
    #     print(diffrn_source)
    #     if length >= 2:
    #         multi_source_out = []
    #         for dif_id in range(0, len(diffrn_source) + 1, 1):
    #             multi_source = diffrn_source[dif_id]
    #             print(multi_source)
    #             multi_source_ = str(multi_source["pdbx_synchrotron_site"]) + " " + str(multi_source["pdbx_synchrotron_beamline"])
    #             multi_source_out += [multi_source_]
    #         diffrn_source = multi_source_out
    #     elif length == 1:
    #         diffrn_source = diffrn_source[1]
    #         diffrn_source = [str(diffrn_source["pdbx_synchrotron_site"]) + " " + str(diffrn_source["pdbx_synchrotron_beamline"])]
    #         print(diffrn_source)
    #     elif length == 0:
    #         print('no len')
    #         diffrn_source = None
    #     else:
    #         pass
    # except:
    #     print("except")
    #     diffrn_source = None
    # if diffrn_source == None:
    #     pass
    # else:
    #     return diffrn_source

if __name__ == '__main__':
    # val = ""
    # for x in range(17, 40, 1):
    #     out = search((x/10))
    #     val += f"{out} "
        
    # print(val)
    
    lim, pdbs = search(2.1)
    
    with open("pdbstosearch.txt", "w") as out:
        for x in pdbs:
            x = str(x) + "\n"
            out.write(x)
            
    with open("pdb_lambda_beamline.txt", "w") as out:        
        allbeamlines = []
        for pdb in pdbs:
            info = getinfo(pdb)
            if info is not None:
                beamlines = ', '.join(info[1])
                allbeamlines += [beamlines]
                x = str(str(pdb) + ', ' + ', '.join(info[0]) + ' on ' + ', '.join(info[1]))
                out.write(x + "\n")
            else:
                pass
        count = Counter(allbeamlines)
        for key, value in count.most_common():
            print(f"{key}: {value}")        