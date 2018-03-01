# Load Sciris
from sciris.api import makeapp
import config

app = makeapp(config=config) # Create the app
app.run() # Run the server