import pylab as pl
import sciris as sc
import hiptool as hp

doplot = False

P = hp.Project()
P.loadburden(filename='demo_BoD.xlsx')
P.loadinterventions(filename='CIV_interventions.xlsx')
P.intervsets[0].data['Spending'] *= 0 # Set current spending to 0
P.makepackage()

spendings = [0.1, 0.5, 1, 5, 10, 50, 100, 500, 1000, 5000, 10000]
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

fig = pl.figure()


platcounts = sc.odict().make(keys=platforms, vals=0)
platnot = sc.dcp(platcounts)
for s in range(nspendings):
    thiscolor = colors[s]
    theseresults = results[s,:]
    for r in range(len(theseresults)):
        platind = platforms.index(allplatforms[r])
        print(platforms[platind], platind, platcounts[platind], platnot[platind])
        if theseresults[r]:
            platcounts[platind] += 1
            pl.scatter(platcounts[platind], platind, c=thiscolor, s=200)
        elif s==nspendings-1:
            platnot[platind] += 1

for platind in range(nplatforms):
    x = pl.arange(platcounts[platind], platcounts[platind]+platnot[platind]+1)
    pl.scatter(x, [platind]*len(x), facecolor='none', edgecolor='k', s=200)


pl.gca().set_yticks(pl.arange(nplatforms))
pl.gca().set_yticklabels(platforms)


    


print('Done')