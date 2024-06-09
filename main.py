import sys

# Redirect stdout and stderr to a log file
#sys.stdout = open(r'C:\Users\aweclops\Documents\Python\Spotify_Shortcuts\stdout.log', 'w')
#sys.stderr = open(r'C:\Users\aweclops\Documents\Python\Spotify_Shortcuts\stderr.log', 'w')

from time import sleep
sleep(5)

import os
import spotipy
import keyboard
from spotipy.oauth2 import SpotifyOAuth
import os

import pickle

print("Finished importing libraries.")

current_vol = 69
volume_file_path = os.path.join(os.getenv('APPDATA'), 'volume.pickle')
                                

def save_vol():
    global current_vol
    with open(volume_file_path, 'wb') as file:
        pickle.dump(current_vol, file)

def resume():
    wait_for_connection()
    sp.start_playback(device_id=None, context_uri=None, uris=None, offset=None, position_ms=None)

def pause():
    wait_for_connection()
    sp.pause_playback()

def invert_playback():
    wait_for_connection()
    try:
        if sp.current_user_playing_track()['is_playing']:
            pause()
        else: 
            resume()
    except:
        print("Lost connection to device")
    
def skip():
    wait_for_connection()
    sp.next_track(device_id=None)

def go_back():
    wait_for_connection()
    sp.previous_track(device_id=None)

def play_playlist_1():
    wait_for_connection()
    sp.start_playback(device_id=None, context_uri='spotify:playlist:09ArxQD7XoZKgXBgYvHuDp', uris=None, offset=None, position_ms=None)

def play_playlist_2():
    wait_for_connection()
    sp.start_playback(device_id=None, context_uri='spotify:playlist:4U3OIyfLyXfAsEVTcFhMWK', uris=None, offset=None, position_ms=None)

def vol_up():
    wait_for_connection()
    global current_vol
    current_vol+=5
    if current_vol > 100:
        current_vol=100
    sp.volume(current_vol)
    print(f'vol up. new vol: {current_vol}')
    save_vol()

def vol_down():
    wait_for_connection()
    global current_vol
    current_vol-=5
    if current_vol<0:
        current_vol=0
    print(f'vol down. new vol: {current_vol}')
    sp.volume(current_vol)
    save_vol()

print("Finished defining variables.")
# Checking if volume file exists, otherwise create.

if os.path.isfile(volume_file_path):
    pass
else: 
    f = open(volume_file_path, "x")
    save_vol()

print("checked whether volume file exists.")
# Loading Volume

try:    
    with open(r'C:\Users\aweclops\AppData\Roaming\Spotify\volume.pickle', 'rb') as file:
        current_vol=pickle.load(file)
        print(f"loaded volume. current volume {current_vol}")
except: 
    print('error: not loaded volume')

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

def is_connected():
    try:
        sp.volume(current_vol)
        print("Connected to spotify.")
        return True

    except:
            print('Failed to connect to spotify.')
            return False

def wait_for_connection():
    """
    Waits until the Spotify connection is established.

    This function continuously checks the connection status until the Spotify connection is established.
    It does this by calling the `is_connected` function in a loop until it returns `True`.
    It also sets the volume to the current volume stored in the volume.pickle file.

    Returns:
        None
    """
    while True:
        if is_connected():
            break
        else:
            sleep(7)


keyboard.add_hotkey('print screen', lambda: invert_playback())
keyboard.add_hotkey('ctrl+page up',lambda: play_playlist_1())
keyboard.add_hotkey('ctrl+page down',lambda: play_playlist_2())
keyboard.add_hotkey('ctrl+right', lambda: skip())
keyboard.add_hotkey('ctrl+left', lambda: go_back())
keyboard.add_hotkey('ctrl+up', lambda: vol_up())
keyboard.add_hotkey('ctrl+down', lambda: vol_down())
print("added keyboard hotkeys.")
while True:
    sleep(5)
    wait_for_connection()