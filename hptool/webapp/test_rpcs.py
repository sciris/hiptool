###########################################################################
### Housekeeping
###########################################################################

import sciris as sc
import scirisweb as sw
import hptool as hp
from hptool.webapp import rpcs, main

torun = [
#'project_io',
'intervset_io',
]


###########################################################################
### Definitions
###########################################################################

def demoproj(proj_id, username):
    P = hp.demo()
    P.name = 'RPCs test %s' % proj_id[:6]
    P.uid = proj_id
    rpcs.save_new_project(P, username)
    return P

def heading(string, style=None):
    divider = '='*60
    sc.blank()
    if style == 'big': string = '\n'.join([divider, string, divider])
    sc.colorize('blue', string)
    return None


T = sc.tic()
app = main.make_app()
user = sw.make_default_users(app)[0] # WARNING, broken!
proj_id  = sc.uuid(as_string=True) # These can all be the same
proj = demoproj(proj_id, user.username)


###########################################################################
### Run the tests
###########################################################################

string = 'Starting tests for proj = %s' % proj_id
heading(string, 'big')


if 'project_io' in torun:
    heading('Running project_io', 'big')
    uid = rpcs.save_new_project(proj, user.username)
    P = rpcs.load_project_record(uid)
    print(P)



if 'intervset_io' in torun:
    heading('Running intervset_io', 'big')
    output = rpcs.get_project_interv_set_intervs(proj_id)
    sc.pp(output)


sc.toc(T)
print('Done.')