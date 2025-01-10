import os
import pandas as pd
import requests
import solrq

cwd = os.getcwd()

def getPDBInfo() -> None:
    url = "https://www.ebi.ac.uk/pdbe/search/pdb/select?"
    query = solrq.Q(
        status="REL",
        experimental_method="X-ray diffraction",
        experiment_data_available="y",
        resolution=solrq.Range(0, 6),
        molecule_type="Protein",
    )
    filter_list = "pdb_id,resolution,percent_solvent,diffraction_wavelengths,synchrotron_beamline,synchrotron_site,data_collection_year,diffraction_protocol,diffraction_source_type"
    data = {"q": query, "fl": filter_list, "rows": 1000000, "wt": "json"}
    #data = {"q": query, "rows": 10, "wt": "json"} # prints without filter, makes huge file!
    response = requests.post(url, data=data, timeout=120)
    docs = response.json()["response"]["docs"]
    df = pd.DataFrame(docs)
    print(df.head())
    df.drop_duplicates(inplace=True, subset=["pdb_id"], keep="first")
    df.to_csv("entries.csv", index=False)


if __name__ == "__main__":
    getPDBInfo()
