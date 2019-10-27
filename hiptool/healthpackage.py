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
        
        # Include burdens -- WARNING, contains everything, needs to be refactored
        bod = sc.objdict()
        bod.codes = hp.burdeninfo.dict.keys()
        bod.intervnames = df['shortname'][:].tolist()
        bod.nburdens = len(bod.codes)
        bod.nintervs = len(bod.intervnames)
        bod.codeinds = sc.odict()
        bod.nameinds = sc.odict()
        bod.original   = pl.zeros(bod.nburdens)
        bod.remaining  = pl.zeros(bod.nburdens)
        bod.prevalence = pl.zeros(bod.nburdens)
        for i in range(bod.nburdens):
            code = bod.codes[i]
            bod.codeinds[code] = i
            bod.nameinds[hp.burdeninfo.dict[code]] = i
            thisburden = burdenset.data.findrow(key=code, col=burdenset.colnames['code'], asdict=True, die=True)
            bod.prevalence[i] = thisburden[burdenset.colnames['prevalence']]
            bod.original[i]   = thisburden[burdenset.colnames['dalys']]
            bod.remaining[i]  = bod.original[i]
        bod.intervinds = sc.odict()
        for i in range(bod.nintervs):
            bod.intervinds[bod.intervnames[i]] = i
        bod.averted = pl.zeros((bod.nburdens, bod.nintervs))
        bod.max_dalys = sc.dcp(bod.averted)
        self.bod = bod
        
        # Calculate people covered (spending/unitcost)
        df['coverage'] = hp.arr(df['spend'])/(self.eps+hp.arr(df['unitcost']))
        
        # Pull out DALYS and prevalence
        df.addcol('max_prevalence',   value=0)
        df.addcol('total_dalys',        value=0) # Value=0 by default, but just to be explicit
        df.addcol('max_dalys',          value=0)
        df.addcol('dalys_averted',      value=0)
        notfound = []
        lasterror = None
        for r in range(df.nrows):
            theseburdencovs = df['parsedbc', r]
            for burdencov in theseburdencovs:
                key = burdencov[0]
                val = burdencov[1] # WARNING, add validation here
                codeind = bod.nameinds[key]
                dalys = bod.original[codeind]
                prevalence = bod.prevalence[codeind]
                df['max_prevalence',r] += prevalence
                df['total_dalys',r]    += dalys
                df['max_dalys',r]      += dalys * val
                bod.max_dalys[codeind,r] = dalys*val
        
        # Validation
        if len(notfound):
            errormsg = 'The following burden(s) were not found: "%s"\nError:\n%s' % (set(notfound), str(lasterror))
            raise hp.HPException(errormsg)
            
        # WARNING, the previous invalid checks didn't consider that disease burden already included the impact of interventions!
        for r in range(df.nrows):
            df['dalys_averted',r] = df['spend',r]/(self.eps+df['icer',r])
            
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
        remaining_budget = sc.dcp(self.budget)
        for r in range(df.nrows):
            if df['fixed',r]:
                remaining_budget -= df['spend',r]
                df['opt_spend',r]         = df['spend',r]
                df['opt_dalys_averted',r] = df['dalys_averted',r]
        
        # Do the "optimization"
        sortorder = df.sort(col='benefit', reverse=True) # Sort from most to least cost-effective
        reverseorder = pl.argsort(sortorder)
        averted = self.bod.averted
        max_coverage   = hp.arr(df['max_prevalence'])
        icers     = hp.arr(df['icer'])
        unitcosts = hp.arr(df['unitcost'])
        if verbose: print('Optimizing...')
        
        bod = self.bod # Make easier to get
        for r in range(df.nrows): # Loop over each intervention
            
            if remaining_budget > 0:
            
                # Calculate burden coverages
                theseburdencovs = df['parsedbc', r]
                
                # Calculate maximum coverage for this intervention based on unit cost and prevalence
                max_spend_coverage = min(remaining_budget, max_coverage[r] * unitcosts[r])
                
                # Calculate maximum DALYs
                this_max_dalys = 0
                for burdencov in theseburdencovs: # Loop over each listed burden
                    name = burdencov[0] # Name of burden, e.g. "Caries of deciduous teeth"
                    mec  = burdencov[1] # Maximum effective coverage, e.g. 0.2
                    burdenind = self.bod.nameinds[name]
                    remainingburden = bod.remaining[burdenind]
                    available = remainingburden*mec
                    this_max_dalys += available
                    averted[burdenind,reverseorder[r]] = available
                    
                max_spend_dalys  = this_max_dalys * icers[r]
                
                ratio = 1.0
                if max_spend_coverage > max_spend_dalys:
                    ratio = 1.0
                else:
                    ratio = max_spend_coverage/max_spend_dalys
                    averted[r,:] *= ratio
                
                max_spend = max_spend_dalys*ratio
                
                print(f'{r}: {remaining_budget:10.0f} {max_spend:10.0f} {max_spend_dalys:10.0f} {max_spend_coverage:10.0f}')
                
                df['opt_spend',r] = max_spend
                df['opt_dalys_averted',r] = averted[r,:].sum()
                remaining_budget -= max_spend
                
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
        
    
    def plot_dalys(self, which=None, max_entries=11):
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
        pl.axes([0.18,0.13,0.42,0.77])
        pl.pie(plot_data, labels=data_labels, colors=colors, startangle=90, counterclock=False, radius=0.95, labeldistance=1.03)
        pl.title("%s DALYs averted ('000s; total: %s)" % (titlekey, format(int(round(total_averted)), ',')))
        pl.legend(plot_labels, bbox_to_anchor=(1,0.8))
        pl.gca().set_facecolor('none')
        return fig
    
    
    def plot_spending(self, which=None, max_entries=11):
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
        df.sort(col=colkey, reverse=True)
        DA_data = hp.arr(df[colkey])
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
        pl.title("%s spending (total: %s)" % (titlekey, format(int(round(total_averted)), ',')))
        pl.legend(plot_labels, bbox_to_anchor=(1,0.8))
        pl.gca().set_facecolor('none')
        return fig


    def plot_cascade(self, vertical=True, cutoff=200e3):
        if vertical:
            fig_size = (12,12)
            ax_size = [0.45,0.05,0.5,0.9]
        else:
            fig_size = (16,8)
            ax_size = [0.05,0.45,0.9,0.5]
        df = sc.dcp(self.data)
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