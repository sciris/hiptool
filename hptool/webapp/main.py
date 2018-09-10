"""
main.py -- main module for HealthPrior webapp.
    
Last update: 2018sep10
"""

import hptool as hp
import scirisweb as sw

def make_app():
    app = sw.ScirisApp(__file__, name='HealthPrior', config=hp.webapp.config) 	# Create the ScirisApp object.  NOTE: app.config will thereafter contain all of the configuration parameters, including for Flask.
    app.add_RPC_dict(hp.webapp.rpcs.RPC_dict) # Register the RPCs in the project.py module.
    hp.webapp.projects.init_projects(app) # Initialize the projects.
    return app

def run():
    app = make_app() # Make the app
    app.run() # Run the client page with Flask and a Twisted server.
    return None

if __name__ == '__main__':
    run()
