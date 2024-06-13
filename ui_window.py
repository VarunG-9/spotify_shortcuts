from functions import *
import tkinter as tk
from tkinter import ttk
import keyboard
import pystray
from PIL import Image, ImageDraw
import ctypes as ct
from pystray import MenuItem as item

def open_action():
    global root
    root, frame, scrollbar, canvas, frame, save_frame, save_button = create_window()
    root.mainloop()

def quit_action():
    global root, icon
    try:
        root.destroy()
        print("Destroyed Root")
    except:
        print("Root not found. Stopping item.")
    
    icon.stop()
    print("Stopped item")

def main():
    global icon
    icon = pystray.Icon(
    'Spotify_Shortcuts',
    icon=create_image(64, 64, 'black', 'white'))
    

    menu = (item('Open Window', open_action), item('Quit App', quit_action))
    icon.menu = menu
    icon.run()

if __name__ == "__main__":
    main()