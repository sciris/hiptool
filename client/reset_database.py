#!/usr/bin/env python

'''
Small script to reset the user database -- WARNING, deletes everything!!!

Version: 2018sep22
'''

import scirisweb as sw
import hiptool_app as ha
import os
import six

webapp_dir = os.path.abspath(ha.config.CLIENT_DIR)
redis_url = ha.config.REDIS_URL
datastore = sw.DataStore(redis_url=redis_url)
prompt = 'Are you sure you want to reset the database for the following?\n  %s\n  %s\nAnswer (y/[n]): ' % (webapp_dir, redis_url)
if six.PY2:
    answer = raw_input(prompt)
else:
    answer = input(prompt)
if answer == 'y':
	datastore.flushdb()
else:
	print('Database not reset.')