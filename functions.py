import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep


scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

def get_vol():
    """
    Returns the current volume.

    Returns:
        int: The current volume.
    """
    return sp.devices()['devices'][0]['volume_percent']

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
    current_vol = get_vol()
    current_vol += 5
    if current_vol > 100:
        current_vol=100
    sp.volume(current_vol)
    
def vol_down():
    wait_for_connection()
    current_vol = get_vol()
    current_vol -= 5
    if current_vol < 0:
        current_vol=0
    sp.volume(current_vol)

def is_connected():
    try:
        get_vol()
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

    Returns:
        None
    """
    while True:
        if is_connected():
            break
        else:
            sleep(7)