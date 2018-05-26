"""
main.py -- main module for HealthPrior webapp.
    
Last update: 5/26/18 (gchadder3)
"""

# Imports
from sciris2gc.scirisapp import ScirisApp
import config

# Create the ScirisApp object.  NOTE: app.config will thereafter contain all 
# of the configuration parameters, including for Flask.
app = ScirisApp(__file__, app_config=config)

# Run the client page with Flask and a Twisted server.
app.run_server()