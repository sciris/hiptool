# -*- coding: utf-8 -*-
"""
This file performs all necessary imports, so HealthPrior (HP) can be used either as

from hptool import Project
or
import hptool as hp
or
from hptool import *

Now, the legal part:

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Version: 2018mar19
"""

# Specify the version, for the purposes of figuring out which version was used to create a project
from .version import version, versiondate

# Print the license
HPlicense = 'HealthPrior %s (%s)' % (version, versiondate)
print(HPlicense)

#####################################################################################################################
### Load helper functions/modules
#####################################################################################################################

# Utilities -- import all
from sciris.utils import *
from sciris.colortools import *
from sciris.fileio import *

#####################################################################################################################
### Define debugging and exception functions/classes
#####################################################################################################################

# Tool path
def HPpath(subdir=None, trailingsep=True):
    ''' Returns the parent path of the HealthPrior module. If subdir is not None, include it in the path '''
    import os
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    if subdir is not None:
        tojoin = [path, subdir]
        if trailingsep: tojoin.append('') # This ensures it ends with a separator
        path = os.path.join(*tojoin) # e.g. ['/home/optima', 'tests', '']
    return path


# Debugging information
def debuginfo(dooutput=False, shalength=7):
    output = '\nHealthPrior debugging info:\n'
    output += '   Version: %s\n' % version
    output += '   Branch:  %s\n' % gitinfo()[0]
    output += '   SHA:     %s\n' % gitinfo()[1][:shalength]
    output += '   Path:    %s\n' % HPpath()
    if dooutput: 
        return output
    else: 
        print(output)
        return None

class HPException(Exception):
    ''' A tiny class to allow for Optima-specific exceptions -- define this here to allow for Optima-specific info '''
    
    def __init__(self, errormsg, *args, **kwargs):
        if isinstance(errormsg, basestring): errormsg = errormsg+debuginfo(dooutput=True) # If it's not a string, not sure what it is, but don't bother with this
        Exception.__init__(self, errormsg, *args, **kwargs)



#####################################################################################################################
### Load HealthPrior functions and classes
#####################################################################################################################

# Core functions
default_key = -1 # Define what the default key is -- WARNING, move

from .burden import Burden
from .interventions import Interventions
from .healthpackage import HealthPackage
from .project import Project

# Webapp
import webapp




