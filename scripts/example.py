"""
This script demonstrates example usage of HealthPrior.

Version: 2018feb28
"""

from hptool import Project, HPpath
from pylab import show

dp = HPpath('data')
P = Project(burdenfile=dp+'ihme-gbd.xlsx', interventionsfile=dp+'dcp-data-afg-v1.xlsx')

P.burden().popsize = 36373.176 # From UN population division

print('\n\nExample burden entry:\n\n%s' % P.burdensets[0].data[37])

print('\n\nExample interventions entry:\n\n%s' % P.intersets[0].data[37])

P.burden().plottopcauses()
P.package().plot_dalys()
#P.burden().plottopcauses(which='prevalence', n=15)
# dd = P.burden().export(cols=['cause','dalys','deaths','prevalence'])

show()