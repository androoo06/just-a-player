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
saved_queue = [] # for looped queues
recency_stack = read_file_as_list("data/stack.txt") # for previous songs
action_stack = [] # used for stopping bugs with the music_ended event

current_song = {
    "name": None,
    "length": 0,
}

mixer_loaded = False

open_tab = None
slider = None
root = None
playImg = None
pauseImg = None

def set_data(_slider=None, _root=None, _open_tab=None, _playImg=None, _pauseImg=None):
    global slider, root, open_tab, mixer_loaded, playImg, pauseImg

    slider       = _slider       if (_slider       != None) else slider
    root         = _root         if (_root         != None) else root
    open_tab     = _open_tab     if (_open_tab     != None) else open_tab
    playImg      = _playImg      if (_playImg      != None) else playImg
    pauseImg     = _pauseImg     if (_pauseImg     != None) else pauseImg

def get_root():
    return root

def set_song_pos(percent=0):
    length = current_song["length"]
    mixer.music.set_pos(length * percent)

def change_volume(percent=0.5):
    setting = change_setting("volume", percent)
    mixer.music.set_volume(setting)

def rewind_song(event):
    pass

def skip_song(event):
    pass

def stop_song():
    try:
        mixer.music.stop()
        mixer.music.unload()
    except Exception as e: print(e)

def create_queue(event):
    global song_queue, recency_stack
    action_stack.append("Creating Queue")

    o = get_root().nametowidget("display_playlist").nametowidget("o")
    list = [i.split("   ")[-1] for i in o.get("1.0", "end").split("\n") if i]
    song_queue = list
    recency_stack = []

    if (len(song_queue) > 0):
        load_song(song_queue[0])

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

    slider.set_pos(0)
    slider.unbind()

    mixer.music.unload()
    mixer_loaded = False

    return song_txt

def load_song(song_name=None, progress=0):
    global mixer_loaded

    # display the song on the ui & configure the mixer
    song_txt = unload_song(keep_enabled=True)

    song_txt.insert("end", song_name)
    song_txt.config(state="disabled")

    current_song["name"] = song_name
    current_song["length"] = MP3(f"songs/{song_name}.mp3").info.length

    try:
        mixer.music.load(f"songs/{song_name}.mp3")
        mixer_loaded = True
    except Exception as e: print(e)

    slider.bind(set_song_pos)

def play_song(song=None, autoplay_disabled=False):
    # stop_song()
    # if (autoplay_disabled == False):
    #     mixer.music.play()
    pass

def play_btn_pressed(event):
    pass

def music_ended():
    pass