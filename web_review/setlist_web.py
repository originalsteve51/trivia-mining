from flask import Flask, render_template, jsonify, request
import os, json

app = Flask(__name__)

run_on_host = os.environ.get('RUN_ON_HOST') 
using_port = os.environ.get('USING_PORT')
update_interval = os.environ.get('UPDATE_INTERVAL')
debug_mode = os.environ.get('DEBUG_MODE')

# Global data that is set from the engine and later provided
# to the view page
rows = []
setlist_data = []
songs_info = []
playlist_name='My Playlist'

songs_played = []

print(f"run_on_host: {run_on_host}, Using Port: {using_port}, Update interval: {update_interval}, Debug: {debug_mode}")

"""
Display the index.html page, which is used to view a set list whose
contents were previously posted here from the engine.
"""
@app.route('/')
def home():
    global playlist_name
    return render_template('index.html', playlist_name=playlist_name)

@app.route('/admin', methods=['GET'])
def admin():
    global playlist_name
    return render_template('admin.html', playlist_name=playlist_name)

@app.route('/listener', methods=['GET'])
def listener():
    global playlist_name
    return render_template('listener.html', playlist_name=playlist_name)

@app.route('/api/song_played', methods=['POST'])
def song_played():
    global songs_played
    data = request.get_json()

    if 'song_id' in data:
        song_id = data['song_id']
        # print(f'Song id number: {song_id}')
        
        if not song_id in songs_played:
            songs_played.append(song_id)
        else:
            songs_played.remove(song_id)
        print(songs_played)

        return jsonify(success=True, message=f'Song id {song_id} was marked as played')
    else:
        print(f'Song id not received in request')
        return jsonify(success=False, message=f'Song id not received')

@app.route('/api/clear', methods=['GET'])
def clear():
    global playlist_name
    global setlist_data
    global songs_info
    playlist_name=' '
    setlist_data.clear() 
    songs_info.clear()
    return render_template('listener.html', playlist_name=playlist_name)  

@app.route('/api/get_playlist_name', methods=['GET'])
def get_playlist_name():
    global playlist_name
    name_json= playlist_name
    return jsonify(name_json) 

"""
The set list is prepared by the engine and posted here as a list of JSON
rows containing info about songs.
"""
@app.route('/load_setlist',methods=['POST'])
def load_setlist():
    global setlist_data
    global songs_info

    # First, clear out the setlist and info in case there's already something there
    setlist_data.clear()
    songs_info.clear()

    # Data posted here by the engine is saved in global data for retrieval
    # by requests issued to /get_rows from a web page wanting to view the set list
    json_string = request.get_json()
    setlist_data = json.loads(json_string)

    print('======>>  ', len(setlist_data))

    for _ in range(0, len(setlist_data)):
        songs_info.append({'info': setlist_data[_]['song_info'], 'name': setlist_data[_]['song_name'] })
        print(songs_info[_]['name'])
    
    # Respond to the client with an OK status (jsonify with no args does this)
    return jsonify()

@app.route('/load_onesong',methods=['POST'])
def load_onesong():
    global setlist_data
    global songs_info

    # First, clear out the setlist and info in case there's already something there
    # setlist_data.clear()
    # songs_info.clear()

    # Data posted here by the engine is saved in global data for retrieval
    # by requests issued to /get_rows from a web page wanting to view the set list
    json_string = request.get_json()
    raw_data = json.loads(json_string)

    for _ in range(0, len(raw_data)):
        songs_info.append({'info': raw_data[_]['song_info'], 'name': raw_data[_]['song_name'] })
        print(f'{songs_info}')
        setlist_data.append(raw_data[_])
        
    # Respond to the client with an OK status (jsonify with no args does this)
    return jsonify()

@app.route('/get_song_info', methods=['GET'])
def get_song_info():
    song_number = int(request.args.get('song_number')) 
    song_name = songs_info[song_number]['name']
    return render_template('info.html', song_name=song_name, song_number=song_number)

@app.route('/song_info', methods=['GET'])
def song_info():
    song_number = request.args.get('song_number') 
    song_info = songs_info[int(song_number)] 
    return jsonify(song_info)   

@app.route('/playlist_info', methods=['POST'])
def playlist_info():
    global playlist_name
    json_string = request.get_json()
    playlist_data = json.loads(json_string)
    playlist_name = playlist_data['name']

    return jsonify()


"""
The index page calls /get_rows to obtain the set list data.
"""
@app.route('/get_rows',methods=['GET'])
def get_rows():
    global setlist_data
    global rows
    global songs_info

    caller = request.args.get('id')

    # Get a clean start!
    rows.clear()

    # Build the list of rows from the JSON data provided by the engine.
    # Each row is just a string with song information that will be shown
    # on the index page.
    if caller == 'admin':
        for song_number in range(len(setlist_data)):
            row_data = setlist_data[song_number]
            a_row = list()
            a_row.append(f"{row_data['song_name']}")
            a_row.append(f"{row_data['artist_name']}")
            a_row.append(f"{row_data['album_name']}")
            a_row.append(f"{row_data['year_released']}")
            a_row.append(f"{song_number}")
            rows.append(a_row)
    elif caller == 'listener':
        for song_number in range(len(setlist_data)):
            # The listener view shows the rows in a last-in-first-out manner, so
            # the data has to be viewed from last element to first element.
            # Hence the indexing gymnastics below...
            row_data = setlist_data[len(setlist_data)-song_number-1]
            a_row = list()
            a_row.append(f"{row_data['song_name']}")
            a_row.append(f"{row_data['artist_name']}")
            a_row.append(f"{row_data['album_name']}")
            a_row.append(f"{row_data['year_released']}")
            info_idx = len(setlist_data) - song_number - 1
            a_row.append(f"{info_idx}")
            rows.append(a_row)
    else:
        for song_idx in range(len(songs_played)):    
            reverse_songs_played = songs_played[::-1]
            song_number = reverse_songs_played[song_idx]
            row_data = setlist_data[song_number]
            a_row = list()
            a_row.append(f"{row_data['song_name']}")
            a_row.append(f"{row_data['artist_name']}")
            a_row.append(f"{row_data['album_name']}")
            a_row.append(f"{row_data['year_released']}")
            a_row.append(f"{song_number}")
            rows.append(a_row)

    
    # Return the list in JSON form for the page to render.
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=using_port, host='0.0.0.0')
