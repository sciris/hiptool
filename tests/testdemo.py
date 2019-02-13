"""
Version:
"""

import hptool as hp
#P = hp.demo()
Q = hp.demo(country='Kiribati')
Q.burden().plottopcauses(which='prevalence', n=15)