import tkinter as tk
from tkinter import *  
from PIL import ImageTk,Image  
from tkinter.ttk import *
from tkinter import messagebox
import os, os.path, sys
import gm_config as gmc
from gm_resources import resource_path, retrieve_file, download_file

players = gmc.config["players"]

def roster_setup(notebook):

    roster_frame = Frame(notebook)
    notebook.add(roster_frame, text="Players")
    roster_frame.rowconfigure(index=0, weight=1)
    roster_frame.columnconfigure(index=0, weight=1)

    roster = Frame(master=roster_frame,width=20, height=10, relief=SUNKEN, borderwidth=3)
    roster.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)

    roster.rowconfigure(index=0, weight=0)
    roster.rowconfigure(index=1, weight=1)
    roster.columnconfigure(index=0, weight=1)
    roster.columnconfigure(index=1, weight=1)
    roster.columnconfigure(index=2, weight=1)
    roster.columnconfigure(index=3, weight=0)

    roster_scroll = Scrollbar(master=roster, orient=VERTICAL)
    roster_scroll.grid(row=1, column=3, sticky=NS)

    roster_list = Canvas(master=roster, yscrollcommand=roster_scroll.set, bg="white", width=20, height=1000)
    roster_list.grid(row=1, column=0, columnspan=3, sticky=NSEW, padx=5, pady=5)
    roster_scroll.config(command=roster_list.yview)


    lbl_rosters = Label(roster, text="Rosters",font=("Arial",18,""), justify=CENTER)
    lbl_rosters.grid(row=0, column=0, columnspan=3, sticky=S)
