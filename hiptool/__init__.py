# -*- coding: utf-8 -*-
"""
This file performs all necessary imports, so HIPtool (HP) can be used either as

from hiptool import Project
or
import hiptool as hp
or
from hiptool import *

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


#####################################################################################################################
### Define debugging and exception functions/classes
#####################################################################################################################

# Tool path
def HPpath(subdir=None, trailingsep=True):
    ''' Returns the parent path of the HIPtool module. If subdir is not None, include it in the path '''
    import os
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    if subdir is not None:
        tojoin = [path, subdir]
        if trailingsep: tojoin.append('') # This ensures it ends with a separator
        path = os.path.join(*tojoin) # e.g. ['/home/optima', 'tests', '']
    return path


# Debugging information
def debuginfo(output=False):
    import sciris as sc
    outstr = '\nHIPtool debugging info:\n'
    outstr += '   Version: %s\n' % version
    outstr += '   Branch:  %s\n' % sc.gitinfo()['branch']
    outstr += '   SHA:     %s\n' % sc.gitinfo()['hash']
    outstr += '   Date:    %s\n' % sc.gitinfo()['date']
    outstr += '   Path:    %s\n' % HPpath()
    if output:
        return outstr
    else: 
        print(outstr)
        return None

class HPException(Exception):
    ''' A tiny class to allow for Optima-specific exceptions -- define this here to allow for Optima-specific info '''
    
    def __init__(self, errormsg, *args, **kwargs):
#        if isinstance(errormsg, basestring): errormsg = errormsg+debuginfo(output=True) # If it's not a string, not sure what it is, but don't bother with this
        Exception.__init__(self, errormsg, *args, **kwargs)


def arr(data):
    ''' Force float, or give helpful error '''
    import numpy as np
    try:
        output = np.array(data, dtype=float)
    except Exception as E:
        errormsg = 'Data contain non-numeric values (%s):\n%s' % (str(E), data)
        raise Exception(errormsg)
    return output

#####################################################################################################################
### Load HIPtool functions and classes
#####################################################################################################################

# Core functions
default_key = -1 # Define what the default key is -- WARNING, move

from .utils import getcountryburden, countrylist, causedict, twigcausedict
from .burden import Burden
from .interventions import Interventions
from .healthpackage import HealthPackage
from .project import Project, demo

# Import webapp
from . import webapp

# Print the license
HPlicense = 'HIPtool %s (%s)' % (version, versiondate)
print(HPlicense)

