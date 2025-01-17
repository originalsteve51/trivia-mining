import sqlite3
from sqlite3 import Error

from dbaccess import DatabaseAccessor


# Main code to demonstrate CRUD operations
if __name__ == '__main__':
    database_name = 'jtrivia.db'

    db = DatabaseAccessor(database_name)

    # Example CRUD operations
    try:
        print("Creating categories...")
        category_id = db.create_category( 
                                        "General Knowledge")

        difficulty_id = db.create_difficulty( "Medium")
        
        showinfo_id = db.create_showinfo( 
                                    "1234", 
                                    "5678",
                                    "2025-01-01", 
                                    "Tournament of Champions")
        
        print("Creating a question...")
        question_id = db.create_question( 
                                        "What is the answer to life, the universe, and everything?", 
                                        difficulty_id, 
                                        category_id, 
                                        showinfo_id)

         # Assuming "42" is a possible answer and correct
        print("Creating an answer...")
        answer_id = db.create_answer( "42", question_id, True) 


        db.update_questions_stage_for_use(question_id, 1)
    except Exception as e:
        print(f'Exception occurred: {e}')
        db.rollback()
    else:
        print('Completed succesfully')
        db.commit()
    finally:
        pass

    