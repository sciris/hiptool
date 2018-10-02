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
                                  ('burdencov','Causes of burden (max coverage)'),
                                  ('icer',     'ICER'),
                                  ('unitcost', 'Unit cost'),
                                  ('spend',    'Spending'),
                                  ('frp',      'FRP'),
                                  ('equity',   'Equity'),])
        
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
    
    def loaddata(self, filename=None, folder=None, verbose=True):
        ''' Load data from a spreadsheet '''
        self.data = sc.loadspreadsheet(filename=filename, folder=folder)
        self.filename = filename
        
        # Do validation
        if verbose: print('Validating data...')
        burdencov = self.data(col=self.colnames['burdencov'])
        for r in range(burdencov.nrows()):
            thisburdencov = burdencov[r]
            if verbose: print('Working on "%s"' % thisburdencov)
            try:
                burdencovsplit = thisburdencov.split(';') # Try to split into causes
            except Exception as E:
                errormsg = 'Could not split "%s" into separate burdens: %s' % (thisburdencov, str(E))
                raise Exception(errormsg)
            try:
                for b,bs in enumerate(burdencovsplit):
                    burdencovsplit[b] = bs.split(':') # Split into burden and coverage
                    if len(burdencovsplit[b]) != 2:
                        errormsg = 'Could not split "%s" into burden and coverage: %s' % (burdencovsplit[b], str(E))
                        raise Exception(errormsg)
                    else:
                        burdencovsplit[0] = burdencovsplit[0].lstrip().rstrip() # Strip leading and trailing spaces
                        try:
                            burdencovsplit[1] = float(burdencovsplit[1])
                        except Exception as E:
                            errormsg = 'Could not convert "%s" from "%s" to a number: %s' % (burdencovsplit[1], thisburdencov, str(E))
                            raise Exception(errormsg)
                        if burdencovsplit[1]<0 or burdencovsplit[1]>1:
                            errormsg = 'Maximum coverage must be between 0 and 1, not %s (from "%s")' % (burdencovsplit[1], thisburdencov)
                            raise Exception(errormsg)
            except Exception as E:
                errormsg = 'Could not split "%s" into burden and coverage: %s' % (thisburdencov, str(E))
                raise Exception(errormsg)
            
            self.data[self.colnames['burdencov'], r] = burdencovsplit # Save back to the data structure
        return None
    
    def savedata(self, filename=None, folder=None):
        ''' Export data from a spreadsheet '''
        filepath = self.data.export(filename=filename)
        return filepath
    
    def jsonify(self, cols=None, rows=None, header=None):
        ''' Export to a JSON-friendly representation '''
        output = self.data.jsonify(cols=cols, rows=rows, header=header)
        return output