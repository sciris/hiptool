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
 
Last update: 5/26/18 (gchadder3)
"""

# A secret key value used by Python Flask.
SECRET_KEY = 'Pick something unique for your site here'

# Directory containing the client code.
#   DEFAULT = '.'
CLIENT_DIR = '../../client2/dist'

# Directory containing the model code.  This is the primary Python code that 
# the web app will rely on related to the actual model.
# TODO: I'm not sure we will end up needing this parameter.  We should remove 
# it if it is redundant.
MODEL_DIR = '.'

# Directory containing Python code specific to the web app.  sessionmanager 
# (the directory this config file is in) contains general Python functionality 
# that the web app directory code makes use of. 
# TODO: I'm not sure we will end up needing this parameter.  We should remove 
# it if it is redundant.
WEBAPP_DIR = '.'

# Directory where uploaded files will be saved, as well as files saved to be 
# downloadable to user machines.
# If commented out or omitted, a temporary directory will be kept for this, 
# which will be erased when the application is halted.
#TRANSFER_DIR = 'transferfiles'

# Directory where files may be saved that the web app should be able to 
# access.
# If commented out or omitted, a persistent directory will be kept for this, 
# but it will be in a temporary directory location, so it may be subject to 
# accidental deletion on, for example, reboots.
FILESAVEROOT_DIR = 'savedfiles'

# Flag for setting whether we use the datastore functionality provided by 
# Sciris in the webapp.
USE_DATASTORE = True

# URL for the Redis database that the web app will use to manage 
# persistence.  Note that the /N/ number at the end should match the 
# database number you want to use.  (N=0 is the default Redis database.)
REDIS_URL = 'redis://localhost:6379/5/'

# Flag for setting whether we use the users functionality provided by 
# Sciris in the webapp.
USE_USERS = True

# Flag for setting whether registration of a new account automatically 
# spawns a new active account.  If this is set False, then an admin user has 
# to manually activate the account for the user.
REGISTER_AUTOACTIVATE = True