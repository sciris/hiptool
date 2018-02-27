"""
Version:
"""

from hptool import uuid, Link, today, defaultrepr, getdate, loadspreadsheet


class Interventions(object):
    ''' Class to hold all interventions, e.g. from DCP3. Data stored are/will be:
    1.	Intervention name
    2.	Targeted disease
    3.	Delivery platform
    4.	Unit cost per person covered
    5.	DALYs averted per person covered*
    6.	Deaths averted per person covered**
    7.	Cost per DALY averted*
    8.	Cost per death averted**
    9.	Default coverage of intervention
    10.	Maximum coverage of intervention
    11.	Equity score
    12.	Financial risk protection score
    '''
    
    def __init__(self, name='default', project=None):
        self.name = name # Name of the parameter set, e.g. 'default'
        self.uid = uuid() # ID
        self.projectref = Link(project) # Store pointer for the project, if available
        self.created = today() # Date created
        self.modified = today() # Date modified
        self.data = None
        self.filename = None
    
    def __repr__(self):
        ''' Print out useful information when called'''
        output  = defaultrepr(self)
        output += 'Intervention set name: %s\n'    % self.name
        output += '         Date created: %s\n'    % getdate(self.created)
        output += '        Date modified: %s\n'    % getdate(self.modified)
        output += '                  UID: %s\n'    % self.uid
        output += '============================================================\n'
        return output
    
    def loaddata(self, filename=None, folder=None):
        ''' Load data from a spreadsheet '''
        self.data = loadspreadsheet(filename=filename, folder=folder)
        self.filename = filename