import pygame, sys, random, math, datetime
from pygame.locals import *
from dataclasses import dataclass, fields
from typing import Optional
from PIL import Image

# Global Constants

# Colours
PURE_WHITE = (255,255,255)
PURE_BLACK = (0,0,0)
RED = (250,0,0)



# Global Variables
res_x = 1024
res_y = res_x
timelapse_mode = False

def CheckMandelbrot(point: tuple, is_julia: bool):
    if(is_julia):
        cx = zx
        cy = zy
        x = point[0]
        y = point[1]
    else:
        cx = point[0]
        cy = point[1]
        x = zx
        y = zy
    iteration = 0
    max_iterations = 700
    while(x*x + y*y <= 2*2 and iteration < max_iterations):
        new_x = (x*x) - (y*y) + cx
        y = (2*x*y) + cy
        x = new_x
        iteration += 1
    if(iteration == max_iterations):
        return(PURE_BLACK)
    else:
        color = round(50+715*iteration/max_iterations)
        while(color > 765):
            color -= 255
        if(color > 255):
           if(color > 510):
               return((255-color%510,color%510,0))
           return((color%255,0,255-color%255))
        return((0,0,color))

def GenMandelbrot(zoom: float):
    for ix in range(round(-gridx/2),round(gridx/2)):
        for iz in range(round(-gridz/2),round(gridz/2)):
            #print(CheckMandelbrot((((ix+zoomx)/(gridx*zoom)),(iz+zoomz)/(gridz*zoom)), False))
            DISPLAYSURF.set_at((ix+round(gridx/2),iz+round(gridz/2)), CheckMandelbrot((((ix+zoomx)/(gridx*zoom)),(iz+zoomz)/(gridz*zoom)), False))

def GenMandelbrotImage(zoom: float):
    pixels = []
    for ix in range(round(-gridx/2 + zoomx),round(gridx/2 + zoomx)):
        for iz in range(round(-gridz/2 + zoomz),round(gridz/2 + zoomz)):
            pixels.append(CheckMandelbrot(((ix/(gridx*zoom)),iz/(gridz*zoom)), False))
        if(ix%100 == 0):
            print(f"{ix}")
    
    im2 = Image.new("RGB", (gridx,gridz))
    im2.rotate(-90)
    im2.putdata(pixels)
    im2.save(f"tempvideofolder/image{images_produced}.jpg")

# Setup stuff.
pygame.init()
DISPLAYSURF = pygame.display.set_mode((res_x, res_y), RESIZABLE)
pygame.display.set_caption("Fractal")

# Loads and sets fonts.
pygame.font.init()
my_font = pygame.font.SysFont("Agency FB", 30)

images_produced = 0

gridx = DISPLAYSURF.get_width()
gridz = DISPLAYSURF.get_height()

zoom = 0.125
true_zoomx = (262.000000014993/500)
true_zoomz = (250.90000001/500)
zoomx = 0
zoomz = 0

for x in range(0):
    zoom = round(zoom*1.25, 3)

high_res = res_x

zx = 0
zy = 0

display_live = True
debug_mode = False

while True: # Main game loop.
    if(display_live):
        gridx = DISPLAYSURF.get_width()
        gridz = DISPLAYSURF.get_height()

        zoom = round(zoom*1.25, 3)
        #zx -= 0.01
        #zy += 0.02
        zoomx = round(-gridx * true_zoomx * zoom)
        zoomz = round(-gridz * true_zoomz * zoom)

        GenMandelbrot(zoom)

        if(debug_mode):
            pygame.draw.line(DISPLAYSURF, RED, (DISPLAYSURF.get_width()/2, 0), (DISPLAYSURF.get_width()/2, DISPLAYSURF.get_height()), 3)
            pygame.draw.line(DISPLAYSURF, RED, (0, DISPLAYSURF.get_height()/2), (DISPLAYSURF.get_width(), DISPLAYSURF.get_height()/2), 3)


        #text_surface = my_font.render(f"Zoom: {zoom}", False, (255, 255, 255))
        #DISPLAYSURF.blit(text_surface, (0,0))
        pygame.display.update()
        pygame.image.save(DISPLAYSURF, f"tempvideofolder/image{images_produced}.jpg")
        images_produced += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if(event.key == pygame.K_F2):
                    pygame.image.save(DISPLAYSURF, f"screenshots/screenshot {str(datetime.datetime.now()).replace(":", "")}.png")
                    print("Screenshot Saved")
                if(event.key == pygame.K_F3):
                    print(f"Zoom: {zoom}")
                if(event.key == pygame.K_0):
                    print(pygame.mouse.get_pos())
    else:
        gridx = high_res
        gridz = high_res

        zoom = round(zoom*1.25, 3)
        zoomx = round(-high_res * true_zoomx * zoom)
        zoomz = round(-high_res * true_zoomz * zoom)

        GenMandelbrotImage(zoom)
        images_produced += 1