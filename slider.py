# making a custom slider class using tkinter stuff

import tkinter as tk
from util import clamp

created_sliders = []

def class_from_bg(bg):
    for slider in created_sliders:
        if (slider.bg == bg):
            return slider

class Slider:
    def __init__(self, parent, bg=None, trough=None, trough_progress=None, name=None):
        #, min_text=None, max_text=None
        self.bg = bg or tk.Frame(parent, name=name)
        self.trough = trough or tk.Frame(self.bg)
        self.trough_progress = trough_progress or tk.Frame(self.trough)
        self.progress = 0
        #self.min_text = min_text or tk.Entry(self.bg)
        #self.max_text = max_text or tk.Entry(self.bg)
        created_sliders.append(self)

    # places all elements (otherwise use respective place methods)
    # chainable
    def place(self, *options):
        self.bg.place(*options)
        self.trough.place(relheight=1, relwidth=1, relx=0, rely=0)
        self.trough_progress.place(relheight=1, relwidth=0, relx=0, rely=0)
        
        return self

    # chainable
    def bind(self, func=None):
        self.unbind()
        self.__bind__("<B1-Motion>")
        self.__bind__("<Button-1>")
        self.__changecallback__ = func
        return self
    
    # chainable
    def unbind(self):
        self.__unbind__("<B1-Motion>")
        self.__unbind__("<Button-1>")
        self.__changecallback__ = None
        return self
    
    # chainable [not implemented]
    def display_text(self, bool=False):
        print("display_text not implemented")
        return self

    # chainable [not implemented]
    def set_text(self, min=0, max=180):
        print("set_text not implemented")
        return self

    # chainable
    def set_pos(self, percent):
        percent = clamp(percent, 0, 1)
        if (percent == 0):
            if (hasattr(self, "old_bg_color") and (self.old_bg_color != self.trough_progress.cget("bg"))):
                self.old_bg_color = self.trough_progress.cget("bg")
            self.trough_progress.config(bg=self.trough.cget("bg"))
        else:
            self.trough_progress.config(bg=(self.old_bg_color if (hasattr(self, "old_bg_color")) else "#eeeeee"))
            self.trough_progress.place(relheight=1, relwidth=percent, relx=0, rely=0)
        self.progress = percent

        return self

    ##### util functions #####

    # not recommended to modify but plausible
    # fires when user interacts with slider
    def on_change(self, event):
        width = self.trough.winfo_width()
        percent = clamp(event.x / width, 0, 1)
        self.set_pos(percent)
        
        if (self.__changecallback__ != None):
            self.__changecallback__(percent)

    # wrapper actual bind function (bind() is a wrapper for this)
    def __bind__(self, sequence):
        self.trough.bind(sequence=sequence, func=self.on_change)
        self.trough_progress.bind(sequence=sequence, func=self.on_change)

    # wrapper actual unbind function (unbind() is a wrapper for this)
    def __unbind__(self, sequence):
        self.trough.unbind(sequence=sequence)
        self.trough_progress.unbind(sequence=sequence)

# temporary tkinter program for testing #
# root = tk.Tk()
# root.config(bg="black")
# root.state("zoomed")
# ------------------------------------- #

# def tf(percent):
#     print(percent)

# t = Slider(root).place({"relx":0.25, "rely":0.5, "relwidth":0.25, "relheight":0.1}).bind(func=tf).display_text(True)
# t.trough.config(bg="#454545")
# t.trough_progress.config(bg="#eeeeee")

# ------------------------------------- #
# root.mainloop()