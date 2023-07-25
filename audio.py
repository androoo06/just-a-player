import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from settings import *
from util import read_file_as_list
from pygame import mixer
from mutagen.mp3 import MP3
from time import sleep

import random

mixer.init()
mixer.music.set_endevent(25)

song_queue = read_file_as_list("data/queue.txt") # for upcoming songs
recency_stack = read_file_as_list("data/stack.txt") # for previous songs

saved_queue = [] if (settings["queue_looped"] == False) else [recency_stack[len(recency_stack) - (i+1)] for i in range(len(recency_stack))] + [song for song in song_queue] # for looped queues
action_stack = [] # used for stopping bugs with the music_ended event

if ((len(song_queue) == 0) and (len(saved_queue) > 0)):
    song_queue.clear()
    [song_queue.append(song) for song in saved_queue]

current_song = {
    "name": None,
    "length": 0,
    "position": 0,
    "played": False # has been played (useful to know for startups)
}

mixer_loaded = False

open_tab = None
slider = None
root = None
playImg = None
pauseImg = None
update_song_display = None

def set_data(_slider=None, _root=None, _open_tab=None, _playImg=None, _pauseImg=None, _update_song_display=None):
    global slider, root, open_tab, mixer_loaded, playImg, pauseImg, update_song_display

    slider       = _slider       if (_slider       != None) else slider
    root         = _root         if (_root         != None) else root
    open_tab     = _open_tab     if (_open_tab     != None) else open_tab
    playImg      = _playImg      if (_playImg      != None) else playImg
    pauseImg     = _pauseImg     if (_pauseImg     != None) else pauseImg

    update_song_display = _update_song_display if (_update_song_display != None) else update_song_display

def get_root():
    return root

def get_slider():
    return slider

def dequeue():
    if (len(song_queue) == 0):
        return None
    return song_queue.pop(0)

def update_images():
    p_btn = get_root().nametowidget("bot_bar").nametowidget("p_btn")
    p_btn.config(image=(playImg if (mixer.music.get_busy() == False) else pauseImg))

### audio stuff ###

def set_song_pos(percent=0):
    length = current_song["length"]
    mixer.music.set_pos(length * percent)

def change_volume(percent=0.5):
    setting = change_setting("volume", percent)
    mixer.music.set_volume(setting)

def rewind_song(event):
    if ((current_song["position"] * current_song["length"]) > 5):
        slider.set_pos(0)
        mixer.music.rewind()
    else:
        if (current_song["played"]):
            action_stack.append("Rewinding Song")

        previous = current_song["name"]
        if (len(recency_stack) > 0):
            previous = recency_stack.pop()
            song_queue.insert(0, previous)
        
        load_song(song_name=previous, autoplay=True)

def skip_song(event):
    if (current_song["played"] == False):
        music_ended()
    else:
        stop_song()

def stop_song():
    try:
        mixer.music.stop()
        mixer.music.unload()
    except Exception as e: print(e)

def shuffle_queue(event):
    if (len(song_queue) > 1):
        random.shuffle(song_queue)
        create_queue(None, manual_queue=True)
        if (settings["queue_looped"]):
            loop_queue(state=True)
    
def loop_queue(state=False):
    saved_queue.clear()
    if (state == True):
        [saved_queue.append(song) for song in song_queue]

def create_queue(event, manual_queue=False):
    if (current_song["played"] == True):
        action_stack.append("Creating Queue")

    if (manual_queue == False):
        o = get_root().nametowidget("display_playlist").nametowidget("o")
        list = [i.split("   ")[-1] for i in o.get("1.0", "end").split("\n") if i]
        song_queue.clear()
        [song_queue.append(i) for i in list]
        #print(song_queue)
    recency_stack.clear()

    if (len(song_queue) > 0):
        load_song(song_queue[0], autoplay=(not manual_queue))

def unload_song(keep_enabled=False):
    global mixer_loaded

    bot_bar = root.nametowidget("bot_bar")
    song_txt = bot_bar.nametowidget("song_text")
    
    song_txt.config(state="normal")
    try:
        song_txt.delete("1.0", "end")
    except Exception as e: print(e)

    if (keep_enabled == False):
        song_txt.config(state="disabled")

    current_song["name"] = None
    current_song["length"] = 0
    current_song["position"] = 0
    current_song["played"] = False

    slider.set_pos(0)
    slider.unbind()

    stop_song()
    mixer.music.unload()
    mixer_loaded = False

    return song_txt

def load_song(song_name=None, autoplay=False, progress=0):
    global mixer_loaded

    # display the song on the ui & configure the mixer
    song_txt = unload_song(keep_enabled=True)

    if (song_name != None):
        song_txt.insert("end", song_name)
        song_txt.config(state="disabled")

        current_song["name"] = song_name
        current_song["length"] = MP3(f"songs/{song_name}.mp3").info.length
        current_song["position"] = 0
        current_song["played"] = False

        slider.bind(set_song_pos)

        try:
            mixer.music.load(f"songs/{song_name}.mp3")
            mixer_loaded = True
        except Exception as e: print(e)

    if (open_tab=="YOUR QUEUE"):
        update_song_display(None, override=True)

    if (autoplay and mixer_loaded):
        play_btn_pressed(None)
    else:
        update_images()

def play_btn_pressed(event):
    if ((mixer.music.get_busy() == False) and current_song["position"] == 0):
        mixer.music.play()
        current_song["played"] = True
    elif (mixer_loaded):
        if (mixer.music.get_busy()):
            mixer.music.pause()
        elif (current_song["position"] > 0):
            mixer.music.unpause()

    update_images()

def music_ended():
    if (len(action_stack) > 0):
        action = action_stack.pop()
        print(f"ignoring for action: '{action}'")
    else:
        sleep(0.1)
        previous = dequeue()
        if (previous): recency_stack.append(previous) # add old song to recency stack
        song = song_queue[0] if (len(song_queue) > 0) else None
        if ((song == None) and (len(saved_queue) > 0)):
            song_queue.clear()
            [song_queue.append(i) for i in saved_queue]
            recency_stack.clear()
            song = song_queue[0]

        load_song(song, autoplay=True)