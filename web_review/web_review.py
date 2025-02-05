from flask import Flask, render_template, jsonify, request
import os, sys, json, random

# For now, I want to use dbaccess.py in the parent directory.
# Fix up the path searched by Python for modules to include the absolute path
# to the parent directory...
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ''))
sys.path.insert(0, parent_dir)

from dbaccess import DatabaseAccessor


app = Flask(__name__)

run_on_host = os.environ.get('RUN_ON_HOST') 
using_port = os.environ.get('USING_PORT')
debug_mode = os.environ.get('DEBUG_MODE')

# The db file resides in the parent directory
dbaccessor = DatabaseAccessor(parent_dir+'/jtrivia.db')



DATE = 0
CATEGORY = 1
QUESTION = 2
ANSWER = 3
QUESTION_ID = 5

difficulties = [200,400,600,800,1000,1200,1600,3000]


print(f"run_on_host: {run_on_host}, Using Port: {using_port}, Debug: {debug_mode}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/reject_question', methods=['POST'])
def reject_question():
    data = request.get_json()
    print('rejecting: ', data['question_id'])
    dbaccessor.mark_question_rejected(data['question_id'], True)

    return jsonify()

@app.route('/api/next_q_a', methods=['GET'])
def next_q_a():
    difficulty = random.choice(difficulties);
    
    result = dbaccessor.random_q_a(difficulty)

    if difficulty != 3000:
        difficulty = '$' + str(difficulty)
    else:
        difficulty = 'Final Jeopardy'

    q_a_row = list()
    q_a_row.append(result[CATEGORY])
    q_a_row.append(result[QUESTION])
    q_a_row.append(result[ANSWER])
    q_a_row.append(result[DATE])
    q_a_row.append(difficulty)
    q_a_row.append(result[QUESTION_ID])
    print('question_id: ', result[5])
    
    return jsonify(q_a_row)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=using_port, host='0.0.0.0')
