####################################
# A season number is comprised of a large number of webrefs. Each webref is
# a show.
#
# After attempting to download a show, sometimes a failure occurs because the
# number of questions and answers do not match and are not 61, which is expected.
# This is because screen-scraping is inherently risky because the structure of 
# a show's webpage might not match what I expect. When a page is scraped an
# entry is added to a log file. If an error occurs, it is logged.
#
# Which brings us to the reason I have this utility program. Another program 
# (process_jscrape_log.py) analyzes the log and finds shows (webrefs) that had
# errors. If a show is error-free, a flag in the webrefs is set by this utility 
# that indicates it was successfully downloaded.
#
# This allows a later process that addresses the problems of screen-scraping to
# find webrefs to download that failed once before.
#
# Right now (30Jan2025) that better screen-scraper has not been written.  
####################################

import sqlite3
from sqlite3 import Error

import os
import sys

# For now, I want to use dbaccess.py in the parent directory.
# Fix up the path searched by Python for modules to include the absolute path
# to the parent directory...
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ''))
sys.path.insert(0, parent_dir)


from dbaccess import DatabaseAccessor

database_name = '../jtrivia.db'

db = DatabaseAccessor(database_name)

# A season number is passed in and we need to return an unprocessed webid
# from that season. Mark it processed after retrieving it.
season_number = sys.argv[1]

x = db.get_season_id(season_number)

x = db.get_webref(x)

if x:

	webref_id = x[0]
	webref = x[1]

	db.update_webref_downloaded(webref_id, True)

	print (f'{webref}')

	db.commit()
else:
	print(-1)
