import pygame
from pygame import mixer
from time import sleep

pygame.init()
mixer.init()

MUSIC_END = pygame.USEREVENT+1

# mixer.music.load("songs/moo.mp3")
# mixer.music.set_endevent(MUSIC_END)
# mixer.music.set_volume(0.7)
# mixer.music.play()

def check_event():
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            print('music end event')
            return True
        if event.type == pygame.KEYDOWN:
            print(event.key)
            return True

while (not check_event()):
    sleep(0.25)
 
print('a')