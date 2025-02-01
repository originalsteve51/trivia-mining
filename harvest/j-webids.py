# --------------------
# j-webids.py
#
# Obtain a listing of the show web ids for a given season of Jeopardy
#
# Virtual environment created by following commands:
# conda create --name trivia python=3.12
# conda update -n base conda
# conda install -c anaconda beautifulsoup4
# conda install -c anaconda lxml
#
# Access the environment:
# conda activate trivia

# To use j-scrape.py to obtain questions and answers from a show it is necessary to know
# the show's web identification number. These numbers are mostly, but not all, sequentisl
# during a season. There is a listing of show web ids available for each season using
# a url of this form:
# https://j-archive.com/showseason.php?season=41
#
# This program accepts on the command line a season number (e.g. season 41 as seen above)
# to access the listing of show web ids for that season.
# 
# The sqllite database named jtrivia.db includes a table named webrefs where the results of 
# accessing https://j-archive.com/showseason.php?season=?? are stored for each season.
#
# Two tables are used:
# seasons season_id int, season_number int; 
# webrefs webref_id int, webref int, [fk from seasons cascade on delete] season_id int
#
# --------------------

import requests 
from bs4 import BeautifulSoup
import re

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

def extract_game_id(s):
    match = re.search(r'game_id=(\d+)$', s)
    if match:
        return int(match.group(1))
    return None

# ############################################        

if __name__ == '__main__':

	num_args = len(sys.argv)

	if num_args != 2:
		print('You must provide an season number when invoking this program...')
		sys.exit(0)
	else:
		season_number = int(sys.argv[1])
	
	
	db = DatabaseAccessor('../jtrivia.db')


	try:

		url = 'https://j-archive.com/showseason.php?season=' + str(season_number)

		response = requests.get(url)

		if response.status_code == 200:
			print('Obtained the season web page')
		else:
			print(f'Failed retrieval with code: {response.status_code}')

		seasonsoup = BeautifulSoup(response.content, "html.parser")

		season_id = db.create_season(str(season_number))
		
		for anchor in seasonsoup.find_all('a'):
			game_id = extract_game_id(anchor.get('href'))
			if game_id:
				# print (game_id)
				db.create_webref(str(game_id), season_id)



	except Exception as e:
		print('=======')
		print(f'======> Exception occurred: {e} rolling back the database transaction.')
		print('=======')		
		db.rollback()
	else:
		print('=======')
		print('======> Success.')
		print('=======')		
		db.commit()
	finally:
		pass
