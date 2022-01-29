"""    
GameMaster
Copyright (C) 2021  TheLittleDoctor

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
# For old-times sake:
# uwu

from ctypes import alignment
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
from gm_resources import download_file, resource_path

gmc.set_config()

config = gmc.config
try:
    settings_list = gmc.settings_list
except:
    messagebox.showinfo("Warning","Settings not present in config file. Features which require settings are disabled until the problem is resolved")

def focus(event):
    widget = window.focus_get()
    try:
        if "score" in widget.name:
            print("score in focus")
        else:
            print("Enter pressed")
    except:
        print("unknown in focus")

window = Tk()
window.title("GameMaster")
window.geometry("600x620")
img = tk.Image("photo", file=resource_path("icon.png"))
window.tk.call('wm', 'iconphoto', window._w, img)

window.resizable(0,1)
window.minsize(600, 620)
window.bind("<Return>", lambda e: focus(e))
window.lift()
window.attributes("-topmost", True)
window.focus_set()
if config["version"] > 1:
    window.attributes("-topmost", settings_list["on top"])
else:
    window.attributes("-topmost", False)

window.rowconfigure(0, weight=0)
window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)

notebook = Notebook(master=window, padding=0)
notebook.grid(column=0, row=1, sticky=tk.NSEW, padx=0, pady=0, ipadx=0, ipady=0)

main_frame = Frame(notebook)
notebook.add(main_frame, text="Main")
main_frame.rowconfigure(index=0, weight=0)
main_frame.rowconfigure(index=1, weight=1)
main_frame.rowconfigure(index=2, weight=1)
main_frame.columnconfigure(index=0, weight=10)
main_frame.columnconfigure(index=1, weight=0)

settings_frame = Frame(notebook)
notebook.add(settings_frame, text="Settings",state=DISABLED)

config_frame = Frame(notebook)
notebook.add(config_frame, text="Config",state=DISABLED)

header = Frame(master=window,width=40, height=10)
header.grid(column=0, row=0, sticky=EW, columnspan=2, rowspan=1, padx=0, pady=0)
canvas = Canvas(master=header,width = 700, height = 96)
canvas.grid(column=0, row=0, columnspan=2, rowspan=2, sticky=NSEW)
img = ImageTk.PhotoImage(Image.open(resource_path("header_alt.png")))  
canvas.create_image(0, 0, anchor=NW, image=img) 

#==================================================#
#              Timing Setup and Content            #
#==================================================#
gmt.timing_setup(main_frame)

#==================================================#
#             Scoring Setup and Content            #
#==================================================#
scoring = Frame(master=main_frame,width=20, height=10, relief=SUNKEN, borderwidth=3)
scoring.grid(row=2, column=0, sticky=NSEW, padx=5, pady=5)

scoring.columnconfigure(index=0, weight=1)
scoring.columnconfigure(index=1, weight=1)
scoring.rowconfigure(index=0, weight=0)
scoring.rowconfigure(index=1, weight=10)
lbl_home = Label(master=scoring,text="Scoring",font=("Arial",18,""), justify=CENTER)
lbl_home.grid(sticky=S,row=0,column=0,columnspan=2)

global teams_scores
teams_scores = {}
teams_scores["home"] = 0
teams_scores["away"] = 0

teams_names = {}
teams_names["home"] = ""
teams_names["away"] = ""

name_home = StringVar()
score_home = StringVar()
name_away = StringVar()
score_away = StringVar()
def scoreadd(target_team,value):
    teams_scores[target_team] += value
    score_home.set(str(teams_scores["home"]))
    score_away.set(str(teams_scores["away"]))
    for x in teams_scores:
        with open(str("output/")+str(x)+str("_score.txt"), "w") as f:
            f.write(str(teams_scores[x]))
            f.close()

def scoreset(target_team):
    time.sleep(.1)
    if target_team == "home":
        teams_scores["home"] = int(ent_home.get())
    elif target_team == "away":
        teams_scores["away"] = int(ent_away.get())
    score_home.set(str(teams_scores["home"]))
    score_away.set(str(teams_scores["away"]))
    for x in teams_scores:
        with open(str("output/")+str(x)+str("_score.txt"), "w") as f:
            f.write(str(teams_scores[x]))
            f.close()

def nameset(target_team):
    if target_team == "home":
        teams_names[target_team] = str(ent_homename.get())
    elif target_team == "away":
        teams_names[target_team] = str(ent_awayname.get())
    for x in teams_names:
        with open(str("output/")+str(x)+str("_name.txt"), "w", encoding="utf-8") as f:
            f.write(str(teams_names[x]))
            f.close()



score_home.set("0")
homeframe = Frame(master=scoring, borderwidth=3, relief="sunken")
homeframe.grid(row=1, column=0, sticky=NSEW, pady=2, padx=2)
homeframe.columnconfigure(index=0, weight=0, minsize=38)
homeframe.columnconfigure(index=1, weight=1)
homeframe.columnconfigure(index=2, weight=0, minsize=38)
homeframe.rowconfigure(index=0, weight=0)
homeframe.rowconfigure(index=1, weight=1)
homeframe.rowconfigure(index=2, weight=1)
homeframe.rowconfigure(index=2000, weight=100)
lbl_home = Label(master=homeframe,text="Home: ", width=2)
lbl_home.grid(sticky=EW,row=0,column=0,columnspan=1)
ent_homename = Entry(master=homeframe, width=2, font=("Arial",12,""),textvariable=name_home)#, justify="center")
ent_homename.grid(row=0,column=1,columnspan=2, sticky=NSEW, pady=2, padx=2)
ent_home = Entry(name="score",master=homeframe, width=4, font=("Arial",26,""),textvariable=score_home, justify="center")
ent_home.grid(sticky=NS, column=1, row=1, pady=5, padx=5)
btn_homeup = Button(master=homeframe, text="+",width=0,command=lambda: scoreadd("home",1))
btn_homeup.grid(column=2, row=1)
btn_homedn = Button(master=homeframe, text="-",width=0,command=lambda: scoreadd("home",-1))
btn_homedn.grid(column=0, row=1)
btn_homeset = Button(master=homeframe, text="Set Score", width=2,command=lambda: scoreset("home"))
btn_homeset.grid(column=0, row=2, columnspan=3, sticky=NSEW, pady=5, padx=5)

score_away.set("0")
awayframe = Frame(master=scoring, borderwidth=3, relief="sunken")
awayframe.grid(row=1, column=1, sticky=NSEW, pady=2, padx=2)
awayframe.columnconfigure(index=0, weight=0, minsize=38)
awayframe.columnconfigure(index=1, weight=1)
awayframe.columnconfigure(index=2, weight=0, minsize=38)
awayframe.rowconfigure(index=0, weight=0)
awayframe.rowconfigure(index=1, weight=1)
awayframe.rowconfigure(index=2, weight=1)
awayframe.rowconfigure(index=2000, weight=100)
lbl_away = Label(master=awayframe,text="Away: ", width=2)
lbl_away.grid(sticky=EW,row=0,column=0,columnspan=1)
ent_awayname = Entry(master=awayframe, width=2, font=("Arial",12,""),textvariable=name_away)#, justify="center")
ent_awayname.grid(row=0,column=1,columnspan=2, sticky=NSEW, pady=2,padx=2)
ent_away = Entry(name="score",master=awayframe, width=4, font=("Arial",26,""),textvariable=score_away, justify="center")
ent_away.grid(sticky=NS, column=1, row=1, pady=5, padx=5)
btn_awayup = Button(master=awayframe, text="+", width=-1, padding=0,command=lambda: scoreadd("away",1))
btn_awayup.grid(column=2, row=1)
btn_awaydn = Button(master=awayframe, text="-", width=-1,command=lambda: scoreadd("away",-1))
btn_awaydn.grid(column=0, row=1)

btn_awayset = Button(master=awayframe, text="Set Score", width=2,command=lambda: scoreset("away"))
btn_awayset.grid(column=0, row=2, columnspan=3, sticky=NSEW, pady=5, padx=5)

name_home.trace("w", lambda name, index, mode: nameset("home"))

# score_home.trace("w", lambda name, index, mode, score_home=score_home: scoreset("home"))

name_away.trace("w", lambda name, index, mode: nameset("away"))

# score_away.trace("w", lambda name, index, mode, score_away=score_away: scoreset("away"))


# Sets all the scores and variables into the window
scrs = config["scores"]
scrs_index = scrs.keys()
s = {}

for x in scrs:
    homeframe.rowconfigure(index=list(scrs.keys()).index(x)+3, weight=0)
    s["btn_"+x] = Button(master=homeframe, text=str(x), command=lambda x=x: scoreadd("home",int(scrs[x])))
    s["btn_"+x].grid(column=0, columnspan=3, padx=10, row=list(scrs.keys()).index(x)+3, sticky=EW)

for x in scrs:
    awayframe.rowconfigure(index=list(scrs.keys()).index(x)+3, weight=0)
    s["btn_"+x] = Button(master=awayframe, text=str(x), command=lambda x=x: scoreadd("away",int(scrs[x])))
    s["btn_"+x].grid(column=0, columnspan=3, padx=10, row=list(scrs.keys()).index(x)+3, sticky=EW)

for x in teams_scores:
    with open(str("output/")+str(x)+str("_score.txt"), "w") as f:
        f.write(str(teams_scores[x]))
        f.close()

for x in teams_names:
    with open(str("output/")+str(x)+str("_name.txt"), "w") as f:
        f.write(str(teams_names[x]))
        f.close()

# Score: 0/100

#==================================================#
#            Variables Setup and Content           #
#==================================================#
variables = Frame(master=main_frame,width=20, height=10, relief=GROOVE, borderwidth=3)
variables.grid(row=1, column=1, sticky=NSEW, padx=5, pady=5)

variables.columnconfigure(index=0, weight=1)
variables.columnconfigure(index=1, weight=1)
variables.columnconfigure(index=2, weight=1)
variables.rowconfigure(index=0, weight=0)
variables.rowconfigure(index=2000, weight=1)

#[  Timing and sections functions  ]#
def varset(varname,value):
    with open(str("output/")+str(varname)+str(".txt"), "w") as f:
        f.write(str(value))
        f.close()

lbl_variables = Label(master=variables,text="Other Variables",font=("Arial",18,""),justify="center")
lbl_variables.grid(sticky=S,row=0,column=0,columnspan=3)

vars = config["vars"]
v = {}
for x in vars:
    variables.rowconfigure(index=vars.index(x)+1, weight=0)
    v["lbl_"+x] = Label(master=variables, text=x)
    v["ent_"+x] = Entry(master=variables, font=("Arial",12,""),justify="center",width=5) 
    v["ent_"+x].name = x #                                    Fixed \/
    v["btn_"+x] = Button(master=variables, text=str("Set"), width=4,command=lambda x=x: varset(str(x), int(v["ent_"+x].get())))
    v["lbl_"+x].grid(sticky=E, column=0, row=int(vars.index(x)+2))
    v["ent_"+x].grid(sticky=NS, column=1, row=int(vars.index(x)+2))
    v["btn_"+x].grid(sticky=W, column=2, row=int(vars.index(x)+2), columnspan=2, padx=2)

#==================================================#
#            Settings Setup and Content            #
#==================================================#
settings = Frame(master=main_frame,width=20, height=10, relief=GROOVE, borderwidth=3)
settings.grid(row=2, column=1, sticky=NSEW, padx=5, pady=5)

settings.columnconfigure(index=0, weight=0)
settings.columnconfigure(index=1, weight=1)
settings.rowconfigure(index=0, weight=1)
settings.rowconfigure(index=1, weight=1)
settings.rowconfigure(index=1999, weight=100)
settings.rowconfigure(index=2000, weight=0)
settings.rowconfigure(index=2001, weight=0)
settings.rowconfigure(index=2002, weight=0)
settings.rowconfigure(index=2010, weight=0, minsize=2)

configname = StringVar()

#[      Settings functions      ]#
def config_name():
    config["name"] = ent_name.get()
    gmc.set_config()

def settings_set(setting,value):
    settings_list[setting] = value
    if (setting == "seconds" and value == True) and (stvar["bool_minutes"].get() == False):
        
        st["box_hours"].config(state=DISABLED)
        stvar["bool_hours"].set(False)
        settings_set("hours",False)
    elif (setting == "hours" and value == True) and (stvar["bool_minutes"].get() == False):
        st["box_seconds"].config(state=DISABLED)
        stvar["bool_seconds"].set(False)
        settings_set("seconds",False)
    elif (setting == "minutes" and value == True):
        st["box_seconds"].config(state=NORMAL)
        st["box_hours"].config(state=NORMAL)
    elif (setting == "minutes" and value == False) and (stvar["bool_seconds"].get() == True) and (stvar["bool_hours"].get() == False) or (setting == "minutes" and value == False) and (stvar["bool_hours"].get() == True) and (stvar["bool_seconds"].get() == True):
        st["box_hours"].config(state=DISABLED)
        stvar["bool_hours"].set(False)
        settings_set("hours",False)
    elif (setting == "minutes" and value == False) and (stvar["bool_hours"].get() == True) and (stvar["bool_seconds"].get() == False):
        st["box_seconds"].config(state=DISABLED)
        stvar["bool_seconds"].set(False)
        settings_set("seconds",False)
    
    else:
        None

    config["settings"] = settings_list
    gmc.set_config()
    window.attributes("-topmost", settings_list["on top"])
    
lbl_settings = Label(master=settings,text="Settings",font=("Arial",18,""))#,padx=5)
lbl_settings.grid(sticky=S,row=0,column=0,columnspan=3)
lbl_name = Label(master=settings,text="Name:")
lbl_name.grid(column=0, row=1, sticky=NS, padx=1)
ent_name = Entry(master=settings, width=10, font=("Arial",12,""),textvariable=configname)
ent_name.grid(column=1, row=1, sticky=NSEW, padx=5)
ent_name.insert(0, config["name"])
configname.trace("w", lambda name, index, mode: config_name())
# btn_name = Button(master=settings,text="Set", command=config_name,width=4)
# btn_name.grid(column=2, row=1, sticky=NW, padx=5)
btn_find = Button(master=settings,text="Open output files", width=20,command=lambda: os.startfile(str("output\\")))
btn_find.grid(column=0, row=2000, sticky=NS, padx=5, columnspan=2)
btn_reload = Button(master=settings,text="Reload config", width=20, command=gmc.config_reload)
btn_reload.grid(column=0, row=2001, sticky=NS, padx=5, columnspan=2)
btn_choose = Button(master=settings,text="Select config file", width=20,command=gmc.config_choose)
btn_choose.grid(column=0, row=2002, sticky=NS, padx=5, columnspan=2)

if config["version"] > 1:
    st = {}
    stvar = {}
    for x in settings_list:
        settings.rowconfigure(index=list(settings_list.keys()).index(x)+2, weight=1)
        if isinstance(settings_list[x], bool):
            stvar["bool_"+x] = BooleanVar()
            st["box_"+x] = Checkbutton(text=("Toggle " + x.capitalize()),master=settings, variable=stvar["bool_"+x], command=lambda x=x: settings_set(str(x), stvar["bool_"+x].get())) # Check the syntax for getting boolean status on this checkbox
            st["box_"+x].grid(column=1, columnspan=2, row=list(settings_list.keys()).index(x)+2, sticky=W)
            stvar["bool_"+x].set(settings_list[x])
            if x not in ["hours","minutes","seconds","on top", "end on time", "countup"]:
                stvar["bool_"+x].set(False)
                st["box_"+x].config(state=DISABLED)

#==================================================#
#                     About Tab                    #
#==================================================#
gma.about_setup(notebook)

persistentgeo = window.winfo_geometry()

def tab_change():
    if notebook.index(notebook.select()) == 3:
        global persistentgeo
        persistentgeo = window.winfo_geometry()
        window.geometry("600x720")
    else:
        window.geometry(persistentgeo[0:persistentgeo.find("+")-1])

window.bind("<<NotebookTabChanged>>", lambda event: tab_change())

try:
    with open("news.txt","r") as f:
        news = f.read()
except:
    download_file("https://raw.githubusercontent.com/TheLittleDoc/GameMaster/master/version_info/news-en.txt","news.txt")
    gma.show_file("GameMaster News", "news.txt", "github.com/TheLittleDoc/GameMaster")
    with open("news.txt","r") as f:
        news = f.read()

if news != download_file("https://raw.githubusercontent.com/TheLittleDoc/GameMaster/master/version_info/news-en.txt", "news.txt"):
    with open("news.txt","r") as f:
        news = f.read()
    gma.show_file("GameMaster News", "news.txt", "github.com/TheLittleDoc/GameMaster")


#[================================================]#

def clean_exit():
    gmc.donation_alarm()
    os._exit(0)

#[================================================]#
window.bind('<Destroy>', lambda event: clean_exit())
window.mainloop()