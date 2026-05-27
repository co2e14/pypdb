import requests
from multiprocessing import Pool
import os
import pandas as pd
import tqdm
import re

RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"

def makeQuery():
    """Query the RCSB PDB search API for every X-ray diffraction entry.

    Uses the RCSB search v2 REST endpoint directly so we don't depend on
    rcsbsearchapi (which currently crashes at import against the live schema).

    Returns:
        list[str]: all PDB IDs whose exptl.method == "X-RAY DIFFRACTION".
    """
    payload = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "exptl.method",
                "operator": "exact_match",
                "value": "X-RAY DIFFRACTION",
            },
        },
        "return_type": "entry",
        "request_options": {"return_all_hits": True},
    }
    response = requests.post(RCSB_SEARCH_URL, json=payload, timeout=120)
    response.raise_for_status()
    return [hit["identifier"] for hit in response.json().get("result_set", [])]

def fetch_pdb_details(pdb_id):
    """fetches pdb details from pdb_id and returns dictionary of wavelength, beamline and pdbid

    Args:
        pdb_id (_type_): _description_

    Returns:
        _type_: _description_
    """
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
                'pdbx_synchrotron_beamline': synchrotron_beamline,
                'pdbid': pdb_id
            })
        extracted_tuples = [tuple(source.values()) for source in extracted_sources]
        if extracted_tuples != [] and extracted_tuples != [('?', '?', '?')]:
            return extracted_tuples
        else:
            pass
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching details for PDB ID {pdb_id}: {e}")
        return None
    
def parse_row(line):
    """
    Parses a line of the CSV and extracts the four fields.
    """
    line = line.strip().lstrip('(').rstrip(')')
    matches = re.findall(r"'([^']*)'", line)
    
    if len(matches) != 4:
        return None
    return matches 

def process_file(file_path):
    """
    Processes the CSV file and returns a dataframe with WAVELENGTH, BEAMLINE, and PDBID.
    """
    pairs = [] 
    with open(file_path, 'r') as f:
        for line_number, line in enumerate(f, start=1):
            parsed = parse_row(line)
            if not parsed:
                print(f"Skipping invalid line {line_number}: {line.strip()}")
                continue  
            
            X, Y, Z, PDBID = parsed  
            
            if X != '?':
                WAVELENGTH = X.strip()
                BEAMLINE = Z.strip()
                pairs.append({'WAVELENGTH': WAVELENGTH, 'BEAMLINE': BEAMLINE, 'PDBID': PDBID.strip()})
            else:
                if Y.strip() == '?':
                    print(f"Skipping row {line_number} because both X and Y are '?'.")
                    continue
                
                Y_values = [y.strip() for y in Y.split(',')]
                Z_values = [z.strip() for z in Z.split(',')]
                
                if len(Z_values) == 1:
                    for y in Y_values:
                        pairs.append({'WAVELENGTH': y, 'BEAMLINE': Z_values[0], 'PDBID': PDBID.strip()})
                elif len(Z_values) == len(Y_values):
                    for y, z in zip(Y_values, Z_values):
                        pairs.append({'WAVELENGTH': y, 'BEAMLINE': z, 'PDBID': PDBID.strip()})
                else:
                    min_length = min(len(Y_values), len(Z_values))
                    for i in range(min_length):
                        pairs.append({'WAVELENGTH': Y_values[i], 'BEAMLINE': Z_values[i], 'PDBID': PDBID.strip()})
                    if len(Y_values) > len(Z_values):
                        for y in Y_values[min_length:]:
                            pairs.append({'WAVELENGTH': y, 'BEAMLINE': Z_values[-1], 'PDBID': PDBID.strip()})
                    elif len(Z_values) > len(Y_values):
                        print(f"Row {line_number}: More Z values than Y values. Extra Z values are ignored.")
    
    df = pd.DataFrame(pairs)
    return df

if __name__ == "__main__":
    pool = Pool(os.cpu_count())
    PDBIDs = makeQuery()
    print(f"Found {len(PDBIDs)} X-ray entries to fetch")
    wavelengthList = list(
        tqdm.tqdm(pool.imap_unordered(fetch_pdb_details, PDBIDs), total=len(PDBIDs))
    )
    with open("allinfoout.csv", "w") as file:
        for value in wavelengthList:
            if value is None:
                continue
            for secondval in value:
                if secondval is not None:
                    file.write(str(secondval) + '\n')

    df = process_file("allinfoout.csv")
    df.to_csv("wl_bl_id.csv", index=False)
