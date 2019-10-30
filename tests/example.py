"""
This script demonstrates example usage of HIPtool.

Usage:

python3 -i example.py

Version: 2019may22
"""

import hiptool as hp
import pylab as pl

dosave = False # Whether or not to save an example data file
doplot = False # Whether or not to plot


dp = hp.HPpath('data')
P = hp.Project()
P.loadburden(filename=dp+'Demo BoD.xlsx')
P.loadinterventions(filename=dp+'Demo interventions.xlsx')
print('\n\nExample burden entry:\n\n%s' % P.burdensets[0].data[27])
print('\n\nExample interventions entry:\n\n%s' % P.intervsets[0].data[27])

P.makepackage()
P.package().optimize()
df = P.package().data
df.sort(col='shortname')


if dosave:
    P.burden().savedata('temp.xlsx')

# Ploting
if doplot:
    P.burden().plot()

    fig1 = P.package().plot_spending(which='current')
    fig2 = P.package().plot_spending(which='optimized')
    fig3 = P.package().plot_dalys(which='current')
    fig4 = P.package().plot_dalys(which='optimized')
    fig5 = P.package().plot_cascade()
    pl.show()
    
print('Done')


# More examples
# dd = P.burden().export(cols=['cause','dalys','deaths','prevalence'])
# P.burden().plottopcauses(which='prevalence', n=15)