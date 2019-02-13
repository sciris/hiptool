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

    Version: 2018oct02
    '''
    
    def __init__(self, name=None, project=None, filename=None, folder=None):
        if name is None: name = 'Default'
        self.projectref = sc.Link(project) # Store pointer for the project
        self.name       = sc.uniquename(name, namelist=self.projectref().intervsets.keys()) # Name of the parameter set, e.g. 'default'
        self.uid        = sc.uuid() # ID
        self.created    = sc.now() # Date created
        self.modified   = sc.now() # Date modified
        
        # Define hard-coded column names
        self.colnames = sc.odict([('active',   'Active'),
                                  ('shortname','Short name'),
                                  ('platform', 'Platform'),
                                  ('burdencov','Causes of burden (max coverage)'),
                                  ('icer',     'ICER'),
                                  ('unitcost', 'Unit cost'),
                                  ('spend',    'Spending'),
                                  ('frp',      'FRP'),
                                  ('equity',   'Equity'),
                                  ])
        
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
    
    
    def parse(self, rows=None, verbose=False):
        if verbose: print('Parsing data...')
        burdencov = sc.dcp(self.data[self.colnames['burdencov']])
        
        # Validation
        if 'parsedbc' not in self.data.cols: self.data.addcol('parsedbc')
        if rows is None: rows = range(len(burdencov))
        else:            rows = sc.promotetolist(rows)
            
        # Iterate
        for r in rows:
            thisburdencov = burdencov[r]
            if verbose: print('Working on "%s"' % thisburdencov)
            try:
                burdencovsplit = thisburdencov.split(';') # Try to split into causes
            except Exception as E:
                errormsg = 'Could not split "%s" into separate burdens: %s' % (thisburdencov, str(E))
                raise Exception(errormsg)
            for b,bs in enumerate(burdencovsplit):
                burdencovsplit[b] = bs.split(':') # Split into burden and coverage
                thisbcsplit = burdencovsplit[b]
                if len(thisbcsplit) != 2:
                    errormsg = 'Could not split "%s" into burden and coverage, perhaps coverage is missing?' % (thisbcsplit)
                    raise Exception(errormsg)
                else:
                    thisbcsplit[0] = thisbcsplit[0].lstrip().rstrip() # Strip leading and trailing spaces
                    try:
                        thisbcsplit[1] = float(thisbcsplit[1])
                    except Exception as E:
                        errormsg = 'Could not convert "%s" from "%s" to a number: %s' % (thisbcsplit[1], thisburdencov, str(E))
                        raise Exception(errormsg)
                    if thisbcsplit[1]<0 or thisbcsplit[1]>1:
                        errormsg = 'Maximum coverage must be between 0 and 1, not %s (from "%s")' % (thisbcsplit[1], thisburdencov)
                        raise Exception(errormsg)
            
            self.data['parsedbc', r] = burdencovsplit # Save back to the data structure
        return None
        
    
    def loaddata(self, filename=None, folder=None):
        ''' Load data from a spreadsheet '''
        self.data = sc.loadspreadsheet(filename=filename, folder=folder)
        self.data.filtercols(self.colnames.values(), die=True)
        self.filename = filename
        self.parse()
        return None
    
    def savedata(self, filename=None, folder=None, cols=None):
        ''' Export data from a spreadsheet '''
        filepath = self.data.export(filename=filename, cols=self.colnames.values())
        return filepath
    
    def jsonify(self, cols=None, rows=None, header=None):
        ''' Export to a JSON-friendly representation '''
        output = self.data.jsonify(cols=self.colnames.values(), rows=rows, header=header)
        return output