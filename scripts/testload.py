from hpptool import Project
P = Project(interventionsfile='../data/dcp-data.xlsx')
print('\n\nExample entry:\n\n%s' % P.intersets[0].data[37])