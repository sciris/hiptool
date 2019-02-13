#!/usr/bin/env python

'''
Small script to reset the user database -- WARNING, deletes everything!!!

Version: 2018sep22
'''

import scirisweb as sw
import hiptool as hp
import os

webapp_dir = os.path.abspath(hp.webapp.config.CLIENT_DIR)
redis_url = hp.webapp.config.REDIS_URL
datastore = sw.DataStore(redis_url=redis_url)
prompt = 'Are you sure you want to reset the database for the following?\n  %s\n  %s\nAnswer (y/[n]): ' % (webapp_dir, redis_url)
answer = raw_input(prompt)
if answer == 'y':
	datastore.flushdb()
else:
	print('Database not reset.')