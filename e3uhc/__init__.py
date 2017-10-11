from optima import makefilepath, odict

from .version import version, versiondate

from .loaddcp import Databook, loaddcp, e3uhcpath

# Print the license
e3uhclicense = 'E3UHC %s (%s) -- (c) Optima Consortium' % (version, versiondate)
print(e3uhclicense)


