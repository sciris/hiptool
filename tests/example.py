"""
This script demonstrates example usage of HealthPrior.

Version: 2018sep28
"""

from hptool import Project, HPpath
from pylab import show

dp = HPpath('data')
P = Project()

P.add_burden(filename=dp+'burdens-demo.xlsx')

print('\n\nExample burden entry:\n\n%s' % P.burdensets[0].data[37])

P.burden().plot()

#print('\n\nExample interventions entry:\n\n%s' % P.intervsets[0].data[37])

#P.burden().plottopcauses()
#P.package().plot_cascade()
#P.package().plot_spending()
#P.burden().plottopcauses(which='prevalence', n=15)
# dd = P.burden().export(cols=['cause','dalys','deaths','prevalence'])

show()