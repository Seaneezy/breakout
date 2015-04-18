import pygame
from pygame.locals import *
from sys import exit

background_image_filename='welcome.jpg'
mouse_image_filename='minecraft.png'

_W=1280
_H=840

pygame.init()
screen=pygame.display.set_mode([_W,_H])
pygame.display.set_caption("Hello,World!")
background=pygame.image.load(background_image_filename).convert()
mouse_cursor = pygame.image.load(mouse_image_filename).convert_alpha()

font=pygame.font.Font(None, 72)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.blit(background, (0,0))
    x,y=pygame.mouse.get_pos()
    x-mouse_cursor.get_width()/2
    y-=mouse_cursor.get_height()/2
    text=font.render(str(pygame.mouse.get_pos()), True, (255,255,255))
    textPos=text.get_rect(centerx=background.get_width()/2)
    textPos.top=20
    #screen.blit(mouse_cursor, (x,y))
    screen.blit(text, (textPos))
    pygame.display.update()







"""
#pos=pygame.mouse.get_pos()
screenW=800
screenH=600
pygame.init()
screen=pygame.display.set_mode([screenW,screenH])
clock=pygame.time.Clock()
exit_program=False
while exit_program != True:
    clock.tick(45)

    for event in pygame.event.get():
        #if you quit the game via window closure, exit_program is TRUE
        if event.type ==pygame.QUIT:
            exit_program=True
"""