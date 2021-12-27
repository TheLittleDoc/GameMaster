import tkinter as tk
from tkinter import *  
from PIL import ImageTk,Image  
from tkinter.ttk import *
from tkinter import messagebox
import os, os.path, sys
import json
import types
import gm_config as gmc
import webbrowser
from gm_resources import resource_path, retrieve_file, download_file

current = 0

def first_run():
    frames_setup = {}

    window_setup = tk.Toplevel()
    window_setup.title("GameMaster Setup")
    window_setup.geometry("600x400")
    window_setup.resizable(False, False)
    window_setup.lift()
    window_setup.attributes("-topmost", True)
    window_setup.iconbitmap(resource_path("icon.ico"))

    window_setup.rowconfigure(index=0, weight=0)
    window_setup.rowconfigure(index=1, weight=1)
    window_setup.rowconfigure(index=2, weight=0)
    window_setup.columnconfigure(index=0, weight=0)
    window_setup.columnconfigure(index=1, weight=1)
    window_setup.columnconfigure(index=2, weight=0)

    bar = Progressbar(window_setup, orient=HORIZONTAL, length=500, mode='determinate')
    bar.grid(row=2, column=1, sticky=NSEW, padx=10, pady=10)
    bar['value'] = current*100/(len(frames_setup)-1)

    def next_frame():
        global current
        frames_setup[current].grid_forget()
        current += 1
        bar['value'] = current*100/(len(frames_setup)-1)
        frames_setup[current].grid(row=1, column=0,columnspan=3, sticky=NSEW, padx=10, pady=10)
        if current == 0:
            btn_setupbw['state'] = "disabled"
        else:
            btn_setupbw['state'] = "normal"
        if current == len(frames_setup)-1:
            btn_setupfw['text'] = "Finish"
            btn_setupfw['command'] = lambda: os.execv(sys.executable, ["python"] + sys.argv)
        else:
            btn_setupfw['text'] = "Next"
            btn_setupfw['command'] = lambda: next_frame()

    def prev_frame():
        global current
        try:
            frames_setup[current].grid_forget()
        except:
            None
        current -= 1
        bar['value'] = current*100/len(frames_setup)
        frames_setup[current].grid(row=1, column=0,columnspan=3, sticky=NSEW, padx=10, pady=10)
        if current == 0:
            btn_setupbw['state'] = "disabled"
        else:
            btn_setupbw['state'] = "normal"
        if current == len(frames_setup)-1:
            btn_setupfw['text'] = "Finish"
            btn_setupfw['command'] = lambda: os.execv(sys.executable, ["python"] + sys.argv)
        else:
            btn_setupfw['text'] = "Next"
            btn_setupfw['command'] = lambda: next_frame()
        

        
    btn_setupfw = Button(window_setup, text="Next", command=lambda: next_frame())
    btn_setupfw.grid(row=2, column=2, sticky=NSEW, padx=10, pady=10)
    btn_setupbw = Button(window_setup, text="Back", state=DISABLED,command=lambda: prev_frame())
    btn_setupbw.grid(row=2, column=0, sticky=NSEW, padx=10, pady=10)

    header = tk.Frame(master=window_setup,width=40, height=10)
    header.grid(column=0, row=0, sticky=tk.EW, columnspan=3, rowspan=1, padx=0, pady=0)
    canvas = Canvas(master=header,width = 700, height = 96)
    canvas.grid(column=0, columnspan=3,row=0, rowspan=2, sticky=tk.NSEW)
    img = ImageTk.PhotoImage(Image.open(resource_path("header_alt.png")))  
    canvas.create_image(0, 0, anchor=NW, image=img)

    body = Frame(master=window_setup,width=40, height=10)
    body.grid(column=0, row=1, sticky=tk.NSEW, columnspan=3, rowspan=1, padx=5, pady=5)
    body.rowconfigure(index=0, weight=0)
    body.rowconfigure(index=1, weight=1)
    body.columnconfigure(index=0, weight=1)



    frames_setup[0] = Frame(master=window_setup,width=40, height=10, relief=GROOVE, borderwidth=5)
    frames_setup[1] = Frame(master=window_setup,width=40, height=10, relief=GROOVE, borderwidth=5)
    frames_setup[0].grid(column=0, row=1, sticky=tk.NSEW, columnspan=3, rowspan=1, padx=10, pady=10)


    lbl_setup = Label(master=frames_setup[0], text="Welcome to GameMaster!", font=("Arial", 18))
    lbl_setup.grid(column=0, row=0, sticky=tk.NSEW)
    lbl_intro = Label(master=frames_setup[0], wraplength=560, justify=LEFT, text="Let’s get you started. In this setup dialog, we’ll walk you through the basics of setting up and using GameMaster, as well as delving into the setup involved with displaying your values inside of OBS. \n\nGameMaster is constantly being updated and maintained by Bears Broadcast Group with help from TheLittleDoctor. Feel free to contact us through any of the channels in the “About” tab following setup.", font=("Arial", 10))
    lbl_intro.grid(column=0, row=1, sticky=tk.NW)

    lbl_configsetup = Label(master=frames_setup[1], text="Config Setup", font=("Arial", 18))
    lbl_configsetup.grid(column=0, row=0, sticky=tk.NSEW)
    lbl_configsetup_intro = Label(master=frames_setup[1], wraplength=560, justify=LEFT, text="Setup will be added later. Right now, I was just verifying that all the underlying systems work.", font=("Arial", 10))
    lbl_configsetup_intro.grid(column=0, row=1, sticky=tk.NW)

    window_setup.mainloop()