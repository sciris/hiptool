"""
main.py -- main module for HealthPrior webapp.
    
Last update: 6/1/18 (gchadder3)
"""

# Imports
from sciris2gc.scirisapp import ScirisApp
import config
import sciris.core as sc
import hptool as hp
import project

# Create the ScirisApp object.  NOTE: app.config will thereafter contain all 
# of the configuration parameters, including for Flask.
app = ScirisApp(__file__, app_config=config)

#
# RPC definitions
#

@app.register_RPC()
def get_version_info():
	''' Return the information about the project. '''
	gitinfo = sc.gitinfo(__file__)
	version_info = {
        'version': hp.version,
        'date': hp.versiondate,
        'gitbranch': gitinfo['branch'],
        'githash': gitinfo['hash'],
        'gitdate': gitinfo['date'],
	}
	return version_info

# Register the RPCs in the project.py module.
app.add_RPC_dict(project.RPC_dict)

# Initialize the projects.
project.init_projects(app)

# Run the client page with Flask and a Twisted server.
app.run_server()