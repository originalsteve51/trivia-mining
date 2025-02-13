# Question Browser

import cmd
import requests
import json
import os
import sys
import shlex
import random

# For now, I want to use dbaccess.py in the parent directory.
# Fix up the path searched by Python for modules to include the absolute path
# to the parent directory...
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ''))
sys.path.insert(0, parent_dir)
# print('======> ', parent_dir)

from dbaccess import DatabaseAccessor

# To support random selection of difficulty level and years, these
# lists are used.
diffs = [200,400,600,800,1000,1200,1600,2000,3000]
years = [1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,\
         2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,\
         2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025]

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

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
# ExitCmdException class - Provides an Exception for when breaking
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

class CommandProcessor(cmd.Cmd):
    def __init__(self):
        super(CommandProcessor, self).__init__()
        self.openai = OpenAIAccessor() 
        self.dbaccess = DatabaseAccessor('../jtrivia.db')

    prompt = '(Issue a command)'

    def do_songinfo(self, args):
    	'''
    	songinfo is here for testing the OpenAI class. Provide two arguments, each surrounded with quotes, for the artist name and the song name.
    	'''
    	arg_vals = shlex.split(args)
    	artist = arg_vals[0]
    	song = arg_vals[1]
    	print(self.openai.get_song_info(artist, song))

    def do_random_q_a(self, arg):
        params = parse(arg)
        if len(params) != 2:
            value = random.choice(diffs)
            year = random.choice(years)
        else:
            value = params[0]
            year = params[1]
        self.dbaccess.random_q_a(value, year)

    def do_category_questions(self, cat_id):
    	self.dbaccess.read_questions_for_catid(cat_id)       

    def do_quit(self, _):
    	print(_)
    	raise ExitCmdException()


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
    
            if exception_name == 'ExitCmdException':
                continue_running = False
                print('\nEXITING the program...')
                os._exit(0)
            else:
                display_general_exception(e)
            
            choice = input('Try correcting this problem and press "Y" to try again, or any other key to exit. ')
            if choice.upper() != 'Y':
                continue_running = False
                print('Exiting the program')        

