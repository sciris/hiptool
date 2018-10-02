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
        colnames = intervset.colnames
        
        # Data cleaning: remove if missing: cause, icer, unitcost, spending
        origdata = sc.dcp(intervset.data)
        print(origdata.cols)
        critical_cols = ['active', 'burdencov', 'unitcost', 'spend', 'icer', 'frp', 'equity']
        for col in critical_cols:
            origdata.filter_out(key='', col=colnames[col], verbose=True)
        origdata.replace(col=colnames['spend'], old='', new=0.0)
        nrows = origdata.nrows()
        
        # Create new dataframe
        df = sc.dataframe(cols=[colnames['active']], data=np.ones(nrows))
        for col in ['shortname']+critical_cols: # Copy columns over
            colname = colnames[col]
            df[col] = origdata[colname]
        
        # Calculate people covered (spending/unitcost)
        df['coverage'] = arr(df['spend'])/(self.eps+arr(df['unitcost']))
        
        # Pull out DALYS and prevalence
        df.addcol('total_dalys',      value=0)
        df.addcol('max_dalys',        value=0)
        df.addcol('total_prevalence', value=0)
        df.addcol('dalys_averted',    value=0)
        notfound = []
        for r in range(df.nrows()):
            theseburdencovs = df['burdencov', r]
            for burdencov in theseburdencovs:
                key = burdencov[0]
                val = burdencov[1]
                try:
                    thisburden = burdenset.data.findrow(key=key, col=burdenset.colnames['cause'], asdict=True, die=True)
                    df['total_dalys',r]      += thisburden[burdenset.colnames['dalys']]
                    df['total_prevalence',r] += thisburden[burdenset.colnames['prevalence']]
                    df['max_dalys',r]        += df['total_dalys',r] * val
                    print('HIIIIIIIIII %s %s' % (key, thisburden[burdenset.colnames['dalys']]))
                except Exception as E:
                    notfound.append(key)
        
        # Validation
        if len(notfound):
            errormsg = 'The following burden(s) were not found: "%s"\nError:\n%s' % (notfound, str(E))
            raise hp.HPException(errormsg)
        for r in range(df.nrows()):
            df['dalys_averted',r] = df['spend',r]/(self.eps+df['icer',r])
            if df['dalys_averted',r]>df['total_dalys',r]:
                errormsg = 'Data input error: DALYs averted for "%s" greater than total DALYs (%s vs. %s); please reduce total spending, increase ICER, or increase DALYs' % (theseburdencovs, df['dalys_averted',r], df['total_dalys',r])
                raise Exception(errormsg)
            
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
    
    def optimize(self, budget=None, frpwt=None, equitywt=None, verbose=False):
        # Handle inputs
        if budget   is None: budget = self.budget
        if frpwt    is None: frpwt     = self.frpwt
        if equitywt is None: equitywt  = self.equitywt
        self.budget   = budget
        self.frpwt    = frpwt
        self.equitywt = equitywt
        df = sc.dcp(self.data)
        
        if verbose:
            print('Optimization inputs:')
            print('         Budget: %s' % self.budget)
            print('     FRP weight: %s' % self.frpwt)
            print('  Equity weight: %s' % self.equitywt)
        
        # Do the processing
        frpdata = sc.dcp(arr(df['frp']))
        frpdata += 1.0 - frpdata.min()
        frpdata /= frpdata.max()
        equitydata = sc.dcp(arr(df['equity']))
        equitydata += 1 - equitydata.min()
        equitydata /= equitydata.max()
        equitydata = 1.0 - equitydata
        df['icerwt'] = (1-frpwt-equitywt) + frpdata*frpwt + equitydata*equitywt
        df['benefit'] = (1.0/(arr(df['icer'])+self.eps)) * arr(df['icerwt'])
        df.sort(col='benefit', reverse=True)
        remaining = sc.dcp(self.budget)
        max_dalys = arr(df['max_dalys'])
        icers     = arr(df['icer'])
        if verbose: print('Optimizing...')
        for r in range(df.nrows()):
            max_spend = max_dalys[r]*icers[r]
            if verbose: print('  row %s | remaining %s | name %s | icer %s | icerwt %s | benefit %s | max_dalys %s | max_spend %s' % (r, remaining, df['shortname',r], df['icer',r], df['icerwt',r], df['benefit',r], max_dalys[r], max_spend))
            if remaining >= max_spend:
                remaining -= max_spend
                df['opt_spend',r] = max_spend
                df['opt_dalys_averted',r] = max_dalys[r]
            else:
                df['opt_spend',r] = remaining
                df['opt_dalys_averted',r] = max_dalys[r]*remaining/max_spend
                remaining = 0
#        df['dalys_averted'] = arr(df['dalys_averted']) * df['icerwt']
        df.sort(col='shortname')
        self.data = df
        if verbose:
            print('Optimization output:')
            print(self.data)
        return self.data
        
    def plot_dalys(self, which=None):
        if which is None: which = 'current'
        if which == 'current':
            colkey = 'dalys_averted'
            titlekey = 'Current'
        elif which == 'optimized':
            colkey = 'opt_dalys_averted'
            titlekey = 'Optimized'
        else:
            errormsg = '"which" not recognized: %s' % which
            raise Exception(errormsg)
        df = self.data
        fig = pl.figure(figsize=(10,6))
        max_entries = 11
        colors = sc.gridcolors(ncolors=max_entries+2)[2:]
        df.sort(col=colkey, reverse=True)
        DA_data = arr(df[colkey])
        plot_data = list(DA_data[:max_entries-1])
        plot_data.append(sum(DA_data[max_entries:]))
        plot_data = np.array(plot_data)/1e3
#        plot_data = plot_data.round()
        total_averted = (plot_data.sum()*1e3)
        data_labels = ['%i'%datum for datum in plot_data]
        DA_labels = df['shortname']
        plot_labels = list(DA_labels[:max_entries-1])
        plot_labels.append('Other')
        pl.axes([0.15,0.1,0.45,0.8])
        pl.pie(plot_data, labels=data_labels, colors=colors, startangle=90, counterclock=False, radius=0.5, labeldistance=1.03)
        pl.gca().axis('equal')
        pl.title("%s DALYs averted ('000s; total: %0.0f)" % (titlekey, total_averted))
        pl.legend(plot_labels, bbox_to_anchor=(1,0.8))
        pl.gca().set_facecolor('none')
        return fig
    
    def plot_spending(self, which=None):
        if which is None: which = 'current'
        if which == 'current':
            colkey = 'spend'
            titlekey = 'Current'
        elif which == 'optimized':
            colkey = 'opt_spend'
            titlekey = 'Optimized'
        else:
            errormsg = '"which" not recognized: %s' % which
            raise Exception(errormsg)
        df = self.data
        fig = pl.figure(figsize=(10,6))
        max_entries = 11
        colors = sc.gridcolors(ncolors=max_entries+2)[2:]
        df.sort(col=colkey, reverse=True)
        DA_data = arr(df[colkey])
        plot_data = list(DA_data[:max_entries-1])
        plot_data.append(sum(DA_data[max_entries:]))
        plot_data = np.array(plot_data)/1e6
#        plot_data = plot_data.round()
        total_averted = (plot_data.sum())
        data_labels = ['%0.1fm'%datum for datum in plot_data]
        DA_labels = df['shortname']
        plot_labels = list(DA_labels[:max_entries-1])
        plot_labels.append('Other')
        pl.axes([0.15,0.1,0.45,0.8])
        pl.pie(plot_data, labels=data_labels, colors=colors, startangle=90, counterclock=False, radius=0.5, labeldistance=1.03)
        pl.gca().axis('equal')
        pl.title("%s spending (total: %0.3f million)" % (titlekey, total_averted))
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
        DA_data = arr(df['opt_spend'])
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
            pl.xlabel('Optimized investment cascade')
            pl.gca().set_yticks(x)
            ticklabels = pl.gca().set_yticklabels(DA_labels)
        else:
            pl.ylabel('Optimized investment cascade')            
            pl.gca().set_xticks(x)
            ticklabels = pl.gca().set_xticklabels(DA_labels, rotation=90)
        for t,tl in enumerate(ticklabels):
            tl.set_color(colors[t])
        
        pl.gca().set_facecolor('none')
        pl.title('Investment cascade')
        return fig