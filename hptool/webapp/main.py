"""
main.py -- main module for HealthPrior webapp.
    
Last update: 2018sep25
"""

import sciris as sc
import scirisweb as sw
import hptool as hp

def make_app(**kwargs):
    T = sc.tic()
    print(hp.webapp.config.CLIENT_DIR)
    app = sw.ScirisApp(name='HealthPrior', filepath=__file__, config=hp.webapp.config, RPC_dict=hp.webapp.rpcs.RPC_dict) # Create the ScirisApp object.  NOTE: app.config will thereafter contain all of the configuration parameters, including for Flask.
    sw.make_default_users(app)
    print('>> Webapp initialization complete (elapsed time: %0.2f s)' % sc.toc(T, output=True))
    return app

def run(**kwargs):
    app = make_app(**kwargs) # Make the app
    app.run() # Run the client page with Flask and a Twisted server.
    return None

if __name__ == '__main__':
    run()
