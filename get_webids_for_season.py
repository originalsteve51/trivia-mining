import sqlite3
from sqlite3 import Error

import sys

from dbaccess import DatabaseAccessor

database_name = 'jtrivia.db'

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
