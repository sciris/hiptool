from hpptool import Project, HPpath
P = Project(interventionsfile=HPpath('data')+'dcp-data.xlsx')
print('\n\nExample entry:\n\n%s' % P.intersets[0].data[37])