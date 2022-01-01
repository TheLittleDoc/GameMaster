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
config = config = {"name": None, "version": 2, "unit": None, "ct": None, "times": {"hours": None, "minutes": None, "seconds": None}, "scores": {}, "vars": [], "players": None, "settings": {"hours": False,"minutes": True,"seconds": True,"on top": False, "alarm": True}}

# make_shortcut(os.path.abspath(os.getcwd())+'\gamemaster.exe', name='GameMaster', icon=resource_path('icon.ico'))

def setup():
    frames_setup = {}
    

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
            download_file("https://raw.githubusercontent.com/TheLittleDoc/GameMaster/master/examples/"+cb_sportselect.get().lower()+".json",cb_sportselect.get().lower()+".json")
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
                if cb_sportselect.get() == "Football" or cb_sportselect.get() == "Basketball" or cb_sportselect.get() == "Soccer":
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
    cb_sportselect = Combobox(frames_setup[2], state="readonly", values=("Custom", "Soccer", "Football", "Basketball"),width=15)
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
        elif sport == "Football" or sport == "Soccer" or sport == "Basketball":
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
    score_frame.rowconfigure(index=0, weight=1)
    score_frame.rowconfigure(index=1, weight=0)
    score_frame.rowconfigure(index=2, weight=0)
    score_frame.rowconfigure(index=20, weight=100)

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