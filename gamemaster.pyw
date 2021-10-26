import tkinter as tk
import os, os.path, sys
import json
import time
import threading
from tkinter import *
from tkinter import messagebox

VERSION = 2

with open('gamemaster.json', 'r') as f:
    try:
        config = json.load(f)
        print(config)

    except:
        ask_error = messagebox.askokcancel("Error while loading config", "GameMaster configuration file misformatted. Continuing will revert to a known-working default configuration.",icon='error')
        if ask_error:
            with open('gamemaster.json', 'w') as f:
                config = {'name': 'Football', 'version': 1, 'unit': 'Quarter', 'ct': 4, 'times': {'hours': 0, 'minutes': 12, 'seconds': 0}, 'scores': {'Touchdown': 6, 'Field Goal': 3, 'Safety': 2, 'Two point': 2, 'Extra': 1}, 'vars': ['Down', 'To Go'], 'players': None, 'settings': {'on top': False, 'alarm': True}}
                json.dump(config, f, indent=4)
                f.close()
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            messagebox.showinfo("Stopping...","GameMaster will now stop running. Please provide a valid configuration file on the next run.")
            exit()
        #raise Exception("Error while loading config %s. A stock config file can be found at https://granbybears.live/gamemaster/fix" % f.name) 
        #None
            
#print(config)

# If the config is able to load, only then are these functions defined.
def set_config():
    with open('gamemaster.json', 'w') as f:
        json.dump(config, f, indent=4)
def config_reload():
    reload_ask = messagebox.askyesno("Reload?","Reloading the config will require restarting GameMaster. This will stop the timer and reset scores and team names. Are you sure you want to continue?",icon='warning')
    if reload_ask:
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        None

if 'version' in config:
    versions_tuple = (int(config['version']),int(VERSION))
else:
    ask_version = messagebox.askokcancel("Unknown version number", "The loaded config doesn't contain a version number, or includes an unknown version value. Continuing will add a valid version number to your configuration file.",icon="warning")
    if ask_version:
        if 'settings' in config:
            config['version'] = 2
        else:
            config['version'] = 1
    else:
        messagebox.showinfo("Stopping...","GameMaster will now stop running. Please provide a valid configuration file on the next run.")
        exit()
    versions_tuple = (int(config['version']),int(VERSION))

if config['version'] != VERSION:
    messagebox.showinfo("Config version mismatch", "The loaded config is verion %i, but GameMaster expected configs of version %i. Proceed with caution." % versions_tuple)
    if config['version'] == 1:
        update_ask = messagebox.askyesno("Outdated config", "The loaded config is verion %i, but configs of version 2 and above are required to use settings. Would you like to try to update?" % versions_tuple[0])
        if update_ask:
            config['settings'] = {'on top': False, 'alarm': True}
            config['version'] = 2
            set_config()
            config_reload()
        else:
            None

else:
    settings_list = config['settings']

set_config()

#def focus(event):
#    widget = window.focus_get()
#    if "score" in widget.name:
#        #print("score in focus")
#    else:
#        #print("Enter pressed")

window = tk.Tk()
window.title("GameMaster")
window.geometry("700x575")
window.iconbitmap('icon.ico')
window.resizable(0,1)
window.bind("<Return>", lambda e: focus(e))
window.lift()
window.attributes("-topmost", True)
window.focus_set()
if config['version'] > 1:
    window.attributes("-topmost", settings_list['on top'])
else:
    window.attributes("-topmost", False)

window.rowconfigure(index=0, weight=2)
window.rowconfigure(index=1, weight=1)
window.columnconfigure(index=0, weight=10)
window.columnconfigure(index=1, weight=0)

#==================================================#
#              Timing Setup and Content            #
#==================================================#
timing = tk.Frame(width=20, height=10, bd='5', relief=SUNKEN)
timing.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)

timing.columnconfigure(index=0, weight=2)
timing.columnconfigure(index=1, weight=1)
timing.columnconfigure(index=2, weight=1)
timing.columnconfigure(index=3, weight=1)
timing.columnconfigure(index=4, weight=2)
timing.rowconfigure(index=0, weight=1)
timing.rowconfigure(index=1, weight=2)
timing.rowconfigure(index=2, weight=2)
timing.rowconfigure(index=4, weight=1)
timing.rowconfigure(index=5, weight=2)
timing.rowconfigure(index=6, weight=3)

#[  Timing and sections functions  ]#
global running
running = False
thread_count = 0
# Declaration of variables
hour=StringVar()
minute=StringVar()
second=StringVar()
times = config['times']
# setting the default value
hour.set("{0:02d}".format(times['hours']))
minute.set("{0:02d}".format(times['minutes']))
second.set("{0:02d}".format(times['seconds']))
class TimerClass(threading.Thread):
    
    def __init__(self, thread_ID):
        #print("Thread Created")
        threading.Thread.__init__(self)
        #self.name = thread_name
        self.id = thread_ID
        self.event = threading.Event()
        self.count = int(hour.get())*3600 + int(minute.get())*60 + int(second.get())
    def run(self):
        global to_file
        #self.count = int(hour.get())*3600 + int(minute.get())*60 + int(second.get())
        running = True
        mins,secs = divmod(self.count,60)
        to_file = str("%02d" % (mins))+str(":")+str("%02d" % (secs))

            # writes to the output file the formatted version of the time
        with open('output/time.txt', 'w') as f:
            f.write(to_file)
            f.close()
    
        while self.count > -1 and not self.event.is_set():
            
            # print(self.count)
            # print(running)
            mins,secs = divmod(self.count,60)
      
            # Converting the input entered in mins or secs to hours,
            # mins ,secs(input = 110 min --> 120*60 = 6600 => 1hr :
            # 50min: 0sec)
            hours=0
            if mins >60:
                 
                # divmod(firstvalue = temp//60, secondvalue
                # = temp%60)
                hours, mins = divmod(mins, 60)
             
            # using format () method to store the value up to
            # two decimal places
            hour.set("{0:02d}".format(hours))
            minute.set("{0:02d}".format(mins))
            second.set("{0:02d}".format(secs))
            # stores the formatted version of the time
            to_file = str("%02d" % (mins))+str(":")+str("%02d" % (secs))

            # writes to the output file the formatted version of the time
            with open('output/time.txt', 'w') as f:
                f.write(to_file)
                f.close()
      
            # updating the GUI window after decrementing the
            # temp value every time
            # when temp value = 0; then a messagebox pop's up
            # with a message:"Time's up"
            if (self.count == 0):
                if settings['alarm'] == True:
                    messagebox.showinfo("Time Countdown", "Time's up ")
                    timer_stop()
                else:
                    None
            self.count -= 1
            self.event.wait(1)
            
    def stop(self):
        #print("Stopping...")
        thread_count =+ 1
        # print("Thread count is now %d" % thread_count)
        self.event.set()
        running = False
th = {}
def timer(running):
    # print(running)
    running = running
    running = True
    th[thread_count] = TimerClass(thread_count)
    btn_timer.configure(text='Stop', command=lambda: timer_stop())
    btn_timer.grid(column=1,columnspan=3, sticky=tk.EW, row=2, ipadx=20, ipady=2, padx=0, pady=2)
    th[thread_count].start()

def timer_stop():
    th[thread_count].stop()
    # print(th)
    btn_timer.configure(text='Start', command=lambda: timer(running))
    btn_timer.grid(column=1,columnspan=3, sticky=tk.EW, row=2, ipadx=20, ipady=2, padx=0, pady=2)

def time_set_default():
    #print(times)
    hour.set("{0:02d}".format(times['hours']))
    minute.set("{0:02d}".format(times['minutes']))
    second.set("{0:02d}".format(times['seconds']))
    to_file = str("%02d" % (int(times['minutes'])))+str(":")+str("%02d" % (int(times['seconds'])))
    #print(to_file)
    with open('output/time.txt', 'w') as f:
        f.write(to_file)
        f.close()
    timer_stop()

def section_set(type):
    type=type
    with open('output/Section.txt', 'w') as f:
        if type == 1:
            if(int(section.get()) < config['ct']):
                #print("section setting")
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

lbl_tmr = tk.Label(master=timing,text="Timer",font=("Arial",18,""),padx=30)
lbl_tmr.grid(sticky=S,row=0,column=1,columnspan=3)
hourEntry= Entry(master=timing, width=2, font=("Arial",26,""),textvariable=hour, justify="center")
hourEntry.grid(sticky=NSEW, column=1, row=1)
minuteEntry= Entry(master=timing, width=2, font=("Arial",26,""),textvariable=minute, justify="center")
minuteEntry.grid(sticky=NSEW, column=2, row=1)
secondEntry= Entry(master=timing, width=2, font=("Arial",26,""),textvariable=second, justify="center")
secondEntry.grid(sticky=NSEW, column=3, row=1)
btn_timer = Button(master=timing, text='Start', bd='5',command=lambda: timer(running))
btn_timer.grid(column=1,columnspan=3, sticky=tk.EW, row=2, ipadx=20, ipady=2, padx=0, pady=2)
btn_time = Button(master=timing, text='Default', bd='5',command=lambda: time_set_default())
btn_time.grid(column=0,columnspan=1, sticky=tk.E, row=1, ipadx=0, ipady=2, padx=4, pady=2)
btn_clear = Button(master=timing, text='Clear', bd='5',command=lambda: time_clear())
btn_clear.grid(column=4,columnspan=1, sticky=tk.W, row=1, ipadx=0, ipady=2, padx=4, pady=2)
hour.set("{0:02d}".format(times['hours']))
minute.set("{0:02d}".format(times['minutes']))
second.set("{0:02d}".format(times['seconds']))
to_file = str("%02d" % (int(times['minutes'])))+str(":")+str("%02d" % (int(times['seconds'])))
#print(to_file)
with open('output/time.txt', 'w') as f:
    f.write(to_file)
    f.close()


lbl_section = tk.Label(master=timing,text=config["unit"],font=("Arial",18,""),padx=30)
lbl_section.grid(sticky=S,row=4,column=1,columnspan=3)
section=StringVar()
section.set("1")
with open('output/Section.txt', 'w') as f:
    f.write(section.get())
    f.close()
ent_section = Entry(master=timing, width=3, font=("Arial",18,""),textvariable=section, justify='center', bd='3')
ent_section.grid(sticky=NSEW, column=2, row=5)
btn_sectionup = Button(master=timing, text='+', width=2, bd='5',command=lambda: section_set(1))
btn_sectionup.grid(column=3, row=5)
btn_sectiondn = Button(master=timing, text='-', width=2, bd='5',command=lambda: section_set(0))
btn_sectiondn.grid(column=1, row=5)


#==================================================#
#             Scoring Setup and Content            #
#==================================================#
scoring = tk.Frame(width=20, height=10, bd='5', relief=SUNKEN)
scoring.grid(row=1, column=0, sticky=NSEW, padx=5, pady=5)

scoring.columnconfigure(index=0, weight=1)
scoring.columnconfigure(index=1, weight=1)
scoring.rowconfigure(index=0, weight=0)
scoring.rowconfigure(index=1, weight=10)
lbl_home = tk.Label(master=scoring,text="Scoring",font=("Arial",18,""))
lbl_home.grid(sticky=EW,row=0,column=0,columnspan=2)

name_home = StringVar()
score_home = StringVar()
name_away = StringVar()
score_away = StringVar()

teams_scores = {}
teams_scores["home"] = 0
teams_scores["away"] = 0

def scoreadd(target_team,value):
    teams_scores[target_team] += value
    #print(teams_scores)
    score_home.set(str(teams_scores["home"]))
    score_away.set(str(teams_scores["away"]))
    for x in teams_scores:
        with open(str('output/')+str(x)+str('_score.txt'), 'w') as f:
            f.write(str(teams_scores[x]))
            f.close()

def scoreset(target_team):
    if target_team == "home":
        teams_scores["home"] = int(ent_home.get())
    elif target_team == "away":
        teams_scores["away"] = int(ent_away.get())
    #print(teams_scores)
    score_home.set(str(teams_scores["home"]))
    score_away.set(str(teams_scores["away"]))
    for x in teams_scores:
        with open(str('output/')+str(x)+str('_score.txt'), 'w') as f:
            f.write(str(teams_scores[x]))
            f.close()

teams_names = {}
teams_names["home"] = ""
teams_names["away"] = ""

def nameset(target_team):
    if target_team == "home":
        teams_names[target_team] = ent_homename.get()
        print(name_home.get())
    elif target_team == "away":
        teams_names[target_team] = ent_awayname.get()
        print(name_away.get())
    for x in teams_names:
        with open(str('output/')+str(x)+str('_name.txt'), 'w') as f:
            f.write(str(teams_names[x]))
            f.close()

score_home.set("0")
homeframe = tk.Frame(master=scoring, bd='5', relief="sunken")
homeframe.grid(row=1, column=0, sticky=NSEW, pady=2, padx=2)
homeframe.columnconfigure(index=0, weight=1)
homeframe.columnconfigure(index=1, weight=5)
homeframe.columnconfigure(index=2, weight=1)
homeframe.rowconfigure(index=0, weight=1)
homeframe.rowconfigure(index=1, weight=1)
homeframe.rowconfigure(index=2000, weight=100)
lbl_home = tk.Label(master=homeframe,text="Home",font=("Arial",12,""))
lbl_home.grid(sticky=EW,row=0,column=0,columnspan=1)
ent_homename = Entry(master=homeframe, width=2, font=("Arial",12,""),textvariable=name_home, justify="center")
ent_homename.grid(row=0,column=1, sticky=NSEW, pady=2)
btn_homename = Button(master=homeframe, text="Set", bd='5', command=lambda: nameset("home"))
btn_homename.grid(row=0,column=2, sticky=NSEW, padx=5)
ent_home = Entry(master=homeframe, width=4, font=("Arial",26,""),textvariable=score_home, justify="center")
ent_home.grid(sticky=NS, column=1, row=1, pady=5, padx=5)
btn_homeup = Button(master=homeframe, text='+', width=2, bd='5',command=lambda: scoreadd("home",1))
btn_homeup.grid(column=2, row=1)
btn_homedn = Button(master=homeframe, text='-', width=2, bd='5',command=lambda: scoreadd("home",-1))
btn_homedn.grid(column=0, row=1)
btn_homeset = Button(master=homeframe, text='Set Score', width=2, bd='5',command=lambda: scoreset("home"))
btn_homeset.grid(column=0, row=2, columnspan=3, sticky=EW, pady=5, padx=5)

score_away.set("0")
awayframe = tk.Frame(master=scoring, bd='5', relief="sunken")
awayframe.grid(row=1, column=1, sticky=NSEW, pady=2, padx=2)
awayframe.columnconfigure(index=0, weight=1)
awayframe.columnconfigure(index=1, weight=5)
awayframe.columnconfigure(index=2, weight=1)
awayframe.rowconfigure(index=0, weight=1)
awayframe.rowconfigure(index=1, weight=1)
awayframe.rowconfigure(index=2000, weight=100)
lbl_away = tk.Label(master=awayframe,text="Away",font=("Arial",12,""))
lbl_away.grid(sticky=EW,row=0,column=0,columnspan=1)
ent_awayname = Entry(master=awayframe, width=2, font=("Arial",12,""),textvariable=name_away, justify="center")
ent_awayname.grid(row=0,column=1, sticky=NSEW, pady=2)
btn_awayname = Button(master=awayframe, text="Set", bd='5', command=lambda: nameset("away"))
btn_awayname.grid(row=0,column=2, sticky=NSEW, padx=5)
ent_away = Entry(master=awayframe, width=4, font=("Arial",26,""),textvariable=score_away, justify="center")
ent_away.grid(sticky=NS, column=1, row=1, pady=5, padx=5)
btn_awayup = Button(master=awayframe, text='+', width=2, bd='5',command=lambda: scoreadd("away",1))
btn_awayup.grid(column=2, row=1)
btn_awaydn = Button(master=awayframe, text='-', width=2, bd='5',command=lambda: scoreadd("away",-1))
btn_awaydn.grid(column=0, row=1)
btn_awayset = Button(master=awayframe, text='Set Score', width=2, bd='5',command=lambda: scoreset("away"))
btn_awayset.grid(column=0, row=2, columnspan=3, sticky=EW, pady=5, padx=5)

# Sets all the scores and variables into the window
scrs = config['scores']
scrs_index = scrs.keys()
#print(scrs_index)
s = {}
#print(scrs)
# Home
for x in scrs:
    homeframe.rowconfigure(index=list(scrs.keys()).index(x)+3, weight=1)
    s["btn_".join(x)] = tk.Button(master=homeframe, bd='5', text=str(x), command=lambda x=x: scoreadd("home",int(scrs[x])))
    s["btn_".join(x)].grid(column=1, row=list(scrs.keys()).index(x)+3, sticky=EW)

for x in scrs:
    awayframe.rowconfigure(index=list(scrs.keys()).index(x)+3, weight=1)
    s["btn_".join(x)] = tk.Button(master=awayframe, bd='5', text=str(x), command=lambda x=x: scoreadd("away",int(scrs[x])))
    s["btn_".join(x)].grid(column=1, row=list(scrs.keys()).index(x)+3, sticky=EW)

for x in teams_scores:
    with open(str('output/')+str(x)+str('_score.txt'), 'w') as f:
        f.write(str(teams_scores[x]))
        f.close()

for x in teams_names:
    with open(str('output/')+str(x)+str('_name.txt'), 'w') as f:
        f.write(str(teams_names[x]))
        f.close()


# Score: 0/100

#==================================================#
#            Variables Setup and Content           #
#==================================================#
variables = tk.Frame(width=20, height=10, bd='5', relief=GROOVE)
variables.grid(row=0, column=1, sticky=NSEW, padx=5, pady=5)

variables.columnconfigure(index=0, weight=1)
variables.columnconfigure(index=1, weight=1)
variables.columnconfigure(index=2, weight=1)
variables.rowconfigure(index=0, weight=1)
variables.rowconfigure(index=2000, weight=100)

#[  Timing and sections functions  ]#
def varset(varname,value):
    with open(str('output/')+str(varname)+str('.txt'), 'w') as f:
        f.write(str(value))
        #print(str(varname) + " Saved")
        f.close()

lbl_variables = tk.Label(master=variables,text="Other Variables",font=("Arial",18,""),padx=5,justify="center")
lbl_variables.grid(sticky=S,row=0,column=0,columnspan=3)

vars = config['vars']
v = {}
for x in vars:
    variables.rowconfigure(index=vars.index(x)+1, weight=1)
    v["lbl_".join(x)] = tk.Label(master=variables, text=x, padx=5, pady=5)
    v["ent_".join(x)] = tk.Entry(master=variables, font=("Arial",12,""),justify="center",width=5) 
    v["ent_".join(x)].name = x #                                    Fixed \/
    v["btn_".join(x)] = tk.Button(master=variables, bd='5', text=str("Set ")+str(x), command=lambda x=x: varset(str(x), int(v["ent_".join(x)].get())))
    v["lbl_".join(x)].grid(sticky=tk.E, column=0, row=int(vars.index(x)+2))
    v["ent_".join(x)].grid(sticky=NS, column=1, row=int(vars.index(x)+2))
    v["btn_".join(x)].grid(sticky=W, column=2, row=int(vars.index(x)+2), columnspan=2, padx=2)

#==================================================#
#            Settings Setup and Content            #
#==================================================#
settings = tk.Frame(width=20, height=10, bd='5', relief=GROOVE)
settings.grid(row=1, column=1, sticky=NSEW, padx=5, pady=5)

settings.columnconfigure(index=0, weight=1)
settings.columnconfigure(index=1, weight=1)
settings.columnconfigure(index=2, weight=1)
settings.rowconfigure(index=0, weight=1)
settings.rowconfigure(index=1, weight=1)
settings.rowconfigure(index=2000, weight=100)
settings.rowconfigure(index=2001, weight=1)

#[      Settings functions      ]#
def config_name():
    #print("Config name set: "+str(ent_name.get()))
    config['name'] = ent_name.get()
    set_config()


lbl_settings = tk.Label(master=settings,text="Settings",font=("Arial",18,""),padx=5)
lbl_settings.grid(sticky=S,row=0,column=0,columnspan=3)
lbl_name = tk.Label(master=settings,text="Config Name:")
lbl_name.grid(column=0, row=1, sticky=tk.NE, padx=5, pady=5)
ent_name = tk.Entry(master=settings,)
ent_name.grid(column=1, row=1, sticky=tk.N, padx=5, pady=5)
ent_name.insert(0, config['name'])
btn_name = tk.Button(master=settings,text="Set", command=config_name)
btn_name.grid(column=2, row=1, sticky=tk.NW, padx=5, pady=5)
btn_reload = tk.Button(master=settings,text="Reload config", command=config_reload)
btn_reload.grid(column=1, row=2001, sticky=tk.NW, padx=5, pady=5)


if config['version'] > 1:
    st = {}
    for x in settings_list:
        settings.rowconfigure(index=list(settings_list.keys()).index(x)+2, weight=1)
        st["btn_".join(x)] = tk.Button(master=settings, bd='5', text=str(x).capitalize(), command=None)
        st["btn_".join(x)].grid(column=1, row=list(settings_list.keys()).index(x)+2, sticky=EW)

#[================================================]#
#[================================================]#
window.mainloop()