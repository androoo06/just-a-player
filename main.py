from tkinter import *
from PIL import Image, ImageTk
from settings import write_settings, read_settings, settings
from slider import Slider
from main_events import *
from audio import *

root = Tk()
root.state("zoomed") # auto-maximize

screen_width  = root.winfo_screenwidth()
screen_height = root.winfo_screenheight() - 80
height_dim  = int(screen_height * 0.1)
height_dim2 = int(screen_height * 0.15)

#### create elements ####

playImg = ImageTk.PhotoImage(Image.open("media/playBtn.png").resize((height_dim, height_dim), Image.ANTIALIAS))
pauseImg = ImageTk.PhotoImage(Image.open("media/pauseBtn.png").resize((height_dim, height_dim), Image.ANTIALIAS))
volumeImg = ImageTk.PhotoImage(Image.open("media/volume.png").resize((int(height_dim2/2), int(height_dim2/2)), Image.ANTIALIAS))

display_playlist = Text(root, background='#131313', foreground="white", borderwidth=0, name="display_playlist")
select_playlist = Text(root, background='#131313', foreground="white", borderwidth=0)
top_bar_left = Entry(root, font=("Cascadia Mono SemiBold", 24, 'underline'), background='#131313', foreground='white', borderwidth=0, justify='center', disabledbackground="#131313", disabledforeground="white")
top_bar_right = Frame(root, background='#131313', borderwidth=0, name="top_bar_right")
bot_bar = Entry(root, font=("Cascadia Mono SemiBold", 24), background='#131313', foreground='white', borderwidth=0, justify='center', disabledbackground="#131313", disabledforeground="white", name="bot_bar")

plb = Button(top_bar_right, font=("Cascadia Mono SemiBold", 24, 'underline'), bg="#131313", fg="white", bd=0, image=playImg, name="playlist_playbtn")
pll = Label(top_bar_right, font=("Cascadia Mono SemiBold", 24, 'underline'), bg="#131313", fg="white", bd=0, text="YOUR QUEUE", name="playlist_label")
o = Text(display_playlist, font=("Cascadia Mono SemiBold", 24), background='#1b1b1b', foreground="white", border=0, name="o")
l = Text(select_playlist, background='#1b1b1b', borderwidth=0)
p = Button(bot_bar, image=playImg, relief="solid", bg="#131313", bd=0, name="p_btn")
r = Button(bot_bar, font=("Cascadia Mono SemiBold", 24, 'underline'), text="<<", bg="#131313", bd=0, fg="white", name="rewind_btn")
s = Button(bot_bar, font=("Cascadia Mono SemiBold", 24, 'underline'), text=">>", bg="#131313", bd=0, fg="white", name="skip_btn")
sq = Button(bot_bar, font=("Cascadia Mono SemiBold", 24, 'underline'), text="S", bg="#131313", bd=0, fg="white", name="shuffle_queue")
ls = Button(bot_bar, font=("Cascadia Mono SemiBold", 24, 'underline'), text="L", bg="#131313", bd=0, fg="white", name="loop_queue")
st = Text(bot_bar, font=("Cascadia Mono SemiBold", 24, 'underline'), bg="#131313", fg="white", bd=0, name="song_text")
vl = Label(bot_bar, bg="#131313", image=volumeImg)
qb = Button(bot_bar, font=("Cascadia Mono SemiBold", 24, 'underline'), text="Q", bg="#131313", bd=0, fg="white", name="open_queue_btn")

ps = Slider(bot_bar, name="progress_slider_bg").place({"width":height_dim*5, "height":height_dim/2, "x":int(screen_width/2 - (height_dim/2)) - (height_dim*2), "y":height_dim})
ps.bg.config(bg="#131313")
ps.trough.place(relheight=0.7, relwidth=1, rely=0.15, relx=0)
ps.trough.config(bg="#454545")
ps.trough_progress.config(bg="#eeeeee")

v = Slider(bot_bar).place({"relwidth": 0.2,"height": int(height_dim2 / 2),"relx": 0.79,"y": int(height_dim2 / 4)}).bind(func=change_volume)
v.bg.config(bg="#131313")
v.trough.place(relheight=0.7, relwidth=1, rely=0.15, relx=0)
v.trough.config(bg="#454545")
v.trough_progress.config(bg="#eeeeee")

#### place elements ####

display_playlist.place(relheight=0.75, relwidth=0.7, rely=0.1, relx=0.3)
select_playlist.place(relheight=0.75, relwidth=0.3, rely=0.1, relx=0)
top_bar_left.place(relheight=0.1, relwidth=0.3, relx=0, rely=0)
top_bar_right.place(relheight=0.1, relwidth=0.7, relx=0.3, rely=0)
bot_bar.place(relheight=0.15, relwidth=1, relx=0, rely=0.85)

pll.place(relheight=1, relwidth=0.4, relx=0.25)
o.place(relheight=0.9, relwidth=0.9, rely=0.05, relx=0.05)
l.place(relheight=0.9, relwidth=0.9, rely=0.05, relx=0.05)
p.place(width=height_dim, height=height_dim, x=int(screen_width/2 - height_dim/2))
r.place(width=height_dim, height=height_dim, x=int(screen_width/2 - (height_dim/2) - height_dim - 15))
s.place(width=height_dim, height=height_dim, x=int(screen_width/2 - (height_dim/2) + height_dim + 15))
sq.place(width=height_dim, height=height_dim, x=int(screen_width/2 - (height_dim/2) - ((2*height_dim)) - 30))
ls.place(width=height_dim, height=height_dim, x=int(screen_width/2 - (height_dim/2) + ((2*height_dim)) + 30))
vl.place(height=int(height_dim2/2), y=int(height_dim2/4), width=int(height_dim2/2), relx=0.75)
qb.place(height=int(height_dim2/2), y=int(height_dim2/4), width=int(height_dim2/2), relx=0.69)
st.place(relwidth=0.33, relx=0, height=int(height_dim2/2), y=int(height_dim2/4))

#### bind elements ####

sq.bind("<Button-1>", shuffle_queue)
ls.bind("<Button-1>", btn_status)
qb.bind("<Button-1>", get_fn())
plb.bind("<Button-1>", create_queue)
p.bind("<Button-1>", play_btn_pressed)
r.bind("<Button-1>", rewind_song)
s.bind("<Button-1>", skip_song)

#### on startup ####
mixer.music.set_volume(settings["volume"])
set_data(
    _slider=ps, 
    _root=root,
    _playImg=playImg,
    _pauseImg=pauseImg,
    _update_song_display=get_fn()
)

color_btn(ls, settings["queue_looped"]=="True")

for file in os.listdir("playlists"):
    name = file.split(".")[0]
    if (name == ""): continue
    btn1 = Button(l, font=("Cascadia Mono SemiBold", 16), background='#1b1b1b', foreground="white", bd=0, text=name, width=10, anchor="w", name=name)
    l.window_create("end", window=btn1)
    l.insert("end", "\n")
    btn1.bind("<Button-1>", get_fn())
l.configure(state="disabled")

top_bar_left.insert("end", "SELECT PLAYLIST")
top_bar_left.config(state="disabled")

v.set_pos(settings["volume"])

# configure the root window
root.title('Just a Player')
root['bg'] = '#131313'

# main loop
on_start() # for the audio
root.after(0, update, root)
root.mainloop()

# save data on close
if (len(song_queue) > 0):
    pos = current_song["position"]
    song_queue[0] += f",position={pos}"

write_settings()
write_list_to_file(song_queue, "data/queue.txt")
write_list_to_file(recency_stack, "data/stack.txt")