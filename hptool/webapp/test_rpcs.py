###########################################################################
### Housekeeping
###########################################################################

import sciris as sc
import hptool as hp
from hptool.webapp import rpcs, main

torun = [
#'project_io',
'intervset_io',
]


# Set parameters
user_id  = '12345678123456781234567812345678' # This is the hard-coded UID of the "demo" user
proj_id  = sc.uuid(as_string=True) # These can all be the same


###########################################################################
### Definitions
###########################################################################

def demoproj(online=True):
    name = 'RPCs test %s' % proj_id[:6]
    P = hp.demo(name=name)
    if online:
        rpcs.save_project_as_new(P, user_id=user_id, uid=proj_id)
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

string = 'Starting tests for:\n  user = %s\n  proj = %s' % (user_id, proj_id)
heading(string, 'big')
T = sc.tic()
app = main.make_app()
proj = demoproj()


if 'project_io' in torun:
    heading('Running project_io', 'big')
    uid = rpcs.save_project_as_new(proj, user_id=user_id)
    P = rpcs.load_project_record(uid)
    print(P)



if 'intervset_io' in torun:
    heading('Running intervset_io', 'big')
    output = rpcs.get_project_interv_set_intervs(proj_id)
    sc.pp(output)