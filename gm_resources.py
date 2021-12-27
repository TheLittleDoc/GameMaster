import os
import sys
from tkinter import messagebox
from urllib import request

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
        file = request.urlopen(url)
        f[name] = ""
        for line in file:
            decoded_line = line.decode("utf-8")
            f[name] += decoded_line
        print(f[name])

def download_file(url, name):
    if not "http" in url:
        messagebox.ABOUT(title='Invalid URL',message='URL must start with "http"', icon='warning')
    else:
        request.urlretrieve(url, name)