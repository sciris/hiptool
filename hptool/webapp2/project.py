"""
project.py -- code related to HealthPrior project management
    
Last update: 5/29/18 (gchadder3)
"""

#
# Imports
#

from sciris2gc.rpcs import make_register_RPC
import sciris2gc.scirisobjects as sobj
import sciris2gc.datastore as ds
import sciris2gc.user as user
import sciris.core as sc
import hptool as hp
import os
import uuid
from zipfile import ZipFile
from flask import request
from flask_login import current_user
from sciris.exceptions import ProjectDoesNotExist

#
# Globals
#

# The ProjectCollection object for all of the app's projects.  Gets 
# initialized by and loaded by init_projects().
proj_collection = None

# Dictionary to hold all of the registered RPCs in this module.
RPC_dict = {}

# RPC registration decorator factory created using call to make_register_RPC().
register_RPC = make_register_RPC(RPC_dict)

#
# Classes
#

class ProjectSO(sobj.ScirisObject):
    """
    A ScirisObject-wrapped Optima Nutrition Project object.
    
    Methods:
        __init__(proj: Project, owner_uid: UUID, uid: UUID [None]): 
            void -- constructor
        load_from_copy(other_object): void -- assuming other_object is another 
            object of our type, copy its contents to us (calls the 
            ScirisObject superclass version of this method also)   
        show(): void -- print the contents of the object
        get_user_front_end_repr(): dict -- get a JSON-friendly dictionary 
            representation of the object state the front-end uses for non-
            admin purposes  
        save_as_file(load_dir: str): str -- given a load dictionary, save the 
            project in a file there and return the file name
                    
    Attributes:
        proj (Project) -- the actual Project object being wrapped
        owner_uid (UUID) -- the UID of the User that owns the Project
        
    Usage:
        >>> my_project = ProjectSO(proj, owner_uid)                      
    """
    
    def  __init__(self, proj, owner_uid, uid=None):
        # NOTE: uid argument is ignored but kept here to not mess up
        # inheritance.
        
        # Make sure the owner UID argument is a valid UUID, converting a hex 
        # text to a UUID object, if needed.        
        valid_uuid = sobj.get_valid_uuid(owner_uid)
        
        # If we have a valid UUID...
        if valid_uuid is not None:       
            # Set superclass parameters.
            super(ProjectSO, self).__init__(proj.uid)
                                   
            # Set the project to the Optima Project that is passed in.
            self.proj = proj
            
            # Set the owner (User) UID.
            self.owner_uid = valid_uuid
        
    def load_from_copy(self, other_object):
        if type(other_object) == type(self):
            # Do the superclass copying.
            super(ProjectSO, self).load_from_copy(other_object)
            
            # Copy the Project object itself.
            self.proj = sc.dcp(other_object.proj)
            
            # Copy the owner UID.
            self.owner_uid = other_object.owner_uid
                
    def show(self):
        # Show superclass attributes.
        super(ProjectSO, self).show()  
        
        # Show the Optima defined display text for the project.
        print '---------------------'
        print 'Owner User UID: %s' % self.owner_uid.hex
        print 'Project Name: %s' % self.proj.name
        print 'Creation Time: %s' % self.proj.created
        print 'Update Time: %s' % self.proj.modified
            
    def get_user_front_end_repr(self):
        obj_info = {
            'project': {
                'id': self.uid,
                'name': self.proj.name,
                'user_id': self.owner_uid,
                'creation_time': self.proj.created,
                'updated_time': self.proj.modified     
            }
        }
        return obj_info
    
    def save_as_file(self, load_dir):
        # Create a filename containing the project name followed by a .prj 
        # suffix.
        file_name = '%s.prj' % self.proj.name
        
        # Generate the full file name with path.
        full_file_name = '%s%s%s' % (load_dir, os.sep, file_name)   
     
        # Write the object to a Gzip string pickle file.
        ds.object_to_gzip_string_pickle_file(full_file_name, self.proj)
        
        # Return the filename (not the full one).
        return self.proj.name + ".prj"
    
        
class ProjectCollection(sobj.ScirisCollection):
    """
    A collection of Projects.
    
    Methods:
        __init__(uid: UUID [None], type_prefix: str ['projectscoll'], 
            file_suffix: str ['.pc'], 
            instance_label: str ['Projects Collection']): void -- constructor  
        get_user_front_end_repr(owner_uid: UUID): list -- return a list of dicts 
            containing JSON-friendly project contents for each project that 
            is owned by the specified user UID
        get_project_entries_by_user(owner_uid: UUID): list -- return the ProjectSOs 
            that match the owning User UID in a list
        
    Usage:
        >>> proj_collection = ProjectCollection(uuid.UUID('12345678123456781234567812345678'))                      
    """
    
    def __init__(self, uid, type_prefix='projectscoll', file_suffix='.pc', 
        instance_label='Projects Collection'):
        # Set superclass parameters.
        super(ProjectCollection, self).__init__(uid, type_prefix, file_suffix, 
             instance_label)
            
    def get_user_front_end_repr(self, owner_uid):
        # Make sure the argument is a valid UUID, converting a hex text to a
        # UUID object, if needed.        
        valid_uuid = sobj.get_valid_uuid(owner_uid)
        
        # If we have a valid UUID...
        if valid_uuid is not None:               
            # Get dictionaries for each Project in the dictionary.
            projects_info = [self.obj_dict[key].get_user_front_end_repr() \
                for key in self.obj_dict \
                if self.obj_dict[key].owner_uid == valid_uuid]
            return projects_info
        
        # Otherwise, return an empty list.
        else:
            return []
        
    def get_project_entries_by_user(self, owner_uid):
        # Make sure the argument is a valid UUID, converting a hex text to a
        # UUID object, if needed.        
        valid_uuid = sobj.get_valid_uuid(owner_uid)
        
        # If we have a valid UUID...
        if valid_uuid is not None:    
            # Get ProjectSO entries for each Project in the dictionary.
            project_entries = [self.obj_dict[key] \
                for key in self.obj_dict \
                if self.obj_dict[key].owner_uid == valid_uuid]
            return project_entries
        
        # Otherwise, return an empty list.
        else:
            return []


#
# Initialization function
#

def init_projects():
    global proj_collection
    
    # Look for an existing ProjectCollection.
    proj_collection_uid = ds.data_store.get_uid_from_instance('projectscoll', 
        'Projects Collection')
    
    # Create the projects collection object.  Note, that if no match was found, 
    # this will be assigned a new UID.    
    proj_collection = ProjectCollection(proj_collection_uid)
    
    # If there was a match...
    if proj_collection_uid is not None:
        print '>> Loading ProjectCollection from the DataStore.'
        proj_collection.load_from_data_store() 
    
    # Else (no match)...
    else:
        # Load the data path holding the Excel files.
        data_path = hp.HPpath('data')
    
        print '>> Creating a new ProjectCollection.'   
        proj_collection.add_to_data_store()
        
        print '>> Starting a demo project.'
        proj = hp.Project(name='Afghanistan test 1', 
            burdenfile=data_path + 'ihme-gbd.xlsx', 
            interventionsfile=data_path + 'dcp-data-afg-v1.xlsx')  
        projSO = ProjectSO(proj, user.get_scirisdemo_user())
#        projSO = ProjectSO('Afghanistan test 1', 
#            user.get_scirisdemo_user(), 
#            spreadsheet_path=None)
        proj_collection.add_object(projSO)
        
        print '>> Starting a second demo project.'
        proj = hp.Project(name='Afghanistan HBP equity')
        projSO = ProjectSO(proj, user.get_scirisdemo_user())
#        projSO = ProjectSO('Afghanistan HBP equity', 
#            user.get_scirisdemo_user(), 
#            spreadsheet_path=None)
        proj_collection.add_object(projSO)
        
        print '>> Starting a third demo project.'
        proj = hp.Project(name='Final Afghanistan HBP')
        projSO = ProjectSO(proj, user.get_scirisdemo_user())
#        projSO = ProjectSO('Final Afghanistan HBP', 
#            user.get_scirisdemo_user(), 
#            spreadsheet_path=None)
        proj_collection.add_object(projSO)
        
        print '>> Starting a fourth demo project.'
        proj = hp.Project(name='Pakistan test 1')  
        projSO = ProjectSO(proj, user.get_scirisdemo_user())
#        projSO = ProjectSO('Pakistan test 1', 
#            user.get_scirisdemo_user(), 
#            spreadsheet_path=None)
        proj_collection.add_object(projSO)
        
    # Show what's in the ProjectCollection.    
    proj_collection.show()
        
#
# Other functions (mostly helpers for the RPCs)
#

def load_project_record(project_id, raise_exception=True):
    """
    Return the project DataStore reocord, given a project UID.
    """ 
    
    # Load the matching ProjectSO object from the database.
    project_record = proj_collection.get_object_by_uid(project_id)

    # If we have no match, we may want to throw an exception.
    if project_record is None:
        if raise_exception:
            raise ProjectDoesNotExist(id=project_id)
            
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
            raise ProjectDoesNotExist(id=project_id)
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
          
def get_unique_name(name, other_names=None):
    """
    Given a name and a list of other names, find a replacement to the name 
    that doesn't conflict with the other names, and pass it back.
    """
    
    # If no list of other_names is passed in, load up a list with all of the 
    # names from the project summaries.
    # TODO: The function call below will need to be replaced.
    if other_names is None:
        other_names = [p['project']['name'] for p in load_current_user_project_summaries(check_endpoint=False)['projects']]
      
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

#
# RPC functions
#

def get_scirisdemo_projects():
    """
    Return the projects associated with the Sciris Demo user.
    """
    
    # Check (for security purposes) that the function is being called by the 
    # correct endpoint, and if not, fail.
    if request.endpoint != 'normalProjectRPC':
        return {'error': 'Unauthorized RPC'}
    
    # Get the user UID for the _ScirisDemo user.
    user_id = user.get_scirisdemo_user()
   
    # Get the ProjectSO entries matching the _ScirisDemo user UID.
    project_entries = proj_collection.get_project_entries_by_user(user_id)

    # Collect the project summaries for that user into a list.
    project_summary_list = map(load_project_summary_from_project_record, 
        project_entries)
    
    # Sort the projects by the project name.
    sorted_summary_list = sorted(project_summary_list, 
        key=lambda proj: proj['project']['name']) # Sorts by project name
    
    # Return a dictionary holding the project summaries.
    output = {'projects': sorted_summary_list}
    return output

def load_project_summary(project_id):
    """
    Return the project summary, given the Project UID.
    """ 
    
    # Check (for security purposes) that the function is being called by the 
    # correct endpoint, and if not, fail.
    if request.endpoint != 'normalProjectRPC':
        return {'error': 'Unauthorized RPC'}
    
    # Load the project record matching the UID of the project passed in.
    project_entry = load_project_record(project_id)
    
    # Return a project summary from the accessed ProjectSO entry.
    return load_project_summary_from_project_record(project_entry)

@register_RPC(validation_type='nonanonymous user')
def load_current_user_project_summaries():
    """
    Return project summaries for all projects the user has to the client.
    """ 
    
    # Get the ProjectSO entries matching the user UID.
    project_entries = proj_collection.get_project_entries_by_user(current_user.get_id())
    
    # Grab a list of project summaries from the list of ProjectSO objects we 
    # just got.
    return {'projects': map(load_project_summary_from_project_record, 
        project_entries)}
                
def load_all_project_summaries():
    """
    Return project summaries for all projects to the client.
    """ 
    
    # Check (for security purposes) that the function is being called by the 
    # correct endpoint, and if not, fail.
    if request.endpoint != 'normalProjectRPC':
        return {'error': 'Unauthorized RPC'}   
    
    # Get all of the ProjectSO entries.
    project_entries = proj_collection.get_all_objects()
    
    # Grab a list of project summaries from the list of ProjectSO objects we 
    # just got.
    return {'projects': map(load_project_summary_from_project_record, 
        project_entries)}
    
def delete_projects(project_ids):
    """
    Delete all of the projects with the passed in UIDs.
    """ 
    
    # Check (for security purposes) that the function is being called by the 
    # correct endpoint, and if not, fail.
    if request.endpoint != 'normalProjectRPC':
        return {'error': 'Unauthorized RPC'}   
    
    # Loop over the project UIDs of the projects to be deleted...
    for project_id in project_ids:
        # Load the project record matching the UID of the project passed in.
        record = load_project_record(project_id, raise_exception=True)
        
        # If a matching record is found, delete the object from the 
        # ProjectCollection.
        if record is not None:
            proj_collection.deleteObjectByUID(project_id)
   
def download_project(project_id):
    """
    For the passed in project UID, get the Project on the server, save it in a 
    file, minus results, and pass the full path of this file back.
    """
    
    # Check (for security purposes) that the function is being called by the 
    # correct endpoint, and if not, fail.
    if request.endpoint != 'downloadProjectRPC':
        return {'error': 'Unauthorized RPC'}   
    
    # Load the project with the matching UID.
    proj = load_project(project_id, raise_exception=True)
    
    # Use the downloads directory to put the file in.
    dirname = ds.downloads_dir.dir_path
        
    # Create a filename containing the project name followed by a .prj 
    # suffix.
    file_name = '%s.prj' % proj.name
        
    # Generate the full file name with path.
    full_file_name = '%s%s%s' % (dirname, os.sep, file_name)
        
    # Write the object to a Gzip string pickle file.
    ds.object_to_gzip_string_pickle_file(full_file_name, proj)
    
    # Display the call information.
    print(">> download_project %s" % (full_file_name))
    
    # Return the full filename.
    return full_file_name

def load_zip_of_prj_files(project_ids):
    """
    Given a list of project UIDs, make a .zip file containing all of these 
    projects as .prj files, and return the full path to this file.
    """
    
    # Check (for security purposes) that the function is being called by the 
    # correct endpoint, and if not, fail.
    if request.endpoint != 'downloadProjectRPC':
        return {'error': 'Unauthorized RPC'}   
    
    # Use the downloads directory to put the file in.
    dirname = ds.downloads_dir.dir_path

    # Build a list of ProjectSO objects for each of the selected projects, 
    # saving each of them in separate .prj files.
    prjs = [load_project_record(id).save_as_file(dirname) for id in project_ids]
    
    # Make the zip file name and the full server file path version of the same..
    zip_fname = '{}.zip'.format(uuid.uuid4())
    server_zip_fname = os.path.join(dirname, zip_fname)
    
    # Create the zip file, putting all of the .prj files in a projects 
    # directory.
    with ZipFile(server_zip_fname, 'w') as zipfile:
        for prj in prjs:
            zipfile.write(os.path.join(dirname, prj), 'projects/{}'.format(prj))
            
    # Display the call information.
    print(">> load_zip_of_prj_files %s" % (server_zip_fname))

    # Return the server file name.
    return server_zip_fname