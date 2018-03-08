"""
main.py -- main code for Sciris users to change to create their web apps
    
Last update: 3/8/18 (gchadder3)
"""

#
# Imports (Block 1)
#

from flask import request, current_app, json, jsonify, send_from_directory
from flask_login import current_user
from werkzeug.utils import secure_filename
import numpy as np
import mpld3
import sys
import os
import re
import copy
import sciris
import sciris.scirisobjects as sobj
import sciris.datastore as ds
import sciris.user as user
import sciris.project as project
from pylab import subplot
import config

#
# Script code (Block 1)
#

# Get the full path for the loaded sciris repo.  (It in sys path at the 
# beginning because the caller puts it there.)
scirisRepoFullPath = os.path.dirname(sciris.__file__)

# If we have a full path for the model directory, load scirismain.py from that.
if os.path.isabs(config.MODEL_DIR):
    modelDirTarget = config.MODEL_DIR
    
# Otherwise (we have a relative path), use it (correcting so it is with 
# respect to the sciris repo directory).
else:
    modelDirTarget = '%s%s%s' % (os.pardir, os.sep, config.MODEL_DIR) 
    
# If we have a full path for the webapp directory, load scirismain.py from that.
if os.path.isabs(config.WEBAPP_DIR):
    webappDirTarget = config.WEBAPP_DIR
    
# Otherwise (we have a relative path), use it (correcting so it is with 
# respect to the sciris repo directory).
else:
    webappDirTarget = '%s%s%s' % (os.pardir, os.sep, config.WEBAPP_DIR) 
    
#
# Imports (Block 2, dependent on config file)
#  
    
# Append the model directory to the path and import needed files.    
sys.path.append(modelDirTarget)
import hptool

# Append the webapp directory to the path and import needed files.    
sys.path.append(webappDirTarget)

#
# Classes
#

# ProjectSO goes here...

#
# Initialization functions 
#
        
def init_filepaths(theApp):
    # Set the Sciris root path to the parent of the current directory, the 
    # latter being the sciris/bin directory since that is where the code is 
    # executed from.
    ds.scirisRootPath = os.path.abspath(os.pardir)
    
    #  Using the current_app set to the passed in app..
    with theApp.app_context():
        # Set the uploads path.
        
        # If we have an absolute directory, use it.
        if os.path.isabs(current_app.config['UPLOADS_DIR']):
            ds.uploadsPath = current_app.config['UPLOADS_DIR']
            
        # Otherwise (we have a relative path), use it (correcting so it is with 
        # respect to the sciris repo directory).
        else:
            ds.uploadsPath = '%s%s%s' % (os.pardir, os.sep, 
                current_app.config['UPLOADS_DIR'])  
        
        # Set the file save root path.
        
        # If we have an absolute directory, use it.
        if os.path.isabs(current_app.config['FILESAVEROOT_DIR']):
            ds.fileSaveRootPath = current_app.config['FILESAVEROOT_DIR']
            
        # Otherwise (we have a relative path), use it (correcting so it is with 
        # respect to the sciris repo directory).
        else:
            ds.fileSaveRootPath = '%s%s%s' % (os.pardir, os.sep, 
                current_app.config['FILESAVEROOT_DIR'])
         
    # If the datafiles path doesn't exist yet...
    if not os.path.exists(ds.fileSaveRootPath):
        # Create datafiles directory.
        os.mkdir(ds.fileSaveRootPath)
        
        # Create an uploads subdirectory of this.
        os.mkdir(ds.uploadsPath)
        
        # # Create the fake data for scatterplots.
        # sd = model.ScatterplotData(model.makeUniformRandomData(50))
        # fullFileName = '%s%sgraph1.csv' % (ds.fileSaveRootPath, os.sep)
        # sd.saveAsCsv(fullFileName)
        
        # sd = model.ScatterplotData(model.makeUniformRandomData(50))
        # fullFileName = '%s%sgraph2.csv' % (ds.fileSaveRootPath, os.sep)
        # sd.saveAsCsv(fullFileName)
        
        # sd = model.ScatterplotData(model.makeUniformRandomData(50))
        # fullFileName = '%s%sgraph3.csv' % (ds.fileSaveRootPath, os.sep)
        # sd.saveAsCsv(fullFileName) 
        
def init_datastore(theApp):
    # Create the DataStore object, setting up Redis.
    with theApp.app_context():
        ds.theDataStore = ds.DataStore(redisDbURL=current_app.config['REDIS_URL'])

    # Load the DataStore state from disk.
    ds.theDataStore.load()
    
    # Uncomment this line (for now) to reset the database, and then recomment
    # before running for usage.
#    ds.theDataStore.deleteAll()
    
def init_users(theApp):
    # Look for an existing users dictionary.
    theUserDictUID = ds.theDataStore.getUIDFromInstance('userdict', 'Users Dictionary')
    
    # Create the user dictionary object.  Note, that if no match was found, 
    # this will be assigned a new UID.
    user.theUserDict = user.UserDict(theUserDictUID)
    
    # If there was a match...
    if theUserDictUID is not None:
        print '>> Loading UserDict from the DataStore.'
        user.theUserDict.loadFromDataStore() 
    
    # Else (no match)...
    else:
        print '>> Creating a new UserDict.'   
        user.theUserDict.addToDataStore()
        user.theUserDict.add(user.testUser)
        user.theUserDict.add(user.testUser2)
        user.theUserDict.add(user.testUser3)

    # Show all of the handles in theDataStore.
    print '>> List of all DataStore handles...'
    ds.theDataStore.showHandles()
    
    # Show all of the users in theUserDict.
    print '>> List of all users...'
    user.theUserDict.show()
    
def init_projects(theApp):
    # Look for an existing ProjectCollection.
    theProjsUID = ds.theDataStore.getUIDFromInstance('projectscoll', 
        'Projects Collection')
    
    # Create the projects collection object.  Note, that if no match was found, 
    # this will be assigned a new UID.    
    project.theProjCollection = project.ProjectCollection(theProjsUID)
    
    # If there was a match...
    if theProjsUID is not None:
        print '>> Loading ProjectCollection from the DataStore.'
        project.theProjCollection.loadFromDataStore() 
    
    # Else (no match)...
    else:
        print '>> Creating a new ProjectCollection.'   
        project.theProjCollection.addToDataStore()
        
        print '>> Starting a demo project.'
        theProject = project.Project('Afghanistan test 1', 
            user.get_scirisdemo_user(), 
            spreadsheetPath=None)
        project.theProjCollection.addObject(theProject)
        
        print '>> Starting a second demo project.'
        theProject = project.Project('Afghanistan HBP equity', 
            user.get_scirisdemo_user(), 
            spreadsheetPath=None)
        project.theProjCollection.addObject(theProject)
        
        print '>> Starting a third demo project.'
        theProject = project.Project('Final Afghanistan HBP', 
            user.get_scirisdemo_user(), 
            spreadsheetPath=None)
        project.theProjCollection.addObject(theProject)
        
        print '>> Starting a fourth demo project.'
        theProject = project.Project('Pakistan test 1', 
            user.get_scirisdemo_user(), 
            spreadsheetPath=None)
        project.theProjCollection.addObject(theProject)
        
    # Show what's in the ProjectCollection.    
    project.theProjCollection.show()
    
def init_main(theApp): 
    print '-- Version 1 of the HealthPrior app --'
    
#
# Other functions
#

# Do the meat of the RPC calls, passing args and kwargs to the appropriate 
# function in the appropriate handler location.
def doRPC(rpcType, handlerLocation, requestMethod, username=None):
    # If we are doing an upload, pull the RPC information out of the request 
    # form instead of the request data.
    if rpcType == 'upload':
        # Pull out the function name, args, and kwargs
        fn_name = request.form.get('funcname')
        args = json.loads(request.form.get('args', "[]"))
        kwargs = json.loads(request.form.get('kwargs', "{}"))
    
    # Otherwise (normal and download RPCs), pull the RPC information from the 
    # request data.
    else:
        # Convert the request.data JSON to a Python dict, and pull out the 
        # function name, args, and kwargs.  
        if requestMethod in ['POST', 'PUT']:
            reqdict = json.loads(request.data)
        elif requestMethod == 'GET':
            reqdict = request.args
        fn_name = reqdict['funcname']
        args = reqdict.get('args', [])
        # Insert the username as a the first argument if it is passed in not
        # None.
        if username is not None:
            args.insert(0, username)
        kwargs = reqdict.get('kwargs', {})
        
    # Check to see if the function exists here in main.py and get it 
    # ready to call if it is.  Any versions of the functions in main.py 
    # override those versions in user.py or project.py (or other places 
    # where we have handlers).
    funcExists = hasattr(sys.modules[__name__], fn_name)
    print('>> Checking RPC function "main.%s" -> %s' % (fn_name, funcExists))
    if funcExists:
        func = getattr(sys.modules[__name__], fn_name)
        handlerLocation = 'main'
        
    # Otherwise (it's not in main.py), if the handlerLocation is 'user'...
    elif handlerLocation == 'user':
        # Check to see if there is a match.
        funcExists = hasattr(user, fn_name)
        print('>> Checking RPC function "user.%s" -> %s' % (fn_name, funcExists))
        
        # If there is a match, get the function ready.
        if funcExists:
            func = getattr(user, fn_name)
            
    # Otherwise (the function isn't in main.py and the handler is not 'user')...
    elif handlerLocation == 'project':
        # Check to see if there is a match.
        funcExists = hasattr(project, fn_name)
        print('>> Checking RPC function "project.%s" -> %s' % (fn_name, funcExists))
        
        # If there is a match, get the function ready.
        if funcExists:
            func = getattr(project, fn_name)   
            
    elif handlerLocation not in['scirismain', 'main', 'user', 'project']:
        return jsonify({'error': 
            'Attempted to call RPC function in non-existent handler location \'%s\'' \
                % handlerLocation}) 

    # If the function doesn't exist, return an error to the client saying it 
    # doesn't exist.
    if not funcExists:
        return jsonify({'error': 
            'Attempted to call non-existent RPC function \'%s\'' % fn_name}) 
    
    # If we are doing an upload.
    if rpcType == 'upload':
        # Grab the formData file that was uploaded.    
        file = request.files['uploadfile']
        
        # Grab the filename of this file, and generate the full upload path / 
        # filename.
        filename = secure_filename(file.filename)
        uploaded_fname = os.path.join(ds.uploadsPath, filename)
        
        # Save the file to the uploads directory.
        file.save(uploaded_fname)
        
        # Prepend the file name to the args list.
        args.insert(0, uploaded_fname)
        
    # Show the call of the function.    
    print('>> Calling RPC function "%s.%s"' % (handlerLocation, fn_name))
    
    # Execute the function to get the results.
    result = func(*args, **kwargs)  
    
    # If we are doing a download, prepare the response and send it off.
    if rpcType == 'download':
        # If we got None for a result (the full file name), return an error to 
        # the client.
        if result is None:
            return jsonify({'error': 'Could not find requested resource'})
    
        # Pull out the directory and file names from the full file name.
        dirName, fileName = os.path.split(result)
         
        # Make the response message with the file loaded as an attachment.
        response = send_from_directory(dirName, fileName, as_attachment=True)
        response.status_code = 201  # Status 201 = Created
        response.headers['filename'] = fileName
        
        # Return the response message.
        return response
    
    # Otherwise (normal and upload RPCs), 
    else:
        # If None was returned by the RPC function, return ''.
        if result is None:
            return ''
        
        # Otherwise, convert the result (probably a dict) to JSON and return it.
        else:
            return jsonify(json_sanitize_result(result))

def json_sanitize_result(theResult):
    """
    This is the main conversion function for Python data-structures into
    JSON-compatible data structures.

    Use this as much as possible to guard against data corruption!

    Args:
        theResult: almost any kind of data structure that is a combination
            of list, numpy.ndarray, etc.

    Returns:
        A converted dict/list/value that should be JSON compatible
    """

    if isinstance(theResult, list) or isinstance(theResult, tuple):
        return [json_sanitize_result(p) for p in list(theResult)]
    
    if isinstance(theResult, np.ndarray):
        if theResult.shape: # Handle most cases, incluing e.g. array([5])
            return [json_sanitize_result(p) for p in list(theResult)]
        else: # Handle the special case of e.g. array(5)
            return [json_sanitize_result(p) for p in list(np.array([theResult]))]

    if isinstance(theResult, dict):
        return {str(k): json_sanitize_result(v) for k, v in theResult.items()}

    if isinstance(theResult, np.bool_):
        return bool(theResult)

    if isinstance(theResult, float):
        if np.isnan(theResult):
            return None

    if isinstance(theResult, np.float64):
        if np.isnan(theResult):
            return None
        else:
            return float(theResult)

    if isinstance(theResult, unicode):
        return str(theResult)

    if isinstance(theResult, set):
        return list(theResult)

#    if isinstance(theResult, UUID):
#        return str(theResult)

    return theResult
        
#
# RPC functions
#

##
## User RPCs
##

# We will have some overrides here because we want to handle account editing 
# and password changing in a way different than the defaults.

##
## Project RPCs
##

# We will probably have some of these here, though I want to move as much as 
# I can into sciris/project.py.

##
## Temporary (development) RPCs
##

# This is a temporary RPC, just a development placeholder.

def read_ihme_table():
    # Check (for security purposes) that the function is being called by the 
    # correct endpoint, and if not, fail.
    if request.endpoint != 'normalRPC':
        return {'error': 'Unauthorized RPC'}
    
    # Load the data path holding the Excel files.
    dataPath = hptool.HPpath('data')
    
    # Load the project.
    P = hptool.Project(burdenfile=dataPath + 'ihme-gbd.xlsx', 
        interventionsfile=dataPath + 'dcp-data.xlsx')
    
    # The data of interest is in
    # P.burdensets[0].data, which is a list of odicts.  Each odict contains
    # the elements for that row of data.

    # Gather the list for all of the diseases.
    diseaseData = [list(theDisease) for theDisease in P.burdensets[0].data]
    
    # Return success.
    return { 'diseases': diseaseData }