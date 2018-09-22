"""
main.py -- main module for HealthPrior webapp.
    
Last update: 2018sep10
"""

import hptool as hp
import scirisweb as sw

def make_app():
    app = sw.ScirisApp(name='HealthPrior', filepath=__file__, config=hp.webapp.config, RPC_dict=hp.webapp.rpcs.RPC_dict) # Create the ScirisApp object.  NOTE: app.config will thereafter contain all of the configuration parameters, including for Flask.
    sw.make_default_users(app)
    return app

def run():
    app = make_app() # Make the app
    app.run() # Run the client page with Flask and a Twisted server.
    return None

if __name__ == '__main__':
    run()
