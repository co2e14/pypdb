import pandas as pd
import pypdb as pp
import ast

data = pd.read_csv('longWavelengthExperiments_filtererd.csv')
data.columns = ['PDBID', 'LAMBDA']
threshold = 1.7

sorted_data = data.sort_values(by='LAMBDA', ascending=False)

synchrotron_PDBs = []

for pdbid in sorted_data['PDBID']:
    pdbinfo = pp.get_info(pdbid)
    try:
        diffrn_source = str(pdbinfo["diffrn_source"])
        for char in "[]":
            diffrn_source = diffrn_source.replace(char, "")
        length = diffrn_source.count("source")
        diffrn_source = ast.literal_eval(diffrn_source)
        if length <= 2:
            multi_source_out = []
            for dif_id in range(0, len(diffrn_source), 1):
                multi_source = diffrn_source[dif_id]
                multi_source_ = str(multi_source["pdbx_synchrotron_beamline"])
                multi_source_out += [multi_source_]
            diffrn_source = multi_source_out
        elif length == 1:
            diffrn_source = [str(diffrn_source["source"])]
        elif length == 0:
            diffrn_source = None
        else:
            pass
    except:
        diffrn_source = None
    if diffrn_source == None:
        pass
    elif diffrn_source == "SYNCHROTRON":
        synchrotron_PDBs += diffrn_source
    else:
        pass
        
print(len(synchrotron_PDBs))
        
filtered_data = sorted_data[sorted_data['LAMBDA'] > threshold]

filtered_data.to_csv(f'over_{str(threshold)}')

print(filtered_data[1])
    