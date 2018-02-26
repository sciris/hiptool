from .version import version, versiondate

from .utils import makefilepath, odict

from .loaddcp import Databook, loaddcp, healthpriorpath

# Print the license
healthpriorlicense = 'HealthPrior %s (%s)' % (version, versiondate)
print(healthpriorlicense)


