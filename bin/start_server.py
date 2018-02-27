#!/usr/bin/env python

# Load Sciris
from sciris import _autoreload
from sciris import _twisted_wsgi

# Run the server
_autoreload.main(_twisted_wsgi.run)