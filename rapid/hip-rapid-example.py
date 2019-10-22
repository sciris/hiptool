import hiptool as hp

P = hp.Project()
P.loadburden(filename='Demo BoD.xlsx')
P.loadinterventions(filename='CIV_interventions.xlsx')
P.intervsets[0].data['Spending'] *= 0 # Set current spending to 0
P.makepackage()

P.package().optimize()
df = P.package().data
df.sort(col='shortname')

print('Done')