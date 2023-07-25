from util import *
from settings import change_setting, settings
from audio import *
from slider import class_from_bg
import pygame
import os

pygame.init()

update_ms = 250
def update(root):
    for event in pygame.event.get():
        if event.type == 25:
            music_ended(fn=update_song_display)

    if ((current_song["name"] != None) and (current_song["playing"] == True)):
        slider = class_from_bg(root.nametowidget("bot_bar").nametowidget("progress_slider_bg"))
        add_val = (update_ms/1000) / current_song["length"]
        slider.set_pos(slider.progress + add_val)

    root.after(update_ms, update, root)

def color_btn(btn, bool):
    if (bool):
        btn.config(bg="white", fg="#131313")
    else:
        btn.config(fg="white", bg="#131313")

def btn_status(event):
    btn = event.widget
    
    # change in settings
    setting = "queue_looped" if (btn.cget("text") == "L") else "playlist_shuffled"
    new_state = not (settings[setting] == "True")
    change_setting(setting, str(new_state))
    color_btn(btn, new_state)

def update_song_display(o, tbr, playlist):
    o.config(state="normal")

    try:
        o.delete("1.0", "end")
    except Exception as e:
        print(e)

    # song names (for a playlist)
    if (playlist == "playlists/$default$.txt"):
        #default playlist (add all songs in songs folder)
        file_list = os.listdir("songs")
        total_spaces = get_num_spaces(len(file_list))
        i = 1
        for file in file_list:
            song_name = file.split(".")[0]
            offset_space = get_num_spaces(i)
            song_display = (" "*(total_spaces - offset_space)) + str(i) + "   " + song_name + "\n"
            o.insert("end", song_display)
            i += 1
    elif (playlist == "data/queue.txt"):
        # use q from audio
        i = 1
        total_spaces = get_num_spaces(len(queue))
        for song_name in queue:
            offset_space = get_num_spaces(i)
            song_display = (" "*(total_spaces - offset_space)) + str(i) + "   " + song_name + "\n"
            o.insert("end", song_display)
            i += 1
    else:
        # any other arb playlist
        f = open_file(playlist, "r")
        i = 1
        list = f.read().splitlines()
        total_spaces = get_num_spaces(len(list))
        for line in list:
            offset_space = get_num_spaces(i)
            song_display = (" "*(total_spaces - offset_space)) + str(i) + "   " + line + "\n"
            o.insert("end", song_display)
            i += 1

    o.config(state="disabled")

    # top bar 
    title = "YOUR QUEUE" if (playlist == "data/queue.txt") else playlist.split("/")[1].split(".")[0]
    btn = tbr.master.nametowidget("playlist_playbtn")

    if (playlist != "data/queue.txt"):
        btn.place(relheight=1, relwidth=0.1, relx=0.14)
    else:
        btn.place_forget()

    set_open_tab(title)
    tbr.config(text=title)

def start_playback(event, playImg=None, pauseImg=None):
    playlist = event.widget.master.winfo_children()[1].cget("text")
    create_queue(f"playlists/{playlist}.txt", playImg=playImg, pauseImg=pauseImg)