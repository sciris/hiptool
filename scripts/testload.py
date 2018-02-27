from hpptool import Project, HPpath

dp = HPpath('data')
P = Project(burdenfile=dp+'ihme-gbd.xlsx', interventionsfile=dp+'dcp-data.xlsx')

print('\n\nExample burden entry:\n\n%s' % P.burdensets[0].data[37])

print('\n\nExample interventions entry:\n\n%s' % P.intersets[0].data[37])