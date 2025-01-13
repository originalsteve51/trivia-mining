import sqlite3
from sqlite3 import Error

# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute('PRAGMA foreign_keys = ON')
        conn.commit()
    except Error as e:
        print(e)
    return conn

# Function to create a new question
def create_question(conn, question_text, difficulty_id, category_id, show_date):
    sql = ''' INSERT INTO Questions(question_text, difficulty_id, category_id, showinfo_id)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (question_text, difficulty_id, category_id, showinfo_id))
    conn.commit()
    return cur.lastrowid

# Function to read all questions
def read_questions(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Questions")
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Function to update a question
def update_question(conn, question_id, question_text, difficulty_id, category_id, showinfo_id):
    sql = ''' UPDATE Questions 
              SET question_text = ?,  
                  difficulty_id = ?, 
                  category_id = ?,
                  showinfo_id = ?,
              WHERE question_id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (question_text, difficulty_id, category_id, showinfo_id, question_id))
    conn.commit()

# Function to delete a question
def delete_question(conn, question_id):
    sql = 'DELETE FROM Questions WHERE question_id = ?'
    cur = conn.cursor()
    cur.execute(sql, (question_id,))
    conn.commit()

# Function to create an answer
def create_answer(conn, answer_text, question_id, is_correct):
    sql = ''' INSERT INTO Answers(answer_text, question_id, is_correct)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (answer_text, question_id, is_correct))
    conn.commit()
    return cur.lastrowid

# Function to create a category
def create_category(conn, category_name):
    sql = ''' INSERT INTO Categories(category_name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (category_name))
    conn.commit()
    return cur.lastrowid

# Function to create a difficulty
def create_difficulty(conn, difficulty_level):
    sql = ''' INSERT INTO Difficulties(difficulty_level)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (difficulty_level,))
    conn.commit()
    return cur.lastrowid

# Function to create a showinfo record
def create_showinfo(conn, show_number, show_date, show_comments):
    sql = ''' INSERT INTO Showinfo(show_number, show_date, show_comments)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (show_number, show_date, show_comments))
    conn.commit()
    return cur.lastrowid

# Main code to demonstrate CRUD operations
if __name__ == '__main__':
    database = "jtrivia.db"

    # Create a database connection
    conn = create_connection(database)

    with conn:
        # Example CRUD operations
        print("Creating categories...")
        category_id = create_category(conn, 
                                        "General Knowledge", 
                                        "Questions related to general knowledge.")

        difficulty_id = create_difficulty(conn, "Medium")
        
        showinfo_id = create_showinfo(conn, 
                                    "1234", 
                                    "2025-01-01", 
                                    "Tournament of Champions")
        
        print("Creating a question...")
        question_id = create_question(conn, 
                                        "What is the answer to life, the universe, and everything?", 
                                        difficulty_id, 
                                        category_id, 
                                        showinfo_id)

        print("Creating an answer...")
        answer_id = create_answer(conn, "42", question_id, 1)  # Assuming "42" is a possible answer and correct

        #print("Reading all questions...")
        #read_questions(conn)

        """
        print("Updating a question...")
        update_question(conn, question_id, "What is the ultimate answer?", answer_id, difficulty_id, category_id, "2023-01-01")
        
        print("Reading all questions after update...")
        read_questions(conn)
        """

        """
        print(f"Deleting question with id {question_id}...")
        delete_question(conn, question_id)

        print("Reading all questions after deletion...")
        read_questions(conn)
        """