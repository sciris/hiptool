"""
This script demonstrates example usage of HealthPrior.

Version: 2018feb28
"""

from hptool import Project, HPpath

dp = HPpath('data')
P = Project(burdenfile=dp+'ihme-gbd.xlsx', interventionsfile=dp+'dcp-data.xlsx')

P.burden().popsize = 36373.176 # From UN population division

print('\n\nExample burden entry:\n\n%s' % P.burdensets[0].data[37])

print('\n\nExample interventions entry:\n\n%s' % P.intersets[0].data[37])

P.burden().plottopcauses(axsize=(0.55, 0.15, 0.4, 0.8), figsize=(15,5))
#P.burden().plottopcauses(which='prevalence', n=15)