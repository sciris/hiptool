from hpptool import odict, uuid, today, version, gitinfo, objrepr, getdate
from hpptool import isnumber, printv
from hpptool import HPException, Interventions


#######################################################################################################
## Project class -- this contains everything else!
#######################################################################################################

class Project(object):
    """
    PROJECT

    The main HealthPrior project class. Almost all functionality is provided by this class.

    An HP project is based around 4 major lists:
        1. burdens -- an odict of burden data
        2. intervs -- an odict of program sets
        3. optims -- an odict of optimization structures
        4. results -- an odict of results associated with the choices above


    Methods for structure lists:
        1. add -- add a new structure to the odict
        2. remove -- remove a structure from the odict
        3. copy -- copy a structure in the odict
        4. rename -- rename a structure in the odict

    Version: 2017oct30
    """



    #######################################################################################################
    ### Built-in methods -- initialization, and the thing to print if you call a project
    #######################################################################################################

    def __init__(self, name='default', burdenfile=None, interventionsfile=None, verbose=2, **kwargs):
        ''' Initialize the project '''

        ## Define the structure sets
        self.burdensets  = odict()
        self.intersets   = odict()
        self.optims      = odict()
        self.results     = odict()

        ## Define other quantities
        self.name = name
        self.uid = uuid()
        self.created = today()
        self.modified = today()
        self.spreadsheetdate = 'Spreadsheet never loaded'
        self.version = version
        self.gitbranch, self.gitversion = gitinfo()
        self.filename = None # File path, only present if self.save() is used
        self.warnings = None # Place to store information about warnings (mostly used during migrations)

        ## Load burden spreadsheet, if available
        if burdenfile:
            self.loadburden(burdenfile, verbose=verbose, **kwargs)
        
        ## Load interventions spreadsheet, if available
        if interventionsfile:
            interventions = Interventions(project=self)
            interventions.loaddata(filename=interventionsfile)
            self.intersets['default'] = interventions

        return None


    def __repr__(self):
        ''' Print out useful information when called '''
        output = objrepr(self)
        output += '      Project name: %s\n'    % self.name
        output += '\n'
        output += '       Burden sets: %i\n'    % len(self.burdensets)
        output += ' Intervention sets: %i\n'    % len(self.intersets)
        output += '     Optimizations: %i\n'    % len(self.optims)
        output += '      Results sets: %i\n'    % len(self.results)
        output += '\n'
        output += '        HP version: %s\n'    % self.version
        output += '      Date created: %s\n'    % getdate(self.created)
        output += '     Date modified: %s\n'    % getdate(self.modified)
        output += 'Spreadsheet loaded: %s\n'    % getdate(self.spreadsheetdate)
        output += '        Git branch: %s\n'    % self.gitbranch
        output += '       Git version: %s\n'    % self.gitversion
        output += '               UID: %s\n'    % self.uid
        output += '============================================================\n'
        output += self.getwarnings(doprint=False) # Don't print since print later
        return output
    
    
    def getinfo(self):
        ''' Return an odict with basic information about the project -- used in resultsets '''
        info = odict()
        for attr in ['name', 'version', 'created', 'modified', 'spreadsheetdate', 'gitbranch', 'gitversion', 'uid']:
            info[attr] = getattr(self, attr) # Populate the dictionary
        info['parsetkeys'] = self.parsets.keys()
        info['progsetkeys'] = self.parsets.keys()
        return info
    
    
    def addwarning(self, message=None, **kwargs):
        ''' Add a warning to the project, which is printed when migrated or loaded '''
        if not hasattr(self, 'warnings') or type(self.warnings)!=str: # If no warnings attribute, create it
            self.warnings = ''
        self.warnings += '\n'*3+str(message) # # Add this warning
        return None


    def getwarnings(self, doprint=True):
        ''' Tiny method to print the warnings in the project, if any '''
        if hasattr(self, 'warnings') and self.warnings: # There are warnings
            output = '\nWARNING: This project contains the following warnings:'
            output += str(self.warnings)
        else: # There are no warnings
            output = ''
        if output and doprint: # Print warnings if requested
            print(output)
        return output


    #######################################################################################################
    ### Methods for I/O and spreadsheet loading
    #######################################################################################################

#    def loadspreadsheet(self, filename=None, folder=None, name=None, overwrite=False, makedefaults=True, dorun=True, **kwargs):
#        ''' Load a data spreadsheet -- enormous, ugly function so located in its own file '''
#        ## Load spreadsheet and update metadata
#        self.data = loadspreadsheet(filename=filename, folder=folder, verbose=self.settings.verbose) # Do the hard work of actually loading the spreadsheet
#        self.spreadsheetdate = today() # Update date when spreadsheet was last loaded
#        self.modified = today()
#        if name is None: name = 'default'
#        self.makeparset(name=name, overwrite=overwrite)
#        if makedefaults: self.makedefaults(name)
#        self.settings.start = self.data['years'][0] # Reset the default simulation start to initial year of data
#        if dorun: self.runsim(name, addresult=True, **kwargs) # Pass all kwargs to runsim as well
#        if self.name == 'default' and filename.endswith('.xlsx'): self.name = os.path.basename(filename)[:-5] # If no project filename is given, reset it to match the uploaded spreadsheet, assuming .xlsx extension
#        return None
#
#
#    def makespreadsheet(self, filename=None, folder=None, pops=None, datastart=None, dataend=None):
#        ''' Create a spreadsheet with the data from the project'''
#        fullpath = makefilepath(filename=filename, folder=folder, default=self.name, ext='xlsx')
#        if datastart is None: 
#            try:    datastart = self.data['years'][0]
#            except: datastart = self.settings.start
#        if dataend is None:   
#            try:    dataend = self.data['years'][-1]
#            except: dataend = self.settings.dataend
#        makespreadsheet(filename=fullpath, pops=pops, data=self.data, datastart=datastart, dataend=dataend)
#        return fullpath






    #######################################################################################################
    ### Methods to handle common tasks with structure lists
    #######################################################################################################


#    def getwhat(self, item=None, what=None):
#        '''
#        Figure out what kind of structure list is being requested, e.g.
#            structlist = getwhat('parameters')
#        will return P.parset.
#        '''
#        if item is None and what is None: raise HPException('No inputs provided')
#        if what is not None: # Explicitly define the type, item be damned
#            if what in ['p', 'pars', 'parset', 'parameters']: structlist = self.parsets
#            elif what in ['pr', 'progs', 'progset', 'progsets']: structlist = self.progsets # WARNING, inconsistent terminology!
#            elif what in ['s', 'scen', 'scens', 'scenario', 'scenarios']: structlist = self.scens
#            elif what in ['o', 'opt', 'opts', 'optim', 'optims', 'optimisation', 'optimization', 'optimisations', 'optimizations']: structlist = self.optims
#            elif what in ['r', 'res', 'result', 'results']: structlist = self.results
#            else: raise HPException('Structure list "%s" not understood' % what)
#        else: # Figure out the type based on the input
#            if type(item)==Parameterset: structlist = self.parsets
#            elif type(item)==Programset: structlist = self.progsets
#            elif type(item)==Resultset: structlist = self.results
#            else: raise HPException('Structure list "%s" not understood' % str(type(item)))
#        return structlist


    def checkname(self, what=None, checkexists=None, checkabsent=None, overwrite=True):
        ''' Check that a name exists if it needs to; check that a name doesn't exist if it's not supposed to '''
        if type(what)==odict: structlist=what # It's already a structlist
        else: structlist = self.getwhat(what=what)
        if isnumber(checkexists): # It's a numerical index
            try: checkexists = structlist.keys()[checkexists] # Convert from 
            except: raise HPException('Index %i is out of bounds for structure list "%s" of length %i' % (checkexists, what, len(structlist)))
        if checkabsent is not None:
            if checkabsent in structlist:
                if overwrite==False:
                    raise HPException('Structure list "%s" already has item named "%s"' % (what, checkabsent))
                else:
                    printv('Structure list already has item named "%s"' % (checkabsent), 3, self.settings.verbose)
                
        if checkexists is not None:
            if not checkexists in structlist:
                raise HPException('Structure list has no item named "%s"' % (checkexists))
        return None


#    def add(self, name=None, item=None, what=None, overwrite=True, consistentnames=True):
#        ''' Add an entry to a structure list -- can be used as add('blah', obj), add(name='blah', item=obj), or add(item) '''
#        if name is None:
#            try: name = item.name # Try getting name from the item
#            except: name = 'default' # If not, revert to default
#        if item is None:
#            if type(name)!=str: # Maybe an item has been supplied as the only argument
#                try: 
#                    item = name # It's actully an item, not a name
#                    name = item.name # Try getting name from the item
#                except: raise HPException('Could not figure out how to add item with name "%s" and item "%s"' % (name, item))
#            else: # No item has been supplied, add a default one
#                if what=='parset':  
#                    item = Parameterset(name=name, project=self)
#                    item.makepars(self.data, verbose=self.settings.verbose) # Create parameters
#                elif what=='progset': 
#                    item = Programset(name=name, project=self)
#                elif what=='scen':
#                    item = Parscen(name=name)
#                elif what=='optim': 
#                    item = Optim(project=self, name=name)
#                else:
#                    raise HPException('Unable to add item of type "%s", please supply explicitly' % what)
#        structlist = self.getwhat(item=item, what=what)
#        self.checkname(structlist, checkabsent=name, overwrite=overwrite)
#        structlist[name] = item
#        if consistentnames: structlist[name].name = name # Make sure names are consistent -- should be the case for everything except results, where keys are UIDs
#        if hasattr(structlist[name], 'projectref'): structlist[name].projectref = Link(self) # Fix project links
#        printv('Item "%s" added to "%s"' % (name, what), 3, self.settings.verbose)
#        self.modified = today()
#        return None
#
#
#    def remove(self, what=None, name=None):
#        ''' Remove an entry from a structure list by name '''
#        if name is None: name = -1 # If no name is supplied, remove the last item
#        structlist = self.getwhat(what=what)
#        self.checkname(what, checkexists=name)
#        structlist.pop(name)
#        printv('%s "%s" removed' % (what, name), 3, self.settings.verbose)
#        self.modified = today()
#        return None
#
#
#    def copy(self, what=None, orig=None, new=None, overwrite=True):
#        ''' Copy an entry in a structure list '''
#        if orig is None: orig = -1
#        if new  is None: new = 'new'
#        structlist = self.getwhat(what=what)
#        self.checkname(what, checkexists=orig, checkabsent=new, overwrite=overwrite)
#        structlist[new] = dcp(structlist[orig])
#        structlist[new].name = new  # Update name
#        structlist[new].uid = uuid()  # Otherwise there will be 2 structures with same unique identifier
#        structlist[new].created = today() # Update dates
#        structlist[new].modified = today() # Update dates
#        if hasattr(structlist[new], 'projectref'): structlist[new].projectref = Link(self) # Fix project links
#        printv('%s "%s" copied to "%s"' % (what, orig, new), 3, self.settings.verbose)
#        self.modified = today()
#        return None
#
#
#    def rename(self, what=None, orig=None, new=None, overwrite=True):
#        ''' Rename an entry in a structure list '''
#        if orig is None: orig = -1
#        if new  is None: new = 'new'
#        structlist = self.getwhat(what=what)
#        self.checkname(what, checkexists=orig, checkabsent=new, overwrite=overwrite)
#        structlist.rename(oldkey=orig, newkey=new)
#        structlist[new].name = new # Update name
#        printv('%s "%s" renamed "%s"' % (what, orig, new), 3, self.settings.verbose)
#        self.modified = today()
#        return None
        

    #######################################################################################################
    ### Convenience functions -- NOTE, do we need these...?
    #######################################################################################################

#    def addparset(self,   name=None, parset=None,   overwrite=True): self.add(what='parset',   name=name, item=parset,  overwrite=overwrite)
#    def addprogset(self,  name=None, progset=None,  overwrite=True): self.add(what='progset',  name=name, item=progset, overwrite=overwrite)
#    def addscen(self,     name=None, scen=None,     overwrite=True): self.add(what='scen',     name=name, item=scen,    overwrite=overwrite)
#    def addoptim(self,    name=None, optim=None,    overwrite=True): self.add(what='optim',    name=name, item=optim,   overwrite=overwrite)
#
#    def rmparset(self,   name=None): self.remove(what='parset',   name=name)
#    def rmprogset(self,  name=None): self.remove(what='progset',  name=name)
#    def rmscen(self,     name=None): self.remove(what='scen',     name=name)
#    def rmoptim(self,    name=None): self.remove(what='optim',    name=name)
#
#
#    def copyparset(self,  orig=None, new=None, overwrite=True): self.copy(what='parset',   orig=orig, new=new, overwrite=overwrite)
#    def copyprogset(self, orig=None, new=None, overwrite=True): self.copy(what='progset',  orig=orig, new=new, overwrite=overwrite)
#    def copyscen(self,    orig=None, new=None, overwrite=True): self.copy(what='scen',     orig=orig, new=new, overwrite=overwrite)
#    def copyoptim(self,   orig=None, new=None, overwrite=True): self.copy(what='optim',    orig=orig, new=new, overwrite=overwrite)
#
#    def renameparset(self,  orig=None, new=None, overwrite=True): self.rename(what='parset',   orig=orig, new=new, overwrite=overwrite)
#    def renameprogset(self, orig=None, new=None, overwrite=True): self.rename(what='progset',  orig=orig, new=new, overwrite=overwrite)
#    def renamescen(self,    orig=None, new=None, overwrite=True): self.rename(what='scen',     orig=orig, new=new, overwrite=overwrite)
#    def renameoptim(self,   orig=None, new=None, overwrite=True): self.rename(what='optim',    orig=orig, new=new, overwrite=overwrite)


#    def addscens(self, scenlist, overwrite=True): 
#        ''' Function to make it slightly easier to add scenarios all in one go '''
#        if overwrite: self.scens = odict() # Remove any existing scenarios
#        scenlist = promotetolist(scenlist) # Allow adding a single scenario
#        for scen in scenlist: self.addscen(name=scen.name, scen=scen, overwrite=True)
#        self.modified = today()
#        return None
#
#
#    def addresult(self, result=None, overwrite=True): 
#        ''' Try adding result by name, but if no name, add by UID '''
#        if result.name is None: keyname = str(result.uid)
#        else: keyname = result.name
#        self.add(what='result',  name=keyname, item=result, consistentnames=False, overwrite=overwrite) # Use UID for key but keep name
#        return keyname # Can be useful to know what ended up being chosen
#    
#    def rmresult(self, name=-1):
#        ''' Remove a single result by name '''
#        resultuids = self.results.keys() # Pull out UID keys
#        resultnames = [res.name for res in self.results.values()] # Pull out names
#        if isnumber(name) and name<len(self.results):  # Remove by index rather than name
#            self.remove(what='result', name=self.results.keys()[name])
#        elif name in resultuids: # It's a UID: remove directly 
#            self.remove(what='result', name=name)
#        elif name in resultnames: # It's a name: find the UID corresponding to this name and remove
#            self.remove(what='result', name=resultuids[resultnames.index(name)]) # WARNING, if multiple names match, will delete oldest one -- expected behavior?
#        else:
#            validchoices = ['#%i: name="%s", uid=%s' % (i, resultnames[i], resultuids[i]) for i in range(len(self.results))]
#            errormsg = 'Could not remove result "%s": choices are:\n%s' % (name, '\n'.join(validchoices))
#            raise HPException(errormsg)
#        return None
#    
#    
#    def cleanresults(self):
#        ''' Remove all results except for BOCs '''
#        for key,result in self.results.items():
#            if type(result)!=BOC: self.results.pop(key)
#        return None
    
#    def save(self, filename=None, folder=None, saveresults=False, verbose=2):
#        ''' Save the current project, by default using its name, and without results '''
#        fullpath = makefilepath(filename=filename, folder=folder, default=[self.filename, self.name], ext='prj', sanitize=True)
#        self.filename = fullpath # Store file path
#        if saveresults:
#            saveobj(fullpath, self, verbose=verbose)
#        else:
#            tmpproject = dcp(self) # Need to do this so we don't clobber the existing results
#            tmpproject.restorelinks() # Make sure links are restored
#            tmpproject.cleanresults() # Get rid of all results
#            saveobj(fullpath, tmpproject, verbose=verbose) # Save it to file
#            del tmpproject # Don't need it hanging around any more
#        return fullpath


    #######################################################################################################
    ### Utilities
    #######################################################################################################

