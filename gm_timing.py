import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import os, os.path, sys
import time
import threading
import gm_config as gmc
from gm_resources import resource_path, retrieve_file, f

global kill_thread
kill_thread = False
# uwu

config = gmc.config
try:
    settings_list = config["settings"]
except:
    print("No settings_list found in config.json")
    settings_list = {"hours": False,"minutes": True,"seconds": True,"on top": False, "countup": False, "end on time": False, "alarm": True}



def timing_setup(main_frame, file):
    timing = Frame(master=main_frame,width=12, height=10, borderwidth=3, relief=SUNKEN)
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
    file_name = "output/{0}.txt".format(file)
    class TimerClass(threading.Thread):
        """Create a functioning timer that counts down to a file."""
        def __init__(self, thread_ID):
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
            # with open("file_name", "w") as f:
            #     f.write(to_file)
            #     f.close()
        
            while self.count > -1 and not self.event.is_set():
                
                if kill_thread:
                    print("called to stop")
                    th[thread_count].timer_stop()
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
                with open(file_name, "w") as f:
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
                            th[thread_count].timer_stop()
                    self.count += 1
                else:
                    if (self.count == 0):
                        if settings_list["alarm"] == True:
                            messagebox.showinfo("Time Countdown", "Time's up ")
                            th[thread_count].timer_stop()
                        else:
                            None
                    else:
                        self.count -= 1
                
                self.event.wait(1)
                
        def stop(self):
            thread_count =+ 1
            self.event.set()
            running = False
        def timer_stop(self):
            th[thread_count].stop()
            btn_timer.configure(text="Start", command=lambda: timer(running))
            btn_timer.grid(column=0,columnspan=1, sticky=NS, row=3, rowspan=2, ipadx=0, ipady=2, padx=4)
    th = {}
    def timer(is_running):
        
        running = True
        th[thread_count] = TimerClass(thread_count)
        btn_timer.configure(text="Stop", command=lambda: th[thread_count].timer_stop())
        btn_timer.grid(column=0,columnspan=1, sticky=NS, row=3, rowspan=2, ipadx=0, ipady=2, padx=4)
        th[thread_count].start()
    
    

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
        with open(file_name, "w") as f:
            f.write(to_file)
            f.close()
        th[thread_count].timer_stop()

    def section_set(type):
        type=type
        with open("output/section.txt", "w") as f:
            if type == 1:
                if(int(section.get()) < int(config["ct"])):
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
            with open(file_name, "w") as f:
                f.write(to_file)
                f.close()
            th[thread_count].timer_stop()
        else:
            None

    additional_timer = []

    def create_timer():
        additional_timer.append(NewTimer(len(additional_timer)+1))

    lbl_tmr = Label(master=timing,text=gmc.lang["timer"],font=("Arial",18,""))
    lbl_tmr.grid(sticky=S,row=0,column=0,columnspan=4)
    hourEntry= Entry(master=timing, width=2, font=("Arial",26,""),textvariable=hour, justify="center")
    hourEntry.grid(sticky=NSEW, column=1, row=1, rowspan=2)
    minuteEntry= Entry(master=timing, width=2, font=("Arial",26,""),textvariable=minute, justify="center")
    minuteEntry.grid(sticky=NSEW, column=2, row=1, rowspan=2)
    secondEntry= Entry(master=timing, width=2, font=("Arial",26,""),textvariable=second, justify="center")
    secondEntry.grid(sticky=NSEW, column=3, row=1, rowspan=2)
    btn_timer = Button(master=timing, text=gmc.lang["start"],command=lambda: timer(running))
    btn_timer.grid(column=0,columnspan=1, sticky=NS, row=3, rowspan=2, ipadx=0, ipady=2, padx=4)
    btn_add_timer = Button(master=timing, text="Add Timer",command=lambda: create_timer())
    btn_add_timer.grid(column=0,columnspan=1, sticky=NS, row=5, rowspan=1, ipadx=0, ipady=2, padx=4)
    btn_time = Button(master=timing, text="Default",command=lambda: time_set_default())
    btn_time.grid(column=0,columnspan=1, sticky=NE, row=1, ipadx=0, ipady=2, padx=4)
    btn_clear = Button(master=timing, text="Clear",command=lambda: time_clear())
    btn_clear.grid(column=0,columnspan=1, sticky=NE, row=2, ipadx=0, ipady=2, padx=4)
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
    if not os.path.exists("output"):
        os.makedirs("output")
    with open(file_name, "w") as f:
        f.write(to_file)
        f.close()

    lbl_section = Label(master=timing,text=config["unit"],font=("Arial",18,""))
    lbl_section.grid(sticky=S,row=4,column=1,columnspan=3)
    section=StringVar()
    section.set("1")

    with open("output/section.txt", "w") as f:
        f.write(section.get())
        f.close()
    ent_section = Entry(master=timing, width=3, font=("Arial",18,""),textvariable=section, justify="center", state="readonly")
    ent_section.grid(sticky=NS, column=2, row=5)
    btn_sectionup = Button(master=timing, text="+", width=2,command=lambda: section_set(1))
    btn_sectionup.grid(column=3, row=5, sticky=W)
    btn_sectiondn = Button(master=timing, text="-", width=2,command=lambda: section_set(0))
    btn_sectiondn.grid(column=1, row=5, sticky=E)

def quit_stop():
    kill_thread = True

def del_timer(timer_instance):
    del timer_instance

class NewTimer():
        def __init__(self, id):
            self.top = Toplevel()
            self.top.title("New Timer")
            self.top.geometry("409x184")
            self.top.rowconfigure(1, weight=1)
            self.top.columnconfigure(0, weight=1)
            self.main_frame = Frame(self.top)
            self.main_frame.columnconfigure(0, weight=1)
            self.main_frame.grid(sticky=NSEW)
            self.th = {}
            timing_setup(self.top, str(id))
            print(id)
            self.thread_count = 0
            
        
    