

import cmd
import time
import requests
import json
import os
import sys
import threading

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from openai import OpenAI

from player import Player
from playlist import Playlist


web_controller_url = os.environ['WEB_CONTROLLER_URL']
print('Web controller url: ', web_controller_url)




#-----------------------------------------------------------
# Spotify is a class that provides access to the Spotify API
# The spotipy library performs its magic here by using values
# found in the environment to authenticate the user. Once
# authenticated, the api can be called.
# This depends on the following environment variable values, which
# should be set by a shell script.
# export SPOTIPY_CLIENT_ID=
# export SPOTIPY_CLIENT_SECRET=
# export SPOTIPY_REDIRECT_URI="http://127.0.0.1:8080"
#-----------------------------------------------------------
class Spotify():
    def __init__(self):
        ascope = 'user-read-currently-playing,\
                playlist-modify-private,\
                user-read-playback-state,\
                user-modify-playback-state'
        ccm=SpotifyOAuth(scope=ascope, open_browser=True)
        self.sp = spotipy.Spotify(client_credentials_manager=ccm)

              

class OpenAIAccessor():
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        self.url='https://api.openai.com/v1/chat/completions'
        self.headers={
                        'Authorization':f'Bearer {api_key}',
                        'Content-Type':'application/json'
                    }

    def get_song_info(self, artist, song_name):
        
        data = {
            'model': 'gpt-4o-mini',
            'messages': [{'role': 'user', 
                        'content': f"Give me history including lyrical themes of the \
                                    {artist}'s song '{song_name}', \
                                    max length 400 words, using words that a fifth grader \
                                    can understand. Break this into paragraphs \
                                    with <p> at the start of each paragraph and </p><br/> \
                                    at the end of each paragraph."}],
            'max_tokens':500,
            'temperature':0.8
        }
        print('-------> get_song_info called')
        raw_info = requests.post(self.url, headers=self.headers, json=data)
        json_info = json.loads(raw_info.text)

        return json_info['choices'][0]['message']['content']

#-------------------------------------------------------------------
# ExitCmdException class - Just so we have a good name when breaking
# out of the command loop with an Exception
#-------------------------------------------------------------------
class ExitCmdException(Exception):
    pass 


class AutoMonitor():
    def __init__(self, cmdprocessor):
        self._running = False
        self._thread = None
        self.cmdprocessor = cmdprocessor
        self.player = cmdprocessor.player

    def start(self):
        if not self._running:
            # requests.get(web_controller_url+'/clearweb')
            print('Starting AutoMonitor')
            self._running = True
            self._thread = threading.Thread(target=self._run)
            self._thread.start()
    
    def stop(self):
        self._running = False
        if self._thread is not None:
            self._thread.join()
    
    def _run(self):
        while self._running:
            continue_playing = True
            while continue_playing:
                if self.player:
                    track_idx = self.player.play_next_track()
                    if track_idx:
                        self.cmdprocessor.notify_web_controller(track_idx)
                    else:
                        break

                while self.player.currently_playing()[1]:
                    time.sleep(1)
                    # print(self.player.currently_playing()[0])
                    pass


class CommandProcessor(cmd.Cmd):
    def __init__(self):
        super(CommandProcessor, self).__init__()
        spotify = Spotify()
        self.sp = spotify.sp
        self.openai = OpenAIAccessor() 
        self.pl = Playlist(spotify.sp, self.openai)
        self.player = Player(spotify.sp)
        self.automonitor = None

        
    prompt = '(Issue a command)'

    def do_autoplay(self, _):
        if len(self.player.unplayed_track_indexes) > 0:
            if not self.automonitor:
                self.automonitor = AutoMonitor(self)
                self.automonitor.start()
                time.sleep(2)
                print('The AutoMonitor has been started')  
        else:
            print('Cannot autoplay because no tracks are available to play')    

    def do_clearweb(self, _):
        requests.get(web_controller_url+'/api/clear')

    def do_displaylist(self, list_number):
        """ Show the names of tracks in a Spotify playlist. """
        if list_number:
            self.pl.process_playlist(list_number, False)
            self.player.add_from_playlist(self.pl)
        else:
            print('You must enter the number of a playlist to show and load its tracks')

    def do_lists(self, sub_command=None):
        """Display all Spotify playlists for the authorized Spotify user."""
        playlists = self.pl.get_playlists()
        print('\nThese are your playlists:')
        for k in playlists.keys():
            print(f'{k}: {playlists[f"{k}"][0]}')

    def do_play(self, song_idx):
        if len(self.pl.set_data)>0:
            song_idx = int(song_idx)

            self.notify_web_controller(song_idx)

            print(self.pl.set_data[song_idx]['song_name'])
            self.player.play_track(self.pl.set_data[song_idx]['id'], song_idx)
        else:
            print('Empty list of songs to play!')
        
    def do_stagelist(self, list_number):
        """ Show the names of tracks in a Spotify playlist and add ai derived info """
        if list_number:
            self.pl.process_playlist(list_number, True)
            self.player.add_from_playlist(self.pl)
        else:
            print('You must enter the number of a playlist to stage its tracks')
        
    def do_webload(self, _):
        print(f'Loading set list data to web controller')
        playlist_data = {'name': self.pl.playlist_name}
        requests.post(web_controller_url+'/playlist_info',
                            json=json.dumps(playlist_data))

        requests.post(web_controller_url+'/load_setlist',
                            json=json.dumps(self.pl.set_data))

    def do_musicplayers(self, _):
        """List the music players that Spotify can use to play tracks. The first such player
        that is marked 'Active' in Spotify is selected to play your songs."""
        if self.player:
            self.player.show_available_players()
        else:
            print('No players can be listed.')

    def do_nexttrack(self, _):
        if self.player:
            track_idx = self.player.play_next_track()
            if track_idx:
                self.notify_web_controller(track_idx)
            

    def do_pause(self, _):
        self.player.pause_playback()

    def do_resume(self, _):
        self.player.resume()


    def do_quit(self, args):
        if not self.player.paused:
            self.sp.pause_playback()
    
        raise ExitCmdException()

    def notify_web_controller(self, song_idx):
        # print(f'Loading data for one song to web controller')
        playlist_data = {'name': self.pl.playlist_name}
        requests.post(web_controller_url+'/playlist_info',
                            json=json.dumps(playlist_data))

        one_song_list = []
        one_song_list.append(self.pl.set_data[song_idx])
        requests.post(web_controller_url+'/load_onesong',
                            json=json.dumps(one_song_list))


#-------------------------------------------------------------------
# ExitCmdException class - Just so we have a good name when breaking
# out of the command loop with an Exception
#-------------------------------------------------------------------
class ExitCmdException(Exception):
    pass 

def display_general_exception(e):
    exception_name = e.__class__.__name__
    if exception_name == 'ReadTimeout' or exception_name == 'ConnectionError':
        print(f'\n{exception_name}:\nA network error occurred, possibly the web app is not running.')
    else:
        print(f'\n{exception_name}:\nAn unexpected error occurred.')


if __name__ == '__main__':
    continue_running = True
    cp = None
    while continue_running:
        # Enter the command loop, handling Exceptions that break it. Some Exceptions
        # can be handled, like losing the network. We give the user a chance
        # to correct such errors. If the user believes an Exception
        # has been corrected, the command loop will restart.
        try:
            if cp is None:
                cp = CommandProcessor()
            cp.cmdloop()
        except KeyboardInterrupt:
            print('Interrupted by ctrl-C, attempting to clean up first')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        except Exception as e:
            exception_name = e.__class__.__name__
    
            if exception_name == 'ExitCmdException' or exception_name == 'SpotifyException':
                continue_running = False
                print('\nEXITING the program...')
                os._exit(0)
            else:
                display_general_exception(e)
            
            choice = input('Try correcting this problem and press "Y" to try again, or any other key to exit. ')
            if choice.upper() != 'Y':
                continue_running = False
                print('Exiting the program')        
