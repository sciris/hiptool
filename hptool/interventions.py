"""
Version:
"""

import sciris as sc

class Interventions(object):
    '''
    Class to hold all interventions, e.g. from DCP3. Data stored include:
    1.	Intervention name
    2.	Targeted disease
    3.	Delivery platform
    4.	Unit cost per person covered
    5.	ICER
    6.	Equity score
    7.	Financial risk protection score

    Version: 2018sep27
    '''
    
    def __init__(self, name=None, project=None, filename=None, folder=None):
        if name is None: name = 'Default'
        self.projectref = sc.Link(project) # Store pointer for the project
        self.name       = sc.uniquename(name, namelist=self.projectref().intervsets.keys()) # Name of the parameter set, e.g. 'default'
        self.uid        = sc.uuid() # ID
        self.created    = sc.now() # Date created
        self.modified   = sc.now() # Date modified
        self.data       = None
        if filename is not None:
            self.loaddata(filename=filename, folder=folder)
        return None
    
    def __repr__(self):
        ''' Print out useful information when called'''
        output  = sc.prepr(self)
        output += 'Intervention set name: %s\n'    % self.name
        output += '         Date created: %s\n'    % sc.getdate(self.created)
        output += '        Date modified: %s\n'    % sc.getdate(self.modified)
        output += '                  UID: %s\n'    % self.uid
        output += '============================================================\n'
        return output
    
    def loaddata(self, filename=None, folder=None):
        ''' Load data from a spreadsheet '''
        self.data = sc.loadspreadsheet(filename=filename, folder=folder)
        self.filename = filename
        return None
    
    def savedata(self, filename=None, folder=None):
        ''' Export data from a spreadsheet '''
        filepath = self.data.export(filename=filename)
        return filepath
    
    def jsonify(self, cols=None, rows=None, header=None):
        ''' Export to a JSON-friendly representation '''
        output = self.data.jsonify(cols=cols, rows=rows, header=header)
        return output