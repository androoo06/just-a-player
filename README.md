# Just a Player

Music player to play mp3 songs on your pc (that have been legally obtained!) in such a way that resembles other popular applications, like Spotify.

This was created as a fun project to familiarize myself with various concepts and frameworks.


# The __Application__ folder

This folder is where all the files are compiled. This is the only folder you need on your system to use this application (run the .exe and as long as the folders are in the same directory there shouldn't be any problems). Configuration of all of these files are listed throughout this document. 

## Data

The data folder contains the 3 main files the application uses to store/cache your data. Mess with these as you wish:

### __queue.txt__ is your upcoming song list

The first entry of this file will be different than the rest. To save the current song's position upon closing, the first entry of __queue.txt__ is appended with ",position=" followed by the position represented as a float (percentage from 0 to 1).

### __stack.txt__ is your previous song list

Each entry is a string containing the exact name of the mp3 song it correpsonds to

### __settings.txt__ is your settings

There are 2 settings as of right now: __queue_looped__, and __volume__. These can be changed in-app or through the file. Changes in file will be reflected once the file is saved and the application is reopened.

### __The playlists folder__ 
This folder contains your playlists: text files (the name of these is the name of your playlist). It is formatted most similarly to __stack.txt__. It is not recommended to touch the __$default$__ playlist (as this will contain all your songs), but doing so should not raise an error.

### __The songs folder__
This folder is where all of your mp3's should be stored. Use the names of these songs in the other files to reference them.

## Usage

Configuring playlists is as easy as adding a .txt file to the playlists folder and entering the song names you'd like to add

In-app, click a playlist on the left to open its songs on the right. Click the play button above the list to play that playlist. This will delete the current queue & stack.

The '__S__' button refers to queue shuffling. Clicking this will shuffle the current queue and remove all songs in the stack (by creating a new queue)

The '__L__' button refers to queue looping. Enabling this will loop the current queue once it has completed. Disabling will have the opposite effect.

The '__Q__' button opens the current queue.

The rest is fairly intuitive (__pausing__/__playing__, __skipping__/__rewinding__)

## slider.py

I made a custom slider class in slider.py that allows for tkinter customization to its elements, and allows for a callback on change (the file itself contains a demo of its usage). Has a few basic methods to work with as well. (This is because tkinter's "Scale" element is not visually appealng in my opinion and quite a pain to customize.)