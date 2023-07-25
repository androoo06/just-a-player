#https://pypi.org/project/audioplayer/
from audioplayer import AudioPlayer
from mutagen.mp3 import MP3
from time import sleep
import tkinter as tk

current_song = {
    "name": None,
    "obj": None,
    "paused": False,
}

# default settings
settings = {
    "volume": 50,
}

queue = []

def display_current_song(args):
    print(current_song)

def try_number(s):
    try:
        int(s)
        return int(s)
    except ValueError:
        return s

def open_file(file, method):
    f = None
    try:
        f = open(file, method)
    except:
        print("Problem opening file", file)
        return None
    return f

def read_settings():
    f = open_file("settings.txt", "r")
    for line in f.read().splitlines():
        setting = line.split("=")
        settings[setting[0]] = try_number(setting[1])
    f.close()

def write_settings():
    f = open_file("settings.txt", "w")

    for setting in settings.keys():
        f.write(f"{setting}={str(settings[setting])}")

def change_setting(setting, value):
    final = try_number(value)
    settings[setting] = final
    return final

def change_vol(args):
    val = args[0]
    setting = change_setting("volume", val or "50")
    if (current_song["obj"]):
        current_song["obj"].volume = setting

def get_song(name):
    track = None
    try:
        song_path = f"songs/{name}.mp3"
        track = AudioPlayer(song_path)
    except:
        print('Something went wrong')
        return None

    return track

def stop_song(args):
    obj = current_song["obj"]
    if (obj != None):
        obj.stop()
        current_song["paused"] = True

def add_to_queue(args):
    pass

def remove_from_queue(args):
    pass

async def __wait(song):
    length = int(MP3(song.filename).info.length)
    sleep(length)

def play_song(args):
    name = args[0] if (len(args)>0) else current_song["name"]

    if ((name != None) and (current_song["name"] == name)):
        if (current_song["paused"]):
            current_song["obj"].resume()
        else:
            stop_song(0)
        current_song["paused"] = (not current_song["paused"])
    else:
        song = get_song(name)
        if (song != None):
            current_song["obj"] = song
            current_song["name"] = name
            current_song["paused"] = False
            song.volume = settings["volume"]
            song.play()
        else:
            print('Song not found.')

commands = {
    "play"  : play_song,
    "p"     : play_song,
    "stop"  : stop_song,
    
    "v"     : change_vol,
    "volume": change_vol,

    "a2q"   : add_to_queue,
    "rfq"   : remove_from_queue,
    "remove": remove_from_queue,

    "dc"    : display_current_song,
    #skip (skip track)
    #rewind, rw (rewind current track)
    #loop (loop current track)
    #loopqueue, loopq (loops the queue)
    #shuffle (shuffles the queue)
}

read_settings()

# command-line implementation for now
while (True):
    x = input()
    if (x == "x") or (x == "exit"):
        break
    split = x.split(" ")
    if (split[0] in commands):
        commands[split[0]](split[1:])
    else:
        print("Command not found.")

# apply settings to the file upon closing
write_settings()