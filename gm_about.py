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
    btn_datastream = Button(master=datastream,text="Discord Server", command=lambda: external_link("https://discord.gg/invite/WzA4FncR8f"))
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