import pylab as pl
import sciris as sc
import hiptool as hp

sc.heading('Initializing...')

doplot = False
missing_data = ['remove', 'assumption'][1] # Choose how to handle missing data
spendings = [0.1, 0.5, 1, 5, 10, 50, 100, 500, 1000, 5000]
nspendings = len(spendings)
colors = sc.vectocolor(len(spendings))

# Load input files
D = sc.odict() # Data
R = sc.odict() # Results
bod_data = sc.loadobj('gbd-data.dat')
country_data = sc.loadspreadsheet('country-data.xlsx')
baseline_factor = country_data.findrow('Zambia', asdict=True)['icer_multiplier'] # Zambia was used for this

# Create default
P = hp.Project()
P.loadburden(filename='rapid_BoD.xlsx')
P.loadinterventions(filename='rapid_interventions.xlsx')
ninterventions = P.intervsets[0].data.nrows

# Load data
sc.heading('Loading data...')
for c,country in enumerate(country_data['name'].tolist()):
    print(f'  Working on {country}...')
    D[country] = sc.dcp(P)
    
    # Replace with actual burden data
    for k,key in enumerate(['DALYs', 'Deaths', 'Prevalence']):
        D[country].burden().data[key] = bod_data[country][k][:]
    
    # Adjust interventions
    for key in ['Unit cost', 'ICER']:
        this_factor = country_data['icer_multiplier'][c]
        
        df = D[country].interv().data
        missing_inds = sc.findinds(df[key]<0)
        if len(missing_inds):
            if missing_data == 'remove':
                df.rmrows(missing_inds)
            elif missing_data == 'assumption':
                for ind in missing_inds:
                    df['Unit cost', ind] = 1.0 # WARNING, completely arbitrary!
                    df['ICER', ind] = 66 
        
        D[country].interv().data[key] *= this_factor/baseline_factor

      
# Analysis
sc.heading('Analyzing...')
for c,country in enumerate(country_data['name'].tolist()):
    print(f'  Working on {country} ({c+1}/{len(country_data)})...')
    D[country].makepackage()
    
    meta = country_data.findrow(country, asdict=True)
    
    def optimize(P, spend, pop):
        print(f'hi! {spend} {pop}')
        P.package().optimize(budget=spend*pop)
        result = sc.dcp(P.package().data['opt_spend'][:])
        return result
    
    results = sc.parallelize(optimize, iterkwargs={'spend':spendings}, kwargs={'P':D[country], 'pop':meta['population']})
    
    R[country] = sc.odict({'meta':meta, 'results':pl.array(results)})


print('Done.')