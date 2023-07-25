import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from settings import *
from util import read_file_as_list
from pygame import mixer
from slider import class_from_bg
from mutagen.mp3 import MP3
from time import sleep

import random

mixer.init()
mixer.music.set_endevent(25)

queue = read_file_as_list("data/queue.txt") # for upcoming songs
saved_queue = [] # for looped queues
stack = read_file_as_list("data/stack.txt") # for previous songs

current_song = {
    "name": None,
    "playing": False,
    "length": 0,
    "looped": False, # not implemented
}

open_tab = None
slider = None
root = None
creating_queue = False
rewinding_song = False

def set_slider(__slider):
    global slider
    slider = __slider

def set_root(__root):
    global root
    root = __root

def set_open_tab(__tab):
    global open_tab
    open_tab = __tab

def song_pos_cb(percent=0):
    # change the position of the audio to this percent
    length = current_song["length"]
    mixer.music.set_pos(length * percent)

def load_song(name):
    try:
        song_path = f"songs/{name}.mp3"
        mixer.music.load(song_path)
        return True
    except Exception as e:
        #print('Something went wrong loading song:', e)
        return False

def display_song(song, progress=0):
    bot_bar = root.nametowidget("bot_bar")
    song_txt = bot_bar.nametowidget("song_text")
    slider = class_from_bg(bot_bar.nametowidget("progress_slider_bg"))

    song_txt.config(state="normal")

    try:
        song_txt.delete("1.0", "end")
    except Exception as e:
        print(e)

    current_song["playing"] = False
    if (song == None):
        current_song["name"] = None
        current_song["length"] = 0

        slider.set_pos(0)
        slider.unbind()
    else:
        current_song["name"] = queue[0]
        current_song["length"] = MP3(f"songs/{queue[0]}.mp3").info.length

        song_txt.insert("end", song)
        song_txt.config(state="disabled")
    
    slider.bind(song_pos_cb)

def create_queue(playlist, playImg=None, pauseImg=None):
    songs = None

    global creating_queue
    if ((current_song["name"] != None) and (current_song["playing"] == True)):
        creating_queue = True

    # get songs
    if (playlist != "playlists/$default$.txt"):
        songs = open_file(playlist, "r").read().splitlines()
    else:
        song_dirs = os.listdir("songs")
        for i in range(len(song_dirs)): 
            song_dirs[i] = song_dirs[i].split(".")[0]
        songs = song_dirs

    # update the queue
    set_queue(songs)
    set_stack([])

    if (settings["playlist_shuffled"] == "True"):
        shuffle_queue() 

    # load the first song
    if (len(queue) > 0):
        stop_song()
        display_song(queue[0])
        play_song_pressed(override=True, playImg=playImg, pauseImg=pauseImg)

def add_to_queue(songName):
    queue.append(songName)

def dequeue():
    if (len(queue) == 0):
        return None
    return queue.pop(0)

def remove_from_queue(songName):
    queue.remove(songName)

def set_stack(v):
    global stack
    stack = v.copy()

def set_queue(v):
    global queue
    queue = v.copy()

def loop_queue():
    change_setting("queue_looped", not settings["queue_looped"])

def shuffle_queue():
    random.shuffle(queue)

def change_vol(val):
    setting = change_setting("volume", val or "0.5")
    mixer.music.set_volume(setting)

def stop_song():
    try:
        mixer.music.stop()
        mixer.music.unload()
    except Exception as e:
        print(e)

def skip_song(fn):
    # if (mixer.music.get_pos() == -1):
    #     music_ended(fn)
    # else:
    stop_song()

def rewind_song(playImg=None, pauseImg=None):
    bot_bar = root.nametowidget("bot_bar")
    slider = class_from_bg(bot_bar.nametowidget("progress_slider_bg"))

    if ((slider.progress * current_song["length"]) > 5):
        slider.set_pos(0)
        mixer.music.rewind()
    else:
        global rewinding_song
        rewinding_song = True

        previous = current_song["name"]
        if (len(stack) > 0):
            previous = stack.pop()
            queue.insert(0, previous)
        display_song(previous)
        play_song_pressed(override=True, playImg=playImg, pauseImg=pauseImg)


def loop():
    current_song["looped"] = (not current_song["looped"])

def play_song(song=None, autoplay_disabled=False):
    stop_song()
    slider.set_pos(0)
    if (load_song(song or current_song["name"])):
        if (autoplay_disabled == False):
            mixer.music.play()
            current_song["playing"] = True

# pause, unpause, play
def play_song_pressed(playImg=None, pauseImg=None, override=False):
    bot_bar = root.nametowidget("bot_bar")
    p_btn = bot_bar.nametowidget("p_btn")
    slider = class_from_bg(bot_bar.nametowidget("progress_slider_bg"))

    if ((override == False) and (current_song["name"] != None)):
        if (current_song["playing"]):
            mixer.music.pause()
            current_song["playing"] = False
        elif (slider.progress > 0):
            mixer.music.unpause()
            current_song["playing"] = True
        else:
            play_song()
            current_song["playing"] = True
    else:
        play_song()

    if (current_song["name"] != None):
        p_btn.config(image=(playImg if (current_song["playing"] == False) else pauseImg))

def on_start():
    if (len(queue) > 0):
        display_song(queue[0])
        play_song(autoplay_disabled=True)

##### MAIN LOOP ####
def music_ended(fn=None):
    #print('shitended')
    sleep(0.1)

    global creating_queue
    global rewinding_song

    if (creating_queue):
        creating_queue = False
    elif (rewinding_song):
        rewinding_song = False
    else:
        q = queue
        stack.append(dequeue()) # add old song to recency stack
        song = q[0] if (len(q) > 0) else None
        display_song(song)
        play_song()
    
    if (fn and (open_tab=="YOUR QUEUE")):
        o = root.nametowidget("display_playlist").nametowidget("o")
        tbr = root.nametowidget("top_bar_right").nametowidget("playlist_label")
        fn(o, tbr, "data/queue.txt")