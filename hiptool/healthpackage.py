"""
Version: 2019feb13
"""

import numpy as np
import pylab as pl
import hiptool as hp
import sciris as sc

class HealthPackage(object):
    ''' Class to hold the results from the analysis. '''
    
    def __init__(self, project=None, name=None, burdenset=None, intervset=None, makepackage=None, **kwargs):
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
        
        if makepackage: self.makepackage(**kwargs)
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
    
    
    def makepackage(self, burdenset=None, intervset=None, frpwt=None, equitywt=None, verbose=True, die=False):
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
        intervset.parse() # Ensure it's parsed
        colnames = intervset.colnames
        
        # Create new dataframe
        origdata = sc.dcp(intervset.data)
        critical_cols = ['active', 'shortname', 'platform', 'unitcost', 'spend', 'icer', 'frp', 'equity']
        df = sc.dataframe()
        for col in critical_cols: # Copy columns over
            df[col] = sc.dcp(origdata[colnames[col]])
        df['parsedbc'] = sc.dcp(origdata['parsedbc']) # Since not named
        df.filter_out(key=0, col='active', verbose=verbose)
        
        # Calculate people covered (spending/unitcost)
        df['coverage'] = hp.arr(df['spend'])/(self.eps+hp.arr(df['unitcost']))
        
        # Pull out DALYS and prevalence
        df.addcol('total_dalys',      value=0) # Value=0 by default, but just to be explicit
        df.addcol('max_dalys',        value=0)
        df.addcol('total_prevalence', value=0)
        df.addcol('dalys_averted',    value=0)
        notfound = []
        lasterror = None
        for r in range(df.nrows):
            theseburdencovs = df['parsedbc', r]
            for burdencov in theseburdencovs:
                key = burdencov[0]
                val = burdencov[1] # WARNING, add validation here
                try:
                    thisburden = burdenset.data.findrow(key=key, col=burdenset.colnames['cause'], asdict=True, die=True)
                    df['total_dalys',r]      += thisburden[burdenset.colnames['dalys']]
                    df['max_dalys',r]        += thisburden[burdenset.colnames['dalys']] * val
                    df['total_prevalence',r] += thisburden[burdenset.colnames['prevalence']]
                except Exception as E:
                    lasterror = E # Stupid Python 3
                    print('HIIII %s' % str(E))
                    print(type(df['total_dalys',r]))
                    print(type(df['max_dalys',r]))
                    print(type(df['total_prevalence',r]))
#                    print(type(thisburden[burdenset.colnames['dalys']]))
#                    print(type(thisburden[burdenset.colnames['prevalence']]))
                    notfound.append(key)
        
        # Validation
        if len(notfound):
            errormsg = 'The following burden(s) were not found: "%s"\nError:\n%s' % (set(notfound), str(lasterror))
            raise hp.HPException(errormsg)
        invalid = []
        for r in range(df.nrows):
            df['dalys_averted',r] = df['spend',r]/(self.eps+df['icer',r])
            if df['dalys_averted',r]>df['max_dalys',r]:
                errormsg = 'Data input error: DALYs averted for "%s" greater than total DALYs (%0.0f vs. %0.0f); please reduce total spending, increase ICER, increase DALYs, or increase max coverage' % (df['shortname',r], df['dalys_averted',r], df['max_dalys',r])
                df['dalys_averted',r] = df['max_dalys',r] # WARNING, reset to maximum rather than give error if die=False
                invalid.append(errormsg)
        if len(invalid):
            errors = '\n\n'.join(invalid)
            if die: raise Exception(errors)
            else:   print(errors)
            
        # To populate with optimization results and fixed spending
        self.budget = hp.arr(df['spend']).sum()
        df.addcol('opt_spend')
        df.addcol('opt_dalys_averted')
        df.addcol('fixed')
        
        # Store colors
        nintervs = df.nrows
        colors = sc.gridcolors(nintervs+2, asarray=True)[2:] # Skip black and white
        colordict = sc.odict()
        for c,name in enumerate(df['shortname']):
            colordict[name] = colors[c]
        self.colordict = colordict
        
        self.data = df # Store it
        if verbose:
            print('Health package %s recalculated from burdenset=%s and intervset=%s' % (self.name, self.burdenset, self.intervset))
        return None
    
    
    def savedata(self, filename=None, folder=None):
        ''' Export data from a spreadsheet '''
        cols = ['shortname','total_dalys','icer','spend','opt_spend','dalys_averted','opt_dalys_averted']
        filepath = self.data.export(filename=filename, cols=cols)
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
        frpdata = sc.dcp(hp.arr(df['frp']))
        frpdata += 1.0 - frpdata.min()
        frpdata /= frpdata.max()
        equitydata = sc.dcp(hp.arr(df['equity']))
        equitydata += 1 - equitydata.min()
        equitydata /= equitydata.max()
        equitydata = 1.0 - equitydata
        df['icerwt'] = (1-frpwt-equitywt) + frpdata*frpwt + equitydata*equitywt
        df['benefit'] = (1.0/(hp.arr(df['icer'])+self.eps)) * hp.arr(df['icerwt'])
        
        # Handle fixed budgets
        remaining = sc.dcp(self.budget)
        for r in range(df.nrows):
            if df['fixed',r]:
                remaining -= df['spend',r]
                df['opt_spend',r]         = df['spend',r]
                df['opt_dalys_averted',r] = df['dalys_averted',r]
        
        # Do the "optimization"
        df.sort(col='benefit', reverse=True)
        max_dalys = hp.arr(df['max_dalys'])
        icers     = hp.arr(df['icer'])
        if verbose: print('Optimizing...')
        for r in range(df.nrows):
            if not df['fixed',r]:
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
        df.sort(col='shortname')
        self.data = df
        if verbose:
            print('Optimization output:')
            print(self.data)
        return None
        
    def _getcolors(self, labels):
        colors = []
        for label in labels:
            if label in self.colordict: colors.append(self.colordict[label])
            else:                       colors.append(0.7+np.zeros(3)) # Set to gray for "Other"
        return colors
        
    def plot_dalys(self, which=None):
        if which is None: which = 'current'
        if which == 'current':
            colkey   = 'dalys_averted'
            titlekey = 'Current'
        elif which == 'optimized':
            colkey   = 'opt_dalys_averted'
            titlekey = 'Optimized'
        else:
            errormsg = '"which" not recognized: %s' % which
            raise Exception(errormsg)
        df = sc.dcp(self.data)
        fig = pl.figure(figsize=(10,6))
        df.sort(col=colkey, reverse=True)
        DA_data = hp.arr(df[colkey])
        max_entries = 11
        nremaining = len(DA_data)-max_entries
        plot_data = list(DA_data[:max_entries-1])
        plot_data.append(sum(DA_data[max_entries:]))
        plot_data = np.array(plot_data)/1e3
        total_averted = DA_data.sum()
        data_labels = ['%i'%datum for datum in plot_data]
        DA_labels = df['shortname']
        plot_labels = list(DA_labels[:max_entries-1])
        plot_labels.append('All other %s interventions' % nremaining)
        colors = self._getcolors(plot_labels)
#        pl.axes([0.15,0.1,0.45,0.8])
        pl.axes([0.18,0.13,0.42,0.77])
        pl.pie(plot_data, labels=data_labels, colors=colors, startangle=90, counterclock=False, radius=0.95, labeldistance=1.03)
#        pl.gca().axis('equal')
        pl.title("%s DALYs averted ('000s; total: %s)" % (titlekey, format(int(round(total_averted)), ',')))
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
        df = sc.dcp(self.data)
        fig = pl.figure(figsize=(10,6))
        print('WARNING, number of entries is hard-coded')
        df.sort(col=colkey, reverse=True)
        DA_data = hp.arr(df[colkey])
        max_entries = 11
        nremaining = len(DA_data)-max_entries
        plot_data = list(DA_data[:max_entries-1])
        plot_data.append(sum(DA_data[max_entries:]))
        plot_data = np.array(plot_data)/1e6
        total_averted = (DA_data.sum())
        data_labels = ['%0.1fm'%datum for datum in plot_data]
        DA_labels = df['shortname']
        plot_labels = list(DA_labels[:max_entries-1])
        plot_labels.append('All other %s interventions' % nremaining)
        colors = self._getcolors(plot_labels)
        pl.axes([0.18,0.13,0.42,0.77])
        pl.pie(plot_data, labels=data_labels, colors=colors, startangle=90, counterclock=False, radius=0.95, labeldistance=1.03)
#        pl.gca().axis('equal')
        pl.title("%s spending (total: %s)" % (titlekey, format(int(round(total_averted)), ',')))
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
        df = sc.dcp(self.data)
        cutoff = 200e3
        fig = pl.figure(figsize=fig_size)
        df.sort(col='icer', reverse=False)
        DA_data = hp.arr(df['opt_spend'])
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
            pl.xlabel('Spending for optimized investment cascade')
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