import tkinter as tk
from tkinter import ttk
import keyboard
import pystray
from PIL import Image, ImageDraw
import ctypes as ct
from pystray import MenuItem as item
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
from PIL import Image, ImageDraw
from win11toast import toast

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

import tkinter as tk
from tkinter import ttk
import keyboard
from os import getenv
import os
import ctypes as ct
from pathlib import Path
import pickle

def dark_title_bar(window):
    """
    MORE INFO:
    https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))
    window.withdraw()
    window.deiconify()

class ShortcutEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pressed_keys = []
        self.key_listener = None
        self.bind('<FocusIn>', self.start_key_listener)
        self.bind('<FocusOut>', self.stop_key_listener)
        self.config(
            font=("Arial", 20),
            bg='#333',  # Adjusted background color
            fg='white',
            insertbackground='white',
            relief=tk.FLAT,  # Make the textbox flat
            borderwidth=0  # Remove border
        )

    def start_key_listener(self, event):
        self.key_listener = keyboard.on_press(self.on_key_press)

    def stop_key_listener(self, event):
        if self.key_listener:
            keyboard.unhook(self.key_listener)
            self.key_listener = None

    def on_key_press(self, event):
        window_state = load_data()
        if window_state == True:
            print("window open.")
            key = event.name
            print(f"Key Pressed: {key}")
            if key not in self.pressed_keys:
                print(f"New Key. Adding to the list")
                self.pressed_keys.append(key)
                self.update_shortcut()
            else:
                print(f"Key already in list. Not adding to list")
                self.update_shortcut()
        else: 
            self.update_shortcut()

    def get_text(self):
        return self.get()

    def update_shortcut(self):
        self.delete(0, tk.END)
        local_text = " + ".join(self.pressed_keys)
        self.insert(0, local_text)

class ClearButton(tk.Button):
    def __init__(self, master=None, shortcut_entry=None, **kwargs):
        super().__init__(master, **kwargs)
        self.shortcut_entry = shortcut_entry
        self.configure(
            text="Clear",
            font=("Arial", 14),  # Reduced font size
            bg='#111',  # Adjusted background color to blend with black
            fg='white',
            activebackground='#111',  # Adjusted active background color to blend with black
            activeforeground='white',
            bd=0,
            padx=10,  # Reduced padding
            pady=5,  # Reduced padding
            relief=tk.FLAT,  # Make the button flat
            borderwidth=0,  # Remove border
            command=self.clear_keys,
            highlightthickness=0  # Remove highlight thickness
        )

    def clear_keys(self):
        self.shortcut_entry.pressed_keys = []
        self.shortcut_entry.delete(0, tk.END)

def create_window():
    global entries
    entries = []

    root = tk.Tk()
    root.title("Shortcut Entry")
    root.configure(bg='black')
    root.protocol('WM_DELETE_WINDOW', close_window)

    window_width = 1000  # Adjusted window width
    window_height = 500  # Adjusted window height

    root.geometry(f"{window_width}x{window_height}")

    # Create a canvas for scrolling
    canvas = tk.Canvas(root, bg='black')
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure canvas scrolling
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    # Create a frame for holding widgets
    frame = tk.Frame(canvas, bg='black')
    canvas.create_window((0, 0), window=frame, anchor='nw')

    # Labels for the shortcuts
    shortcut_names = [
        "Pause/Play",
        "Volume Up",
        "Volume Down",
        "Skip",
        "Go back",
        "Play first playlist",
        "Play second playlist"
    ]
    
    # Create labels with specific names and place them in the frame
    for i, name in enumerate(shortcut_names):
        label_frame = tk.Frame(frame, bg='#333', bd=0)
        label_frame.grid(row=i, column=0, padx=(10, 20), pady=10, sticky="e")  # Reduced padx here

        label = tk.Label(label_frame, text=name + ":", font=("Arial", 18), fg="white", bg='#333')
        label.pack()

    spotify_path = os.path.join(getenv('APPDATA'), 'Spotify')
    shortcut_path = os.path.join(spotify_path, "shortcuts.pickle")

    if os.path.exists(shortcut_path):
        with open(shortcut_path, 'rb') as f:
            shortcuts = pickle.load(f)
    else:
        shortcuts = []

    for i, name in enumerate(shortcut_names):
        entry = ShortcutEntry(frame, width=30)
        entry.grid(row=i, column=1, padx=20, pady=10)
        entries.append(entry)
        clear_button = ClearButton(frame, shortcut_entry=entry, width=10, height=2, borderwidth=0)
        clear_button.grid(row=i, column=2, padx=(20, 30), pady=10)  # Adjusted padx for clear buttons

    # Correspond the values of the shortcut entry box to the retrieved list
        if i < len(shortcuts):
            entry.insert(0, shortcuts[i])

    # Create a frame for the save button
    save_frame = tk.Frame(root, bg='black')
    save_frame.pack(side=tk.BOTTOM, pady=(20, 0))

    # Add a save button
    save_button = tk.Button(save_frame, text="Save", font=("Arial", 14), bg='#111', fg='white', bd=0, relief=tk.FLAT, command=save_data)
    save_button.pack()

    dark_title_bar(root)

    return root, frame, scrollbar, canvas, frame, save_frame, save_button

def save_data():
    global entries
    shortcuts = []
    for entry in entries:
        shortcuts.append(entry.get_text())
    
    spotify_path = os.path.join(getenv('APPDATA'), 'Spotify')
    print(spotify_path)
    shortcut_path = os.path.join(spotify_path, "shortcuts.pickle")

    if not os.path.exists(shortcut_path):
        with open(shortcut_path, 'w'): pass
        print("File not found. Created one.")
    else:
        print("File already exists. Saving")
        print(shortcuts)

    with open(shortcut_path, 'wb') as f:
        pickle.dump(shortcuts, f)

    global root, icon
    toast("Shortcuts Saved. Restart the app for changes to take effect.")

    root.destroy()
    icon.stop()

def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.open('icon.png')
    return image

def add_hotkeys():
    file_path = os.path.join(getenv('APPDATA'), 'Spotify', 'shortcuts.pickle')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
    else:
        return None
    
    for index in range(len(data)):
        if data[index] == '':
            data[index] = None
    
    if data[0] is not None:
        keyboard.add_hotkey(data[0], lambda: invert_playback())   
    if data[1] is not None:
        keyboard.add_hotkey(data[1], lambda: vol_up())   
    if data[2] is not None:
        keyboard.add_hotkey(data[2], lambda: vol_down())    
    if data[3] is not None:
        keyboard.add_hotkey(data[3], lambda: skip())   
    if data[4] is not None:
        keyboard.add_hotkey(data[4], lambda: go_back())   
    if data[5] is not None:
        keyboard.add_hotkey(data[5], lambda: play_playlist_1())   
    if data[6] is not None:
        keyboard.add_hotkey(data[6], lambda: play_playlist_2())


def load_data(file_path=os.path.join(getenv('APPDATA'), 'Spotify', 'window_state.pickle')):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
        return data
    else:
        return None

def dump_data(data, file_path=os.path.join(getenv('APPDATA'), 'Spotify', 'window_state.pickle')):
    folder_path = os.path.dirname(file_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

def open_action():
    global root
    window_state = True
    dump_data(window_state)
    root, frame, scrollbar, canvas, frame, save_frame, save_button = create_window()
    root.mainloop()

def quit_action():
    global root, icon
    window_state = False
    print("Dumped data.")
    dump_data(window_state)
    print(f"Data dumped: {load_data()}")
    try:
        root.destroy()
        print("Destroyed Root")
    except:
        print("Root not found. Stopping item.")
    
    icon.stop()
    print("Stopped item")
    window_state = True

def close_window():
    global root
    window_state = False
    dump_data(window_state)
    root.destroy()


def main():

    global icon
    icon = pystray.Icon(
        'Spotify_Shortcuts',
        icon=create_image(64, 64, 'black', 'white')
    )
    add_hotkeys()
    menu = (item('Open Window', open_action), item('Quit App', quit_action))
    icon.menu = menu
    icon.run()

if __name__ == "__main__":
    main()
