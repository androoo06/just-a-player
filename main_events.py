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
            music_ended()

    if ((current_song["name"] != None) and (mixer.get_busy() == True)):
        add_val = (update_ms/1000) / current_song["length"]
        slider.set_pos(slider.progress + add_val)

    root.after(update_ms, update, root)

def on_start():
    update_song_display(None, override=True) # load queue elements
    if (len(song_queue) > 0):
        load_song(song_name = song_queue[0])

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

def clear_song_display():
    open_box = get_root().nametowidget("display_playlist").nametowidget("o")
    open_box.config(state="normal")

    try:
        open_box.delete("1.0", "end")
    except Exception as e:
        print(e)

    return open_box

def update_song_display(event, override=False):
    btn_name = "open_queue_btn" if (override) else str(event.widget).split(".")[-1]
    playlist = "queue" if (btn_name == "open_queue_btn") else f"playlists/{btn_name}.txt"
    
    song_list = song_queue
    if (playlist == "playlists/$default$.txt"):
        song_list = os.listdir("songs")
        for i in range(len(song_list)): 
            song_list[i] = song_list[i].split(".")[0]
        song_list = song_list[1:] # to ignore the .gitignore haha
    elif (playlist != "queue"):
        song_list = read_file_as_list(playlist)

    open_box = clear_song_display()

    total_spaces = get_num_spaces(len(song_list))
    for i in range(len(song_list)):
        offset_space = get_num_spaces(i+1)
        song_display = (" "*(total_spaces - offset_space)) + str(i+1) + "   " + song_list[i] + "\n"
        open_box.insert("end", song_display)

    open_box.config(state="disabled")

    # top bar 
    top_bar_right = get_root().nametowidget("top_bar_right")
    playlist_label = top_bar_right.nametowidget("playlist_label")
    playlist_playbtn = top_bar_right.nametowidget("playlist_playbtn")

    if (playlist != "queue"):
        playlist_playbtn.place(relheight=1, relwidth=0.1, relx=0.14)
    else:
        playlist_playbtn.place_forget()

    title = "YOUR QUEUE" if (playlist == "queue") else playlist.split("/")[1].split(".")[0]
    set_data(_open_tab=title)
    playlist_label.config(text=title)