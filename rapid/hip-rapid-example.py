import pylab as pl
import sciris as sc
import hiptool as hp

doplot = False

P = hp.Project()
P.loadburden(filename='demo_BoD.xlsx')
P.loadinterventions(filename='CIV_interventions.xlsx')
P.intervsets[0].data['Spending'] *= 0 # Set current spending to 0
ninterventions = P.intervsets[0].data.nrows
P.makepackage()

spendings = [0.1, 0.5, 1, 5, 10, 50, 100, 500, 1000, 5000]
nspendings = len(spendings)

colors = sc.vectocolor(len(spendings))

results = []

for spend in spendings:
    P.package().optimize(budget=spend*1e6)
    df = P.package().data
    results.append(sc.dcp(df['opt_spend'][:]))

results = pl.array(results)

# Ploting
if doplot:
    fig0 = P.burden().plot()
    fig2 = P.package().plot_spending(which='optimized')
    fig4 = P.package().plot_dalys(which='optimized')
    fig5 = P.package().plot_cascade()
    
# New plotting
allplatforms = df['platform'].tolist()
platforms = ['Population-based Health Interventions', 
             'Community', 
             'Health Center',
             'First-level Hospital',
             'Referral and Specialty Hospital',]

nplatforms = len(platforms)



fig = pl.figure(figsize=(16,8))
ax = fig.add_axes([0.2,0.1,0.7,0.8])

for s,spend in enumerate(spendings):
    pl.scatter(-2, 0, c=colors[s], s=200, label=f'${spend:0.2f} per person')

platdata = pl.zeros(ninterventions)#+pl.nan
#for s in range(nspendings):
#    thiscolor = colors[s]
#    theseresults = results[s,:]
for r in range(ninterventions):
    inds = sc.findinds(results[:,r])
    if len(inds):
        platdata[r] = inds[0]

platdict = sc.odict().make(keys=platforms, vals=[])
for r,plat in enumerate(allplatforms):
    platdict[plat].append(platdata[r])
    
for plat in platforms:
    platdict[plat] = sorted(platdict[plat])
    
for y,plat in enumerate(platforms):
    for x,val in enumerate(platdict[plat]):
        pl.scatter(x, y, c=colors[int(val)], s=200)
        
pl.xlim([-1,55])
pl.xlabel('Number of funded interventions')
pl.title('For different per capita spending levels, which platforms should be funded?', fontweight='bold')
pl.legend()

pl.gca().set_yticks(pl.arange(nplatforms))
pl.gca().set_yticklabels(platforms)

pl.show()


    


print('Done')