"""
Version:
"""

import pylab as pl
import sciris as sc
import hptool as hp

class Burden(object):
    '''
    Class to hold all burden data, e.g. from IHME GBD. Data stored are/will be:
    1.	Primary cause name
    2.	Total DALYs by year
    3.	Total mortality by year
    4.	Population prevalence by year
    
    From http://ghdx.healthdata.org/gbd-results-tool
    
    Version: 2018oct02
    '''
    
    def __init__(self, name=None, project=None, filename=None, folder=None):
        if name is None: name = 'Default'
        self.projectref = sc.Link(project) # Store pointer for the project
        self.name       = sc.uniquename(name, namelist=self.projectref().burdensets.keys()) # Name of the parameter set, e.g. 'default'
        self.uid        = sc.uuid() # ID
        self.created    = sc.now() # Date created
        self.modified   = sc.now() # Date modified
        
        # Define hard-coded column names
        self.colnames = sc.odict([('active',     'Active'),
                                  #('code',       'Code'),
                                  ('cause',      'Cause'),
                                  ('dalys',      'DALYs'),
                                  ('deaths',     'Deaths'),
                                  ('prevalence', 'Prevalence')])
        
        # Load data, if provided
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
        self.data.filtercols(self.colnames.values(), die=True)
        self.filename = filename
        return None
    
    def savedata(self, filename=None, folder=None):
        ''' Export data from a spreadsheet '''
        filepath = self.data.export(filename=filename, cols=self.colnames.values())
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
        
        # Set labels
        titles = {'dalys':     'Top causes of DALYs',
                  'deaths':    'Top causes of mortality',
                  'prevalence':'Most prevalent conditions'}
        
        # Handle options
        if which   is None: which   = titles.keys()
        if n       is None: n       = 10
        if axsize  is None: axsize  = (0.65, 0.15, 0.3, 0.8)
        if figsize is None: figsize = (7,4)
        barw     = 0.8
        
        # Pull out data
        df = sc.dcp(self.data)
        nburdens = df.nrows
        colors = sc.gridcolors(nburdens+2, asarray=True)[2:]
        colordict = sc.odict()
        for c,cause in enumerate(df[self.colnames['cause']]):
            colordict[cause] = colors[c]
        
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
            colname = self.colnames[which]
            try:
                thistitle  = titles[which]
                thisxlabel = colname
            except Exception as E:
                errormsg = '"%s" not found, "which" must be one of %s (%s)' % (which, ', '.join(titles.keys()), str(E))
                raise Exception(errormsg)
            
            # Process data
            df.sort(col=colname, reverse=True)
            topdata   = df[:n]
            try:
                barvals   = hp.arr(topdata[colname])
            except Exception as E:
                for r in range(topdata.nrows):
                    try:
                        float(topdata[colname,r])
                    except Exception as E2:
                        if topdata[colname,r] in ['', None]:
                            errormsg = 'For cause "%s", the "%s" value is missing or empty' % (topdata[self.colnames['cause'],r], colname)
                        else:
                            errormsg = 'For cause "%s", could not convert "%s" value "%s" to number: %s' % (topdata[self.colnames['cause'],r], colname, topdata[colname,r], str(E2))
                        raise Exception(errormsg)
                errormsg = 'An exception was encountered, but could not be reproduced: %s' % str(E)
                raise Exception(errormsg)
            barlabels = topdata[self.colnames['cause']].tolist()
            
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
                thiscause = topdata[self.colnames['cause'],i]
                color = colordict[thiscause]
                pl.barh(yaxis[i], barvals[i], height=barw, facecolor=color, edgecolor='none')
            ax.set_yticks(pl.arange(10, 0, -1))    
            ax.set_yticklabels(barlabels)
            sc.SIticks(ax=ax,axis='x')
            ax.set_xlabel(thisxlabel+unitstr)
            ax.set_title(thistitle)
            sc.boxoff()
            figs.append(fig)
        
        if asarray: return figs
        else:       return figs[0]