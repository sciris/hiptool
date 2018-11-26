"""
config.py -- Configuration file for Sciris

This file gets imported by the Python code and contains settings for parameters
that choose which directories the web application uses, which Redis database
gets used, whether new registered accounts are automatically activated or not,
and other settings the Sciris webapp developer might want to include in the
configuration.

You can also set Flask config parameters in this file, as well as the Sciris-
and webapp-specific ones.

NOTE: For the _DIR parameters, you can use full absolute paths also (though you
need to make sure you use \\ for path separators under Windows OS).  If
you use a relative path, it is interpreted as being with respect to the
"webapp directory," that is, the directory containing this config file and the
main webapp script that imports it.

Last update: 2018sep22
"""

import os


# A secret key value used by Python Flask.
SECRET_KEY = 'adeardeerfacedacab'

# Directory containing the client code.
CLIENT_DIR = os.getenv('CLIENT_DIR')

# Flag for setting whether we use the datastore functionality provided by
# Sciris in the webapp.
USE_DATASTORE = True

# URL for the Redis database that the web app will use to manage
# persistence.  Note that the /N/ number at the end should match the
# database number you want to use.  (N=0 is the default Redis database.)
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/5')

# Flag for setting whether we use the users functionality provided by
# Sciris in the webapp.
USE_USERS = True

# Flag for setting whether registration of a new account automatically
# spawns a new active account.  If this is set False, then an admin user has
# to manually activate the account for the user.
REGISTER_AUTOACTIVATE = True

# Default server port
SERVER_PORT = int(os.getenv('PORT', 8091))

# Matplotlib backend
MATPLOTLIB_BACKEND = 'Agg'

# Slack logging configuration
SLACK = {'webhook':'https://hooks.slack.com/services/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'}
