import os
import sys
from tkinter import messagebox
from requests import *

f = {}

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
        
