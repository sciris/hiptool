"""
Version:
"""

import sciris.core as sc
import pylab as pl

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
        self.name       = name # Name of the parameter set, e.g. 'default'
        self.uid        = sc.uuid() # ID
        self.projectref = sc.Link(project) # Store pointer for the project, if available
        self.created    = sc.today() # Date created
        self.modified   = sc.today() # Date modified
        self.data       = None
        self.filename   = None
        self.popsize    = None
    
    def __repr__(self):
        ''' Print out useful information when called'''
        output  = sc.desc(self)
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
    
    
    def export(self, cols=None, rows=None, header=None):
        ''' Export to a JSON-friendly representation '''
        output = self.data.jsonify(cols=cols, rows=rows, header=header)
        return output
        
    
    def plottopcauses(self, which=None, n=None, axsize=None, figsize=None):
        '''
        Create a bar plot of the top causes of burden. By default, plots the top
        10 causes of DALYs.
        
        Version: 2018mar17        
        '''
        # Handle options
        if which   is None: which   = 'dalys'
        if n       is None: n       = 10
        if axsize  is None: axsize  = (0.45, 0.15, 0.5, 0.8)
        if figsize is None: figsize = (12,5)
        barw     = 0.8
        barcolor = (0.7,0,0.3)
        
        # Set labels
        titles = {'dalys':'Top ten causes of DALYs',
                  'deaths':'Top ten causes of mortality',
                  'prevalence':'Top ten most prevalent conditions'}
        xlabels = {'dalys':'DALYs',
                  'deaths':'Deaths',
                  'prevalence':'Prevalence'}
        try:
            thistitle = titles[which]
            thisxlabel = xlabels[which]
        except:
            errormsg = '"%s" not found, "which" must be one of: %s' % (which, ', '.join(titles.keys()))
            raise HPException(errormsg)
        
        # Pull out data
        burdendata = sc.dcp(self.data)
        burdendata.sort(col=which, reverse=True)
        topdata = burdendata[:n]
        barlabels = topdata['cause'].tolist()
        barvals   = topdata[which]
        
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
        yaxis = pl.arange(len(barvals), 0, -1)
        pl.barh(yaxis, barvals, height=barw, facecolor=barcolor, edgecolor='none')
        ax.set_yticks(arange(10, 0, -1))    
        ax.set_yticklabels(barlabels)
        
        sc.SIticks(ax=ax,axis='x')
        ax.set_xlabel(thisxlabel+unitstr)
        ax.set_title(thistitle)
        sc.boxoff()
        return fig