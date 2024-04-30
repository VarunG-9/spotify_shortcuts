import subprocess
import os
import spotipy
import keyboard
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

subprocess.call([r'C:\Users\aweclops\AppData\Roaming\Spotify\Spotify.exe'])
sleep(4)
keyboard.send('space')
sleep(0.2)
keyboard.send('space')
sleep(3)
scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

sp.volume(69, device_id=None)
current_vol = 69

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

current_vol = 69
def increase_vol(current_vol):
    new_vol = current_vol+5
    current_vol = new_vol
    sp.volume(new_vol)

keyboard.add_hotkey('print screen', lambda: invert_playback())
keyboard.add_hotkey('ctrl+page up',lambda: play_playlist_1())
keyboard.add_hotkey('ctrl+page down',lambda: play_playlist_2())
keyboard.add_hotkey('ctrl+right', lambda: skip())
keyboard.add_hotkey('ctrl+left', lambda: go_back())

keyboard.wait()