import sciris as sc

interv_data = sc.loadspreadsheet('rapid_interventions.xlsx')
spend_data = sc.loadspreadsheet('rapid_spending.xlsx')
R = sc.loadobj('results/rapid_results.obj')

i_int_names = set(interv_data['Short name'].tolist())
s_int_names = set(spend_data['Short name'].tolist())

print(f'Matching:\n{i_int_names.intersection(s_int_names)}\n')
print(f'Extra:\n{s_int_names-i_int_names}\n')
print(f'Missing:\n{i_int_names-s_int_names}\n')