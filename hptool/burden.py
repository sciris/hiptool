"""
Version:
"""

from hptool import uuid, Link, today, defaultrepr, getdate, loadspreadsheet

class Burden(object):
    ''' Class to hold all burden data, e.g. from IHME GBD. Data stored are/will be:
    1.	Primary cause name
    2.	Health category
    3.	Population prevalence by year*
    4.	Number of people affected by year*
    5.	Total DALYs by year
    6.	Total mortality by year
    
    From http://ghdx.healthdata.org/gbd-results-tool
    '''
    
    def __init__(self, name='default', project=None):
        self.name = name # Name of the parameter set, e.g. 'default'
        self.uid = uuid() # ID
        self.projectref = Link(project) # Store pointer for the project, if available
        self.created = today() # Date created
        self.modified = today() # Date modified
        self.data = None
        self.filename = None
        self.popsize = None
    
    def __repr__(self):
        ''' Print out useful information when called'''
        output  = defaultrepr(self)
        output += 'Burden set name: %s\n'    % self.name
        output += '   Date created: %s\n'    % getdate(self.created)
        output += '  Date modified: %s\n'    % getdate(self.modified)
        output += '            UID: %s\n'    % self.uid
        output += '============================================================\n'
        return output
    
    def loaddata(self, filename=None, folder=None):
        ''' Load data from a spreadsheet '''
        self.data = loadspreadsheet(filename=filename, folder=folder)
        self.filename = filename
        return None
    
    def plottopcauses(self, which=None, n=None):
        '''
        Create a bar plot of the top causes of burden. By default, plots the top
        10 causes of DALYs.
        
        Version: 2018mar17        
        '''
        # Handle options
        if which is None: which = 'dalys'
        if n     is None: n     = 10
        
        return None
        