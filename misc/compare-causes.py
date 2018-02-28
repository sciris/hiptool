"""
Compares causes listed for GBD vs. DCP.
"""

gbdfile = 'gbd-causes.txt'
dcpfile = 'dcp-causes.txt'

def loadfile(filename):
    with open(filename) as f:
        output = f.readlines()
    for i,o in enumerate(output):
        output[i] = o.rstrip()
    return output

gbdcauses = loadfile(gbdfile)
dcpcauses = loadfile(dcpfile)

# Find matching causes
sharedcauses = []
dcponlycauses = []
for dcpcause in dcpcauses:
    if dcpcause in gbdcauses:
        sharedcauses.append(dcpcause)
    else:
        dcponlycauses.append(dcpcause)

# Output
print('\n\nShared causes:\n')
for i,cause in enumerate(sharedcauses):
    print('%3i. %s' % (i,cause))

print('\n\nDCP-only causes:\n')
for i,cause in enumerate(dcponlycauses):
    print('%3i. %s' % (i,cause))

print('\n\nGBD-only causes:\n')
for i,cause in enumerate(gbdcauses):
    print('%3i. %s' % (i,cause))

