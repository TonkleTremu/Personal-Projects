import pygame, sys, math, random
from pygame.locals import *

# Setup stuff.
res_x = 1080
res_y = 720
pygame.init()
DISPLAYSURF = pygame.display.set_mode((res_x, res_y))
pygame.display.set_caption("Frictionless Pendulum")
fpsClock = pygame.time.Clock()

# Colours
PURE_WHITE = (255,255,255)
PURE_BLACK = (0,0,0)
PURE_RED = (255,0,0)
NIGHT_SKY_BLUE = (10,20,140)
MINT = (61, 255, 171)
GRAY = (124,125,127)
SUNSET = (250, 100, 10)

# Objects
double_pendulum_size = 50
pendulums = 80
pendulum_ends = [(res_x/2,res_y/2)]
pendulum_rotations = [0]
pendulum_speeds = [0]

# Loads and sets fonts.
pygame.font.init()
my_font = pygame.font.SysFont("Agency FB", 30)

for pendulum in range(1,pendulums+1):
    pendulum_ends.append((0,0))
    pendulum_rotations.append(0)
    if(pendulum%2==0):
        pendulum_speeds.append(random.random()/10)
    else:
        pendulum_speeds.append(-random.random()/10)

DISPLAYSURF.fill(NIGHT_SKY_BLUE)
uni_color = (255,255,255)
directions = [0,0,0]

# Stuff used for recording.
record_screen = False
images_produced = 0

while True: # Main game loop.
    #DISPLAYSURF.fill(NIGHT_SKY_BLUE)
    temp_uni_color = []
    count = 3
    for color in uni_color:
        if(color - count > 0 and directions[count-1] == 0):
            temp_uni_color.append(color - count)
        elif(color + count < 255 and directions[count-1] == 1):
            temp_uni_color.append(color + count)
        elif(directions[count-1] == 1 and color + count >= 255):
            temp_uni_color.append(255)
            directions[count-1] = 0
        else:
            temp_uni_color.append(0)
            directions[count-1] = 1
        count -= 1
    uni_color = temp_uni_color
    for p in range(1,pendulums+1):
        pendulum_ends[p] = (math.cos(pendulum_rotations[p])*double_pendulum_size + pendulum_ends[p-1][0], math.sin(pendulum_rotations[p])*double_pendulum_size + pendulum_ends[p-1][1])
        pendulum_rotations[p] += pendulum_speeds[p]
        pygame.draw.line(DISPLAYSURF, uni_color, pendulum_ends[p], pendulum_ends[p-1], 10)
    #pygame.draw.circle(DISPLAYSURF, (GRAY), pendulum_ends[-1], 20)
    pygame.display.update()
    if(record_screen):
        pygame.image.save(DISPLAYSURF, f"tempvideofolder/image{images_produced}.png")
        images_produced += 1
    fpsClock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()