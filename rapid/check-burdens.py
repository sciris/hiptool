import sciris as sc

bod = sc.loadobj('gbd-data.dat')

countrydata = sc.loadspreadsheet('country-data.xlsx')

bod_countries = set(bod.keys())
data_countries = set(countrydata['name'].tolist())

print(f'Matching:\n{data_countries.intersection(bod_countries)}\n')
print(f'Extra:\n{data_countries-bod_countries}\n')
print(f'Missing:\n{bod_countries-data_countries}\n')

print('Done.')