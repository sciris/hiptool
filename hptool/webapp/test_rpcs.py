###########################################################################
### Housekeeping
###########################################################################

import pylab as pl
import sciris as sc
import atomica.ui as au
from atomica_apps import rpcs, main
pl.switch_backend('Qt4Agg')

torun = [
'project_io',
]


# Set parameters
tool = ['tb','cascade'][1] # Change this to change between TB and Cascade
default_which = {'tb':'tb', 'cascade':'hypertension'}[tool]
user_id  = '12345678123456781234567812345678' # This is the hard-coded UID of the "demo" user
proj_id  = sc.uuid(as_string=True) # These can all be the same
cache_id = sc.uuid(as_string=True) # These can all be the same


###########################################################################
### Definitions
###########################################################################

def demoproj(which=None, online=True):
    if which is None: which = default_which
    P = au.demo(which=which)
    P.name = 'RPCs test %s' % proj_id[:6]
    if online:
        rpcs.save_project_as_new(P, user_id=user_id, uid=proj_id)
        rpcs.make_results_cache_entry(cache_id)
    return P

def heading(string, style=None):
    divider = '='*60
    sc.blank()
    if style == 'big': string = '\n'.join([divider, string, divider])
    sc.colorize('blue', string)
    return None



###########################################################################
### Run the tests
###########################################################################

string = 'Starting tests for:\n  tool = %s\n  which = %s\n  user = %s\n  proj = %s' % (tool, default_which, user_id, proj_id)
heading(string, 'big')
T = sc.tic()
app = main.make_app(which=tool)
proj = demoproj(which=default_which, online=True)


if 'project_io' in torun:
    heading('Running project_io', 'big')
    uid = rpcs.save_project_as_new(proj, user_id=user_id)
    P = rpcs.load_project_record(uid)
    print(P)