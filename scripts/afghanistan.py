# Create results for Afghanistan

#%% Setup

# Create project
import hiptool as hp
import sciris.core as sc
import pylab as pl
import numpy as np

# Set things
plot_dalys        = True
plot_cascade      = False
export            = False
name              = 'Afghanistan'
burdenfile        = hp.HPpath('data')+'ihme-gbd.xlsx'
interventionsfile = hp.HPpath('data')+'dcp-data-afg-v1.xlsx'

P = hp.Project(name=name, burdenfile=burdenfile, interventionsfile=interventionsfile)

#%% Calculations

# Data cleaning: remove if missing: cause, icer, unitcost, spending
df = hp.dcp(P.inter().data)
for col in ['icer', 'unitcost', 'cause']:
    df.filter_out(key='', col=col, verbose=True)
df.replace(col='spend', old='', new=0.0)

for col in [u'Intervention Number', u'fullname', u'frp', u'equity', u'Level 1 cause', u'Level 1 cause name', u'Level 2 cause ', u'Level 3 cause ', u'DCP3 Packages', u'Package Number', u'Urgency', u'Code', u'Codes for  interventions that appear in multiple packages', u'Volume(s) intervention included in', u'Platform in Volume', u'Platform in EUHC']:
    df.rmcol(col)

# Calculate people covered (spending/unitcost)
df['coverage'] = df['spend']/df['unitcost']

# Pull out DALYS and prevalence
df.addcol('total_dalys')
df.addcol('total_prevalence')
for r in range(df.nrows()):
    key = df.get(rows=r, cols='cause')
    tmp_burden = P.burden().data.findrow(key=key, col='cause', asdict=True)
    df['total_dalys',r] = tmp_burden['dalys']
    df['total_prevalence',r] = tmp_burden['prevalence']

# Calculate 80% coverage
print('Not calculating 80% coverage since denominators are wrong')

# Current DALYs averted (spend/icer)
df['dalys_averted'] = df['spend']/df['icer']

# Current % of DALYs averted (dalys_averted/total_dalys)
df['frac_averted'] = df['dalys_averted']/df['total_dalys'] # To list large fractions: df['shortname'][ut.findinds(df['frac_averted']>0.2)]

#%% Make plots

# Current DALYs averted
if plot_dalys:
    pl.figure(figsize=(10,6))
    max_entries = 11
    colors = sc.gridcolors(ncolors=max_entries+2)[2:]
    df.sort(col='dalys_averted', reverse=True)
    DA_data = df['dalys_averted']
    plot_data = list(DA_data[:max_entries-1])
    plot_data.append(sum(DA_data[max_entries:]))
    plot_data = np.array(plot_data)/1e3
    plot_data = plot_data.round()
    total_averted = (plot_data.sum()/1e3)
    data_labels = ['%i'%datum for datum in plot_data]
    DA_labels = df['shortname']
    plot_labels = list(DA_labels[:max_entries-1])
    plot_labels.append('Other')
    pl.axes([0.1,0.1,0.5,0.8])
    pl.pie(plot_data, labels=data_labels, colors=colors, startangle=90, counterclock=False, radius=0.5, labeldistance=1.03)
    pl.gca().axis('equal')
    pl.title("Current DALYs averted by health intervention\n('000s; total: %0.2f million)" % total_averted)
    pl.legend(plot_labels, bbox_to_anchor=(1,0.8))
    pl.savefig('hiptool_afghanistan_DALYS_averted_2018-05-14.png')


# Investment cascade
if plot_cascade:
    cutoff = 200e3
    pl.figure(figsize=(16,8))
    df.sort(col='icer', reverse=False)
    DA_data = df['spend']
    inds = sc.findinds(DA_data>cutoff)
    DA_data = DA_data[inds]
    DA_data /= 1e6
    DA_labels = df['shortname'][inds]
    npts = len(DA_data)
    colors = sc.gridcolors(npts, limits=(0.25,0.75))
    x = np.arange(len(DA_data))
    pl.axes([0.05,0.45,0.9,0.5])
    for pt in range(npts):
        pl.bar(x[pt:], height=DA_data[pt], bottom=sum(DA_data[:pt]), width=0.9, color=colors[pt])
        amount = sum(DA_data[:pt+1])+1
        amountstr = '%0.1f' % amount
        pl.text(x[pt], amount, amountstr, horizontalalignment='center', color=colors[pt])
    pl.gca().set_xticks(x)
    ticklabels = pl.gca().set_xticklabels(DA_labels, rotation=90)
    for t,tl in enumerate(ticklabels):
        tl.set_color(colors[t])
    pl.ylabel('Spending (US$ millions)')
    pl.title('Investment cascade for Afghanistan')
    pl.savefig('hiptool_afghanistan_investment_cascade_2018-05-14.png')

if export:
    df.export(filename='hiptool_afghanistan_data_2018-05-14.xlsx')

print('Done.')