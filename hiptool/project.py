#######################################################################################################
## Imports and setup
#######################################################################################################

import hiptool as hp
import sciris as sc


#######################################################################################################
## Project class -- this contains everything else!
#######################################################################################################

class Project(object):
    """
    PROJECT

    The main HIPtool project class. Almost all functionality is provided by this class.

    An HP project is based around 4 major lists:
        1. burdensets  -- an odict of burden data
        2. intervsets   -- an odict of intervention sets
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

    def __init__(self, name='Default', burdenfile=None, interventionsfile=None, country=None, makepackage=True, verbose=2):
        ''' Initialize the project '''

        ## Define the structure sets
        self.burdensets  = sc.odict()
        self.intervsets   = sc.odict()
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
            self.loadburden(filename=burdenfile, verbose=verbose)
        
        ## Load interventions spreadsheet, if available
        if interventionsfile:
            self.loadinterventions(filename=interventionsfile, verbose=verbose)
        
        ## Combine into health package, if available
        if makepackage and burdenfile and interventionsfile:
            self.makepackage()

        return None


    def __repr__(self):
        ''' Print out useful information when called '''
        output = sc.objrepr(self)
        output += '      Project name: %s\n'    % self.name
        output += '           Country: %s\n'    % self.country
        output += '\n'
        output += '       Burden sets: %i\n'    % len(self.burdensets)
        output += ' Intervention sets: %i\n'    % len(self.intervsets)
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
    
    
    def restorelinks(self):
        for thisset in self.burdensets.values() + self.intervsets.values() + self.packagesets.values():
            thisset.projectref = sc.Link(self)
        return None


    #######################################################################################################
    ### Utilities
    #######################################################################################################

    def burden(self, key=None, verbose=2):
        ''' Shortcut for getting the latest active burden set, i.e. self.burdensets[-1] '''
        if key is None: key = hp.default_key
        try:    return self.burdensets[key]
        except: return sc.printv('Warning, burden set not found!', 1, verbose) # Returns None
    
    def interv(self, key=None, verbose=2):
        ''' Shortcut for getting the latest active interventions set, i.e. self.intersets[-1] '''
        if key is None: key = hp.default_key
        try:    return self.intervsets[key]
        except: return sc.printv('Warning, interventions set not found!', 1, verbose) # Returns None
    
    def package(self, key=None, verbose=2):
        ''' Shortcut for getting the latest active health packages set, i.e. self.intervsets[-1] '''
        if key is None: key = hp.default_key
        try:    return self.packagesets[key]
        except: return sc.printv('Warning, interventions set not found!', 1, verbose) # Returns None


    #######################################################################################################
    ### Data loading
    #######################################################################################################

    def loadburden(self, filename=None, folder=None, name=None, verbose=2):
        ''' Shortcut for getting the latest active burden set, i.e. self.burdensets[-1] '''
        burden = hp.Burden(project=self, filename=filename, folder=folder, name=name)
        self.burdensets[burden.name] = burden
        return burden
    
    def loadinterventions(self, filename=None, folder=None, name=None, verbose=2):
        ''' Shortcut for getting the latest active burden set, i.e. self.burdensets[-1] '''
        interventions = hp.Interventions(project=self, filename=filename, folder=folder, name=name)
        self.intervsets[interventions.name] = interventions
        return interventions
    
    def makepackage(self, burdenset=None, intervset=None, **kwargs):
        if len(self.burdensets)==0:
            errormsg = 'Please ensure you have uploaded burden of disease data (0 burden sets found)'
            raise Exception(errormsg)
        if len(self.intervsets)==0:
            errormsg = 'Please ensure you have uploaded intervention data (0 intervention sets found)'
            raise Exception(errormsg)
        if burdenset is None: burdenset = self.burdensets.keys()[-1]
        if intervset is None: intervset = self.intervsets.keys()[-1]
        name = burdenset + ' + ' + intervset
        package = hp.HealthPackage(project=self, name=name, burdenset=burdenset, intervset=intervset, makepackage=True, **kwargs)
        self.packagesets[package.name] = package
        return package



def demo(country=None):
    datadir     = hp.HPpath('data')
    if country is None:
        burdenspath = datadir + 'Demo BoD.xlsx'
    else:
        burdenspath = country
    intervspath = datadir + 'Demo interventions.xlsx'
    project = Project(name='Demo', burdenfile=burdenspath, interventionsfile=intervspath, makepackage=True)
    return project