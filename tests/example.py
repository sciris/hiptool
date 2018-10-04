"""
This script demonstrates example usage of HealthPrior.

Version: 2018oct04
"""

from hptool import Project, HPpath
from pylab import show

doplot = True

dp = HPpath('data')
P = Project()
P.loadburden(filename=dp+'Afghanistan BoD.xlsx')
P.loadinterventions(filename=dp+'Afghanistan interventions.xlsx')
print('\n\nExample burden entry:\n\n%s' % P.burdensets[0].data[27])
print('\n\nExample interventions entry:\n\n%s' % P.intervsets[0].data[27])

P.makepackage()
df = P.package().optimize()
df.sort(col='shortname')


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