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
    with open("output/time.txt", "w") as f:
        f.write(to_file)
        f.close()

    lbl_section = tk.Label(master=timing,text=config["unit"],font=("Arial",18,""),padx=30)
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
