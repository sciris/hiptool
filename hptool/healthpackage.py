"""
Version:
"""

import numpy as np
import pylab as pl
import hptool as hp
import sciris as sc

def arr(data):
    ''' Force float, or give helpful error '''
    try:
        output = np.array(data, dtype=float)
    except Exception as E:
        errormsg = 'Data contain non-numeric values (%s):\n%s' % (str(E), data)
        raise Exception(errormsg)
    return output

class HealthPackage(object):
    ''' Class to hold the results from the analysis. '''
    
    def __init__(self, project=None, name=None, burdenset=None, intervset=None, makepackage=None):
        self.name       = name # Name of the parameter set, e.g. 'default'
        self.uid        = sc.uuid() # ID
        self.projectref = sc.Link(project) # Store pointer for the project, if available
        self.created    = sc.now() # Date created
        self.modified   = sc.now() # Date modified
        self.eps        = 1e-4 # A nonzero value to help with division
        self.burdenset  = burdenset
        self.intervset  = intervset
        self.budget     = None
        self.frpwt      = None
        self.equitywt   = None
        self.data       = None # The data
        
        # Define hard-coded column names
        self.colnames = sc.odict([('active',   'Active'),
                                  ('shortname','Short name'),
                                  ('bod1',     'BoD (1)'),
                                  ('bod1wt',   'Fraction (1)'),
                                  ('icer',     'ICER'),
                                  ('unitcost', 'Unit cost'),
                                  ('spend',    'Spending'),
                                  ('frp',      'FRP'),
                                  ('equity',   'Equity'),])
        
        if makepackage: self.makepackage()
        return None
    
    def __repr__(self):
        ''' Print out useful information when called'''
        output  = sc.prepr(self)
        output += 'Health packages name: %s\n'    % self.name
        output += '        Date created: %s\n'    % sc.getdate(self.created)
        output += '       Date modified: %s\n'    % sc.getdate(self.modified)
        output += '                 UID: %s\n'    % self.uid
        output += '============================================================\n'
        return output
    
    def makepackage(self, burdenset=None, intervset=None, frpwt=None, equitywt=None, verbose=True):
        ''' Make results '''
        # Handle inputs
        if burdenset is not None: self.burdenset = burdenset # Warning, name is used both as key and actual set!
        if intervset is not None: self.intervset = intervset
        if frpwt     is None: frpwt = 0.25
        if equitywt  is None: equitywt = 0.25
        self.frpwt    = frpwt
        self.equitywt = equitywt
        burdenset = self.projectref().burden(key=self.burdenset)
        intervset = self.projectref().interv(key=self.intervset)
        
        # Data cleaning: remove if missing: cause, icer, unitcost, spending
        origdata = sc.dcp(intervset.data)
        print(origdata.cols)
        critical_cols = ['active', 'bod1', 'bod1wt', 'unitcost', 'spend', 'icer']
        for col in critical_cols:
            origdata.filter_out(key='', col=self.colnames[col], verbose=True)
        origdata.replace(col=self.colnames['spend'], old='', new=0.0)
        nrows = origdata.nrows()
        
        # Create new dataframe
        df = sc.dataframe(cols=[self.colnames['active']], data=np.ones(nrows))
        for col in ['shortname']+critical_cols: # Copy columns over
            colname = self.colnames[col]
            df[col] = origdata[colname]
        
        # Calculate people covered (spending/unitcost)
        df['coverage'] = arr(df['spend'])/(self.eps+arr(df['unitcost']))
        
        # Pull out DALYS and prevalence
        df.addcol('total_dalys')
        df.addcol('max_dalys')
        df.addcol('total_prevalence')
        for r in range(df.nrows()):
            key = df.get(rows=r, cols='bod1')
            try:
                tmp_burden = burdenset.data.findrow(key=key, col=burdenset.colnames['cause'], asdict=True)
            except:
                raise hp.HPException('Burden "%s" not found' % key)
            try:    df['total_dalys',r] = tmp_burden[burdenset.colnames['dalys']]
            except: df['total_dalys',r] = 0 # Warning, will want to fix
            try:    df['total_prevalence',r] = tmp_burden[burdenset.colnames['prevalence']]
            except: df['total_prevalence',r] = 0
            
        # Calculate maximum coverage
        df['max_dalys'] = arr(df['total_dalys']) * arr(df['bod1wt'])
        
        # Current DALYs averted (spend/icer)
        df['dalys_averted'] = arr(df['spend'])/(self.eps+arr(df['icer']))
        
        # Current % of DALYs averted (dalys_averted/total_dalys)
        df['frac_averted'] = arr(df['dalys_averted'])/(self.eps+arr(df['max_dalys'])) # To list large fractions: df['shortname'][ut.findinds(df['frac_averted']>0.2)]

        # To populate with optimization results
        self.budget = arr(df['spend']).sum()
        df.addcol('opt_spend')
        df.addcol('opt_dalys_averted')
        
        self.data = df # Store it
        if verbose:
            print('Health package %s recalculated from burdenset=%s and intervset=%s' % (self.name, self.burdenset, self.intervset))
        return None
    
    def loaddata(self, filename=None, folder=None):
        ''' Load data from a spreadsheet -- WARNING, do we need this? '''
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
    
    def optimize(self, budget=None, frpwt=None, equitywt=None):
        # Handle inputs
        if budget   is None: budget = self.budget
        if frpwt    is None: frpwt     = self.frpwt
        if equitywt is None: equitywt  = self.equitywt
        self.budget   = budget
        self.frpwt    = frpwt
        self.equitywt = equitywt
        df = self.data
        
        # Do the processing
        df.sort(col='icer')
        remaining = sc.dcp(self.budget)
        max_dalys = arr(df['max_dalys'])
        icers     = arr(df['icer'])
        for r in range(df.nrows()):
            max_spend = max_dalys[r]*icers[r]
            if remaining >= max_spend:
                remaining -= max_spend
                df['opt_spend',r] = max_spend
                df['opt_dalys_averted',r] = max_dalys[r]
            else:
                break
        
        return None
        
    def plot_dalys(self):
        df = self.data
        fig = pl.figure(figsize=(10,6))
        max_entries = 11
        colors = sc.gridcolors(ncolors=max_entries+2)[2:]
        df.sort(col='dalys_averted', reverse=True)
        DA_data = arr(df['dalys_averted'])
        plot_data = list(DA_data[:max_entries-1])
        plot_data.append(sum(DA_data[max_entries:]))
        plot_data = np.array(plot_data)/1e3
        plot_data = plot_data.round()
        total_averted = (plot_data.sum()/1e3)
        data_labels = ['%i'%datum for datum in plot_data]
        DA_labels = df['shortname']
        plot_labels = list(DA_labels[:max_entries-1])
        plot_labels.append('Other')
        pl.axes([0.15,0.1,0.45,0.8])
        pl.pie(plot_data, labels=data_labels, colors=colors, startangle=90, counterclock=False, radius=0.5, labeldistance=1.03)
        pl.gca().axis('equal')
        pl.title("Current DALYs averted by health intervention\n('000s; total: %0.2f million)" % total_averted)
        pl.legend(plot_labels, bbox_to_anchor=(1,0.8))
        pl.gca().set_facecolor('none')
        return fig
    
    def plot_spending(self):
        df = self.data
        fig = pl.figure(figsize=(10,6))
        max_entries = 11
        colors = sc.gridcolors(ncolors=max_entries+2)[2:]
        df.sort(col='spend', reverse=True)
        DA_data = arr(df['spend'])
        plot_data = list(DA_data[:max_entries-1])
        plot_data.append(sum(DA_data[max_entries:]))
        plot_data = np.array(plot_data)/1e6
#        plot_data = plot_data.round()
        total_averted = (plot_data.sum())
        data_labels = ['$%0.3fm'%datum for datum in plot_data]
        DA_labels = df['shortname']
        plot_labels = list(DA_labels[:max_entries-1])
        plot_labels.append('Other')
        pl.axes([0.15,0.1,0.45,0.8])
        pl.pie(plot_data, labels=data_labels, colors=colors, startangle=90, counterclock=False, radius=0.5, labeldistance=1.03)
        pl.gca().axis('equal')
        pl.title("Current spending by health intervention\n(total: $%0.3f million)" % total_averted)
        pl.legend(plot_labels, bbox_to_anchor=(1,0.8))
        pl.gca().set_facecolor('none')
        return fig

    def plot_cascade(self, vertical=True):
        if vertical:
            fig_size = (12,12)
            ax_size = [0.45,0.05,0.5,0.9]
        else:
            fig_size = (16,8)
            ax_size = [0.05,0.45,0.9,0.5]
        df = self.data
        cutoff = 200e3
        fig = pl.figure(figsize=fig_size)
        df.sort(col='icer', reverse=False)
        DA_data = arr(df['spend'])
        inds = sc.findinds(DA_data>cutoff)
        DA_data = DA_data[inds]
        DA_data /= 1e6
        DA_labels = df['shortname'][inds]
        npts = len(DA_data)
        colors = sc.gridcolors(npts, limits=(0.25,0.75))
        x = np.arange(len(DA_data))
        pl.axes(ax_size)
        for pt in range(npts):
            loc = x[pt:]
            this = DA_data[pt]
            start = sum(DA_data[:pt])
            prop = 0.9
            color  = colors[pt]
            amount = sum(DA_data[:pt+1])
            amountstr = '%0.1f' % amount
            if vertical: 
                pl.barh(loc, width=this,  left=start,   height=prop, color=color)
                pl.text(amount, x[pt], amountstr, verticalalignment='center', color=colors[pt])
            else:        
                pl.bar(loc,  height=this, bottom=start, width=prop,  color=color)
                pl.text(x[pt], amount+1, amountstr, horizontalalignment='center', color=colors[pt])
        if vertical:
            pl.xlabel('Spending (US$ millions)')
            pl.gca().set_yticks(x)
            ticklabels = pl.gca().set_yticklabels(DA_labels)
        else:
            pl.ylabel('Spending (US$ millions)')            
            pl.gca().set_xticks(x)
            ticklabels = pl.gca().set_xticklabels(DA_labels, rotation=90)
        for t,tl in enumerate(ticklabels):
            tl.set_color(colors[t])
        
        pl.gca().set_facecolor('none')
        pl.title('Investment cascade')
        return fig