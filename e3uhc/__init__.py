from optima import makefilepath, odict

from .version import version, versiondate

#from .loaddcp import Databook, loaddcp
#
#def e3uhcpath(subdir=None, trailingsep=True):
#    ''' Returns the parent path of the E3UHC module. If subdir is not None, include it in the path '''
#    import os
#    path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
#    if subdir is not None:
#        tojoin = [path, subdir]
#        if trailingsep: tojoin.append('') # This ensures it ends with a separator
#        path = os.path.join(*tojoin) # e.g. ['/home/optima', 'tests', '']
#    return path

