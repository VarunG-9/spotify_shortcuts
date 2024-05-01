import os
import spotipy
import keyboard
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import pickle

current_vol = 69
def save_vol():
    global current_vol
    with open(r'C:\Users\aweclops\AppData\Roaming\Spotify\volume.pickle', 'wb') as file:
        pickle.dump(current_vol, file)

def resume():
    sp.start_playback(device_id=None, context_uri=None, uris=None, offset=None, position_ms=None)

def pause():
    sp.pause_playback()

def invert_playback():
    if sp.current_user_playing_track()['is_playing']:
        pause()
    else: 
        resume()

def skip():
    sp.next_track(device_id=None)

def go_back():
    sp.previous_track(device_id=None)

def play_playlist_1():
    sp.start_playback(device_id=None, context_uri='spotify:playlist:09ArxQD7XoZKgXBgYvHuDp', uris=None, offset=None, position_ms=None)

def play_playlist_2():
    sp.start_playback(device_id=None, context_uri='spotify:playlist:4U3OIyfLyXfAsEVTcFhMWK', uris=None, offset=None, position_ms=None)

def vol_up():
    print('vol up')
    global current_vol
    current_vol+=5
    if current_vol > 100:
        current_vol=100
    sp.volume(current_vol)
    save_vol()

def vol_down():
    print('vol down')
    global current_vol
    current_vol-=5
    if current_vol<0:
        current_vol=0
    sp.volume(current_vol)
    save_vol()


# Checking if volume file exists, otherwise create.
path = r'C:\Users\aweclops\AppData\Roaming\Spotify\volume.pickle'
if os.path.isfile(path):
    pass
else: 
    f = open(path, "x")
    save_vol()
    
# Loading Volume

try:    
    with open(r'C:\Users\aweclops\AppData\Roaming\Spotify\volume.pickle', 'rb') as file:
        current_vol=pickle.load(file)
        print("loaded volume")
except: 
    print('error: not loaded volume')


scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))


print('opening spotify')
os.startfile(r'C:\Users\aweclops\AppData\Roaming\Spotify\Spotify.exe')
print('opened spotify')

while True:
    try:
        sp.volume(current_vol)
        print('connecting')
        break
        
    except:
        print('failed to connect. trying again')
        

keyboard.add_hotkey('print screen', lambda: invert_playback())
keyboard.add_hotkey('ctrl+page up',lambda: play_playlist_1())
keyboard.add_hotkey('ctrl+page down',lambda: play_playlist_2())
keyboard.add_hotkey('ctrl+right', lambda: skip())
keyboard.add_hotkey('ctrl+left', lambda: go_back())
keyboard.add_hotkey('ctrl+up', lambda: vol_up())
keyboard.add_hotkey('ctrl+down', lambda: vol_down())

keyboard.wait('esc')