from rcsbsearchapi import AttributeQuery
import requests
from multiprocessing import Pool
import os
import pandas as pd
import tqdm

def makeQuery():
    query = AttributeQuery(
        attribute="exptl.method",
        operator="exact_match",
        value="X-RAY DIFFRACTION"
    )

    results = list(query())
    results = results[:]
    return results

def fetch_pdb_details(pdb_id):
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()        
        diffrn_sources = data.get('diffrn_source', [])        
        extracted_sources = []
        for source in diffrn_sources:
            wavelength = source.get('pdbx_wavelength', '?')
            wavelength_list = source.get('pdbx_wavelength_list', '?')
            synchrotron_beamline = source.get('pdbx_synchrotron_beamline', '?')
            extracted_sources.append({
                'pdbx_wavelength': wavelength,
                'pdbx_wavelength_list': wavelength_list,
                'pdbx_synchrotron_beamline': synchrotron_beamline
            })
        extracted_tuples = [tuple(source.values()) for source in extracted_sources]
        #extracted_sources = tuple(extracted_sources.values())
        if extracted_tuples != [] and extracted_tuples != [('?', '?', '?')]:
            return extracted_tuples
        else:
            pass
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching details for PDB ID {pdb_id}: {e}")
        return None

if __name__ == "__main__":
    pool = Pool(os.cpu_count())
    PDBIDs = makeQuery()
    wavelengthList = list(
        tqdm.tqdm(pool.imap(fetch_pdb_details, PDBIDs), total=len(PDBIDs))
    )
    print(wavelengthList)
    with open("allinfoout.csv", "w") as file:
        for value in wavelengthList:
            if value != None:
                for secondval in value:
                    if secondval != None:
                        print(secondval)
                        file.write(str(secondval) + '\n')
                    else:
                        pass