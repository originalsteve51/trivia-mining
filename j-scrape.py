# https://j-archive.com/showgame.php?game_id=8836
# conda create --name trivia python=3.12
# conda update -n base conda
# conda install -c anaconda beautifulsoup4
# conda install -c anaconda lxml

import requests 
from bs4 import BeautifulSoup
import re

import sys

from dbaccess import DatabaseAccessor

questions = []
answers = []
categories = []
board = []


category_set = set()
difficulty_set = set()
show_number_set = set()

def extract_show_number(title_text):
	matches = re.findall(r'#\s*(\d+)', title_text)
	integers = [int(match) for match in matches]
	return str(integers[0])

def extract_show_date (title_text):
	date_pattern = r'(\d{4}-\d{2}-\d{2})'
	matches = re.findall(date_pattern, title_text)
	return str(matches[0])

def get_offset(idx):
	offset = 0
	if idx>=30 and idx<60:
		offset = 6
	elif idx == 60:
		offset = 12
	return offset

def get_difficulty(idx):
	if idx in [0,1,2,3,4,5]:
		difficulty = 200
	elif idx in [6,7,8,9,10,11] or idx in [30,31,32,33,34,35]:
		difficulty = 400
	elif idx in [12,13,14,15,16,17]:
		difficulty = 600
	elif idx in [18,19,20,21,22,23] or idx in [36,37,38,39,40,41]:
		difficulty = 800
	elif idx in [24,25,26,27,28,29]:
		difficulty = 1000
	elif idx in [42,43,44,45,46,47]:
		difficulty = 1200
	elif idx in [48,49,50,51,52,53]:
		difficulty = 1600
	elif idx in [54,55,56,57,58,59]:
		difficulty = 2000
	else:
		difficulty=3000

	return difficulty

def show_item(item_num):
	global board
	print(board[item_num]['cat'],'\n',
		  board[item_num]['diff'],'\n',
		  board[item_num]['q'],'\n',
		  board[item_num]['a'], '\n',
		  board[item_num]['show_num'], '\n',
		  board[item_num]['show_date'], '\n',
		  board[item_num]['game_comments'])


class JScrapeError(Exception):
    """Exception used for custom error in the application."""

    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code
        self.message = message

    def __str__(self):
        return f"{self.message} (Error Code: {self.error_code})"		

# ############################################        

if __name__ == '__main__':

	num_args = len(sys.argv)

	if num_args != 2:
		print('You must provide an integer show index when invoking this program...')
		sys.exit(0)
	else:
		web_id = int(sys.argv[1])
	
	
	db = DatabaseAccessor('jtrivia.db')


	try:

		url = 'https://j-archive.com/showgame.php?game_id=' + str(web_id)

		response = requests.get(url)

		if response.status_code == 200:
			print('Obtained the question web page')
		else:
			print(f'Failed retrieval with code: {response.status_code}')

		questionsoup = BeautifulSoup(response.content, "html.parser")

		title = str(questionsoup.find('title'))
		show_number = extract_show_number(title)


		show_info_id = db.get_showinfo(show_number)

		if not show_info_id:
			print(f'Adding info to the database for show number {show_number} , web id {web_id}')
			show_date = extract_show_date(title)

			for td in questionsoup.find_all('td'):
				if td.get('class') and td.get('class')[0]=='clue_text' and not td.get('id').endswith('_r') :
					questions.append(td.get_text())
				if td.get('class') and td.get('class')[0]=='category_name':
					categories.append(td.get_text())
			
			for div in questionsoup.find_all('div'):
				if div.get('id') and div.get('id')=='game_comments':
					game_comments = div.get_text()
					break
			if game_comments=='':
				game_comments = 'Regular Game'	
					
			print(f'Saving "{game_comments}" originally shown on {show_date}')		

			url = 'https://j-archive.com/showgameresponses.php?game_id=' + str(web_id)

			response = requests.get(url)

			if response.status_code == 200:
				print('Obtained the response web page')
			else:
				print(f'Failed retrieval with code: {response.status_code}')

			answersoup = BeautifulSoup(response.content, "html.parser")

			for em in answersoup.find_all('em'):
				answers.append(em.get_text())

			# Show 9030 (id=8791) causes an error because len(answers) 
			# exceeds len(questions)

			for idx in range(0, len(answers)):
				# Each summary comprises information about a single question from a J board
				offset = get_offset(idx)
				difficulty = get_difficulty(idx)
				category = categories[(idx%6) + offset]

				"""
				summary = {'cat':category, 
							'q': questions[idx], 
							'a':answers[idx], 
							'diff': difficulty,
							'show_num': show_number,
							'show_date': show_date,
							'game_comments': game_comments}
				"""

				show_info_id = db.get_showinfo(show_number)
				if not show_info_id: 
					show_info_id = db.create_showinfo(show_number, web_id, show_date, game_comments)

				category_id = db.get_category_id(category)
				if not category_id: 
					category_id = db.create_category(category)
					
				difficulty_id = db.get_difficulty_id(difficulty)
				if not difficulty_id: 
					difficulty_id = db.create_difficulty(difficulty)

				question_id = db.create_question(questions[idx], difficulty_id, category_id, show_info_id)
				db.create_answer(answers[idx], question_id, 1)	
		else:
			print(f'Not adding anything to the database because show number {show_number} is already loaded')	
			raise JScrapeError("Duplicate page processing not allowed", show_number)
	except Exception as e:
		print('=======')
		print(f'======> Exception occurred: {e} rolling back the database transaction.')
		print('=======')
		db.rollback()
	else:
		print('=======')
		db.commit()
		print('=======> Finished processing without any Exceptions')
		print('=======')
	finally:
		print('Executing the finally block before exiting')







