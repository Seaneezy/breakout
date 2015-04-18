import pygame
from pygame.locals import *
from sys import exit

background_image_filename='welcome.jpg'
mouse_image_filename='minecraft.png'

_W=640
_H=340

pygame.init()
screen=pygame.display.set_mode([_W,_H])
pygame.display.set_caption("Hello World!")
background=pygame.image.load(background_image_filename).convert()
mouse_cursor=pygame.image.load(mouse_image_filename).convert_alpha()

while True:
    for event in pygame.event.get():
        if event.type==pygame.quit:
            exit()

    screen.blit(background, (0,0))
    x,y = pygame.mouse.get_pos()
    x-=mouse_cursor.get_width()/2
    y-=mouse_cursor.get_height()/2
    screen.blit(mouse_cursor, (x,y))

    pygame.display.update()
"""
anaraugh makes easter themed brick breaker, ball is an egg
douglas has confetti appear after 10 bricks are broken
kintien has fireworks appear after 10 bricks are broken
karthik has power brick that doubles paddle size
sean has a power brick that doesnt dissappear but falls down and will double paddle size if you catch the brick
"""
