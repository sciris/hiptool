"""
HealthPrior remote procedure calls (RPCs)
    
Last update: 2018sep22
"""


###############################################################
### Imports
##############################################################

import os
import numpy as np
import sciris as sc
import scirisweb as sw
import hptool as hp
from . import config
from matplotlib.pyplot import rc
rc('font', size=12)

# Globals
RPC_dict = {} # Dictionary to hold all of the registered RPCs in this module.
RPC = sw.makeRPCtag(RPC_dict) # RPC registration decorator factory created using call to make_RPC().
figures_filename = 'Figures.pdf'
datastore = None # Initialize datastore as a global variable
find_datastore() # Run this on load



###############################################################
### Helper functions
##############################################################

def find_datastore():
    ''' Ensure the datastore is loaded '''
    global datastore
    if datastore is None:
        datastore = sw.get_datastore(config=config)
    return datastore # So can be used externally


def get_path(filename=None, username=None):
    if filename is None: filename = ''
    base_dir = sw.flaskapp.datastore.tempfolder
    user_id = str(get_user(username).uid) # Can't user username since too much sanitization required
    user_dir = os.path.join(base_dir, user_id)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    fullpath = os.path.join(user_dir, filename) # Generate the full file name with path.
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



##################################################################################
### Project load/save/delete
##################################################################################

def load_project(project_key, die=None):
    output = datastore.loadblob(project_key, objtype='project', die=die)
    return output


def save_project(project, die=None): # NB, only for saving an existing project
    project.modified = sc.now()
    output = datastore.saveblob(obj=project, objtype='project', die=die)
    return output


def save_new_project(proj, username=None):
    """
    If we're creating a new project, we need to do some operations on it to
    make sure it's valid for the webapp.
    """ 
    # Preliminaries
    new_project = sc.dcp(proj) # Copy the project, only save what we want...
    new_project.modified = sc.now()
    new_project.uid = sc.uuid()
    
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
        new_project.webapp.username = username
        new_project.webapp.tasks = []
    
    # Save all the things
    key = save_project(new_project)
    user.projects.append(key)
    datastore.saveuser(user)
    return key,new_project


def del_project(project_key, die=None):
    key = datastore.getkey(key=project_key, objtype='project')
    project = load_project(key)
    user = get_user(project.webapp.username)
    output = datastore.delete(key)
    if key in user.projects:
        user.projects.remove(key)
    else:
        print('Warning: deleting project %s (%s), but not found in user "%s" projects' % (project.name, key, user.username))
    datastore.saveuser(user)
    return output


@RPC()
def delete_projects(project_keys):
    ''' Delete one or more projects '''
    project_keys = sc.promotetolist(project_keys)
    for project_key in project_keys:
        del_project(project_key)
    return None



##################################################################################
### Convert to JSON
##################################################################################

@RPC()
def project_json(project_id, verbose=False):
    """ Return the project summary, given the Project UID. """ 
    proj = load_project(project_id) # Load the project record matching the UID of the project passed in.
    json = {
        'project': {
            'id':           proj.uid,
            'name':         proj.name,
            'username':     proj.webapp.username,
            'hasData':      len(proj.datasets)>0,
            'creationTime': proj.created,
            'updatedTime':  proj.modified,
            'n_results':    len(proj.results),
            'n_tasks':      len(proj.webapp.tasks)
        }
    }
    if verbose: sc.pp(json)
    return json
    

@RPC()
def project_jsons(username, verbose=False):
    """ Return project summaries for all projects the user has to the client. """ 
    output = {'projects':[]}
    user = get_user(username)
    for project_key in user.projects:
        json = project_json(project_key)
        output['projects'].append(json)
    if verbose: sc.pp(output)
    return output


def jsonify_burden(burdenset):
    obj_info = {
        'burdenset': {
            'name':         burdenset.name,
            'uid':          burdenset.uid,
            'creationTime': burdenset.created,
            'updateTime':   burdenset.modified
        }
    }
    return obj_info


def jsonify_interv(intervset):
    obj_info = {
        'intervset': {
            'name':         intervset.name,
            'uid':          intervset.uid,
            'creationTime': intervset.created,
            'updateTime':   intervset.modified
        }
    }
    return obj_info


def jsonify_package(packageset):
    obj_info = {
        'packageset': {
            'name':         packageset.name,
            'uid':          packageset.uid,
            'creationTime': packageset.created,
            'updateTime':   packageset.modified
        }
    }
    return obj_info



##################################################################################
### Project RPCs
##################################################################################

@RPC()
def rename_project(project_summary):
    """ Given the passed in project summary, update the underlying project accordingly. """ 
    proj = load_project(project_summary['project']['id']) # Load the project corresponding with this summary.
    proj.name = project_summary['project']['name'] # Use the summary to set the actual project.
    proj.modified = sc.now() # Set the modified time to now.
    save_project(proj) # Save the changed project to the DataStore.
    return None


@RPC()
def add_demo_project(username):
    """ Add a demo Optima Nutrition project """
    proj = hp.demo()  # Create the project, loading in the desired spreadsheets.
    proj.name = 'Demo project'
    print(">> add_demo_project %s" % (proj.name)) # Display the call information.
    key,proj = save_new_project(proj, username) # Save the new project in the DataStore.
    return {'projectID': str(proj.uid)} # Return the new project UID in the return message.


#!!!FIX
@RPC(call_type='download')
def create_new_project(username, proj_name, *args, **kwargs):
    """ Create a new Optima Nutrition project. """
    proj = hp.Project() # Create the project
    print(">> create_new_project %s" % (proj.name))     # Display the call information.
    key,proj = save_new_project(proj, username) # Save the new project in the DataStore.
    file_name = '%s databook.xlsx' % proj.name # Create a filename containing the project name followed by a .prj suffix.
    full_file_name = get_path(file_name, username)
    proj.input_sheet.save(full_file_name)
    print(">> download_databook %s" % (full_file_name))
    return full_file_name

    
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
    copy_project_id = new_project.uid # Remember the new project UID (created in save_project_as_new()).
    return { 'projectId': copy_project_id } # Return the UID for the new projects record.



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
    return { 'projectId': str(proj.uid) } # Return the new project UID in the return message.


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


def get_set(proj, which, key):
    ''' Helper function to pick a set '''
    if   which == 'burdenset':       thisset = proj.burden(key)
    elif which == 'interventionset': thisset = proj.interv(key) # Full name since used in filenames
    elif which == 'packageset':      thisset = proj.package(key)
    else: raise Exception('Set %s not found' % which)
    return thisset
    

@RPC(call_type='upload')
def upload_set(filename, project_id, which, key=None):
    proj = load_project(project_id)
    thisset = get_set(proj, which, key)
    thisset.loaddata(filename)
    print('Loaded data into %s %s' % (which, thisset.name))
    proj.modified = sc.now()
    print('Updating health package...')
    proj.package().make_package()
    save_project(proj)
    return None
    
@RPC(call_type='download')
def download_set(project_id, which, key=None):
    proj = load_project(project_id)
    thisset = get_set(proj, which, key)
    filepath = get_path('%s_%s.xlsx' % (thisset.name, which))
    thisset.savedata(filepath)
    print('Downloading data from %s %s' % (which, thisset.name))
    return filepath

@RPC(call_type='download')
def download_figures():
    filepath = get_path(figures_filename) # Must match 
    print('Downloading figures from %s' % filepath)
    return filepath



###################################################################################
###  Burden set RPCs
################################################################################### 
    
@RPC()     
def get_project_burden_sets(project_id):
    # Get the Project object.
    proj = load_project(project_id)
    
    # Get a list of the Burden objects.
    burdensets = [proj.burdensets[ind] for ind in range(len(proj.burdensets))] 
    
    # Return the JSON-friendly result.
    return {'burdensets': map(get_burden_set_fe_repr, burdensets)}

@RPC()
def get_project_burden_set_diseases(project_id, burdenset_numindex):
    # Get the Project object.
    proj = load_project(project_id)
    
    # Get the burden set that matches burdenset_numindex.
    burdenset = proj.burden(key=burdenset_numindex)
    
    # Return an empty list if no data is present.
    if burdenset.data is None:
        return { 'diseases': [] }

    # Gather the list for all of the diseases.
    disease_data = burdenset.jsonify(cols=['active','cause','dalys','deaths','prevalence'], header=False)
    
    # Return success.
    return { 'diseases': disease_data }

@RPC()    
def create_burden_set(project_id, new_burden_set_name):

    def update_project_fn(proj):
        # Get a unique name (just in case the one provided collides with an 
        # existing one).
        unique_name = get_unique_name(new_burden_set_name, 
            other_names=list(proj.burdensets))
        
        # Create a new (empty) burden set.
        new_burden_set = hp.Burden(project=proj, name=unique_name)
                
        # Load data from the Excel spreadsheet.
        # NOTE: We may want to take this out later in favor leaving the 
        # new sets empty to start.
        data_path = hp.HPpath('data')
        new_burden_set.loaddata(data_path+'ihme-gbd.xlsx')
        
        # Put the new burden set in the dictionary.
        proj.burdensets[unique_name] = new_burden_set
        proj.package().make_package() # Update with the latest data
        
    # Do the project update using the internal function.
    update_project_with_fn(project_id, update_project_fn)

    # Return the new burden sets.
    return get_project_burden_sets(project_id)

@RPC()
def delete_burden_set(project_id, burdenset_numindex):

    def update_project_fn(proj):
        proj.burdensets.pop(burdenset_numindex)
        
    # Do the project update using the internal function.    
    update_project_with_fn(project_id, update_project_fn)   

@RPC()    
def copy_burden_set(project_id, burdenset_numindex):

    def update_project_fn(proj):
        # Get a unique name (just in case the one provided collides with an 
        # existing one).
        unique_name = get_unique_name(proj.burdensets[burdenset_numindex].name, 
            other_names=list(proj.burdensets))
        
        # Create a new burdenset which is a copy of the old one.
        new_burden_set = sc.dcp(proj.burdensets[burdenset_numindex])
        
        # Overwrite the old name with the new.
        new_burden_set.name = unique_name
       
        # Put the new burden set in the dictionary.
        proj.burdensets[unique_name] = new_burden_set
        
    # Do the project update using the internal function.  
    update_project_with_fn(project_id, update_project_fn)
    
    # Return the new burden sets.
    return get_project_burden_sets(project_id) 

@RPC()
def rename_burden_set(project_id, burdenset_numindex, new_burden_set_name):

    def update_project_fn(proj):
        # Overwrite the old name with the new.
        proj.burdensets[burdenset_numindex].name = new_burden_set_name
        
    # Do the project update using the internal function. 
    update_project_with_fn(project_id, update_project_fn)

@RPC()
def update_burden_set_disease(project_id, burdenset_numindex, disease_numindex, data):
    proj = load_project(project_id)
    data_record = proj.burdensets[burdenset_numindex].data[disease_numindex]
    print('Modifying')
    print(data_record)
    print('to')
    print(data)
    if len(data_record) != len(data):
        print('WARNING, lengths do not match: %s vs. %s' % (len(data_record), len(data)))
    for i,datum in enumerate(data):
        data_record[i] = sanitize(datum)
    
    proj.package().make_package() # Update with the latest data
    proj.modified = sc.now()
    save_project(proj)
    print('Done updating burden set.')
    return None



@RPC()
def get_project_burden_plots(project_id, burdenset_numindex, engine='matplotlib', dosave=True):
    ''' Plot the disease burden '''
    
    # Get the Project object.
    proj = load_project(project_id)
    
    # Get the burden set that matches burdenset_numindex.
    burdenset = proj.burden(key=burdenset_numindex)
    
    figs = []
    for which in ['dalys','deaths','prevalence']:        
        fig = burdenset.plottopcauses(which=which) # Create the figure
        figs.append(fig)
    
    # Gather the list for all of the diseases.
    graphs = []
    for fig in figs:
        graph_dict = sw.mpld3ify(fig, jsonify=False)
        graphs.append(graph_dict)
    
    if dosave:
        filepath = getpath(filename=figures_filename)
        sc.savefigs(figs=figs, filetype='singlepdf', filename=filepath)
        print('Figures saved to %s' % filepath)
    
    # Return success -- WARNING, hard-coded to 3 graphs!
    return {'graph1': graphs[0],
            'graph2': graphs[1],
            'graph3': graphs[2],}
    
    


@RPC()
def add_burden(project_id, intervkey):
    proj = load_project(project_id)
    data = proj.burdensets[intervkey].data
    ['active', 'cause', 'dalys', 'deaths', 'prevalence']
    placeholder = [0, '~Cause of burden~', 0, 0, 0]
    data[data.nrows()] = placeholder
    proj.modified = sc.now()
    save_project(proj)
    return None

@RPC()
def copy_burden(project_id, intervkey, index):
    proj = load_project(project_id)
    data = proj.burdensets[intervkey].data
    value = sc.dcp(data[index])
    value[1] += ' (copy)'
    data.insert(row=index, value=value)
    proj.modified = sc.now()
    save_project(proj)
    return None

@RPC()
def delete_burden(project_id, intervkey, index):
    proj = load_project(project_id)
    data = proj.burdensets[intervkey].data
    data.pop(index)
    proj.modified = sc.now()
    save_project(proj)
    return None

###################################################################################
### Intervention set RPCs
###################################################################################

@RPC()    
def get_project_interv_sets(project_id):
    # Get the Project object.
    proj = load_project(project_id)
    
    # Get a list of the Interventions objects.
    interv_sets = [proj.intervsets[ind] for ind in range(len(proj.intervsets))] 
    
    # Return the JSON-friendly result.
    return {'intervsets': map(get_interv_set_fe_repr, interv_sets)}

@RPC()
def get_project_interv_set_intervs(project_id, intervset_numindex=None):
    # Get the Project object.
    proj = load_project(project_id)
    
    # Get the intervention set that matches intervset_numindex.
    intervset = proj.interv(key=intervset_numindex)
    
    # Return an empty list if no data is present.
    if intervset.data is None:
        return { 'interventions': [] } 
    
    # Gather the list for all of the interventions.
    interv_data = [list(interv) for interv in intervset.data]
    
    # Return success.
    return { 'interventions': interv_data }

@RPC()
def create_interv_set(project_id, new_interv_set_name):

    def update_project_fn(proj):
        # Get a unique name (just in case the one provided collides with an 
        # existing one).
        unique_name = get_unique_name(new_interv_set_name, 
            other_names=list(proj.intervsets))
        
        # Create a new (empty) intervention set.
        new_intervset = hp.Interventions(project=proj, name=unique_name)
        
        # Load data from the Excel spreadsheet.
        # NOTE: We may want to take this out later in favor leaving the 
        # new sets empty to start.
        data_path = hp.HPpath('data')
        new_intervset.loaddata(data_path+'dcp-data-afg-v1.xlsx')
        
        # Put the new intervention set in the dictionary.
        proj.intervsets[unique_name] = new_intervset
        
        proj.package().make_package() # Update with the latest data
        
    # Do the project update using the internal function.
    update_project_with_fn(project_id, update_project_fn)

    # Return the new intervention sets.
    return get_project_interv_sets(project_id)

@RPC()
def delete_interv_set(project_id, intervset_numindex):

    def update_project_fn(proj):
        proj.intervsets.pop(intervset_numindex)
        proj.package().make_package() # Update with the latest data
        
    # Do the project update using the internal function.    
    update_project_with_fn(project_id, update_project_fn)   

@RPC()    
def copy_interv_set(project_id, intervset_numindex):

    def update_project_fn(proj):
        # Get a unique name (just in case the one provided collides with an 
        # existing one).
        unique_name = get_unique_name(proj.intervsets[intervset_numindex].name, 
            other_names=list(proj.intervsets))
        
        # Create a new intervention set which is a copy of the old one.
        new_intervset = sc.dcp(proj.intervsets[intervset_numindex])
        
        # Overwrite the old name with the new.
        new_intervset.name = unique_name
       
        # Put the new intervention set in the dictionary.
        proj.intervsets[unique_name] = new_intervset
        
    # Do the project update using the internal function.  
    update_project_with_fn(project_id, update_project_fn)
    
    # Return the new intervention sets.
    return get_project_interv_sets(project_id)

@RPC()
def rename_interv_set(project_id, intervset_numindex, new_interv_set_name):

    def update_project_fn(proj):
        # Overwrite the old name with the new.
        proj.intervsets[intervset_numindex].name = new_interv_set_name
        
    # Do the project update using the internal function. 
    update_project_with_fn(project_id, update_project_fn)

@RPC()    
def update_interv_set_interv(project_id, intervkey, interv_numindex, data):
    proj = load_project(project_id)
    data_record = proj.intervsets[intervkey].data[interv_numindex]
    print('Original intervention set record:')
    print(data_record)
    data_record[0] = sanitize(data[0])
    data_record[1] = data[1]
    data_record[3] = sanitize(data[2])
    data_record[4] = sanitize(data[3])
    data_record[5] = sanitize(data[4])
    data_record[6] = sanitize(data[5])
    data_record[7] = sanitize(data[6])
    data_record[8] = sanitize(data[7])
    print('New intervention set record:')
    print(data_record)
    proj.package().make_package() # Update with the latest data
    proj.modified = sc.now()
    save_project(proj)
    return None

@RPC()
def add_interv(project_id, intervkey):
    proj = load_project(project_id)
    data = proj.intervsets[intervkey].data
    placeholder = ['~Intervention Number~', '~Name~', '~Full name~', '~Platform~', '~Cause~', 0, 0, 0, 0, 0, 0, 0, '<Level 1 cause>', '<Level 1 cause name>', '<Level 2 cause >', '<Level 3 cause >', '<DCP3 Packages>', '<Package Number>', '<Urgency>', '<Code>', '<Codes for  interventions that appear in multiple packages>', '<Volume(s) intervention included in>', '<Platform in Volume>', '<Platform in EUHC>']
    data[data.nrows()] = placeholder
    proj.modified = sc.now()
    save_project(proj)
    return None

@RPC()
def copy_interv(project_id, intervkey, index):
    proj = load_project(project_id)
    data = proj.intervsets[intervkey].data
    value = sc.dcp(data[index])
    value[1] += ' (copy)'
    data.insert(row=index, value=value)
    proj.modified = sc.now()
    save_project(proj)
    return None

@RPC()
def delete_interv(project_id, intervkey, index):
    proj = load_project(project_id)
    data = proj.intervsets[intervkey].data
    data.pop(index)
    proj.modified = sc.now()
    save_project(proj)
    return None

###################################################################################
###  Package set RPCs
################################################################################### 

@RPC()    
def get_project_package_sets(project_id):
    # Get the Project object.
    proj = load_project(project_id)
    
    # Get a list of the package objects.
    packagesets = [proj.packagesets[ind] for ind in range(len(proj.packagesets))] 
    
    # Return the JSON-friendly result.
    return {'packagesets': map(get_package_set_fe_repr, packagesets)}

@RPC()
def get_project_package_set_results(project_id, packageset_numindex):
    # Get the Project object.
    proj = load_project(project_id)
    
    # Get the package set that matches packageset_numindex.
    packageset = proj.package(key=packageset_numindex)
    packageset.make_package()
    
    # Return an empty list if no data is present.
    if packageset.data is None:
        return { 'results': [] }

    # Gather the list for all of the diseases.
    result_data = packageset.jsonify(cols=['active','shortname','cause','coverage','dalys_averted', 'frac_averted'], header=False)
    
    # Return success.
    return { 'results': result_data }

@RPC()    
def create_package_set(project_id, new_package_set_name):

    def update_project_fn(proj):
        # Get a unique name (just in case the one provided collides with an 
        # existing one).
        unique_name = get_unique_name(new_package_set_name, 
            other_names=list(proj.packagesets))
        
        # Create a new (empty) package set.
        new_packageset = hp.HealthPackage(project=proj, name=unique_name)
        
        # Put the new package set in the dictionary.
        proj.packagesets[unique_name] = new_packageset
        
    # Do the project update using the internal function.
    update_project_with_fn(project_id, update_project_fn)

    # Return the new package sets.
    return get_project_package_sets(project_id)

@RPC()
def delete_package_set(project_id, packageset_numindex):

    def update_project_fn(proj):
        proj.packagesets.pop(packageset_numindex)
        
    # Do the project update using the internal function.    
    update_project_with_fn(project_id, update_project_fn)   

@RPC()    
def copy_package_set(project_id, packageset_numindex):

    def update_project_fn(proj):
        # Get a unique name (just in case the one provided collides with an 
        # existing one).
        unique_name = get_unique_name(proj.packagesets[packageset_numindex].name, 
            other_names=list(proj.packagesets))
        
        # Create a new packageset which is a copy of the old one.
        new_packageset = sc.dcp(proj.packagesets[packageset_numindex])
        
        # Overwrite the old name with the new.
        new_packageset.name = unique_name
       
        # Put the new package set in the dictionary.
        proj.packagesets[unique_name] = new_packageset
        
    # Do the project update using the internal function.  
    update_project_with_fn(project_id, update_project_fn)
    
    # Return the new package sets.
    return get_project_package_sets(project_id) 

@RPC()
def rename_package_set(project_id, packageset_numindex, new_package_set_name):

    def update_project_fn(proj):
        # Overwrite the old name with the new.
        proj.packagesets[packageset_numindex].name = new_package_set_name
        
    # Do the project update using the internal function. 
    update_project_with_fn(project_id, update_project_fn)

@RPC()
def get_project_package_plots(project_id, packageset_numindex, dosave=True):
    ''' Plot the health packages '''
    
    # Get the Project object.
    proj = load_project(project_id)
    
    # Get the package set that matches packageset_numindex.
    packageset = proj.package(key=packageset_numindex)
    packageset.make_package()
    
    figs = []
    fig1 = packageset.plot_spending()
    fig2 = packageset.plot_dalys()
    fig3 = packageset.plot_cascade()
    figs.append(fig1)
    figs.append(fig2)
    figs.append(fig3)
    
    # Gather the list for all of the diseases.
    graphs = []
    for fig in figs:
        graph_dict = sw.mpld3ify(fig, jsonify=False)
        graphs.append(graph_dict)
    
    if dosave:
        filepath = getpath(filename=figures_filename)
        sc.savefigs(figs=figs, filetype='singlepdf', filename=filepath)
        print('Figures saved to %s' % filepath)
    
    # Return success -- WARNING, should not be hard-coded!
    return {'graph1': graphs[0],
            'graph2': graphs[1],
            'graph3': graphs[2],}