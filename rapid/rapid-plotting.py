import pylab as pl
import sciris as sc

dosave = True
fig1 = False
fig2 = True

sc.heading('Loading data...')
country_data = sc.loadspreadsheet('country-data.xlsx')
interv_data = sc.loadspreadsheet('rapid_interventions.xlsx')
D = sc.loadobj('results/rapid_data.obj')
R = sc.loadobj('results/rapid_results.obj')


#%% Fig. 1 -- DALYs
if fig1:
    sc.heading('DALYs figure')
    interv_category = interv_data['Category 1'].tolist()
    categories = sorted(set(interv_category))
    ncategories = len(categories)
    nspends, nintervs = R[0]['dalys'].shape
    mapping = []
    for i_c in interv_category:
        for c,cat in enumerate(categories):
            if i_c == cat:
                mapping.append(c)
    
    dalydata = pl.zeros((nspends, ncategories))
    for country in R.keys():
        dalys = R[country]['dalys']
        for i in range(nintervs):
            c = mapping[i]
            dalydata[:,c] += dalys[:,i]
    
    fig = pl.figure()
    x = pl.arange(nspends)
    axlist = []
    previous = pl.zeros(nspends)
    for c in range(len(categories)):
        current = dalydata[:,c]/1e9
        ax = pl.bar(x, current, bottom=previous)
        previous += current
        axlist.append(ax)
    
    xticks = ['$%s' % val for val in [0.1, 0.3, 1, 3, 10, 30, 100, 300, '1k', '3k', '10k']]
    pl.ylabel('DALYs averted (billions)')
    pl.title('Global DALYs averted annually by funding level and disease area')
    pl.xticks(x, xticks)
    pl.xlabel('Additional EUHC expenditure per person per year globally')
    pl.legend([ax[0] for ax in axlist], categories)
    
    pl.show()
    
    if dosave:
        pl.savefig('results/rapid_dalys-averted.png', dpi=200)


#%% Fig. 2 -- interventions
if fig2:
    sc.heading('Top interventions figure')
    df = sc.dataframe(cols=['Short name', 'Category 1', 'Category 2', 'Percent'], nrows=len(interv_data))
    for key in ['Short name', 'Category 1', 'Category 2']:
        df[key] = interv_data[key]
    df['Percent'] = 0.0
    
    nspends, nintervs = R[0]['dalys'].shape
    for country in R.keys():
        alloc = R[country]['alloc']
        counts = pl.array((alloc>0).sum(axis=0), dtype=float)
        df['Percent'] += counts/nspends/len(R)
        
    if dosave:
        df.export('results/rapid_top-interventions.xlsx')
        
    data = {'Communicable': [
                ['ART care for PLHIV','Communicable','HIV/AIDS','100.00%'],
                ['Treatment eligibility for hepatitis B and C','Communicable','Other','80.93%'],
                ['Surgery for filarial hydrocele','Communicable','NTDs','74.87%'],
                ['Severe malaria management','Communicable','Malaria', '74.45%'],
                ['Medical male circumcision','Communicable','HIV/AIDS','73.93%'],
                ['IPT for malaria in pregnancy','Communicable','Malaria','72.57%'],
                ['Testing and counseling for HIV, STIs, hepatitis','Communicable','HIV/AIDS','72.57%'],
                ['Provision of insecticide nets','Communicable','Malaria','68.70%'],
                ['Test for G6PD deficiency','Communicable','Malaria','68.70%'],
                ['Primaquine first-line malaria treatment','Communicable','Malaria','65.52%']
                ],
            
            'NCDs': [
                ['Urgent surgery for orthopedic injuries','NCDs','Injuries','96.55%'],
                ['Tube thoracostomy','NCDs','Injuries','86.68%'],
                ['Trauma-related amputations','NCDs','Injuries','85.79%'],
                ['Trauma laparotomy','NCDs','Surgery','84.80%'],
                ['Burr hole','NCDs','Cardiovascular','82.39%'],
                ['Therapy for moderate to severe arthritis','NCDs','Other','76.44%'],
                ['Suturing laceration','NCDs','Injuries','74.97%'],
                ['Non-displaced fractures management','NCDs','Injuries','74.35%'],
                ['Elective surgery for orthopedic injuries','NCDs','Injuries','73.93%'],
                ['Acute management of swallowing dysfunction','NCDs','Other','72.94%'],
                ],
            
            'RMNCH+N': [
                ['Parent training for high-risk families','RMNCH+N Child health','83.33%'],
                ['Repair of obstetric fistula','RMNCH+N','Maternal health','74.76%'],
                ['Miscarriage and abortions management','RMNCH+N Maternal health','74.09%'],
                ['Antenatal and postpartum education','RMNCH+N Child health','73.09%'],
                ['WASH behavior change interventions','RMNCH+N Nutrition','68.81%'],
                ['Provision of condoms','RMNCH+N Family planning','65.52%'],
                ['Induction of labor post-term','RMNCH+N Maternal health','64.73%'],
                ['Acute severe malnutrition management','RMNCH+N Nutrition','64.05%'],
                ['Jaundice management with phototherapy','RMNCH+N Child health','63.32%'],
                ['Care for fetal growth restriction','RMNCH+N Nutrition','63.17%'],
                ],
            
            'Vaccination': [
                ['Flu and pneumococcal vaccinations','Vaccination Other vaccines','61.08%'],
                ['Childhood vaccination series','Vaccination Child vaccines','60.24%'],
                ['Rotavirus vaccination','Vaccination Child vaccines','60.24%'],
                ['Use of vaccines for endemic infections','Vaccination Other vaccines','48.17%'],
                ['Pneumococcus vaccination','Vaccination Other vaccines','46.19%'],
                ['School based HPV vaccination for girls','Vaccination Other vaccines','43.99%'],
                ['Tetanus toxoid immunization','Vaccination Child vaccines','22.00%'],
                ]
            }

    fig = pl.figure(figsize=(9,17))
    ax = fig.add_axes([0.5,0.1,0.45,0.85])
    count = 50
    ticklocs = []
    ticklabels = []
    darkest = [pl.array([0.5, 0.1, 0.0]),
               pl.array([0.0, 0.1, 0.5]),
               pl.array([0.5, 0.0, 0.5]),
               pl.array([0.1, 0.5, 0.0]),
               ]
    for k,key,vals in sc.odict(data).enumitems():
        count -= 2
        count2 = 0
        pl.text(-35, count, key, fontweight='bold')
        for row in vals:
            count -= 1
            count2 += 1
            thiscolor = darkest[k] + (count2/20)*pl.array([1,1,1])
            ticklocs.append(count)
            ticklabels.append(row[0])
            pl.barh(count, float(row[-1].rstrip('%')), facecolor=thiscolor, edgecolor='none')
    
    ax.set_yticks(ticklocs)
    ax.set_yticklabels(ticklabels)
    pl.xlabel('Frequency of inclusion of intervention in EUHC package (%)')
    
    if dosave:
        pl.savefig('results/rapid_top-interventions.png', dpi=200)
        
    



print('Done.')