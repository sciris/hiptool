"""
Version:
"""

import hiptool as hp
P = hp.demo()
#Q = hp.demo(country='Kiribati')
P.burden().plottopcauses(which='prevalence', n=15)