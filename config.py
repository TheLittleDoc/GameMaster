from tkinter import messagebox
import os, os.path, sys
import json
import time

NAME = "GameMaster"
APP_VERSION = "1.1.0"
VERSION = 2

config = {}

def get_config():
    with open("gamemaster.json", "r") as f:
        try:
            config = json.load(f)
            return config
            print(config)

        except:
            ask_error = messagebox.askokcancel("Error while loading config", "GameMaster configuration file misformatted. Continuing will revert to a known-working default configuration.",icon="error")
            if ask_error:
                with open("gamemaster.json", "w") as f:
                    config = {"name": "Football", "version": 1, "unit": "Quarter", "ct": 4, "times": {"hours": 0, "minutes": 12, "seconds": 0}, "scores": {"Touchdown": 6, "Field Goal": 3, "Safety": 2, "Two point": 2, "Extra": 1}, "vars": ["Down", "To Go"], "players": None, "settings": {"on top": False, "alarm": True}}
                    json.dump(config, f, indent=4)
                    f.close()
                os.execv(sys.executable, ["python"] + sys.argv)
            else:
                messagebox.showinfo("Stopping...","GameMaster will now stop running. Please provide a valid configuration file on the next run.")
                exit()
            #raise Exception("Error while loading config %s. A stock config file can be found at https://granbybears.live/gamemaster/fix" % f.name) 
            #None
            
#print(config)

# If the config is able to load, only then are these functions defined.
def set_config():
    with open("gamemaster.json", "w") as f:
        json.dump(config, f, indent=4)
def config_reload():
    reload_ask = messagebox.askyesno("Reload?","Reloading the config will require restarting GameMaster. This will stop the timer and reset scores and team names. Are you sure you want to continue?",icon="warning")
    if reload_ask:
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
        else:
            config["version"] = 1
    else:
        messagebox.showinfo("Stopping...","GameMaster will now stop running. Please provide a valid configuration file on the next run.")
        exit()
    versions_tuple = (int(config["version"]),int(VERSION))

if config["version"] != VERSION:
    messagebox.showinfo("Config version mismatch", "The loaded config is version %i, but GameMaster expected configs of version %i. Proceed with caution." % versions_tuple)
    if config["version"] == 1:
        update_ask = messagebox.askyesno("Outdated config", "The loaded config is version %i, but configs of version 2 and above are required to use settings. Would you like to try to update?" % versions_tuple[0])
        if update_ask:
            config["settings"] = {"on top": False, "alarm": True}
            config["version"] = 2
            set_config()
            config_reload()
        else:
            None
    elif config["version"] == 2:
        if not "settings" in config.keys:
            messagebox.showinfo("Config version mismatch", "The loaded config is version %i, but appears to be malformed or improperly updated. If errors arrise or features are unavailable, it is recommended that you reset to a known-working default configuration." % config["version"])


else:
    settings_list = config["settings"]
