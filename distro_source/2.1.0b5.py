#[                                              Hooray! You're looking at the source! How exciting!                                              ]#
#[                                                                                                                                               ]#
#[ Being under AGPLv3, we believe in free software; that's "free" in the sense that it's free to use, free to modify, and free to redistribute.  ]#
#[         While this is one way that you *can* look at the source, we recommend you get the most up-to-date copies from our GitHub page.        ]#
#[ GameMaster is broken up into a handful of different modules to help compartmentalize the code for debugging purposes. At the end of each file,]#
#[                                           you'll see a comment that looks just like this:                                                     ]#
#                                                                                                                                                 #
#                                               {----=====+  End of module  +=====----}                                                           #
#                                                                                                                                                 #
#[                  Thank you for using GameMaster! If you have any questions, comments, or suggestions, please let us know!                     ]#


#                                                            gamemaster.py                                                                        #

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

gmc.set_config()

config = gmc.config
try:
    settings_list = gmc.settings_list
    print(settings_list)
except:
    messagebox.showinfo("Warning","Settings not present in config file. Features which require settings are disabled until the problem is resolved")

def focus(event):
    widget = window.focus_get()
    print(widget.name)
    try:
        if "score" in widget.name:
            print("score in focus")
        else:
            print("Enter pressed")
    except:
        print("unknown in focus")

window = tk.Tk()
window.title("GameMaster")
window.geometry("600x620")
window.iconbitmap(resource_path("icon.ico"))
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

notebook = Notebook(master=window)
notebook.grid(column=0, row=1, sticky=tk.NSEW)

main_frame = tk.Frame(notebook,padx=0, pady=0)
notebook.add(main_frame, text="Main")
main_frame.rowconfigure(index=0, weight=0)
main_frame.rowconfigure(index=1, weight=1)
main_frame.rowconfigure(index=2, weight=1)
main_frame.columnconfigure(index=0, weight=10)
main_frame.columnconfigure(index=1, weight=0)

settings_frame = tk.Frame(notebook,padx=0, pady=0)
notebook.add(settings_frame, text="Settings",state=DISABLED)

config_frame = tk.Frame(notebook,padx=0, pady=0)
notebook.add(config_frame, text="Config",state=DISABLED)

header = tk.Frame(master=window,width=40, height=10)
header.grid(column=0, row=0, sticky=tk.EW, columnspan=2, rowspan=1, padx=0, pady=0)
canvas = Canvas(master=header,width = 700, height = 96)
canvas.grid(column=0, row=0, columnspan=2, rowspan=2, sticky=tk.NSEW)
img = ImageTk.PhotoImage(Image.open(resource_path("header_alt.png")))  
canvas.create_image(0, 0, anchor=NW, image=img) 

#==================================================#
#              Timing Setup and Content            #
#==================================================#
gmt.timing_setup(main_frame)

#==================================================#
#             Scoring Setup and Content            #
#==================================================#
scoring = tk.Frame(master=main_frame,width=20, height=10, relief=SUNKEN, bd="3")
scoring.grid(row=2, column=0, sticky=NSEW, padx=5, pady=5)

scoring.columnconfigure(index=0, weight=1)
scoring.columnconfigure(index=1, weight=1)
scoring.rowconfigure(index=0, weight=0)
scoring.rowconfigure(index=1, weight=10)
lbl_home = tk.Label(master=scoring,text="Scoring",font=("Arial",18,""))
lbl_home.grid(sticky=EW,row=0,column=0,columnspan=2)

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
    print("adding...")
    teams_scores[target_team] += value
    print(teams_scores)
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
    print(teams_scores)
    score_home.set(str(teams_scores["home"]))
    score_away.set(str(teams_scores["away"]))
    for x in teams_scores:
        with open(str("output/")+str(x)+str("_score.txt"), "w") as f:
            f.write(str(teams_scores[x]))
            f.close()

def nameset(target_team):
    if target_team == "home":
        teams_names[target_team] = ent_homename.get()
        # print(name_home.get())
    elif target_team == "away":
        teams_names[target_team] = ent_awayname.get()
        # print(name_away.get())
    for x in teams_names:
        with open(str("output/")+str(x)+str("_name.txt"), "w") as f:
            f.write(str(teams_names[x]))
            f.close()



score_home.set("0")
homeframe = tk.Frame(master=scoring, bd="3", relief="sunken")
homeframe.grid(row=1, column=0, sticky=NSEW, pady=2, padx=2)
homeframe.columnconfigure(index=0, weight=0, minsize=38)
homeframe.columnconfigure(index=1, weight=1)
homeframe.columnconfigure(index=2, weight=0, minsize=38)
homeframe.rowconfigure(index=0, weight=0)
homeframe.rowconfigure(index=1, weight=1)
homeframe.rowconfigure(index=2, weight=1)
homeframe.rowconfigure(index=2000, weight=100)
lbl_home = tk.Label(master=homeframe,text="Home",font=("Arial",10,""))
lbl_home.grid(sticky=EW,row=0,column=0,columnspan=1)
ent_homename = Entry(master=homeframe, width=2, font=("Arial",12,""),textvariable=name_home)#, justify="center")
ent_homename.grid(row=0,column=1,columnspan=2, sticky=NSEW, pady=2, padx=2)
ent_home = Entry(name="score",master=homeframe, width=4, font=("Arial",26,""),textvariable=score_home, justify="center")
ent_home.grid(sticky=NS, column=1, row=1, pady=5, padx=5)
btn_homeup = Button(master=homeframe, text="+", width=2,command=lambda: scoreadd("home",1))
btn_homeup.grid(column=2, row=1)
btn_homedn = Button(master=homeframe, text="-", width=2,command=lambda: scoreadd("home",-1))
btn_homedn.grid(column=0, row=1)
btn_homeset = Button(master=homeframe, text="Set Score", width=2,command=lambda: scoreset("home"))
btn_homeset.grid(column=0, row=2, columnspan=3, sticky=NSEW, pady=5, padx=5)

score_away.set("0")
awayframe = tk.Frame(master=scoring, bd="3", relief="sunken")
awayframe.grid(row=1, column=1, sticky=NSEW, pady=2, padx=2)
awayframe.columnconfigure(index=0, weight=0, minsize=38)
awayframe.columnconfigure(index=1, weight=1)
awayframe.columnconfigure(index=2, weight=0, minsize=38)
awayframe.rowconfigure(index=0, weight=0)
awayframe.rowconfigure(index=1, weight=1)
awayframe.rowconfigure(index=2, weight=1)
awayframe.rowconfigure(index=2000, weight=100)
lbl_away = tk.Label(master=awayframe,text="Away",font=("Arial",10,""))
lbl_away.grid(sticky=EW,row=0,column=0,columnspan=1)
ent_awayname = Entry(master=awayframe, width=2, font=("Arial",12,""),textvariable=name_away)#, justify="center")
ent_awayname.grid(row=0,column=1,columnspan=2, sticky=NSEW, pady=2,padx=2)
ent_away = Entry(name="score",master=awayframe, width=4, font=("Arial",26,""),textvariable=score_away, justify="center")
ent_away.grid(sticky=NS, column=1, row=1, pady=5, padx=5)
btn_awayup = Button(master=awayframe, text="+", width=2,command=lambda: scoreadd("away",1))
btn_awayup.grid(column=2, row=1)
btn_awaydn = Button(master=awayframe, text="-", width=2,command=lambda: scoreadd("away",-1))
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
# print(scrs_index)
s = {}
# print(scrs)
# Home
for x in scrs:
    homeframe.rowconfigure(index=list(scrs.keys()).index(x)+3, weight=0)
    s["btn_"+x] = Button(master=homeframe, text=str(x), command=lambda x=x: scoreadd("home",int(scrs[x])))
    s["btn_"+x].grid(column=1, row=list(scrs.keys()).index(x)+3, sticky=EW)

for x in scrs:
    awayframe.rowconfigure(index=list(scrs.keys()).index(x)+3, weight=0)
    s["btn_"+x] = Button(master=awayframe, text=str(x), command=lambda x=x: scoreadd("away",int(scrs[x])))
    s["btn_"+x].grid(column=1, row=list(scrs.keys()).index(x)+3, sticky=EW)

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
variables = tk.Frame(master=main_frame,width=20, height=10, bd="3", relief=GROOVE)
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
        # print(str(varname) + " Saved")
        f.close()

lbl_variables = tk.Label(master=variables,text="Other Variables",font=("Arial",18,""),padx=5,justify="center")
lbl_variables.grid(sticky=S,row=0,column=0,columnspan=3)

vars = config["vars"]
v = {}
for x in vars:
    variables.rowconfigure(index=vars.index(x)+1, weight=0)
    v["lbl_"+x] = Label(master=variables, text=x)#, padx=5, pady=5)
    v["ent_"+x] = Entry(master=variables, font=("Arial",12,""),justify="center",width=5) 
    v["ent_"+x].name = x #                                    Fixed \/
    v["btn_"+x] = Button(master=variables, text=str("Set"), width=4,command=lambda x=x: varset(str(x), int(v["ent_"+x].get())))
    v["lbl_"+x].grid(sticky=tk.E, column=0, row=int(vars.index(x)+2))
    v["ent_"+x].grid(sticky=NS, column=1, row=int(vars.index(x)+2))
    v["btn_"+x].grid(sticky=W, column=2, row=int(vars.index(x)+2), columnspan=2, padx=2)
    # print("btn_"+x)

#==================================================#
#            Settings Setup and Content            #
#==================================================#
settings = tk.Frame(master=main_frame,width=20, height=10, relief=GROOVE, bd="3")
settings.grid(row=2, column=1, sticky=NSEW, padx=5, pady=5)

settings.columnconfigure(index=0, weight=0)
settings.columnconfigure(index=1, weight=1)
# settings.columnconfigure(index=2, weight=1)
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
    # print("Config name set: "+str(ent_name.get()))
    config["name"] = ent_name.get()
    gmc.set_config()

def settings_set(setting,value):
    # print(setting,value)
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
lbl_name.grid(column=0, row=1, sticky=tk.NS, padx=1)
ent_name = Entry(master=settings, width=10, font=("Arial",12,""),textvariable=configname)
ent_name.grid(column=1, row=1, sticky=tk.NSEW, padx=5)
ent_name.insert(0, config["name"])
configname.trace("w", lambda name, index, mode: config_name())
# btn_name = Button(master=settings,text="Set", command=config_name,width=4)
# btn_name.grid(column=2, row=1, sticky=tk.NW, padx=5)
btn_find = Button(master=settings,text="Open output files", width=20,command=lambda: os.startfile(str("output\\")))
btn_find.grid(column=0, row=2000, sticky=tk.NS, padx=5, columnspan=2)
btn_reload = Button(master=settings,text="Reload config", width=20, command=gmc.config_reload)
btn_reload.grid(column=0, row=2001, sticky=tk.NS, padx=5, columnspan=2)
btn_choose = Button(master=settings,text="Select config file", width=20,command=gmc.config_choose)
btn_choose.grid(column=0, row=2002, sticky=tk.NS, padx=5, columnspan=2)

if config["version"] > 1:
    st = {}
    stvar = {}
    for x in settings_list:
        settings.rowconfigure(index=list(settings_list.keys()).index(x)+2, weight=1)
        print(x)
        if isinstance(settings_list[x], bool):
            # print("hi")
            stvar["bool_"+x] = tk.BooleanVar()
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

#[================================================]#
#[================================================]#
window.mainloop()


#                                               {----=====+  End of module  +=====----}                                                           #


#                                                            gm_config.py                                                                         #
from ast import Break
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog as fd
import os, os.path, sys
import json
from turtle import update
from gm_resources import resource_path, retrieve_file, download_file, external_link
from gm_setup import setup
from packaging.version import Version, parse
try:
    import pyi_splash
    pyi_splash.update_text('UI Loaded ...')
    pyi_splash.close()
except:
    pass

NAME = "GameMaster"
APP_VERSION = Version("2.1.0b5")
VERSION = 3

print(APP_VERSION)


print("Checking for updates...")
remoteversion = Version(retrieve_file("https://raw.githubusercontent.com/TheLittleDoc/GameMaster/master/version_info/latest.txt", "Newest Version"))
if APP_VERSION > remoteversion:
    prerelease = Version(retrieve_file("https://raw.githubusercontent.com/TheLittleDoc/GameMaster/master/version_info/pre.txt", "Prerelease"))
    if APP_VERSION < prerelease:
        betaupdate = messagebox.askyesno(title='New Version',message='New Version Available!\n\n' + prerelease.public +"\n\nDo you want to update?", icon='info')
        if(betaupdate):
            external_link("https://github.com/TheLittleDoc/GameMaster/releases/tag/v" + prerelease.public)
            os._exit(0)
elif APP_VERSION < remoteversion:
    update = messagebox.askyesno(title='New Version',message='New Version Available!\n\n' + remoteversion.public +"\n\nDo you want to update?", icon='info')
    if(update):
        external_link("https://github.com/TheLittleDoc/GameMaster/releases/latest")
        os._exit(0)
#except:
    #print("Error checking for updates")

def check():
    firstrun = messagebox.askyesno("First run?","Is this your first time running GameMaster?",icon="warning")
    cfgsettings = {"path": "gamemaster.json", "recents": []}
    with open("cfgsettings.json", "w") as f:
        json.dump(cfgsettings, f, indent=4)
        
        f.close()
    with open("cfgsettings.json", "r") as f:
        cfgsettings = json.load(f)
        # print(cfgsettings)
    
    if firstrun:
        setup()
    else:
        None
    os.execv(sys.executable, ["python"] + sys.argv)


print("Loading config...")
source = retrieve_file("https://raw.githubusercontent.com/TheLittleDoc/GameMaster/master/distro_source/"+APP_VERSION.public+".py","Source Code")

print(source)
print(APP_VERSION.public)
if source == "404: Not Found":
    messagebox.showerror("Error","Could not retrieve source. Under a GNU AGPLv3 License, a source must be made available to end users. Please check your connection and try again.")
    os._exit(0) 

try:
    with open("cfgsettings.json", "r") as f:
        cfgsettings = json.load(f)
        # print(cfgsettings)
        filename = cfgsettings["path"]
except:
    check()


with open(filename, "r") as f:
    try:
        config = json.load(f)
        # print(config)

    except:
        ask_error = messagebox.askokcancel("Error while loading config", "GameMaster configuration file misformatted. Continuing will revert to a known-working default configuration.",icon="error")
        if ask_error:
            with open(filename, "w") as f:
                config = {"name": "Football", "version": 2, "unit": "Quarter", "ct": 4, "times": {"hours": 0, "minutes": 12, "seconds": 0}, "scores": {"Touchdown": 6, "Field Goal": 3, "Safety": 2, "Two point": 2, "Extra": 1}, "vars": ["Down", "To Go"], "players": None, "settings": {"hours": False,"minutes": True,"seconds": True,"on top": False, "alarm": True}}
                json.dump(config, f, indent=4)
                f.close()
            os.execv(sys.executable, ["python"] + sys.argv)
        else:
            messagebox.showinfo("Stopping...","GameMaster will now stop running. Please provide a valid configuration file on the next run.")
            exit()
        #raise Exception("Error while loading config %s. A stock config file can be found at https://granbybears.live/gamemaster/fix" % f.name) 
        #None
            
# print(config)

if config["name"] == None:
    check()
else:
    None

# If the config is able to load, only then are these functions defined.
def set_config():
    with open(filename, "w") as f:
        json.dump(config, f, indent=4)
def edit_config(property, value):
    config[property] = value
    print(value)
    set_config()
def config_reload():
    reload_ask = messagebox.askyesno("Reload?","Reloading the config will require restarting GameMaster. This will stop the timer and reset scores and team names. Are you sure you want to continue?",icon="warning")
    if reload_ask:
        os.execv(sys.executable, ["python"] + sys.argv)
    else:
        None
def config_choose():
    filetypes = (('JSON Files', '*.json'), ('All Files', '*.*'))
    choose_ask = messagebox.askyesno("Choose new config?","Choosing a new config will require restarting GameMaster. This will stop the timer and reset scores and team names. Are you sure you want to continue?",icon="warning")
    if choose_ask:
        filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)
        if filename == "":
            filename = cfgsettings["path"]
            messagebox.showinfo(title='Config not changed',message=filename, icon='warning')
        else:
            cfgsettings["recents"].insert(0,cfgsettings["path"])
            cfgsettings["path"] = filename
            messagebox.showinfo(title='Selected File',message=filename)
            if filename in cfgsettings["recents"]:
                cfgsettings["recents"].remove(filename)
            else:
                None
            
            with open("cfgsettings.json", "w") as f:
                json.dump(cfgsettings, f, indent=4)
                
                f.close()
            os.execv(sys.executable, ["python"] + sys.argv)
    else:
        None


if "version" in config:
    versions_tuple = (int(config["version"]),int(VERSION))
else:
    ask_version = messagebox.askokcancel("Unknown version number", "The loaded config doesn't contain a version number, or includes an unknown version value. Continuing will add a valid version number to your configuration file.",icon="warning")
    if ask_version:
        if "settings" in config:
            config["version"] = 2
        if "countup" in config["settings"]:
            config["version"] = 3
        else:
            config["version"] = 1
    else:
        messagebox.showinfo("Stopping...","GameMaster will now stop running. Please provide a valid configuration file on the next run.")
        exit()
    versions_tuple = (int(config["version"]),int(VERSION))

if config["version"] != VERSION:
    messagebox.showinfo("Config version mismatch", "The loaded config is version %i, but GameMaster expected configs of version %i. Proceed with caution." % versions_tuple)
    if config["version"] == 1:
        update_ask = messagebox.askyesno("Outdated config", "The loaded config is version %i, but configs of version 2 and above are required to use settings and stopwatch mode. Would you like to try to update?" % versions_tuple[0])
        if update_ask:
            config["settings"] = {"hours": False,"minutes": True,"seconds": True,"on top": False, "countup": False, "end on time": False, "alarm": True}
            config["version"] = 3
            set_config()
            config_reload()
        elif not update_ask:
            print("skip")
    elif config["version"] == 2:
        update_ask = messagebox.askyesno("Outdated config", "The loaded config is version %i, but configs of version 3 and above are required to use settings and stopwatch mode. Would you like to try to update?" % versions_tuple[0])
        if update_ask:
            config["settings"]["countup"] = False
            config["settings"]["end on time"] = False
            config["version"] = 3
            set_config()
            config_reload()
    elif config["version"] == 3:
        if not "countup" in config["settings"]:
            messagebox.showinfo("Config version mismatch", "The loaded config is version %i, but appears to be malformed or improperly updated. If errors arrise or features are unavailable, it is recommended that you reset to a known-working default configuration." % config["version"])


else:
    settings_list = config["settings"]
#                                                            gm_timing.py                                                                         #
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import os, os.path, sys
import time
import threading
import gm_config as gmc
from gm_resources import resource_path, retrieve_file, f

# uwu

config = gmc.config
try:
    settings_list = gmc.settings_list
except:
    settings_list = {"hours": False,"minutes": True,"seconds": True,"on top": False, "countup": False, "end on time": False, "alarm": True}

def timing_setup(main_frame):
    timing = tk.Frame(master=main_frame,width=12, height=10, bd="3", relief=SUNKEN)
    timing.grid(row=1, column=0, sticky=NSEW, padx=5, pady=5, ipadx=5)

    timing.columnconfigure(index=0, weight=0)
    timing.columnconfigure(index=1, weight=4)
    timing.columnconfigure(index=2, weight=4)
    timing.columnconfigure(index=3, weight=4)
    timing.columnconfigure(index=4, weight=0, minsize=5)
    timing.rowconfigure(index=0, weight=0)
    timing.rowconfigure(index=1, weight=0)
    timing.rowconfigure(index=2, weight=0)
    timing.rowconfigure(index=4, weight=3)
    timing.rowconfigure(index=5, weight=3)
    timing.rowconfigure(index=6, weight=1)

    #[  Timing and sections functions  ]#
    global running
    running = False
    thread_count = 0
    # Declaration of variables
    hour=StringVar()
    minute=StringVar()
    second=StringVar()
    times = config["times"]
    # setting the default value
    hour.set("{0:02d}".format(int(0 if (times["hours"] is None) or (settings_list["countup"] == True) else times["hours"])))
    minute.set("{0:02d}".format(int(0 if (times["minutes"] is None) or (settings_list["countup"] == True) else times["minutes"])))
    second.set("{0:02d}".format(int(0 if (times["seconds"] is None) or (settings_list["countup"]) else times["seconds"])))
    class TimerClass(threading.Thread):
        
        def __init__(self, thread_ID):
            # print("Thread Created")
            threading.Thread.__init__(self)
            # self.name = thread_name
            self.id = thread_ID
            self.event = threading.Event()
            self.count = int(hour.get())*3600 + int(minute.get())*60 + int(second.get())
        def run(self):
            global to_file
            # self.count = int(hour.get())*3600 + int(minute.get())*60 + int(second.get())
            running = True
            # mins,secs = divmod(self.count,60)
            # to_file = str("%02d" % (mins))+str(":")+str("%02d" % (secs))

                # writes to the output file the formatted version of the time
            # with open("output/time.txt", "w") as f:
            #     f.write(to_file)
            #     f.close()
        
            while self.count > -1 and not self.event.is_set():
                print("count")
                # print(self.count)
                # print(running)
                mins,secs = divmod(self.count,60)
        
                # Converting the input entered in mins or secs to hours,
                # mins ,secs(input = 110 min --> 120*60 = 6600 => 1hr :
                # 50min: 0sec)
                hours=0
                if mins >= 60 and settings_list["hours"] == True:
                    
                    # divmod(firstvalue = temp//60, secondvalue
                    # = temp%60)
                    hours, mins = divmod(mins, 60)
                
                
                # using format () method to store the value up to
                # two decimal places
                hour.set("{0:02d}".format(hours))
                minute.set("{0:02d}".format(mins))
                second.set("{0:02d}".format(secs))

                # stores the formatted version of the time
                if settings_list["hours"] == True and settings_list["minutes"] == True and settings_list["seconds"] == True:
                    to_file = str("%02d" % (hours))+str(":")+str("%02d" % (mins))+str(":")+str("%02d" % (secs))
                elif settings_list["hours"] == False and settings_list["minutes"] == True and settings_list["seconds"] == True:
                    to_file = str("%02d" % (mins+(hours*60)))+str(":")+str("%02d" % (secs))
                elif settings_list["hours"] == True and settings_list["minutes"] == True and settings_list["seconds"] == False:
                    to_file = str("%02d" % (hours))+str(":")+str("%02d" % (mins))
                elif settings_list["hours"] == False and settings_list["minutes"] == True and settings_list["seconds"] == False:
                    to_file = str("%02d" % (mins+(hours*60)))
                elif settings_list["hours"] == True and settings_list["minutes"] == False and settings_list["seconds"] == False:
                    to_file = str("%02d" % (hours))
                elif settings_list["hours"] == False and settings_list["minutes"] == False and settings_list["seconds"] == True:
                    to_file = str("%02d" % (secs))
                    

                # writes to the output file the formatted version of the time
                with open("output/time.txt", "w") as f:
                    f.write(to_file)
                    f.close()
        
                # updating the GUI window after decrementing the
                # temp value every time
                # when temp value = 0; then a messagebox pops up
                # with a message:"Time's up"
                if settings_list["countup"]:
                    if (self.count >= int(times["hours"])*3600 + int(times["minutes"])*60 + int(times["seconds"])):
                        # messagebox.showinfo("Time Countdown", "Time's up ") # I will revisit this later, but for now, I'm just removing it entirely.
                        if settings_list["end on time"]:
                            messagebox.showinfo("Time Countdown", "Time's up ")
                            timer_stop()
                    self.count += 1
                else:
                    if (self.count == 0):
                        if settings_list["alarm"] == True:
                            messagebox.showinfo("Time Countdown", "Time's up ")
                            timer_stop()
                        else:
                            None
                    else:
                        self.count -= 1
                
                self.event.wait(1)
                
        def stop(self):
            # print("Stopping...")
            thread_count =+ 1
            # print("Thread count is now %d" % thread_count)
            self.event.set()
            running = False
    th = {}
    def timer(is_running):
        
        running = True
        # print(running)
        th[thread_count] = TimerClass(thread_count)
        btn_timer.configure(text="Stop", command=lambda: timer_stop())
        btn_timer.grid(column=0,columnspan=1, sticky=tk.NS, row=3, rowspan=2, ipadx=0, ipady=2, padx=4)
        th[thread_count].start()

    def timer_stop():
        th[thread_count].stop()
        # print(th)
        btn_timer.configure(text="Start", command=lambda: timer(running))
        btn_timer.grid(column=0,columnspan=1, sticky=tk.NS, row=3, rowspan=2, ipadx=0, ipady=2, padx=4)

    def time_set_default():
        hour.set("{0:02d}".format(int(0 if (times["hours"] is None) or (settings_list["countup"] == True) else times["hours"])))
        minute.set("{0:02d}".format(int(0 if (times["minutes"] is None) or (settings_list["countup"] == True) else times["minutes"])))
        second.set("{0:02d}".format(int(0 if (times["seconds"] is None) or (settings_list["countup"]) else times["seconds"])))
        #[ Here is where the initial output happens! Don't forget to fix this too! ]#
        if settings_list["hours"] == True and settings_list["minutes"] == True and settings_list["seconds"] == True:
            to_file = str("%02d" % (int(0 if (times["hours"] is None) or (settings_list["countup"] == True) else times["hours"])))+str(":")+str("%02d" % (int(0 if (times["minutes"] is None) or (settings_list["countup"] == True) else times["minutes"])))+str(":")+str("%02d" % (int(0 if (times["seconds"] is None) or (settings_list["countup"] == True) else times["seconds"])))
        elif settings_list["hours"] == False and settings_list["minutes"] == True and settings_list["seconds"] == True:
            to_file = str("%02d" % (int(0 if (times["minutes"] is None) or (settings_list["countup"] == True) else times["minutes"])))+str(":")+str("%02d" % (int(0 if (times["seconds"] is None) or (settings_list["countup"] == True) else times["seconds"])))
        elif settings_list["hours"] == True and settings_list["minutes"] == True and settings_list["seconds"] == False:
            to_file = str("%02d" % (int(0 if (times["hours"] is None) or (settings_list["countup"] == True) else times["hours"])))+str(":")+str("%02d" % (int(0 if (times["minutes"] is None) or (settings_list["countup"] == True) else times["minutes"])))
        elif settings_list["hours"] == False and settings_list["minutes"] == True and settings_list["seconds"] == False:
            to_file = str("%02d" % (int(0 if (times["minutes"] is None) or (settings_list["countup"]) else times["minutes"])))
        elif settings_list["hours"] == True and settings_list["minutes"] == False and settings_list["seconds"] == False:
            to_file = str("%02d" % (int(0 if (times["hours"] is None) or (settings_list["countup"]) else times["hours"])))
        elif settings_list["hours"] == False and settings_list["minutes"] == False and settings_list["seconds"] == True:
            to_file = str("%02d" % (int(0 if (times["seconds"] is None) or (settings_list["countup"]) else times["seconds"])))
        elif settings_list["hours"] == False and settings_list["minutes"] == False and settings_list["seconds"] == False:
            to_file=""
        with open("output/time.txt", "w") as f:
            f.write(to_file)
            f.close()
        timer_stop()

    def section_set(type):
        type=type
        with open("output/section.txt", "w") as f:
            if type == 1:
                if(int(section.get()) < int(config["ct"])):
                    # print("section setting")
                    section.set(int(ent_section.get())+1)
                else:
                    None
            else:
                if(int(section.get()) > 1):
                    section.set(int(ent_section.get())-1)
                else:
                    None
            f.write(str(section.get()))
            f.close()

    def time_clear():
        clearing = True # messagebox.askyesno("Clear timer","Are you sure you want to clear the timer? This will set it to 00:00:00, not default. If you wish to set it back to the default time, choose \"no\" and then select \"default\" in GameMaster.")
        if clearing:
            hour.set("{0:02d}".format(0))
            minute.set("{0:02d}".format(0))
            second.set("{0:02d}".format(0))
            if settings_list["hours"] == True and settings_list["minutes"] == True and settings_list["seconds"] == True:
                to_file = str("%02d" % (0))+str(":")+str("%02d" % (0))+str(":")+str("%02d" % (0))
            elif settings_list["hours"] == False and settings_list["minutes"] == True and settings_list["seconds"] == True:
                to_file = str("%02d" % (0))+str(":")+str("%02d" % (0))
            elif settings_list["hours"] == True and settings_list["minutes"] == True and settings_list["seconds"] == False:
                to_file = str("%02d" % (0))+str(":")+str("%02d" % (0))
            elif settings_list["hours"] == False and settings_list["minutes"] == True and settings_list["seconds"] == False:
                to_file = str("%02d" % (0))
            elif settings_list["hours"] == True and settings_list["minutes"] == False and settings_list["seconds"] == False:
                to_file = str("%02d" % (0))
                # print(to_file)
            with open("output/time.txt", "w") as f:
                f.write(to_file)
                f.close()
            timer_stop()
        else:
            None

    lbl_tmr = Label(master=timing,text="Timer",font=("Arial",18,""))
    lbl_tmr.grid(sticky=S,row=0,column=0,columnspan=4)
    hourEntry= Entry(master=timing, width=2, font=("Arial",26,""),textvariable=hour, justify="center")
    hourEntry.grid(sticky=NSEW, column=1, row=1, rowspan=2)
    minuteEntry= Entry(master=timing, width=2, font=("Arial",26,""),textvariable=minute, justify="center")
    minuteEntry.grid(sticky=NSEW, column=2, row=1, rowspan=2)
    secondEntry= Entry(master=timing, width=2, font=("Arial",26,""),textvariable=second, justify="center")
    secondEntry.grid(sticky=NSEW, column=3, row=1, rowspan=2)
    btn_timer = Button(master=timing, text="Start",command=lambda: timer(running))
    btn_timer.grid(column=0,columnspan=1, sticky=tk.NS, row=3, rowspan=2, ipadx=0, ipady=2, padx=4)
    btn_time = Button(master=timing, text="Default",command=lambda: time_set_default())
    btn_time.grid(column=0,columnspan=1, sticky=tk.NE, row=1, ipadx=0, ipady=2, padx=4)
    btn_clear = Button(master=timing, text="Clear",command=lambda: time_clear())
    btn_clear.grid(column=0,columnspan=1, sticky=tk.NE, row=2, ipadx=0, ipady=2, padx=4)
    # hour.set("{0:02d}".format(times["hours"]))
    # minute.set("{0:02d}".format(times["minutes"]))
    # second.set("{0:02d}".format(times["seconds"]))
    if settings_list["hours"] == True and settings_list["minutes"] == True and settings_list["seconds"] == True:
        to_file = str("%02d" % (int(0 if (times["hours"] is None) or (settings_list["countup"] == True) else times["hours"])))+str(":")+str("%02d" % (int(0 if (times["minutes"] is None) or (settings_list["countup"] == True) else times["minutes"])))+str(":")+str("%02d" % (int(0 if (times["seconds"] is None) or (settings_list["countup"] == True) else times["seconds"])))
    elif settings_list["hours"] == False and settings_list["minutes"] == True and settings_list["seconds"] == True:
        to_file = str("%02d" % (int(0 if (times["minutes"] is None) or (settings_list["countup"] == True) else times["minutes"])))+str(":")+str("%02d" % (int(0 if (times["seconds"] is None) or (settings_list["countup"] == True) else times["seconds"])))
    elif settings_list["hours"] == True and settings_list["minutes"] == True and settings_list["seconds"] == False:
        to_file = str("%02d" % (int(0 if (times["hours"] is None) or (settings_list["countup"] == True) else times["hours"])))+str(":")+str("%02d" % (int(0 if (times["minutes"] is None) or (settings_list["countup"] == True) else times["minutes"])))
    elif settings_list["hours"] == False and settings_list["minutes"] == True and settings_list["seconds"] == False:
        to_file = str("%02d" % (int(0 if (times["minutes"] is None) or (settings_list["countup"]) else times["minutes"])))
    elif settings_list["hours"] == True and settings_list["minutes"] == False and settings_list["seconds"] == False:
        to_file = str("%02d" % (int(0 if (times["hours"] is None) or (settings_list["countup"]) else times["hours"])))
    elif settings_list["hours"] == False and settings_list["minutes"] == False and settings_list["seconds"] == True:
        to_file = str("%02d" % (int(0 if (times["seconds"] is None) or (settings_list["countup"]) else times["seconds"])))
    elif settings_list["hours"] == False and settings_list["minutes"] == False and settings_list["seconds"] == False:
        to_file=""
    # print(to_file)
    if not os.path.exists("output"):
        os.makedirs("output")
    with open("output\\time.txt", "w") as f:
        f.write(to_file)
        f.close()

    lbl_section = tk.Label(master=timing,text=config["unit"],font=("Arial",18,""),padx=30)
    lbl_section.grid(sticky=S,row=4,column=1,columnspan=3)
    section=StringVar()
    section.set("1")

    with open("output\\section.txt", "w") as f:
        f.write(section.get())
        f.close()
    ent_section = Entry(master=timing, width=3, font=("Arial",18,""),textvariable=section, justify="center", state="readonly")
    ent_section.grid(sticky=NS, column=2, row=5)
    btn_sectionup = Button(master=timing, text="+", width=2,command=lambda: section_set(1))
    btn_sectionup.grid(column=3, row=5, sticky=W)
    btn_sectiondn = Button(master=timing, text="-", width=2,command=lambda: section_set(0))
    btn_sectiondn.grid(column=1, row=5, sticky=E)

#                                                             gm_about.py                                                                         #
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
import webbrowser
from gm_resources import resource_path, retrieve_file, f

def external_link(link):
    asklink = messagebox.askyesno("Open link", "GameMaster is opening \"%s\" in your default browser.\n\nDo you want to continue?" % link)
    if asklink == True:
        webbrowser.open(link)
    else:
        None



def show_file(name,to_open,more_info):
    if "http" in to_open:
        retrieve_file(to_open, name)
        text = f[name]
    else:
        try:
            file = open(to_open, "r")
        except:
            file = open(resource_path(to_open), "r")
        text = file.read()
        file.close()
    file_window = tk.Toplevel()
    
    file_window.title(name)
    file_window.resizable(True, True)
    file_window.geometry("660x600+610+0")
    file_window.minsize(660,600)
    file_window.iconbitmap(resource_path("icon.ico"))
    file_window.rowconfigure(index=0, weight=0)
    file_window.rowconfigure(index=1, weight=1)
    file_window.columnconfigure(index=0, weight=1)
    file_window.columnconfigure(index=1, weight=0)

    controls_frame = Frame(master=file_window, height=1, relief=RAISED, borderwidth="3")
    controls_frame.grid(row=0, column=0, sticky=NSEW)
    controls_frame.rowconfigure(index=0, weight=0)
    controls_frame.columnconfigure(index=0, weight=0)
    controls_frame.columnconfigure(index=1, weight=1)
    controls_frame.columnconfigure(index=2, weight=0)

    def exit_button():
        file_window.destroy()

    btn_close = Button(master=controls_frame, text="Close", command=lambda: exit_button())
    btn_close.grid(sticky=NSEW, row=0, column=0)

    lbl_file = Label(master=controls_frame,justify=LEFT,text=name, font=("Arial",18,""), padding=3)
    lbl_file.grid(sticky=NW, row=0, column=1)

    if not more_info == "":
        btn_more = Button(master=controls_frame, text="More Info", command=lambda: external_link(more_info))
        btn_more.grid(sticky=NSEW, row=0, column=2)
    else:
        None
    
    frame_txt = Frame(master=file_window, height=1, relief=SUNKEN, borderwidth="3")
    frame_txt.grid(row=1, column=0, sticky=NSEW, padx=5,pady=5)
    frame_txt.rowconfigure(index=0, weight=1)
    frame_txt.columnconfigure(index=0, weight=1)
    frame_txt.columnconfigure(index=1, weight=0)

    txt = Text(master=frame_txt)
    txt.grid(sticky=NSEW, row=0, column=0)

    txt.insert(1.0, text)
    txt["state"] = "disabled"
    
    scroll_file = Scrollbar(master=frame_txt, orient=VERTICAL,command=txt.yview)
    scroll_file.grid(row=0, column=1, sticky=NSEW, rowspan=2)

    txt['yscrollcommand'] = scroll_file.set
    return file_window


def about_setup(notebook):

    about_frame = tk.Frame(notebook,padx=0, pady=0)
    notebook.add(about_frame, text="About")
    about_frame.rowconfigure(index=0, weight=1)
    about_frame.rowconfigure(index=1, weight=1)
    about_frame.columnconfigure(index=0, weight=1)
    about_frame.columnconfigure(index=1, weight=0)


    info = Frame(master=about_frame, height=1, relief=SUNKEN, borderwidth="3")
    info.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)

    info.rowconfigure(index=0, weight=0)
    info.rowconfigure(index=1, weight=1)
    info.columnconfigure(index=0, weight=1)


    lbl_aboutheader = Label(master=info,justify=LEFT, text="About GameMaster", font=("Arial",18,""), padding=3)
    lbl_aboutheader.grid(sticky=W, row=0, column=0)

    lbl_aboutcontent = Label(master=info, wraplength=400,justify=LEFT,text="GameMaster is maintained by TheLittleDoctor for Bears Broadcast Group. Created in 2021, it sought to fill a need for a simple, easy to use scoreboard and timing app for use with Open Broadcast Software as sporting events all over the world needed to be broadcasted and livestreamed.\n\nGameMaster is open source under the GNU AGPLv3 license, which states that permissions of this license are conditioned on making the complete source code of licensed works available, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors to GameMaster provide an express grant of patent rights. When a modified version is used to provide a service over a network, the complete source code of the modified version must be made available.", font=("Arial",9,""),padding=3)
    lbl_aboutcontent.grid(sticky=NW, row=1, column=0)

    table = tk.Frame(master=about_frame, height=1, relief=SUNKEN, bd="3")
    table.grid(row=1, column=0, sticky=NSEW, padx=5, pady=5)
    table.rowconfigure(index=0, weight=0, minsize=20)
    table.rowconfigure(index=1, weight=0, minsize=20)
    table.rowconfigure(index=2, weight=0, minsize=20)
    table.rowconfigure(index=3, weight=0, minsize=20)
    table.rowconfigure(index=4, weight=0, minsize=5)
    table.rowconfigure(index=5, weight=0, minsize=20)
    table.rowconfigure(index=6, weight=0, minsize=20)
    table.columnconfigure(index=0, weight=0)
    table.columnconfigure(index=1, weight=1)

    lbl_tableheader = tk.Label(master=table,justify=LEFT, text="Resources", font=("Arial",18,""), padx=5)
    lbl_tableheader.grid(sticky=W, row=0, column=0, columnspan=3)

    btn_latest = Button(master=table, text="Latest Version", command=lambda: external_link("https://github.com/TheLittleDoc/GameMaster/releases/latest"))
    btn_latest.grid(sticky=NSEW, row=1, column=0)
    lbl_latest = Label(master=table,justify=LEFT, text="https://github.com/TheLittleDoc/GameMaster/releases/latest", font=("Arial",10,""), relief=SUNKEN, padding=5)
    lbl_latest.grid(sticky=NSEW, row=1, column=1)

    btn_wiki = Button(master=table, text="Wiki", command=lambda: external_link("https://github.com/TheLittleDoc/GameMaster/wiki"))
    btn_wiki.grid(sticky=NSEW, row=2, column=0)
    lbl_wiki = Label(master=table,anchor=W,justify=LEFT, text="https://github.com/TheLittleDoc/GameMaster/wiki", font=("Arial",10,""), relief=SUNKEN, padding=5)
    lbl_wiki.grid(sticky=NSEW, row=2, column=1)

    btn_issues = Button(master=table, text="Issues", command=lambda: external_link("https://github.com/TheLittleDoc/GameMaster/issues"))
    btn_issues.grid(sticky=NSEW, row=3, column=0)
    lbl_issues = Label(master=table,anchor=W,justify=LEFT, text="https://github.com/TheLittleDoc/GameMaster/issues", font=("Arial",10,""), relief=SUNKEN, padding=5)
    lbl_issues.grid(sticky=NSEW, row=3, column=1)



    btn_source = Button(master=table, text="Source", command=lambda: show_file("GameMaster Source","https://raw.githubusercontent.com/TheLittleDoc/GameMaster/master/distro_source/"+gmc.APP_VERSION.public+".py","")) # fix ! ! 
    btn_source.grid(sticky=NSEW, row=5, column=0)
    lbl_source = Label(master=table,anchor=W,justify=LEFT, text="Included copy of source. Opens internally.", font=("Arial",10,""), relief=SUNKEN, padding=5)
    lbl_source.grid(sticky=NSEW, row=5, column=1)

    btn_license = Button(master=table, text="License", command=lambda: show_file("GNU AGPLv3","LICENSE","https://www.gnu.org/licenses/agpl-3.0.en.html"))
    btn_license.grid(sticky=NSEW, row=6, column=0)
    lbl_license = Label(master=table,anchor=W,justify=LEFT, text="Included copy of GNU AGPLv3. Opens internally.", font=("Arial",10,""), relief=SUNKEN, padding=5)
    lbl_license.grid(sticky=NSEW, row=6, column=1)

    links = tk.Frame(master=about_frame, height=1, relief=GROOVE, bd="3")
    links.grid(row=0, column=1, sticky=NSEW, padx=5, pady=5,rowspan=2)
    links.rowconfigure(index=0, weight=0)
    links.rowconfigure(index=1, weight=0)
    links.rowconfigure(index=2, weight=0)
    links.rowconfigure(index=3, weight=0)
    links.rowconfigure(index=7, weight=1)
    links.columnconfigure(index=0, weight=1)

    lbl_links = tk.Label(master=links,text="Links", font=("Arial",18,""), padx=5)
    lbl_links.grid(sticky=W, row=0, column=0, columnspan=2)

    doc = tk.Frame(master=links, height=1, relief=RAISED, bd="2")
    doc.rowconfigure(index=0, weight=0)
    doc.rowconfigure(index=1, weight=0)
    doc.columnconfigure(index=0, weight=1)
    doc.grid(row=1, column=0, sticky=NSEW, padx=5, pady=2.5)
    img_doc = Image.open(resource_path("doc.png"))
    img_doc = img_doc.resize((int(96*1.3),int(72*1.3)), Image.ANTIALIAS)
    img_doc = ImageTk.PhotoImage(img_doc)
    lbl_doc = Label(master=doc, image=img_doc)
    lbl_doc.image = img_doc
    lbl_doc.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)
    btn_doc = Button(master=doc,text="Website", command=lambda: external_link("https://datastream.cf/"))
    btn_doc.grid(row=1, column=0, sticky=NSEW, padx=5, pady=5)

    datastream = tk.Frame(master=links, height=1, relief=RAISED, bd="2")
    datastream.rowconfigure(index=0, weight=0)
    datastream.rowconfigure(index=1, weight=0)
    datastream.columnconfigure(index=0, weight=10)
    datastream.columnconfigure(index=1, weight=1)
    datastream.columnconfigure(index=2, weight=10)
    datastream.grid(row=2, column=0, sticky=NSEW, padx=5, pady=2.5)
    img_discord = Image.open(resource_path("discord.png"))
    img_discord = img_discord.resize((int(72),int(72)), Image.ANTIALIAS)
    img_discord = ImageTk.PhotoImage(img_discord)
    lbl_datastream = Label(master=datastream, image=img_discord, width=72, justify=CENTER)
    lbl_datastream.image = img_discord
    lbl_datastream.grid(row=0, column=1, sticky=NSEW, padx=5, pady=5)
    btn_datastream = Button(master=datastream,text="Discord Server", command=lambda: external_link("https://discord.gg/WzA4FncR8f/"))
    btn_datastream.grid(row=1, column=0, sticky=NSEW, padx=5, pady=5, columnspan=3)

    github = tk.Frame(master=links, height=1, relief=RAISED, bd="2")
    github.rowconfigure(index=0, weight=0)
    github.rowconfigure(index=1, weight=0)
    github.columnconfigure(index=0, weight=10)
    github.columnconfigure(index=1, weight=1)
    github.columnconfigure(index=2, weight=10)
    github.grid(row=3, column=0, sticky=NSEW, padx=5, pady=2.5)
    img_github = Image.open(resource_path("github.png"))
    img_github = img_github.resize((int(72),int(72)), Image.ANTIALIAS)
    img_github = ImageTk.PhotoImage(img_github)
    lbl_github = Label(master=github, image=img_github, width=72, justify=CENTER)
    lbl_github.image = img_github
    lbl_github.grid(row=0, column=1, sticky=NSEW, padx=5, pady=5)
    btn_github = Button(master=github,text="GitHub Repo", command=lambda: external_link("https://github.com/TheLittleDoc/GameMaster/"))
    btn_github.grid(row=1, column=0, sticky=NSEW, padx=5, pady=5, columnspan=3)
#                                                           gm_resources.py                                                                       #
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
        

#                                                             gm_setup.py                                                                         #
import tkinter as tk
from tkinter import *  
from PIL import ImageTk,Image  
from tkinter.ttk import *
from tkinter import messagebox
import os, os.path, sys
import json
import types
import gm_config as gmc
from gm_about import show_file
import webbrowser
from pyshortcuts import make_shortcut
from gm_resources import resource_path, retrieve_file, download_file



# global frame_sportsetup
current = 0
frames_function = {}
config = config = {"name": None, "version": 3, "unit": None, "ct": None, "times": {"hours": None, "minutes": None, "seconds": None}, "scores": {}, "vars": [], "players": None, "settings": {"hours": False,"minutes": True,"seconds": True,"on top": False,"countup": False, "end on time": False, "alarm": True}}

# make_shortcut(os.path.abspath(os.getcwd())+'\gamemaster.exe', name='GameMaster', icon=resource_path('icon.ico'))

def setup():
    frames_setup = {}
    APP_VERSION = gmc.APP_VERSION
    VERSION = gmc.VERSION

    window_setup = tk.Tk()
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

    def retrieve_preset():
        if not cb_sportselect.get() == "Custom":
            download_file("https://raw.githubusercontent.com/TheLittleDoc/GameMaster/master/examples/"+str(VERSION)+"/"+cb_sportselect.get().lower()+".json",cb_sportselect.get().lower()+".json")
            with open("cfgsettings.json", "r") as f:
                cfgsettings = json.load(f)
                # print(cfgsettings)
            with open("cfgsettings.json", "w") as f:
                cfgsettings["path"] = cb_sportselect.get().lower()+".json"
                json.dump(cfgsettings, f, indent=4)
                f.close()
            show_file("gamemaster.json", cfgsettings['path'], "")
        else:
            if not times["hours"] == 0 or not times["minutes"] == 0 or not times["seconds"] == 0:
                btn_setupfw['state'] = "normal"
            else:
                btn_setupfw["state"] = "disabled"

    def scale_window(x,y):
        window_setup.geometry("{}x{}".format(x, y))

    frames_function[0] = lambda: None
    frames_function[1] = lambda: None
    frames_function[2] = lambda: retrieve_preset()
    frames_function[3] = lambda: None# scale_window(600,600)
    frames_function[4] = lambda: scores_set()
    frames_function[5] = lambda: None
    frames_function[6] = lambda: None

    def next_frame():
        global current
        global frames_function
        frames_setup[current].grid_forget()
        frames_function[current]()
        # print(cb_sportselect.get())
        if cb_sportselect.get() == "":
            # print("none")
            if current+1 == 2:
                # print(2)
                btn_setupfw['state'] = "disabled"
                current += 1
            else:
                btn_setupfw['state'] = "normal"
                current += 1
        else:
            if current == 2:
                if cb_sportselect.get() == "Football" or cb_sportselect.get() == "Basketball" or cb_sportselect.get() == "Soccer" or cb_sportselect.get() == "Foomball":
                    current = len(frames_setup)-2
                else:
                    current += 1
            else:
                current += 1
        # print("continue")
        bar['value'] = current*100/(len(frames_setup)-1)
        # print("continue")
        frames_setup[current].grid(row=1, column=0,columnspan=3, sticky=NSEW, padx=10, pady=10)
        if current == 0:
            btn_setupbw['state'] = "disabled"
        else:
            btn_setupbw['state'] = "normal"
        if current == len(frames_setup)-1:
            btn_setupbw['state'] = "disabled"
            btn_setupfw['text'] = "Finish"
            btn_setupfw['command'] = lambda: os.execv(sys.executable, ["python"] + sys.argv)
        else:
            btn_setupfw['text'] = "Next"
            btn_setupfw['command'] = lambda: next_frame()
        if not current == 4:
            scale_window(600,400)
        else:
            scale_window(600,600)

    def prev_frame():
        global current
        try:
            frames_setup[current].grid_forget()
        except:
            None
        if cb_sportselect.get() == "":
            # print("none")
            if current+1 == 2:
                # print(2)
                btn_setupfw['state'] = "normal"
                current -= 1
            else:
                btn_setupfw['state'] = "normal"
                current -= 1
        else:
            if current == 5:
                if cb_sportselect.get() == "Football" or cb_sportselect.get() == "Basketball" or cb_sportselect.get() == "Soccer":
                    current = 2
                else:
                    current -= 1
            else:
                current -= 1
        bar['value'] = current*100/(len(frames_setup)-1)
        frames_setup[current].grid(row=1, column=0,columnspan=3, sticky=NSEW, padx=10, pady=10)
        if current == 0:
            btn_setupbw['state'] = "disabled"
        else:
            btn_setupbw['state'] = "normal"
        if current == len(frames_setup)-1:
            btn_setupbw['state'] = "disabled"
            btn_setupfw['text'] = "Finish"
            btn_setupfw['command'] = lambda: os.execv(sys.executable, ["python"] + sys.argv)
        else:
            btn_setupfw['text'] = "Next"
            btn_setupfw['command'] = lambda: next_frame()
        if not current == 4:
            scale_window(600,400)
        else:
            scale_window(600,600)

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
    frames_setup[0].grid(column=0, row=1, sticky=tk.NSEW, columnspan=3, rowspan=1, padx=10, pady=10)
    frames_setup[0].rowconfigure(index=0, weight=0)
    frames_setup[0].rowconfigure(index=1, weight=1)
    frames_setup[0].columnconfigure(index=0, weight=1)

    lbl_setup = Label(master=frames_setup[0], text="Welcome to GameMaster!", font=("Arial", 18))
    lbl_setup.grid(column=0, row=0, sticky=tk.NSEW)
    lbl_intro = Label(master=frames_setup[0], wraplength=560, justify=LEFT, text="Let’s get you started. In this setup dialog, we’ll walk you through the basics of setting up and using GameMaster, as well as delving into the setup involved with displaying your values inside of OBS. \n\nGameMaster is constantly being updated and maintained by Bears Broadcast Group with help from TheLittleDoctor. Feel free to contact us through any of the channels in the “About” tab following setup.", font=("Arial", 10))
    lbl_intro.grid(column=0, row=1, sticky=tk.NW)

    frames_setup[1] = Frame(master=window_setup,width=40, height=10, relief=GROOVE, borderwidth=5)
    frames_setup[1].rowconfigure(index=0, weight=0)
    frames_setup[1].rowconfigure(index=1, weight=1)
    frames_setup[1].columnconfigure(index=0, weight=1)

    lbl_configsetup = Label(master=frames_setup[1], text="Config Setup", font=("Arial", 18))
    lbl_configsetup.grid(column=0, row=0, sticky=tk.NSEW)
    lbl_configsetup_intro = Label(master=frames_setup[1], wraplength=560, justify=LEFT, text="One of GameMaster's unique features is the ability to change the sport it can score, which includes preset score values, default period durations, and how many periods can be played.\n\nIn theses next few pages, we will set up your GameMaster configuration to be ready to score the sport you need.", font=("Arial", 10))
    lbl_configsetup_intro.grid(column=0, row=1, sticky=tk.NW)

    frames_setup[2] = Frame(master=window_setup,width=40, height=10, relief=GROOVE, borderwidth=5)
    frames_setup[2].rowconfigure(index=0, weight=0)
    frames_setup[2].rowconfigure(index=1, weight=0)
    frames_setup[2].rowconfigure(index=2, weight=0)
    frames_setup[2].columnconfigure(index=0, weight=0)
    frames_setup[2].columnconfigure(index=1, weight=0)
    frames_setup[2].columnconfigure(index=2, weight=1)

    lbl_configsetup_ = Label(master=frames_setup[2], text="Config Setup", font=("Arial", 18))
    lbl_configsetup_.grid(column=0, row=0, sticky=tk.NSEW,columnspan=3)
    lbl_sportselect = Label(master=frames_setup[2], text="Select sport: ", font=("Arial", 12))
    lbl_sportselect.grid(column=0, row=1, sticky=tk.NSEW, pady=15)
    cb_sportselect = Combobox(frames_setup[2], state="readonly", values=("Custom", "Soccer", "Football", "Basketball", "Foomball"),width=15)
    lbl_sportname = Label(frames_setup[2], text="Sport name: ", font=("Arial", 12))
    sportname = StringVar()
    sportname.trace("w", lambda name, index,mode: edit_config("name", str(sportname.get())))
    ent_sportname = Entry(frames_setup[2], textvariable=sportname, width=15)
    lbl_namehelp = Label(frames_setup[2], wraplength=560, justify=LEFT, text="Name of your sport. Ex: Football, Soccer, Basketball", font=("Arial", 10))
    unit = StringVar()
    unit.trace("w", lambda name, index,mode: edit_config("unit", str(unit.get())))
    lbl_unit = Label(frames_setup[2], text="Sections: ", font=("Arial", 12))
    ent_unit = Entry(frames_setup[2], textvariable=unit, width=15)
    lbl_unithelp = Label(frames_setup[2], wraplength=560, justify=LEFT, text="What the time is broken into. Ex: Quarter, Half, Period", font=("Arial", 10))
    lbl_periods = Label(frames_setup[2], text="# of sections: ", font=("Arial", 12))
    periods = IntVar()
    periods.trace("w", lambda name, index,mode: edit_config("ct", str(periods.get())))
    
    ent_periods = Entry(frames_setup[2], textvariable=periods, width=15)
    def set_config():
        # print(config)
        with open("gamemaster.json", "w") as f:
            json.dump(config, f, indent=4)
    def edit_config(property, value):
        config[property] = value
        # print(config[property])
        set_config()

    def sportselect(*args):
        # print(cb_sportselect.get())
        
        btn_setupfw['state'] = "normal"
        global sport
        sport = cb_sportselect.get()
        # print(sport)
        if sport == "Custom":
            # print("custom uwu")
            lbl_sportname.grid(column=0, row=2, sticky=tk.NSEW, pady=5)
            
            ent_sportname.grid(column=1, row=2, sticky=tk.NSEW, pady=5)
            lbl_namehelp.grid(column=2, row=2, sticky=tk.NSEW, pady=5,padx=5)
            lbl_unit.grid(column=0, row=3, sticky=tk.NSEW, pady=5)
            ent_unit.grid(column=1, row=3, sticky=tk.NSEW, pady=5)
            lbl_unithelp.grid(column=2, row=3, sticky=tk.NW, pady=5, padx=5)
            lbl_periods.grid(column=0, row=4, sticky=tk.NSEW, pady=5)
            ent_periods.grid(column=1, row=4, sticky=tk.NSEW, pady=5)
            # frame_sportsetup.grid_forget()
        elif sport == "Football" or sport == "Soccer" or sport == "Basketball" or sport == "Foomball":
            # print("not custom")
            lbl_sportname.grid_forget()
            ent_sportname.grid_forget()
            lbl_namehelp.grid_forget()
            lbl_unit.grid_forget()
            ent_unit.grid_forget()
            lbl_unithelp.grid_forget()
            lbl_periods.grid_forget()
            ent_periods.grid_forget()

    cb_sportselect.bind("<<ComboboxSelected>>", sportselect)
    cb_sportselect.grid(column=1, row=1, sticky=tk.NSEW,pady=15)

    frames_setup[3] = Frame(master=window_setup,width=40, height=10, relief=GROOVE, borderwidth=5)
    frames_setup[3].rowconfigure(index=0, weight=0)
    frames_setup[3].rowconfigure(index=1, weight=0)
    frames_setup[3].rowconfigure(index=2, weight=1)
    frames_setup[3].rowconfigure(index=3, weight=0)
    frames_setup[3].rowconfigure(index=4, weight=1)
    frames_setup[3].columnconfigure(index=0, weight=1)
    frames_setup[3].columnconfigure(index=1, weight=3)
    frames_setup[3].columnconfigure(index=2, weight=1)

    lbl_timing = Label(master=frames_setup[3], text="Timing Setup", font=("Arial", 18))
    lbl_timing.grid(column=0, row=0, sticky=tk.NSEW,columnspan=3)
    lbl_timingex = Label(master=frames_setup[3], wraplength=560, justify=LEFT, text="Below is an example of our timing tool. Fill in the default section length in format HH:MM:SS.", font=("Arial", 10))
    lbl_timingex.grid(column=0, row=1, sticky=tk.NW,columnspan=3)

    timing_setup = Frame(master=frames_setup[3],width=40, height=10, relief=GROOVE, borderwidth=10)
    timing_setup.grid(row=3, column=1, sticky=NSEW, padx=5, pady=5, ipadx=5)
    timing_setup.columnconfigure(index=0, weight=0)
    timing_setup.columnconfigure(index=1, weight=4)
    timing_setup.columnconfigure(index=2, weight=4)
    timing_setup.columnconfigure(index=3, weight=4)
    timing_setup.columnconfigure(index=4, weight=0, minsize=5)
    timing_setup.rowconfigure(index=0, weight=0)
    timing_setup.rowconfigure(index=1, weight=0)
    timing_setup.rowconfigure(index=2, weight=0)
    timing_setup.rowconfigure(index=4, weight=3)
    timing_setup.rowconfigure(index=5, weight=3)
    timing_setup.rowconfigure(index=6, weight=1)
    
    def time_set(var, place, value):
        times[place] = int(value)
        edit_config("times", times)
        if not times["hours"] == None and not times["minutes"] == None and not times["seconds"] == None:
            btn_setupfw['state'] = "normal"
        else:
            None
            # btn_setupfw['state'] = "disabled"        

    def format(var):
        var.set("{0:02d}".format(var.get()))

    times = {
        "hours": None,
        "minutes": None,
        "seconds": None
    }
    hour=IntVar()
    hour.trace("w", lambda place, value, function: time_set(hour, "hours", hour.get()))
    minute=IntVar()
    minute.trace("w", lambda place, value, function: time_set(minute, "minutes", minute.get()))
    second=IntVar()
    second.trace("w", lambda place, value, function: time_set(second,"seconds", second.get()))
    hour.set("{0:02d}".format(int(0)))
    minute.set("{0:02d}".format(int(0)))
    second.set("{0:02d}".format(int(0)))
    lbl_tmr = tk.Label(master=timing_setup,text="Timer",font=("Arial",18,""),padx=30)
    lbl_tmr.grid(sticky=S,row=0,column=0,columnspan=4)
    hourEntry= Entry(master=timing_setup, width=2, font=("Arial",26,""),textvariable=hour, justify="center")
    hourEntry.bind("<FocusIn>", lambda event: hour.set(""))
    hourEntry.bind("<FocusOut>", lambda event: format(hour))
    hourEntry.grid(sticky=NSEW, column=1, row=1, rowspan=2)
    minuteEntry= Entry(master=timing_setup, width=2, font=("Arial",26,""),textvariable=minute, justify="center")
    minuteEntry.bind("<FocusIn>", lambda event: minute.set(""))
    minuteEntry.bind("<FocusOut>", lambda event: format(minute))
    minuteEntry.grid(sticky=NSEW, column=2, row=1, rowspan=2)
    secondEntry= Entry(master=timing_setup, width=2, font=("Arial",26,""),textvariable=second, justify="center")
    secondEntry.bind("<FocusIn>", lambda event: second.set(""))
    secondEntry.bind("<FocusOut>", lambda event: format(second))
    secondEntry.grid(sticky=NSEW, column=3, row=1, rowspan=2)
    btn_timer = Button(master=timing_setup, text="Start", state="disabled",command=lambda: None)
    btn_timer.grid(column=0,columnspan=1, sticky=tk.NS, row=3,rowspan=2, ipadx=0, ipady=2, padx=4)
    btn_time = Button(master=timing_setup, text="Default", state="disabled",command=lambda: None)
    btn_time.grid(column=0,columnspan=1, sticky=tk.NE, row=1, ipadx=0, ipady=2, padx=4)
    btn_clear = Button(master=timing_setup, text="Clear", state="disabled",command=lambda: None)
    btn_clear.grid(column=0,columnspan=1, sticky=tk.NE, row=2, ipadx=0, ipady=2, padx=4)


    frames_setup[4] = Frame(master=window_setup,width=40, height=10, relief=GROOVE, borderwidth=5)
    frames_setup[4].rowconfigure(index=0, weight=0)
    frames_setup[4].rowconfigure(index=1, weight=0)
    frames_setup[4].rowconfigure(index=2, weight=0)
    frames_setup[4].rowconfigure(index=3, weight=0)
    frames_setup[4].columnconfigure(index=0, weight=1)
    frames_setup[4].columnconfigure(index=1, weight=4)
    frames_setup[4].columnconfigure(index=2, weight=1)
    frames_setup[4].columnconfigure(index=3, weight=3)
    frames_setup[4].columnconfigure(index=4, weight=1)

    lbl_scoring = Label(master=frames_setup[4], text="Config Setup", font=("Arial", 18))
    lbl_scoring.grid(column=0, row=0, sticky=tk.NSEW,columnspan=5)
    lbl_scoringex = Label(master=frames_setup[4], wraplength=560, justify=LEFT, text="Add score value presets and other numerical variables you would want to display alongside your scoreboard.", font=("Arial", 10))
    lbl_scoringex.grid(column=0, row=1, sticky=tk.NW,columnspan=5)

    score_frame = Frame(master=frames_setup[4],width=40, height=10, relief=GROOVE, borderwidth=5)
    score_frame.grid(row=2, column=1, sticky=NSEW, padx=5, pady=5, ipadx=5)
    score_frame.columnconfigure(index=0, weight=0, minsize=5)
    score_frame.columnconfigure(index=1, weight=5)
    score_frame.columnconfigure(index=2, weight=0, minsize=5)
    score_frame.columnconfigure(index=3, weight=1)
    score_frame.columnconfigure(index=4, weight=0)
    score_frame.columnconfigure(index=5, weight=0, minsize=5)
    score_frame.rowconfigure(index=0, weight=0)
    score_frame.rowconfigure(index=1, weight=0)
    score_frame.rowconfigure(index=2, weight=0)

    lbl_score = Label(master=score_frame,text="Score",font=("Arial",14,""))
    lbl_score.grid(sticky=S,row=0,column=0,columnspan=6)
    lbl_scorename = Label(master=score_frame,text="Name",font=("Arial",12,""))
    lbl_scorename.grid(sticky=S,row=1,column=1)
    lbl_scorevalue = Label(master=score_frame,text="Pts",font=("Arial",12,""))
    lbl_scorevalue.grid(sticky=S,row=1,column=3)
    
    
    scoring = []
    scores = {}
    
    def scores_set():
        for i in scoring:
            # print(i)
            if i is not None and ((i[2].get() is not '') or (i[0].get() is not '')):
                scores[i[0].get()] = int(i[2].get())
            else:
                None
        edit_config("scores",scores)
        var_set()

    def score_remove(index):
        for i in scoring[index]:
            i.destroy()

        scoring[index] = None
        # print(scoring)
    
    def score_create():
        score_frame.rowconfigure(index=len(scoring)+2, weight=0)
        x = len(scoring)
        scoring.append([Entry(master=score_frame, width=2, font=("Arial",10,""), justify="left"),Label(master=score_frame), Entry(master=score_frame, width=4, font=("Arial",10,""), justify=CENTER), Button(master=score_frame, width=3,text="-", command=lambda x=x: score_remove(x))])
        # print("right here!")
        # print(type(scoring[x][0]))
        btn_score_add.grid_forget()
        btn_score_add.grid(column=1,columnspan=4, sticky=NSEW, row=len(scoring)+2,pady=5)
        for i in scoring[-1]:
            i.grid(sticky=EW, column=scoring[-1].index(i)+1, row=len(scoring)+1)
    
    btn_score_add = Button(master=score_frame, text="+", command=lambda: score_create())
    btn_score_add.grid(column=1,columnspan=4, sticky=tk.NSEW, row=2,pady=5)


    var_frame = Frame(master=frames_setup[4],width=40, height=10, relief=GROOVE, borderwidth=5)
    var_frame.grid(row=2, column=3, sticky=NSEW, padx=5, pady=5, ipadx=5)
    var_frame.columnconfigure(index=0, weight=0, minsize=5)
    var_frame.columnconfigure(index=1, weight=5)
    var_frame.columnconfigure(index=2, weight=0)
    var_frame.columnconfigure(index=3, weight=0)
    var_frame.columnconfigure(index=4, weight=0, minsize=5)

    lbl_var = Label(master=var_frame,text="Variable",font=("Arial",14,""))
    lbl_var.grid(sticky=S,row=0,column=0,columnspan=5)
    lbl_varname = Label(master=var_frame,text="Name",font=("Arial",12,""))
    lbl_varname.grid(sticky=S,row=1,column=1)

    var = []
    vars = []

    def var_set():
        for i in var:
            if i is not None and i[0].get() is not '':
                vars.append(i[0].get())
            else:
                None
        edit_config("vars",vars)
        with open("cfgsettings.json", "r") as f:
                cfgsettings = json.load(f)
        # print(cfgsettings['path'])
        
        show_file("gamemaster.json", cfgsettings['path'], "")
    
    def var_remove(index):
        for i in var[index]:
            i.destroy()

        var[index] = None
        # print(var)
    
    def var_create():
        var_frame.rowconfigure(index=len(var)+2, weight=0)
        global var_x
        x = len(var)
        var.append([Entry(master=var_frame, width=15, font=("Arial",10,""), justify="left"),Label(master=var_frame), Button(master=var_frame, width=3,text="-", command=lambda x=x: var_remove(x))])
        # print("right here!")
        # print(type(var[x][0]))
        for i in var[-1]:
            # print(i)
            # print("column: "+str((var[-1].index(i)+1)))
            # print("row: "+str((len(var)+1)))
            i.grid(sticky=EW, column=var[-1].index(i)+1, row=len(var)+1)
        btn_var_add.grid_forget()
        btn_var_add.grid(column=1,columnspan=4, sticky=NSEW, row=len(var)+2,pady=5)

    btn_var_add = Button(master=var_frame, text="+", command=lambda: var_create())
    btn_var_add.grid(column=1,columnspan=3, sticky=tk.NSEW, row=2,pady=5)

    var_create()
    score_create()

    frames_setup[5] = Frame(master=window_setup,width=40, height=10, relief=GROOVE, borderwidth=5)
    frames_setup[5].rowconfigure(index=0, weight=0)
    frames_setup[5].rowconfigure(index=1, weight=0)
    frames_setup[5].rowconfigure(index=2, weight=0)
    frames_setup[5].columnconfigure(index=0, weight=0)
    frames_setup[5].columnconfigure(index=1, weight=0)
    frames_setup[5].columnconfigure(index=2, weight=1)

    lbl_review = Label(master=frames_setup[5], text="Review config", font=("Arial", 18))
    lbl_review.grid(column=0, row=0, sticky=tk.NSEW,columnspan=3)
    lbl_reviewtext = Label(master=frames_setup[5], text="Please review the textual form of the config now. It will open in about 3 seconds.\nOnce you proceed, you will not be able to edit your config until you re-run the setup tool or unless you edit it textually. Please review it carefully and use the 'Back' button to return and fix any mistakes you find.\n\nNOTE: The 'players' field will not be populated in this version.", font=("Arial", 10), wraplength=560)
    lbl_reviewtext.grid(column=0, row=1, sticky=tk.NSEW,columnspan=3)

    frames_setup[6] = Frame(master=window_setup,width=40, height=10, relief=GROOVE, borderwidth=5)
    frames_setup[6].rowconfigure(index=0, weight=0)
    frames_setup[6].rowconfigure(index=1, weight=0)
    frames_setup[6].rowconfigure(index=2, weight=0)
    frames_setup[6].columnconfigure(index=0, weight=0)
    frames_setup[6].columnconfigure(index=1, weight=0)
    frames_setup[6].columnconfigure(index=2, weight=1)

    lbl_finish = Label(master=frames_setup[6], text="Setup Completed", font=("Arial", 18))
    lbl_finish.grid(column=0, row=0, sticky=tk.NSEW,columnspan=3)
    lbl_closingremarks = Label(master=frames_setup[6], wraplength=560, justify=LEFT, text="Thank you for choosing GameMaster!\n\n", font=("Arial", 10))
    lbl_closingremarks.grid(column=0, row=1, sticky=tk.NW)

    window_setup.mainloop()