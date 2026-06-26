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

@dataclass
class GameObject:
    # The xz location values.
    x: float
    z: float

    # The object's color. By default, it is Sunset.
    color: Optional[tuple] = SUNSET


def RenderPoint(color, point):
        DISPLAYSURF.set_at(point, color)

def GenGrid():
    for ix in range(0,gridx):
        row = []
        for iz in range(0,gridz):
            cur_go = GameObject(ix, iz, color=PURE_WHITE)
            grid_objects.append(cur_go)
            row.append(cur_go)
        grid.append(row)

def GenTartanGrid(para1, para2, para3, para4):
    for ix in range(0,gridx):
        row = []
        for iz in range(0,gridz):
            if(ix % para1 == para3 and iz % para2 == para4):
                cur_go = GameObject(ix, iz, color=PURE_WHITE)
            else:
                cur_go = GameObject(ix, iz, color=PURE_BLACK)
            grid_objects.append(cur_go)
            row.append(cur_go)
        grid.append(row)
    
def GenInvTartanGrid(para1, para2, para3, para4):
    for ix in range(0,gridx):
        row = []
        for iz in range(0,gridz):
            if(ix % para1 == para3 or iz % para2 == para4):
                cur_go = GameObject(ix, iz, color=PURE_WHITE)
            else:
                cur_go = GameObject(ix, iz, color=PURE_BLACK)
            grid_objects.append(cur_go)
            row.append(cur_go)
        grid.append(row)
    
def GenCheckeredGrid(para1, para2):
    for ix in range(0,gridx):
        row = []
        for iz in range(0,gridz):
            if(ix % para1 == iz % para2):
                cur_go = GameObject(ix, iz, color=PURE_WHITE)
            else:
                cur_go = GameObject(ix, iz, color=PURE_BLACK)
            grid_objects.append(cur_go)
            row.append(cur_go)
        grid.append(row)
    
def GenRandomGrid(para1):
    for ix in range(0,gridx):
        row = []
        for iz in range(0,gridz):
            if(random.randint(0,para1) == 0):
                cur_go = GameObject(ix, iz, color=PURE_WHITE)
            else:
                cur_go = GameObject(ix, iz, color=PURE_BLACK)
            grid_objects.append(cur_go)
            row.append(cur_go)
        grid.append(row)

def GenDecimalGrid(para1, para2):
    for ix in range(0,gridx):
        row = []
        for iz in range(0,gridz):
            if(ix % 10 == para1 and iz % 10 == para2):
                cur_go = GameObject(ix, iz, color=PURE_BLACK)
            else:
                cur_go = GameObject(ix, iz, color=PURE_WHITE)
            grid_objects.append(cur_go)
            row.append(cur_go)
        grid.append(row)

def MoveAnt(antdir):
    # If an ant goes out of bounds, this throws an error.
    if(langsant.x < 0 or langsant.z < 0):
        raise(IndexError)
    
    if(antdir < 0):
        antdir = 3
    elif(antdir > 3):
        antdir = 0
    match antdir:
        case 0:
            langsant.x -= 1
        case 1:
            langsant.z -= 1
        case 2:
            langsant.x += 1
        case 3:
            langsant.z += 1

    square = grid[langsant.x][langsant.z]
    if(square.color == PURE_WHITE):
        square.color = PURE_BLACK
        antdir -= 1
    elif(square.color == PURE_BLACK):
        square.color = PURE_WHITE
        antdir += 1
    return(antdir)

def MoveAntWithSkips(antdir):
    square = grid[langsant.x][langsant.z]

    # If an ant goes out of bounds, this throws an error.
    if(langsant.x < 0 or langsant.z < 0):
        raise(IndexError)
    
    if(antdir < 0):
        antdir = 3
    elif(antdir > 3):
        antdir = 0
    if(square.color == GRAY):
        places = -1
    else:
        places = 1
    match antdir:
        case 0:
            langsant.x -= places
        case 1:
            langsant.z -= places
        case 2:
            langsant.x += places
        case 3:
            langsant.z += places

    if(square.color == PURE_WHITE):
        square.color = PURE_BLACK
        antdir -= 1
    elif(square.color == PURE_BLACK):
        square.color = GRAY
        antdir += 1
    elif(square.color == GRAY):
        square.color = PURE_WHITE
    return(antdir)



# Resx,Resy,GridType,Para1,Para2,Para3,Para4,Prewarm
code = input("What is the code?\n").split(",")
res_x = int(code[0])
res_y = int(code[1])
para1 = int(code[3])
para2 = int(code[4])
para3 = int(code[5])
para4 = int(code[6])
prewarm = int(code[7])

try:
    timelapse_mode = bool(code[8])
    print(bool(code[8]))
except:
    print("No 9th parameter input.")

# Setup stuff.
pygame.init()
DISPLAYSURF = pygame.display.set_mode((res_x, res_y))
pygame.display.set_caption("Langton's Ant")
fpsClock = pygame.time.Clock()

# Loads and sets fonts.
pygame.font.init()
my_font = pygame.font.SysFont("Agency FB", 30)

grid = []
grid_objects = []

gridx = res_x
gridz = res_y

match code[2]:
    case "0":
        GenGrid()
    case "1":
        GenCheckeredGrid(para1,para2)
    case "2":
        GenDecimalGrid(para1,para2)
    case "3":
        GenTartanGrid(para1,para2,para3,para4)
    case "4":
        GenInvTartanGrid(para1,para2,para3,para4)
    case "5":
        GenRandomGrid(para1)

langsant = GameObject(int(res_x/2), int(res_y/2), color=SUNSET)
langsantdir = 0
iterations = 0
images_produced = 0
reached_border = False
grid_objects.append(langsant)

for x in range(prewarm):
    try:
        langsantdir = MoveAnt(langsantdir)
        iterations += 1
    except:
        print("The Ant has broke containment.")
        break

while True: # Main game loop.
    if(not(timelapse_mode)):
        DISPLAYSURF.fill(NIGHT_SKY_BLUE)
        for go in grid_objects:
            RenderPoint(go.color, (go.x,go.z))
        pygame.display.update()
    if(timelapse_mode and iterations % 60 == 0):
        for go in grid_objects:
            RenderPoint(go.color, (go.x,go.z))
        text_surface = my_font.render(f"Iterations: {iterations}", False, (0, 0, 0))
        DISPLAYSURF.blit(text_surface, (0,0))
        pygame.display.update()
        pygame.image.save(DISPLAYSURF, f"tempvideofolder/image{images_produced}.jpg")
        images_produced += 1
        #print(f"Time is {datetime.datetime.now()}\nIterations: {iterations}")

    try:
        langsantdir = MoveAnt(langsantdir)
        iterations += 1
    except:
        if(reached_border == False):
            print("The Ant has broke containment.")
            reached_border = True
            pygame.image.save(DISPLAYSURF, f"screenshots/screenshot {str(datetime.datetime.now()).replace(":", "")}.png")
            print(f"Time is {datetime.datetime.now()}\nIterations: {iterations}")

    fpsClock.tick(TICK_RATE)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if(event.key == pygame.K_F2):
                pygame.image.save(DISPLAYSURF, f"screenshots/screenshot {str(datetime.datetime.now()).replace(":", "")}.png")
                print(f"Time is {datetime.datetime.now()}\nIterations: {iterations}")
            if(event.key == pygame.K_F3):
                print(iterations)
                print(langsant)
            if(event.key == pygame.K_m):
                timelapse_mode = not timelapse_mode
                