"""
This script demonstrates example usage of HealthPrior.

Version: 2018sep28
"""

from hptool import Project, HPpath
from pylab import show

doplot = False

dp = HPpath('data')
P = Project()
P.loadburden(filename=dp+'burdens-demo.xlsx')
P.loadinterventions(filename=dp+'interventions-demo.xlsx')
print('\n\nExample burden entry:\n\n%s' % P.burdensets[0].data[27])
print('\n\nExample interventions entry:\n\n%s' % P.intervsets[0].data[27])

P.makepackage()
P.package().optimize()


#P.package().plot_cascade()
#P.package().plot_spending()
#P.burden().plottopcauses(which='prevalence', n=15)
# dd = P.burden().export(cols=['cause','dalys','deaths','prevalence'])

# Ploting
if doplot:
#    P.burden().plot()
    fig1 = P.package().plot_spending()
    fig2 = P.package().plot_dalys()
    fig3 = P.package().plot_cascade()
    show()