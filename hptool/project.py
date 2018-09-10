#######################################################################################################
## Imports and setup
#######################################################################################################

import hptool as hp
import sciris as sc


#######################################################################################################
## Project class -- this contains everything else!
#######################################################################################################

class Project(object):
    """
    PROJECT

    The main HealthPrior project class. Almost all functionality is provided by this class.

    An HP project is based around 4 major lists:
        1. burdensets  -- an odict of burden data
        2. intersets   -- an odict of intervention sets
        3. packagesets -- an odict of health packages


    Methods for structure lists:
        1. add -- add a new structure to the odict
        2. remove -- remove a structure from the odict
        3. copy -- copy a structure in the odict
        4. rename -- rename a structure in the odict

    Version: 2018sep09
    """



    #######################################################################################################
    ### Built-in methods -- initialization, and the thing to print if you call a project
    #######################################################################################################

    def __init__(self, name='Default', burdenfile=None, interventionsfile=None, country=None, make_package=True, verbose=2, **kwargs):
        ''' Initialize the project '''

        ## Define the structure sets
        self.burdensets  = sc.odict()
        self.intersets   = sc.odict()
        self.packagesets = sc.odict()

        ## Define other quantities
        self.name = name
        self.country = country
        self.uid = sc.uuid()
        self.created = sc.now()
        self.modified = sc.now()
        self.version = hp.version
        self.gitinfo = sc.gitinfo(__file__)
        self.filename = None # File path, only present if self.save() is used

        ## Load burden spreadsheet, if available
        if burdenfile:
            burden = hp.Burden(project=self)
            burden.loaddata(filename=burdenfile)
            self.burdensets['Default'] = burden
        
        ## Load interventions spreadsheet, if available
        if interventionsfile:
            interventions = hp.Interventions(project=self)
            interventions.loaddata(filename=interventionsfile)
            self.intersets['Default'] = interventions
        
        ## Combine into health package, if available
        if make_package and burdenfile and interventionsfile:
            package = hp.HealthPackage(project=self)
            package.make_package()
            self.packagesets['Default'] = package

        return None


    def __repr__(self):
        ''' Print out useful information when called '''
        output = sc.objrepr(self)
        output += '      Project name: %s\n'    % self.name
        output += '           Country: %s\n'    % self.country
        output += '\n'
        output += '       Burden sets: %i\n'    % len(self.burdensets)
        output += ' Intervention sets: %i\n'    % len(self.intersets)
        output += '   Health packages: %i\n'    % len(self.packagesets)
        output += '\n'
        output += '        HP version: %s\n'    % self.version
        output += '      Date created: %s\n'    % sc.getdate(self.created)
        output += '     Date modified: %s\n'    % sc.getdate(self.modified)
        output += '        Git branch: %s\n'    % self.gitinfo['branch']
        output += '          Git hash: %s\n'    % self.gitinfo['hash']
        output += '               UID: %s\n'    % self.uid
        output += '============================================================\n'
        return output
    
    
    def getinfo(self):
        ''' Return an odict with basic information about the project'''
        info = sc.odict()
        for attr in ['name', 'version', 'created', 'modified', 'gitbranch', 'gitversion', 'uid']:
            info[attr] = getattr(self, attr) # Populate the dictionary
        return info
    
    
    def save(self, filename=None, folder=None, verbose=2):
        ''' Save the current project, by default using its name, and without results '''
        fullpath = sc.makefilepath(filename=filename, folder=folder, default=[self.filename, self.name], ext='prj', sanitize=True)
        self.filename = fullpath # Store file path
        sc.saveobj(fullpath, self, verbose=verbose)
        return fullpath


    #######################################################################################################
    ### Utilities
    #######################################################################################################

    def burden(self, key=None, verbose=2):
        ''' Shortcut for getting the latest active burden set, i.e. self.burdensets[-1] '''
        if key is None: key = hp.default_key
        try:    return self.burdensets[key]
        except: return sc.printv('Warning, burden set not found!', 1, verbose) # Returns None
    
    def inter(self, key=None, verbose=2):
        ''' Shortcut for getting the latest active interventions set, i.e. self.intersets[-1] '''
        if key is None: key = hp.default_key
        try:    return self.intersets[key]
        except: return sc.printv('Warning, interventions set not found!', 1, verbose) # Returns None
    
    def package(self, key=None, verbose=2):
        ''' Shortcut for getting the latest active health packages set, i.e. self.intersets[-1] '''
        if key is None: key = hp.default_key
        try:    return self.packagesets[key]
        except: return sc.printv('Warning, interventions set not found!', 1, verbose) # Returns None
        

def demo(name=None):
    if name is None: name = 'Default'
    datadir = hp.HPpath('data')
    burdenpath = datadir + 'ihme-gbd.xlsx'
    datapath = datadir + 'dcp-data-afg-v1.xlsx'
    project = Project(name=name, burdenfile=burdenpath, interventionsfile=datapath)  
    project.burden().popsize = 34.66e6 # From UN population division 
    return project