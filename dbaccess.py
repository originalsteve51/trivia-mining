import sqlite3
from sqlite3 import Error


class DatabaseAccessor():
	def __init__(self, db_file):
		self.conn = None
		try:
			conn = sqlite3.connect(db_file)
			cur = conn.cursor()
			cur.execute('PRAGMA foreign_keys = ON')
			conn.commit()
			self.conn = conn
		except Error as e:
			print(e)

	def commit(self):
		self.conn.commit()

	def rollback(self):
		self.conn.rollback()

	# Function to create a new question
	def create_question(self, question_text, difficulty_id, category_id, showinfo_id, commit=False):
	    sql = ''' INSERT INTO Questions(question_text, difficulty_id, category_id, showinfo_id)
	              VALUES(?,?,?,?) '''
	    cur = self.conn.cursor()
	    cur.execute(sql, (question_text, difficulty_id, category_id, showinfo_id))
	    if commit:
	    	self.conn.commit()
	    return cur.lastrowid

	# Function to read all questions
	def read_questions(self):
	    cur = self.conn.cursor()
	    cur.execute("SELECT * FROM Questions")
	    rows = cur.fetchall()
	    for row in rows:
	        print(row)

	# Function to update a question
	def update_question(self, question_id, question_text, difficulty_id, category_id, showinfo_id, commit=False):
	    sql = ''' UPDATE Questions 
	              SET question_text = ?,  
	                  difficulty_id = ?, 
	                  category_id = ?,
	                  showinfo_id = ?,
	              WHERE question_id = ? '''
	    cur = self.conn.cursor()
	    cur.execute(sql, (question_text, difficulty_id, category_id, showinfo_id, question_id))
	    if commit:
	    	self.conn.commit()

	# Function to delete a question
	def delete_question(self, question_id, commit=False):
	    sql = 'DELETE FROM Questions WHERE question_id = ?'
	    cur = self.conn.cursor()
	    cur.execute(sql, (question_id,))
	    if commit:
	    	self.conn.commit()

	# Function to create an answer
	def create_answer(self, answer_text, question_id, is_correct, commit=False):
	    sql = ''' INSERT INTO Answers(answer_text, question_id, is_correct)
	              VALUES(?,?,?) '''
	    cur = self.conn.cursor()
	    cur.execute(sql, (answer_text, question_id, is_correct))
	    if commit:
	    	self.conn.commit()
	    return cur.lastrowid

	# Function to create a category
	def create_category(self, category_name, commit=False):
	    sql = ''' INSERT INTO Categories(category_name)
	              VALUES(?) '''
	    cur = self.conn.cursor()
	    cur.execute(sql, (category_name,))
	    if commit:
	    	self.conn.commit()
	    return cur.lastrowid

	def get_category_id(self, category_name):
		sql = ''' SELECT CATEGORY_ID FROM Categories WHERE CATEGORY_NAME = ?'''
		cur = self.conn.cursor()
		cur.execute(sql, (category_name,))
		row = cur.fetchone()
		if row:
			return row[0]
		else:
			return None
		

	# Function to create a difficulty
	def create_difficulty(self, difficulty_level, commit=False):
	    sql = ''' INSERT INTO Difficulties(difficulty_level)
	              VALUES(?) '''
	    cur = self.conn.cursor()
	    cur.execute(sql, (difficulty_level,))
	    if commit:
	    	self.conn.commit()
	    return cur.lastrowid

	def get_difficulty_id(self, difficulty_level):
		sql = ''' SELECT DIFFICULTY_ID FROM Difficulties WHERE DIFFICULTY_LEVEL = ?'''
		cur = self.conn.cursor()
		cur.execute(sql, (difficulty_level,))
		row = cur.fetchone()
		if row:
			return row[0]
		else:
			return None
		
	# Function to create a showinfo record
	def create_showinfo(self, show_number, game_id, show_date, show_comments, commit=False):
	    sql = ''' INSERT INTO Showinfo(show_number, web_id_number, show_date, show_comments)
	              VALUES(?,?,?,?) '''
	    cur = self.conn.cursor()
	    cur.execute(sql, (show_number, game_id, show_date, show_comments))
	    if commit:
	    	self.conn.commit()
	    return cur.lastrowid

	def get_showinfo(self, show_number):
		sql = ''' SELECT SHOWINFO_ID FROM SHOWINFO WHERE SHOW_NUMBER = ?'''
		cur = self.conn.cursor()
		cur.execute(sql, (show_number,))
		row = cur.fetchone()
		if row:
			return row[0]
		else:
			return None

	# Function to create a season record
	def create_season(self, season_number, commit=False):
		sql = ''' INSERT INTO Seasons(season_number) VALUES(?) '''
		cur = self.conn.cursor()
		cur.execute(sql, (season_number,))
		if commit:
			self.conn.commit()
		return cur.lastrowid

	def get_season(self, season_number):
		sql = ''' SELECT SEASON_ID FROM SEASONS WHERE SEASON_NUMBER = ?'''
		cur = self.conn.cursor()
		cur.execute(sql, (season_number,))
		row = cur.fetchone()
		if row:
			return row[0]
		else:
			return None

	# Function to update a season to show it has been downloaded
	def update_season_downloaded(self, season_number, is_downloaded, commit=False):
	    sql = ''' UPDATE Seasons 
	              SET is_downloaded = ?  
	              WHERE season_number = ? '''
	    cur = self.conn.cursor()
	    cur.execute(sql, (is_downloaded, season_number))
	    if commit:
	    	self.conn.commit()


	# Function to create a webref record
	def create_webref(self, webref_number, season_id, commit=False):
	    sql = ''' INSERT INTO Webrefs(webref, season_id)
	              VALUES(?,?) '''
	    cur = self.conn.cursor()
	    cur.execute(sql, (webref_number, season_id))
	    if commit:
	    	self.conn.commit()
	    return cur.lastrowid

	def get_season_id(self, season_number):
		sql = '''SELECT SEASON_ID FROM SEASONS WHERE SEASON_NUMBER = ? '''
		cur = self.conn.cursor()
		cur.execute(sql, (season_number,))
		row = cur.fetchone()
		return row[0]

	def get_webref(self, season_id):
		sql = ''' SELECT WEBREF_ID, WEBREF FROM WEBREFS WHERE SEASON_ID = ? AND is_downloaded = 0'''
		cur = self.conn.cursor()
		cur.execute(sql, (season_id,))
		row = cur.fetchone()
		if row:
			return row
		else:
			return None

	def update_webref_downloaded_for_webref(self, webref, is_downloaded, commit=False):
		sql = ''' UPDATE WEBREFS 
			SET is_downloaded = ?  
			WHERE webref = ? '''
		cur = self.conn.cursor()
		cur.execute(sql, (is_downloaded, webref))
		if commit:
			self.conn.commit()
		
	# Function to update a webref to show it has been downloaded
	def update_webref_downloaded(self, webref_id, is_downloaded, commit=False):
	    sql = ''' UPDATE WEBREFS 
	              SET is_downloaded = ?  
	              WHERE webref_id = ? '''
	    cur = self.conn.cursor()
	    cur.execute(sql, (is_downloaded, webref_id))
	    if commit:
	    	self.conn.commit()

	# Function to be used when reviewing questions and deciding whether or not
	# to use in a game. The staging_code is an integer to allow staging for different
	# games, eg all questions with value of 1 are for game whose code is established
	# as 1, value 2 is for a different game, 3 for still another game, and so on. 
	def update_questions_stage_for_use(self, question_id, staging_code, commit=False):
		sql = ''' UPDATE QUESTIONS
				  SET stage_for_use_by = ?
				  WHERE question_id = ? '''
		cur = self.conn.cursor()
		cur.execute(sql, (staging_code, question_id))
		if commit:
			self.conn.commit()	 
