import sys
import keyboard
from functions import *
from time import sleep
print("Finished importing libraries.")

keyboard.add_hotkey('print screen', lambda: invert_playback())
keyboard.add_hotkey('ctrl+page up',lambda: play_playlist_1())
keyboard.add_hotkey('ctrl+page down',lambda: play_playlist_2())
keyboard.add_hotkey('ctrl+right', lambda: skip())
keyboard.add_hotkey('ctrl+left', lambda: go_back())
keyboard.add_hotkey('ctrl+up', lambda: vol_up())
keyboard.add_hotkey('ctrl+down', lambda: vol_down())

print("Finished added keyboard hotkeys.")
while True:
    sleep(5)
    wait_for_connection()