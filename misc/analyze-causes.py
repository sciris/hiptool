#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 18:51:43 2019

@author: cliffk
"""

import hptool as hp
import sciris as sc

causedict = hp.causedict
codes = causedict.values()
sorco = sorted(codes)
bs = '\n'.join(sorco)
codict = sc.odict()
for co in sorco:
    codict[co] = bs.count(co)==1 and co!='T'