import pandas as pd

data = pd.read_csv('longWavelengthExperiments_filtererd.csv')
data.columns = ['PDBID', 'LAMBDA']
threshold = 1.7

sorted_data = data.sort_values(by='LAMBDA', ascending=False)

filtered_data = sorted_data[sorted_data['LAMBDA'] > threshold]

print(filtered_data)