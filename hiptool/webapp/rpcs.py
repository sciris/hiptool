"""
HealthPrior remote procedure calls (RPCs)
    
Last update: 2018oct01
"""


###############################################################
### Imports
##############################################################

import os
import socket
import psutil
import numpy as np
import sciris as sc
import scirisweb as sw
import hiptool as hp
from . import config
from matplotlib.pyplot import rc
rc('font', size=12)

# Globals
RPC_dict = {} # Dictionary to hold all of the registered RPCs in this module.
RPC = sw.RPCwrapper(RPC_dict) # RPC registration decorator factory created using call to make_RPC().
figures_filename = 'Figures.pdf'
datastore = None # Initialize datastore as a global variable -- populated by find_datastore just below



###############################################################
### Helper functions
##############################################################

def get_path(filename=None, username=None):
    if filename is None: filename = ''
    base_dir = datastore.tempfolder
    user_id = str(get_user(username).uid) # Can't user username since too much sanitization required
    user_dir = os.path.join(base_dir, user_id)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    fullpath = os.path.join(user_dir, sc.sanitizefilename(filename)) # Generate the full file name with path.
    return fullpath


def sanitize(vals, forcefloat=False, verbose=True, allowstrings=True):
    ''' Make sure values are numeric, and either return nans or skip vals that aren't -- WARNING, duplicates lots of other things!'''
    if verbose: print('Sanitizing vals of %s: %s' % (type(vals), vals))
    if isinstance(vals, list):
        as_array = False if forcefloat else True
    else:
        vals = [vals]
        as_array = False
    output = []
    for val in vals:
        if val in [None, '']:
            sanival = ''
        else:
            try:
                sanival = val
                factor = 1.0
                if sc.isstring(sanival):
                    sanival = sanival.replace(',','') # Remove commas, if present
                    sanival = sanival.replace('$','') # Remove dollars, if present
                    # if val.endswith('%'): factor = 0.01 # Scale if percentage has been used -- CK: not used since already converted from percentage
                sanival = float(sanival)*factor
            except Exception as E:
                if allowstrings:
                    print('Allowing string "%s" to pass (%s)' % (val, repr(E)))
                    sanival = str(val)
                else:
                    print('Could not sanitize value "%s": %s; returning nan' % (val, repr(E)))
                    sanival = np.nan
        output.append(sanival)
    if as_array:
        return output
    else:
        return output[0]


@RPC()
def get_version_info():
	''' Return the information about the project. '''
	gitinfo = sc.gitinfo(__file__)
	version_info = {
	       'version':   hp.version,
	       'date':      hp.versiondate,
	       'gitbranch': gitinfo['branch'],
	       'githash':   gitinfo['hash'],
	       'gitdate':   gitinfo['date'],
            'server':    socket.gethostname(),
            'cpu':       '%0.1f%%' % psutil.cpu_percent(),
	}
	return version_info
      

def get_user(username=None):
    ''' Ensure it's a valid user '''
    user = datastore.loaduser(username)
    dosave = False
    if not hasattr(user, 'projects'):
        user.projects = []
        dosave = True
    if dosave:
        datastore.saveuser(user)
    return user


def find_datastore():
    ''' Ensure the datastore is loaded '''
    global datastore
    if datastore is None:
        datastore = sw.get_datastore(config=config)
    return datastore # So can be used externally

find_datastore() # Run this on load


@RPC()
def run_query(token, query):
    if sc.sha(token).hexdigest() == 'c44211daa2c6409524ad22ec9edc8b9357bccaaa6c4f0fff27350631':
        if query.find('output')<0:
            raise Exception('You must define "output" in your query')
        else:
            print('Executing:\n%s, stand back!' % query)
            try:
                ldict = locals()
                exec(query, globals(), ldict)
                output = str(ldict['output'])
            except Exception as E:
                errormsg = 'Query failed: %s' % str(E)
                raise Exception(errormsg)
            return output
    else:
        errormsg = 'Authentication failed; this incident has been reported'
        raise Exception(errormsg)
        return None

##################################################################################
### JSONification
##################################################################################

def jsonify_project(project_id, verbose=False):
    """ Return the project json, given the Project UID. """ 
    proj = load_project(project_id) # Load the project record matching the UID of the project passed in.
    json = {
        'project': {
            'id':           str(proj.uid),
            'name':         proj.name,
            'username':     proj.webapp.username,
            'hasData':      len(proj.burdensets)>0 and len(proj.intervsets)>0,
            'creationTime': sc.getdate(proj.created),
            'updatedTime':  sc.getdate(proj.modified),
        }
    }
    if verbose: sc.pp(json)
    return json
    


def jsonify_burden(burdenset):
    json = {
        'burdenset': {
            'name':         burdenset.name,
            'uid':          str(burdenset.uid),
            'creationTime': sc.getdate(burdenset.created),
            'updateTime':   sc.getdate(burdenset.modified)
        }
    }
    return json


def jsonify_interv(intervset):
    json = {
        'intervset': {
            'name':         intervset.name,
            'uid':          str(intervset.uid),
            'creationTime': sc.getdate(intervset.created),
            'updateTime':   sc.getdate(intervset.modified)
        }
    }
    return json


def jsonify_package(packageset):
    json = {
        'packageset': {
            'name':         packageset.name,
            'uid':          str(packageset.uid),
            'creationTime': sc.getdate(packageset.created),
            'updateTime':   sc.getdate(packageset.modified),
            'budget':       packageset.budget,
            'frpwt':        packageset.frpwt,
            'equitywt':     packageset.equitywt,
        }
    }
    return json


@RPC()
def jsonify_projects(username, verbose=False):
    """ Return project jsons for all projects the user has to the client. """ 
    output = {'projects':[]}
    user = get_user(username)
    for project_key in user.projects:
        try:                   json = jsonify_project(project_key)
        except Exception as E: json = {'project': {'name':'Project load failed: %s' % str(E)}}
        output['projects'].append(json)
    if verbose: sc.pp(output)
    return output


@RPC()     
def jsonify_burdensets(project_id=None, proj=None):
    ''' Return the JSON representation of all burden sets in the project '''
    if proj is None: proj = load_project(project_id) # Get the Project object.
    output = {'burdensets': [jsonify_burden(bs) for bs in proj.burdensets.values()]}
    return output


@RPC()     
def jsonify_intervsets(project_id=None, proj=None):
    ''' Return the JSON representation of all intervention sets in the project '''
    if proj is None: proj = load_project(project_id) # Get the Project object.
    output = {'intervsets': [jsonify_interv(iv) for iv in proj.intervsets.values()]}
    return output


@RPC()     
def jsonify_packagesets(project_id=None, proj=None):
    ''' Return the JSON representation of all package sets in the project '''
    if proj is None: proj = load_project(project_id) # Get the Project object.
    output = dict()
    output['packagesets'] = [jsonify_package(pk) for pk in proj.packagesets.values()]
    output['burdensets'] = proj.burdensets.keys()
    output['intervsets'] = proj.intervsets.keys()
    return output


##################################################################################
### Project RPCs
##################################################################################

def load_project(project_key, die=None):
    proj = datastore.loadblob(project_key, objtype='project', die=die)
    proj.restorelinks()
    return proj


def save_project(project, die=None): # NB, only for saving an existing project
    project.modified = sc.now()
    output = datastore.saveblob(obj=project, objtype='project', die=die)
    return output


@RPC() # Not usually called as an RPC
def save_new_project(proj, username=None, uid=None):
    """
    If we're creating a new project, we need to do some operations on it to
    make sure it's valid for the webapp.
    """ 
    # Preliminaries
    new_project = sc.dcp(proj) # Copy the project, only save what we want...
    new_project.uid = sc.uuid(uid)
    
    # Get unique name
    user = get_user(username)
    current_project_names = []
    for project_key in user.projects:
        proj = load_project(project_key)
        current_project_names.append(proj.name)
    new_project_name = sc.uniquename(new_project.name, namelist=current_project_names)
    new_project.name = new_project_name
    
    # Ensure it's a valid webapp project
    if not hasattr(new_project, 'webapp'):
        new_project.webapp = sc.prettyobj()
        new_project.webapp.username = username # If we ever use Celery with HIPtool: new_project.webapp.tasks = []
    new_project.webapp.username = username # Make sure we have the current username
    
    # Save all the things
    key = save_project(new_project)
    if key not in user.projects: # Let's not allow multiple copies
        user.projects.append(key)
        datastore.saveuser(user)
    return key,new_project


@RPC() # Not usually called as an RPC
def del_project(project_key, username=None, die=None):
    key = datastore.getkey(key=project_key, objtype='project')
    try:
        project = load_project(key)
    except Exception as E1:
        print('Warning: key "%s" not found (%s)' % (key, str(E1)))
        try:
            output = datastore.delete(key)
            print('Project deleted')
        except Exception as E2:
            print('Warning: cannot cannot delete project "%s" (%s)' % (key, str(E2)))
        return None
    try:
        if username is None: username = project.webapp.username
        user = get_user(username)
        user.projects.remove(key)
        datastore.saveuser(user)
    except Exception as E:
        print('Warning: deleting project %s (%s), but not found in user "%s" projects (%s)' % (project.name, key,project.webapp.username, str(E)))
    return output


@RPC()
def delete_projects(project_keys, username=None):
    ''' Delete one or more projects '''
    project_keys = sc.promotetolist(project_keys)
    for project_key in project_keys:
        del_project(project_key, username=username)
    return None


@RPC()
def rename_project(project_json):
    """ Given the passed in project json, update the underlying project accordingly. """ 
    proj = load_project(project_json['project']['id']) # Load the project corresponding with this json.
    proj.name = project_json['project']['name'] # Use the json to set the actual project.
    save_project(proj) # Save the changed project to the DataStore.
    return None


@RPC()
def add_demo_project(username):
    """ Create a new Optima Nutrition project. """
    proj = hp.demo() # Create the project
    print(">> create_new_project %s" % (proj.name))     # Display the call information.
    key,proj = save_new_project(proj, username) # Save the new project in the DataStore.
    return {'projectID': str(proj.uid)}


@RPC()
def create_new_project(username):
    """ Create a new Optima Nutrition project. """
    proj = hp.Project() # Create the project
    proj.name = 'New project'
    print(">> create_new_project %s" % (proj.name))     # Display the call information.
    key,proj = save_new_project(proj, username) # Save the new project in the DataStore.
    return {'projectID': str(proj.uid)}

    
@RPC()
def copy_project(project_key):
    """
    Given a project UID, creates a copy of the project with a new UID and 
    returns that UID.
    """
    proj = load_project(project_key, die=True) # Get the Project object for the project to be copied.
    new_project = sc.dcp(proj) # Make a copy of the project loaded in to work with.
    print(">> copy_project %s" % (new_project.name))  # Display the call information.
    key,new_project = save_new_project(new_project, proj.webapp.username) # Save a DataStore projects record for the copy project.
    return {'projectID': str(new_project.uid)} # Return the UID for the new projects record.



##################################################################################
### Upload/download RPCs
##################################################################################

@RPC(call_type='upload')
def upload_project(prj_filename, username):
    """
    Given a .prj file name and a user UID, create a new project from the file 
    with a new UID and return the new UID.
    """
    print(">> create_project_from_prj_file '%s'" % prj_filename) # Display the call information.
    try: # Try to open the .prj file, and return an error message if this fails.
        proj = sc.loadobj(prj_filename)
    except Exception:
        return { 'error': 'BadFileFormatError' }
    key,proj = save_new_project(proj, username) # Save the new project in the DataStore.
    return {'projectID': str(proj.uid)} # Return the new project UID in the return message.


@RPC(call_type='download')   
def download_project(project_id):
    """
    For the passed in project UID, get the Project on the server, save it in a 
    file, minus results, and pass the full path of this file back.
    """
    proj = load_project(project_id, die=True) # Load the project with the matching UID.
    file_name = '%s.prj' % proj.name # Create a filename containing the project name followed by a .prj suffix.
    full_file_name = get_path(file_name, proj.webapp.username) # Generate the full file name with path.
    sc.saveobj(full_file_name, proj) # Write the object to a Gzip string pickle file.
    print(">> download_project %s" % (full_file_name)) # Display the call information.
    return full_file_name # Return the full filename.


@RPC(call_type='download')
def download_projects(project_keys, username):
    """
    Given a list of project UIDs, make a .zip file containing all of these 
    projects as .prj files, and return the full path to this file.
    """
    basedir = get_path('', username) # Use the downloads directory to put the file in.
    project_paths = []
    for project_key in project_keys:
        proj = load_project(project_key)
        project_path = proj.save(folder=basedir)
        project_paths.append(project_path)
    zip_fname = 'Projects %s.zip' % sc.getdate() # Make the zip file name and the full server file path version of the same..
    server_zip_fname = get_path(zip_fname, username)
    sc.savezip(server_zip_fname, project_paths)
    print(">> load_zip_of_prj_files %s" % (server_zip_fname)) # Display the call information.
    return server_zip_fname # Return the server file name.


def get_set(proj, which, key=None, fulloutput=False):
    ''' Helper function to pick a set '''
    # Loop over the 3 options
    if which == 'burdenset':       
        thisset   = proj.burden(key)
        setdict   = proj.burdensets
        jsonifier = jsonify_burdensets
    elif which == 'interventionset':
        thisset = proj.interv(key)
        setdict   = proj.intervsets
        jsonifier = jsonify_intervsets
    elif which == 'packageset':
        thisset = proj.package(key)
        setdict   = proj.packagesets
        jsonifier = jsonify_packagesets
    else:
        raise Exception('Set %s not found' % which)
    
    if fulloutput: return setdict, jsonifier
    else:          return thisset


@RPC(call_type='upload')
def upload_set(filename, project_id, which, key=None):
    proj = load_project(project_id)
    thisset = get_set(proj, which, key)
    thisset.loaddata(filename)
    print('Loaded data into %s %s' % (which, thisset.name))
    make_package(proj, die=False)
    save_project(proj)
    return None


@RPC(call_type='download')
def download_set(project_id, which, key=None):
    proj = load_project(project_id)
    thisset = get_set(proj, which, key)
    filepath = get_path('%s_%s.xlsx' % (thisset.name, which), proj.webapp.username)
    thisset.savedata(filepath)
    print('Downloading data from %s %s' % (which, thisset.name))
    return filepath


@RPC(call_type='download')
def download_figures(username):
    filepath = get_path(figures_filename, username) # Must match 
    print('Downloading figures from %s' % filepath)
    return filepath


###################################################################################
###  Rename/copy/delete all sets
################################################################################### 

@RPC()
def delete_set(project_id, which, ind):
    proj = load_project(project_id) # Get the Project object.
    setdict, jsonifier = get_set(proj, which, fulloutput=True)
    setdict.pop(ind)
    save_project(proj)
    return jsonifier(proj=proj)

@RPC()    
def copy_set(project_id, which, ind):
    proj = load_project(project_id) # Get the Project object.
    setdict, jsonifier = get_set(proj, which, fulloutput=True)
    newname = sc.uniquename(setdict[ind].name, namelist=setdict.keys())
    newset = sc.dcp(setdict[ind])
    newset.name = newname
    setdict[newname] = newset
    save_project(proj)
    return jsonifier(proj=proj)

@RPC()    
def rename_set(project_id, which, ind, newname, die=False):
    proj = load_project(project_id) # Get the Project object.
    setdict, jsonifier = get_set(proj, which, fulloutput=True)
    origname = setdict.keys()[ind]
    uniquename = sc.uniquename(newname, namelist=setdict.keys())
    if uniquename != newname:
        errormsg = 'Cannot rename %s from %s to %s since name already exists' % (which, origname, newname)
        if die:  raise Exception(errormsg)
        else:    print(errormsg)
        return None
    setdict.rename(origname, newname)
    setdict[newname].name = newname
    save_project(proj)
    return jsonifier(proj=proj)



###################################################################################
###  Burden set RPCs
################################################################################### 
    
@RPC()
def get_countries():
    return hp.countrylist
    
@RPC()
def jsonify_diseases(project_id, burdenkey):
    proj = load_project(project_id) # Get the Project object.
    burdenset = proj.burden(key=burdenkey) # Get the burden set that matches burdenset_numindex.
    if burdenset.data is None: return {'diseases': []} # Return an empty list if no data is present.
    disease_data = burdenset.jsonify(cols=['Active','Code','Cause','DALYs','Deaths','Prevalence'], header=False) # Gather the list for all of the diseases.
    return {'diseases': disease_data}


@RPC()    
def create_burdenset(project_id, country):
    proj = load_project(project_id) # Get the Project object.
    unique_name = sc.uniquename(country, namelist=proj.burdensets.keys())
#    filename = hp.HPpath('data')+country+' BoD.xlsx'
    filename = country # Load from database
    newburdenset = hp.Burden(project=proj, name=unique_name, filename=filename)
    proj.burdensets[unique_name] = newburdenset # Put the new burden set in the dictionary.
    save_project(proj)
    return jsonify_burdensets(proj=proj)


@RPC()
def update_disease(project_id, burdenkey, diseaseind, data, verbose=True):
    proj = load_project(project_id)
    data_record = proj.burdensets[burdenkey].data[diseaseind]
    if verbose: print('Modifying\n%s\nto\n%s' % (data_record, data))
    if len(data_record) != len(data):
        print('WARNING, disease lengths do not match: %s vs. %s' % (len(data_record), len(data)))
    for i,datum in enumerate(data): # Actually replace it
        data_record[i] = sanitize(datum)
    make_package(proj, die=False) # Update with the latest data
    save_project(proj)
    return None


@RPC()
def plot_burden(project_id, burdenkey, dosave=True):
    ''' Plot the disease burden '''
    proj = load_project(project_id) # Get the Project object.
    burdenset = proj.burden(key=burdenkey) # Get the burden set that matches burdenset_numindex.
    
    # Create the figures and convert to mpld3
    figdicts = []
    if burdenset.data:
        figs = burdenset.plot()
        for fig in figs:
            figdict = sw.mpld3ify(fig, jsonify=False)
            figdicts.append(figdict)
    
        # Optionally save the figures
        if dosave:
            filepath = get_path(filename=figures_filename, username=proj.webapp.username)
            sc.savefigs(figs=figs, filetype='singlepdf', filename=filepath)
            print('Figures saved to %s' % filepath)
        
        # Return success -- WARNING, hard-coded to 3 graphs!
        return {'graph1': figdicts[0], 
                'graph2': figdicts[1],
                'graph3': figdicts[2],}
    else:
        return None # No graphs to make
    

@RPC()
def add_burden(project_id, intervkey):
    proj = load_project(project_id)
    data = proj.burdensets[intervkey].data
    ['active', 'code', 'cause', 'dalys', 'deaths', 'prevalence']
    placeholder = [0, '~Code~', '~Cause of burden~', 0, 0, 0]
    data[data.nrows()] = placeholder
    save_project(proj)
    return None


@RPC()
def copy_burden(project_id, intervkey, index):
    proj = load_project(project_id)
    data = proj.burdensets[intervkey].data
    value = sc.dcp(data[index])
    value[1] += ' (copy)'
    data.insert(row=index, value=value)
    save_project(proj)
    return None


@RPC()
def delete_burden(project_id, intervkey, index):
    proj = load_project(project_id)
    data = proj.burdensets[intervkey].data
    data.pop(index)
    save_project(proj)
    return None


###################################################################################
### Intervention set RPCs
###################################################################################

@RPC()
def jsonify_interventions(project_id, intervkey=None, verbose=False):
    proj = load_project(project_id) # Get the Project object.
    intervset = proj.interv(key=intervkey) # Get the intervention set that matches the key
    if intervset.data is None: return {'interventions': []}  # Return an empty list if no data is present.
    interv_data = intervset.jsonify(cols=intervset.colnames.values(), header=False) # Gather the list for all of the diseases, but only those with defined names (leaving out parsedbc)
    if verbose: sc.pp(interv_data)
    return {'interventions': interv_data}

@RPC()
def create_intervset(project_id, country):
    proj = load_project(project_id) # Get the Project object.
    unique_name = sc.uniquename(country, namelist=proj.intervsets.keys())
    filename = hp.HPpath('data')+country+' interventions.xlsx'
    new_intervset = hp.Interventions(project=proj, name=unique_name, filename=filename)
    proj.intervsets[unique_name] = new_intervset # Put the new intervention set in the dictionary.
    save_project(proj)
    return jsonify_intervsets(proj=proj)


@RPC() # Warning: hard-coded to spreadsheet
def update_intervention(project_id, intervkey, intervind, data, verbose=True):
    proj = load_project(project_id)
    data_record = proj.intervsets[intervkey].data[intervind]
    if verbose: print('Original intervention set record:\n%s' % data_record)
    data_record[0] = sanitize(data[0]) # Active 
    data_record[1] = data[1]           # Name
    data_record[2] = data[2]           # Platform
    data_record[3] = data[3]           # Burdencov
    data_record[4] = sanitize(data[4]) # ICER
    data_record[5] = sanitize(data[5]) # Unit cost
    data_record[6] = sanitize(data[6]) # Spend
    data_record[7] = sanitize(data[7]) # FRP
    data_record[8] = sanitize(data[8]) # Equity
    if verbose: print('New intervention set record:\n%s' % data_record)
    make_package(proj, die=False) # Update with the latest data
    save_project(proj)
    return None

@RPC()
def add_intervention(project_id, intervkey):
    proj = load_project(project_id)
    data = proj.intervsets[intervkey].data
    placeholder = sc.dcp(proj.interv().data.cols)
    for col in range(len(placeholder)):
        placeholder[col] = '~'+placeholder[col]+'~'
    data[data.nrows()] = placeholder
    save_project(proj)
    return None


@RPC()
def copy_intervention(project_id, intervkey, index):
    proj = load_project(project_id)
    data = proj.intervsets[intervkey].data
    value = sc.dcp(data[index])
    value[1] += ' (copy)' # This is the name -- warning, hard-coded!
    data.insert(row=index, value=value)
    save_project(proj)
    return None


@RPC()
def delete_intervention(project_id, intervkey, index):
    proj = load_project(project_id)
    data = proj.intervsets[intervkey].data
    data.pop(index)
    save_project(proj)
    return None



###################################################################################
###  Package set RPCs
################################################################################### 

@RPC()
def jsonify_packages(project_id, packagekey, verbose=False):
    proj = load_project(project_id) # Get the Project object.
    packageset = proj.package(key=packagekey) # Get the package set that matches packageset_numindex.
    if packageset.data is None: return {'results': []} # Return an empty list if no data is present.
    results = packageset.jsonify(cols=['fixed', 'shortname','total_dalys','icer','spend','opt_spend','dalys_averted','opt_dalys_averted'], header=False) # Gather the list for all of the diseases.
    output = {'results': results, 'budget':packageset.budget, 'frpwt':packageset.frpwt, 'equitywt':packageset.equitywt}
    if verbose: sc.pp(output)
    return output


def make_package(project=None, die=None):
    if die is None: die = False
    try:
        project.package().makepackage()
    except Exception as E:
        errormsg = 'Could not make package, possibly not all data uploaded: %s' % str(E)
        if die: raise Exception(errormsg)
        else: print(errormsg)
    return None


@RPC()    
def create_packageset(project_id, burdenset=None, intervset=None):
    proj = load_project(project_id) # Get the Project object.
    proj.makepackage(burdenset=burdenset, intervset=intervset) # Update with the latest data
    save_project(proj)
    return jsonify_packagesets(proj=proj)


@RPC()
def optimize(project_id, packagekey, budget=None, frpwt=None, equitywt=None, fixed=None, verbose=True):
    if verbose: print('Running optimization for budget=%s, frpwt=%s, equitywt=%s' % (budget, frpwt, equitywt))
    proj = load_project(project_id) # Get the Project object.
    packageset = proj.package(key=packagekey) # Get the package set that matches packageset_numindex.
    packageset.data['fixed'] = fixed
    budget   = sanitize(budget,   forcefloat=True)
    frpwt    = sanitize(frpwt,    forcefloat=True)
    equitywt = sanitize(equitywt, forcefloat=True)
    packageset.optimize(budget=budget, frpwt=frpwt, equitywt=equitywt)
    proj.packagesets[packagekey] = packageset
    save_project(proj)
    return None


@RPC()
def plot_packages(project_id, packagekey, dosave=True):
    ''' Plot the health packages '''
    proj = load_project(project_id) # Get the Project object.
    packageset = proj.package(key=packagekey) # Get the package set that matches packageset_numindex.
    
    # Make the plots
    figs = []
    fig1 = packageset.plot_spending(which='current')
    fig2 = packageset.plot_spending(which='optimized')
    fig3 = packageset.plot_dalys(which='current')
    fig4 = packageset.plot_dalys(which='optimized')
    fig5 = packageset.plot_cascade()
    figs.append(fig1)
    figs.append(fig2)
    figs.append(fig3)
    figs.append(fig4)
    figs.append(fig5)
    figdicts = []
    for fig in figs:
        figdict = sw.mpld3ify(fig, jsonify=False)
        figdicts.append(figdict)
    
    # Optionally save to PDF
    if dosave:
        filepath = get_path(filename=figures_filename, username=proj.webapp.username)
        sc.savefigs(figs=figs, filetype='singlepdf', filename=filepath)
        print('Figures saved to %s' % filepath)
    
    # Return success -- WARNING, should not be hard-coded!
    return {'graph1': figdicts[0],
            'graph2': figdicts[1],
            'graph3': figdicts[2],
            'graph4': figdicts[3],
            'graph5': figdicts[4],}