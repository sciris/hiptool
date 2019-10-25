import pylab as pl
import sciris as sc
import hiptool as hp

doplot = False

P = hp.Project()
P.loadburden(filename='rapid_BoD.xlsx')
P.loadinterventions(filename='rapid_interventions.xlsx')
P.intervsets[0].data['Spending'] *= 0 # Set current spending to 0
ninterventions = P.intervsets[0].data.nrows
P.makepackage()