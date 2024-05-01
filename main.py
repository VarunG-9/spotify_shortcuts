import sys
import os
import spotipy
import keyboard
import pickle
from time import sleep
from spotipy.oauth2 import SpotifyOAuth

# Redirect stdout and stderr to log files
stdout_path = r'C:\Users\aweclops\Documents\Python\Spotify_Shortcuts\stdout.log'
stderr_path = r'C:\Users\aweclops\Documents\Python\Spotify_Shortcuts\stderr.log'

try:
    sys.stdout = open(stdout_path, 'w')
    sys.stderr = open(stderr_path, 'w')
except Exception as e:
    print(f"Error: {e}")

print("Finished redirecting stdout and stderr.")

current_vol = 69

def save_vol():
    global current_vol
    with open(r'C:\Users\aweclops\AppData\Roaming\Spotify\volume.pickle', 'wb') as file:
        pickle.dump(current_vol, file)

# Define other functions...

print("Finished defining variables.")

# Check and create volume file if not exists
path = r'C:\Users\aweclops\AppData\Roaming\Spotify\volume.pickle'
if not os.path.isfile(path):
    try:
        with open(path, "x") as f:
            save_vol()
    except Exception as e:
        print(f"Error: {e}")

print("Checked whether volume file exists.")

# Loading Volume
try:    
    with open(r'C:\Users\aweclops\AppData\Roaming\Spotify\volume.pickle', 'rb') as file:
        current_vol=pickle.load(file)
        print("Loaded volume")
except Exception as e:
    print(f"Error: {e}")

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

while True:
    try:
        sp.volume(current_vol)
        print('Connected')
        break
    except Exception as e:
        print(f"Failed to connect: {e}. Trying again.")
        sleep(10)

# Define hotkeys...

keyboard.wait()
print("Added keyboard hotkeys.")
