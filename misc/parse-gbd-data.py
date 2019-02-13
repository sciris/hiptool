#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To create the download file:
    
    1. Go to GBD Results Tool
    2. Select national countries, number only, DALYs/deaths/prevalence
    3. All else should be defaults
"""

import sciris as sc
import pandas as pd

reload = True
countriesandcauses = False
fn = '../archive_data/IHME-GBD_2017_DATA-169f61d2-1.csv'
outfile = '../archive_data/gbd-data.dat'
countriesfile = '../archive_data/gbd-countries.dat'
causesfile = '../archive_data/gbd-causes.dat'

if reload:
    print('Loading...')
    sc.tic()
    rawdata = pd.read_csv(fn)
    sc.toc()
    
    countrieslist = sc.loadobj(countriesfile)
    causeslist = sc.loadobj(causesfile)
    
    print('Parsing...')
    data = sc.odict()
    sc.tic()
    nrows = len(rawdata)
    for r in range(nrows):
        if not r%1000:
            print('%0.2f%%' % (r*100/float(nrows)))
        row = rawdata.iloc[r]
        country = row['location']
        measure = row['measure']
        cause = row['cause']
        val = row['val']
        if country not in data:
            data[country] = sc.odict()
        if measure not in data[country]:
            data[country][measure] = sc.odict()
        data[country][measure][cause] = val
    sc.toc()
    
    print('Processing...')
    addedcauses = []
    data.sort()
    for country in countrieslist:
        if country not in data:
            raise Exception('Country %s not found' % country)
    for country in data.values():
        country.sort()
        for measure in country.values():
            for cause in causeslist:
                if cause not in measure:
                    measure[cause] = 0.0
                    addedcauses.append(cause)
            measure.sort()
    if addedcauses:
        print('These causes were added: %s' % set(addedcauses))
    
    print('Saving...')
    sc.tic()
    sc.saveobj(outfile, data)
    sc.toc()

else:
    sc.tic()
    data = sc.loadobj(outfile)
    sc.toc()

if countriesandcauses:
    print('Saving countries and causes...')
    countrieslist = data.keys()
    causeslist = set(data[0][0].keys()+data[0][1].keys()+data[0][2].keys())
    sc.saveobj(countriesfile, countrieslist)
    sc.saveobj(causesfile, causeslist)


print('Done.')