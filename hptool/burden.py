"""
Version:
"""

from hptool import uuid, Link, today, defaultrepr, getdate, loadspreadsheet, dcp, HPException
from hptool import SIticks, boxoff
from pylab import figure, barh, arange

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
        barw     = 0.8
        barcolor = (0.7,0,0.3)
        axsize   = (0.55, 0.15, 0.4, 0.8)
        figsize  = (12,5)
        
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
        burdendata = dcp(self.data)
        burdendata.sort(col=which, reverse=True)
        topdata = burdendata[:n]
        
        # Create plot
        barlabels = topdata['cause'].tolist()
        barvals   = topdata[which].tolist()
        yaxis = arange(len(barvals), 0, -1)
        fig = figure(facecolor='w', figsize=figsize)
        ax = fig.add_axes(axsize)
        barh(yaxis, barvals, height=barw, facecolor=barcolor, edgecolor='none')
        ax.set_yticks(yaxis+barw/2.)
        ax.set_yticklabels(barlabels)
        SIticks(ax=ax,axis='x')
        ax.set_xlabel(thisxlabel)
        ax.set_title(thistitle)
        boxoff()
        return fig
        