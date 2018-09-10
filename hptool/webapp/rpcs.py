"""
rpcs.py -- code related to HealthPrior project management
    
Last update: 2018sep09 by cliffk
"""

#
# Imports and globals
#

import os
from zipfile import ZipFile
from flask_login import current_user
import numpy as np
import sciris as sc
import scirisweb as sw
import hptool as hp
from . import projects as prj

RPC_dict = {} # Dictionary to hold all of the registered RPCs in this module.
RPC = sw.makeRPCtag(RPC_dict) # RPC registration decorator factory created using call to make_register_RPC().
figures_filename = 'Figures.pdf'

#
# Other functions (mostly helpers for the RPCs)
#

def getpath(filename, online=True):
    if online:
        dirname = sw.globalvars.downloads_dir.dir_path # Use the downloads directory to put the file in.
        fullpath = os.path.join(dirname, filename) # Generate the full file name with path.
    else:
        fullpath = filename
    return fullpath

def savefile(filename, obj, online=True):
    fullpath = getpath(filename=filename, online=online)
    sc.saveobj(fullpath, obj)
    return fullpath


def sanitize(vals, forcefloat=False, verbose=True, allowstrings=True):
    ''' Make sure values are numeric, and either return nans or skip vals that aren't -- WARNING, duplicates lots of other things!'''
    print('Sanitizing this:')
    print(vals)
    if verbose: print('Sanitizing vals of %s: %s' % (type(vals), vals))
    if sc.isiterable(vals):
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
                    sanival = str(val)
                else:
                    print('Could not sanitize value "%s": %s; returning nan' % (val, repr(E)))
                    sanival = np.nan
        output.append(sanival)
    if as_array:
        return output
    else:
        return output[0]
  


def load_project_record(project_id, raise_exception=True):
    """
    Return the project DataStore reocord, given a project UID.
    """ 
    
    # Load the matching prj.ProjectSO object from the database.
    project_record = prj.proj_collection.get_object_by_uid(project_id)

    # If we have no match, we may want to throw an exception.
    if project_record is None:
        if raise_exception:
            raise Exception('ProjectDoesNotExist(id=%s)' % project_id)
            
    # Return the Project object for the match (None if none found).
    return project_record

def load_project(project_id, raise_exception=True):
    """
    Return the Nutrition Project object, given a project UID, or None if no 
    ID match is found.
    """ 
    
    # Load the project record matching the ID passed in.
    project_record = load_project_record(project_id, 
        raise_exception=raise_exception)
    
    # If there is no match, raise an exception or return None.
    if project_record is None:
        if raise_exception:
            raise Exception('ProjectDoesNotExist(id=%s)' % project_id)
        else:
            return None
        
    # Return the found project.
    return project_record.proj

def load_project_summary_from_project_record(project_record):
    """
    Return the project summary, given the DataStore record.
    """ 
    
    # Return the built project summary.
    return project_record.get_user_front_end_repr()
  
def load_current_user_project_summaries2():
    """
    Return project summaries for all projects the user has to the client.
    """ 
    
    # Get the prj.ProjectSO entries matching the user UID.
    project_entries = prj.proj_collection.get_project_entries_by_user(current_user.get_id())
    
    # Grab a list of project summaries from the list of prj.ProjectSO objects we 
    # just got.
    return {'projects': map(load_project_summary_from_project_record, 
        project_entries)}
                
def get_unique_name(name, other_names=None):
    """
    Given a name and a list of other names, find a replacement to the name 
    that doesn't conflict with the other names, and pass it back.
    """
    
    # If no list of other_names is passed in, load up a list with all of the 
    # names from the project summaries.
    if other_names is None:
        other_names = [p['project']['name'] for p in load_current_user_project_summaries2()['projects']]
      
    # Start with the passed in name.
    i = 0
    unique_name = name
    
    # Try adding an index (i) to the name until we find one that no longer 
    # matches one of the other names in the list.
    while unique_name in other_names:
        i += 1
        unique_name = "%s (%d)" % (name, i)
        
    # Return the found name.
    return unique_name

def save_project(proj):
    """
    Given a Project object, wrap it in a new prj.ProjectSO object and put this 
    in the project collection (either adding a new object, or updating an 
    existing one)  skip_result lets you null out saved results in the Project.
    """ 
    
    # Load the project record matching the UID of the project passed in.
    project_record = load_project_record(proj.uid)
    
    # Copy the project, only save what we want...
    new_project = sc.dcp(proj)
    new_project.modified = sc.now()
         
    # Create the new project entry and enter it into the ProjectCollection.
    # Note: We don't need to pass in project.uid as a 3rd argument because 
    # the constructor will automatically use the Project's UID.
    projSO = prj.ProjectSO(new_project, project_record.owner_uid)
    prj.proj_collection.update_object(projSO)
    
def update_project_with_fn(project_id, update_project_fn):
    """
    Do an update of a hptool Project, given the UID and a function that 
    does the actual Project updating.
    """ 
    
    # Load the project.
    proj = load_project(project_id)
    
    # Execute the passed-in function that modifies the project.
    update_project_fn(proj)
    
    # Save the changed project.
    save_project(proj) 
    
def save_project_as_new(proj, user_id, uid=None):
    """
    Given a Project object and a user UID, wrap the Project in a new prj.ProjectSO 
    object and put this in the project collection, after getting a fresh UID
    for this Project.  Then do the actual save.
    """ 
    
    # Set a new project UID, so we aren't replicating the UID passed in.
    proj.uid = sc.uuid(uid)
    
    # Create the new project entry and enter it into the ProjectCollection.
    projSO = prj.ProjectSO(proj, user_id)
    prj.proj_collection.add_object(projSO)  

    # Display the call information.
    print(">> save_project_as_new '%s'" % proj.name)

    # Save the changed Project object to the DataStore.
    save_project(proj)
    
    return None

def get_burden_set_fe_repr(burdenset):
    obj_info = {
        'burdenset': {
            'name': burdenset.name,
            'uid': burdenset.uid,
            'creationTime': burdenset.created,
            'updateTime': burdenset.modified
        }
    }
    return obj_info

def get_interv_set_fe_repr(interv_set):
    obj_info = {
        'intervset': {
            'name': interv_set.name,
            'uid': interv_set.uid,
            'creationTime': interv_set.created,
            'updateTime': interv_set.modified
        }
    }
    return obj_info

def get_package_set_fe_repr(packageset):
    obj_info = {
        'packageset': {
            'name': packageset.name,
            'uid': packageset.uid,
            'creationTime': packageset.created,
            'updateTime': packageset.modified
        }
    }
    return obj_info

#
# RPC functions
#

# RPC definitions
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



###################################################################################
###  Project RPCs
################################################################################### 
    
@RPC()
def get_scirisdemo_projects():
    """
    Return the projects associated with the Sciris Demo user.
    """
    
    # Get the user UID for the _ScirisDemo user.
    user_id = sw.get_scirisdemo_user()
   
    # Get the prj.ProjectSO entries matching the _ScirisDemo user UID.
    project_entries = prj.proj_collection.get_project_entries_by_user(user_id)

    # Collect the project summaries for that user into a list.
    project_summary_list = map(load_project_summary_from_project_record, 
        project_entries)
    
    # Sort the projects by the project name.
    sorted_summary_list = sorted(project_summary_list, 
        key=lambda proj: proj['project']['name']) # Sorts by project name
    
    # Return a dictionary holding the project summaries.
    output = {'projects': sorted_summary_list}
    return output

@RPC()
def load_project_summary(project_id):
    """
    Return the project summary, given the Project UID.
    """ 
    
    # Load the project record matching the UID of the project passed in.
    project_entry = load_project_record(project_id)
    
    # Return a project summary from the accessed prj.ProjectSO entry.
    return load_project_summary_from_project_record(project_entry)

@RPC()
def load_current_user_project_summaries():
    """
    Return project summaries for all projects the user has to the client.
    """ 
    
    return load_current_user_project_summaries2()

@RPC()                
def load_all_project_summaries():
    """
    Return project summaries for all projects to the client.
    """ 
    
    # Get all of the prj.ProjectSO entries.
    project_entries = prj.proj_collection.get_all_objects()
    
    # Grab a list of project summaries from the list of prj.ProjectSO objects we 
    # just got.
    return {'projects': map(load_project_summary_from_project_record, 
        project_entries)}
            
@RPC()    
def delete_projects(project_ids):
    """
    Delete all of the projects with the passed in UIDs.
    """ 
    
    # Loop over the project UIDs of the projects to be deleted...
    for project_id in project_ids:
        # Load the project record matching the UID of the project passed in.
        
        record = load_project_record(project_id, raise_exception=True)
        # If a matching record is found, delete the object from the 
        # ProjectCollection.
        if record is not None:
            prj.proj_collection.delete_object_by_uid(project_id)

@RPC(call_type='download')   
def download_project(project_id):
    """
    For the passed in project UID, get the Project on the server, save it in a 
    file, minus results, and pass the full path of this file back.
    """
    
    # Load the project with the matching UID.
    proj = load_project(project_id, raise_exception=True)
    
    # Use the downloads directory to put the file in.
    dirname = sw.globalvars.downloads_dir.dir_path
        
    # Create a filename containing the project name followed by a .prj 
    # suffix.
    file_name = '%s.prj' % proj.name
        
    # Generate the full file name with path.
    full_file_name = '%s%s%s' % (dirname, os.sep, file_name)
        
    # Write the object to a Gzip string pickle file.
    sc.saveobj(full_file_name, proj)
    
    # Display the call information.
    print(">> download_project %s" % (full_file_name))
    
    # Return the full filename.
    return full_file_name

@RPC(call_type='download')
def load_zip_of_prj_files(project_ids):
    """
    Given a list of project UIDs, make a .zip file containing all of these 
    projects as .prj files, and return the full path to this file.
    """
    
    # Use the downloads directory to put the file in.
    dirname = sw.globalvars.downloads_dir.dir_path

    # Build a list of prj.ProjectSO objects for each of the selected projects, 
    # saving each of them in separate .prj files.
    prjs = [load_project_record(id).save_as_file(dirname) for id in project_ids]
    
    # Make the zip file name and the full server file path version of the same..
    zip_fname = 'Projects.zip'
    server_zip_fname = os.path.join(dirname, sc.sanitizefilename(zip_fname))
    
    # Create the zip file, putting all of the .prj files in a projects 
    # directory.
    with ZipFile(server_zip_fname, 'w') as zipfile:
        for project in prjs:
            zipfile.write(os.path.join(dirname, project), 'projects/{}'.format(project))
            
    # Display the call information.
    print(">> load_zip_of_prj_files %s" % (server_zip_fname))

    # Return the server file name.
    return server_zip_fname

@RPC()
def create_new_project(user_id):
    """
    Create a new HealthPrior project.
    """
    
    # Get a unique name for the project to be added.
    new_proj_name = get_unique_name('New project', other_names=None)
    
    # Create the project, loading in the desired spreadsheets.  
    proj = hp.demo(name=new_proj_name)
    
    # Display the call information.
    print(">> create_new_project %s" % (proj.name))    
    
    # Save the new project in the DataStore.
    save_project_as_new(proj, user_id)
    
    # Return the new project UID in the return message.
    return { 'projectId': str(proj.uid) }
 
@RPC()
def update_project_from_summary(project_summary):
    """
    Given the passed in project summary, update the underlying project 
    accordingly.
    """ 
    
    # Load the project corresponding with this summary.
    proj = load_project(project_summary['project']['id'])
       
    # Use the summary to set the actual project.
    proj.name = project_summary['project']['name']
    
    # Set the modified time to now.
    proj.modified = sc.now()
    
    # Save the changed project to the DataStore.
    save_project(proj)
    
@RPC()    
def copy_project(project_id):
    """
    Given a project UID, creates a copy of the project with a new UID and 
    returns that UID.
    """
    
    # Get the Project object for the project to be copied.
    project_record = load_project_record(project_id, raise_exception=True)
    proj = project_record.proj
    
    # Make a copy of the project loaded in to work with.
    new_project = sc.dcp(proj)
    
    # Just change the project name, and we have the new version of the 
    # Project object to be saved as a copy.
    new_project.name = get_unique_name(proj.name, other_names=None)
    
    # Set the user UID for the new projects record to be the current user.
    user_id = current_user.get_id() 
    
    # Display the call information.
    print(">> copy_project %s" % (new_project.name)) 
    
    # Save a DataStore projects record for the copy project.
    save_project_as_new(new_project, user_id)
    
    # Remember the new project UID (created in save_project_as_new()).
    copy_project_id = new_project.uid

    # Return the UID for the new projects record.
    return { 'projectId': copy_project_id }

@RPC(call_type='upload')
def create_project_from_prj_file(prj_filename, user_id):
    """
    Given a .prj file name and a user UID, create a new project from the file 
    with a new UID and return the new UID.
    """
    
    # Display the call information.
    print(">> create_project_from_prj_file '%s'" % prj_filename)
    
    # Try to open the .prj file, and return an error message if this fails.
    try:
        proj = sc.loadobj(prj_filename)
    except Exception:
        return { 'error': 'BadFileFormatError' }
    
    # Reset the project name to a new project name that is unique.
    proj.name = get_unique_name(proj.name, other_names=None)
    
    # Save the new project in the DataStore.
    save_project_as_new(proj, user_id)
    
    # Return the new project UID in the return message.
    return { 'projectId': str(proj.uid) }


def get_set(proj, which, key):
    if   which == 'burdenset':        thisset = proj.burden(key)
    elif which == 'interventionset':  thisset = proj.interv(key) # Full name since used in filenames
    elif which == 'packageset':       thisset = proj.package(key)
    else: raise Exception('Set %s not found' % which)
    return thisset
    

@RPC(call_type='upload')
def upload_set(filename, project_id, which, key=None):
    proj = load_project(project_id)
    thisset = get_set(proj, which, key)
    thisset.loaddata(filename)
    print('Loaded data into %s %s' % (which, thisset.name))
    proj.modified = sc.now()
    save_project(proj)
    return None
    
@RPC(call_type='download')
def download_set(project_id, which, key=None):
    proj = load_project(project_id)
    thisset = get_set(proj, which, key)
    filepath = getpath('%s_%s.xlsx' % (thisset.name, which))
    thisset.savedata(filepath)
    print('Downloading data from %s %s' % (which, thisset.name))
    return filepath

@RPC(call_type='download')
def download_figures():
    filepath = getpath(figures_filename) # Must match 
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
    data = sanitize(data)
    data_record = proj.burdensets[burdenset_numindex].data[disease_numindex]
    print('Modifying')
    print(data_record)
    print('to')
    print(data)
    if len(data_record) != len(data):
        print('WARNING, lengths do not match: %s vs. %s' % (len(data_record), len(data)))
    for i,datum in enumerate(data):
        data_record[i] = datum
    
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
def update_interv_set_interv(project_id, intervkey, newdata):
    
    proj = load_project(project_id)
    intervdata = proj.intervsets[intervkey].data
    
    for r,rowdata in enumerate(newdata):
        print(r)
        print(rowdata)
        intervdata[r] = rowdata
    
    # WARNING, this should be a method of dataframes!
    if intervdata.nrows()>len(newdata):
        intervdata.rmrows(range(len(newdata), intervdata.nrows()))
        
    proj.package().make_package() # Update with the latest data
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
    
    figs = []
    fig1 = packageset.plot_dalys()
    fig2 = packageset.plot_cascade()
    figs.append(fig1)
    figs.append(fig2)
    
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
            'graph2': graphs[1],}