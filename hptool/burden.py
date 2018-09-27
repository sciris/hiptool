"""
Version:
"""

import sciris as sc
import pylab as pl

class Burden(object):
    ''' Class to hold all burden data, e.g. from IHME GBD. Data stored are/will be:
    1.	Primary cause name
    2.	Total DALYs by year
    3.	Total mortality by year
    4.	Population prevalence by year
    
    From http://ghdx.healthdata.org/gbd-results-tool
    
    Version: 2018sep27
    '''
    
    def __init__(self, name=None, project=None, filename=None, folder=None):
        if name is None: name = 'Default'
        self.projectref = sc.Link(project) # Store pointer for the project
        self.name       = sc.uniquename(name, namelist=self.projectref().burdensets.keys()) # Name of the parameter set, e.g. 'default'
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
        output += 'Burden set name: %s\n'    % self.name
        output += '   Date created: %s\n'    % sc.getdate(self.created)
        output += '  Date modified: %s\n'    % sc.getdate(self.modified)
        output += '            UID: %s\n'    % self.uid
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
        
    
    def plot(self, which=None, n=None, axsize=None, figsize=None):
        '''
        Create a bar plot of the top causes of burden. By default, plots the top
        10 causes of DALYs.
        
        Version: 2018sep27
        '''
        
        # Define hard-coded column names
        colnames = sc.odict([('index',      'Index'),
                             ('cause',      'Cause of disease burden'),
                             ('dalys',      'DALYs'),
                             ('deaths',     'Deaths'),
                             ('prevalence', 'Prevalence')
                              ])

        # Set labels
        titles = {'dalys':     'Top causes of DALYs',
                  'deaths':    'Top causes of mortality',
                  'prevalence':'Most prevalent conditions'}
        
        # Handle options
        if which   is None: which   = titles.keys()
        if n       is None: n       = 10
        if axsize  is None: axsize  = (0.65, 0.15, 0.3, 0.8)
        if figsize is None: figsize = (10,5)
        barw     = 0.8
        
        # Pull out data
        burdendata = sc.dcp(self.data)
        nburdens = burdendata.nrows()
        colors = sc.gridcolors(nburdens, asarray=True)
        
        # Convert to list
        if not isinstance(which, list):
            asarray = False
            whichlist = sc.promotetolist(which)
        else:
            asarray = True
            whichlist = which
        
        # Loop over each option (may only be one)
        figs = []
        for which in whichlist:
            try:
                thistitle  = titles[which]
                thisxlabel = colnames[which]
            except Exception as E:
                errormsg = '"%s" not found, "which" must be one of %s (%s)' % (which, ', '.join(titles.keys()), str(E))
                raise Exception(errormsg)
            
            # Process data
            burdendata.sort(col=colnames[which], reverse=True)
            topdata   = burdendata[:n]
            barlabels = topdata[colnames['cause']].tolist()
            barvals   = topdata[colnames[which]]
            barinds   = topdata[colnames['index']]
            
            # Figure out the units
            largestval = barvals[0]
            if largestval>1e6:
                barvals /= 1e6
                unitstr = ' (millions)'
            elif largestval>1e3:
                barvals /= 1e3
                unitstr = ' (thousands)'
            else:
                unitstr = ''
            
            # Create plot
            fig = pl.figure(facecolor='none', figsize=figsize)
            ax = fig.add_axes(axsize)
            ax.set_facecolor('none')
            yaxis = pl.arange(n, 0, -1)
            for i in range(n):
                pl.barh(yaxis[i], barvals[i], height=barw, facecolor=colors[barinds[i]-1], edgecolor='none')
            ax.set_yticks(pl.arange(10, 0, -1))    
            ax.set_yticklabels(barlabels)
            sc.SIticks(ax=ax,axis='x')
            ax.set_xlabel(thisxlabel+unitstr)
            ax.set_title(thistitle)
            sc.boxoff()
            figs.append(fig)
        
        if asarray: return figs
        else:       return figs[0]