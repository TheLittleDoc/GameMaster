import os
import sys
from tkinter import messagebox
from requests import *
import webbrowser

f = {}

def external_link(link):
    asklink = messagebox.askyesno("Open link", "GameMaster is opening \"%s\" in your default browser.\n\nDo you want to continue?" % link)
    if asklink == True:
        webbrowser.open(link)
    else:
        None

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def retrieve_file(url, name):
    if not "http" in url:
        messagebox.ABOUT(title='Invalid URL',message='URL must start with "http"', icon='warning')
    else:
        file = get(url)
        f[name] = ""
        for line in file:
            decoded_line = line.decode("utf-8")
            f[name] += decoded_line
    return f[name]

def download_file(url, name):
    if not "http" in url:
        messagebox.ABOUT(title='Invalid URL',message='URL must start with "http"', icon='warning')
    else:
        file = get(url)
        print(file.text)
        with open(name, "w") as f:
            f.write(file.text)
            f.close()
        
