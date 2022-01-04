import tkinter as tk
from tkinter import *  
from PIL import ImageTk,Image  
from tkinter.ttk import *
from tkinter import messagebox
import os, os.path, sys
import json
import time
import threading
import types
import gm_config as gmc
import gm_about as gma
import gm_timing as gmt
from gm_resources import resource_path
from flask import *

app = Flask(__name__)

print(gmc.config["name"])

@app.route("/")

def hello_world():
    
    return "<p>Hello, World!</p>"

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    url_for('static', filename='style.css')
    return render_template('hello.html', name=gmc.config["name"])



