"""
This script demonstrates example usage of HealthPrior.

Version: 2018oct04
"""

from hptool import Project, HPpath
from pylab import show

doplot = False

dp = HPpath('data')
P = Project()
P.loadburden(filename=dp+'Zimbabwe BoD.xlsx')
P.loadinterventions(filename=dp+'Zimbabwe interventions.xlsx')
print('\n\nExample burden entry:\n\n%s' % P.burdensets[0].data[27])
print('\n\nExample interventions entry:\n\n%s' % P.intervsets[0].data[27])

P.makepackage()
P.package().optimize()
df = P.package().data
df.sort(col='shortname')



#P.burden().savedata('temp.xlsx')

#P.package().plot_cascade()
#P.package().plot_spending()
#P.burden().plottopcauses(which='prevalence', n=15)
# dd = P.burden().export(cols=['cause','dalys','deaths','prevalence'])

# Ploting
if doplot:
#    P.burden().plot()
#    fig1 = P.package().plot_spending(which='current')
#    fig2 = P.package().plot_spending(which='optimized')
    fig3 = P.package().plot_dalys(which='current')
    fig4 = P.package().plot_dalys(which='optimized')
#    fig5 = P.package().plot_cascade()
    show()