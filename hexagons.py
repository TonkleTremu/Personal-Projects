import pygame, sys, random, math, datetime
from pygame.locals import *
from dataclasses import dataclass, fields
from typing import Optional

# Global Constants
# Reduce to 30 if performance is very poor.
TICK_RATE = 60

# Colours
PURE_WHITE = (255,255,255)
PURE_BLACK = (0,0,0)
PURE_RED = (255,0,0)
NIGHT_SKY_BLUE = (10,20,140)
MINT = (61, 255, 171)
GRAY = (124,125,127)
SUNSET = (250, 100, 10)

# Global Variables
res_x = 250
res_y = 250
timelapse_mode = False


def RenderPoint(color, point):
        DISPLAYSURF.set_at(point, color)

# Setup stuff.
pygame.init()
DISPLAYSURF = pygame.display.set_mode((res_x, res_y))
pygame.display.set_caption("Langton's Ant")
fpsClock = pygame.time.Clock()
hexagon = pygame.image.load('hexagon.png')

while True: # Main game loop.
    DISPLAYSURF.fill(NIGHT_SKY_BLUE)
    x = 0
    y = 0
    while(y < DISPLAYSURF.get_height()):
        while(x < DISPLAYSURF.get_width()):
            DISPLAYSURF.blit(hexagon, (x,y))
            x+=16
        y+=16

    pygame.display.update()
    fpsClock.tick(TICK_RATE)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if(event.key == pygame.K_F2):
                pygame.image.save(DISPLAYSURF, f"screenshots/screenshot {str(datetime.datetime.now()).replace(":", "")}.png")
                