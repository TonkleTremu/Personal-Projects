import pygame, sys, random, math, datetime
from pygame.locals import *
from dataclasses import dataclass, fields
from typing import Optional

# Set to false for distributions.
DEBUG = True

# Global Variables
res_x = 400
res_y = 300

# Global Constants
TICK_RATE = 60
GRAVITY = -3

# Colours
PURE_WHITE = (255,255,255)
PURE_BLACK = (0,0,0)
PURE_RED = (255,0,0)
RED = (250,5,5)
GREEN = (5,250,5)
FAUX_GREEN = (5,140,70)
NIGHT_SKY_BLUE = (10,20,140)
LAVENDER = (135,110,170)
BLUE = (5,5,250)
MINT = (61, 255, 171)
GRAY = (124,125,127)
BROWN = (87,54,0)
DELICIOUS_BLUE = (26,251,255)
CRIMSON = (100, 5, 5)

# World's X and Y size values. Mainly used for scaling.
worldSizeX = 100
worldSizeY = 100

# "Display Surface" - this is where all the stuff is rendered to. 
DISPLAYSURF = pygame.display.set_mode((res_x, res_y), pygame.RESIZABLE)

@dataclass
class GameObject:
    # The x and y size values. Used for physics-based collisions.
    x_size: float 
    y_size: float
    id: str

    # The game object's current co-ordinates.
    x: Optional[float] = 0 
    y: Optional[float] = 0

    color: Optional[tuple] = PURE_BLACK # The object's color. Only used if it is a basic algorithmic shape.
    shape: Optional[str] = "circle" # The object's shape. If a sprite is supplied, that will be used instead.
    sprite: Optional[str] = "sprites/error.png" # The object's sprite. If left blank, a shape will be used instead.

    # The values for velocity.
    speed: Optional[float] = 1 # The GameObject's movement speed, used for movement calculations. Higher = faster.
    vel_x: Optional[float] = 0 
    vel_y: Optional[float] = 0
    isGrounded: Optional[float] = True
    isGround: Optional[float] = False
    isHostile: Optional[float] = False

    # Collision Stuff.
    holding: Optional[dataclass] = None
    collider: Optional[dataclass] = None

def PlayerMovementHandler():
    '''Handles player inputs and such.'''
    BorderY = 0

    try:
        if(player.collider.isGround):
            player.isGrounded = True
        elif(player.y >= worldSizeY - BorderY):
            player.isGrounded = True
        else:
            player.isGrounded = False
    except:
        if(player.y >= worldSizeY - BorderY):
            player.isGrounded = True
        else:
            player.isGrounded = False

    if(player.isGrounded):
        player.vel_y = 0


    # Basic movement script. Accepts either WASD or arrow key inputs.
    if(pygame.key.get_pressed()[K_RIGHT] | pygame.key.get_pressed()[K_d]):
        player.vel_x += player.speed
    if(pygame.key.get_pressed()[K_LEFT] | pygame.key.get_pressed()[K_a]):
        player.vel_x -= player.speed
    if(pygame.key.get_pressed()[K_UP] | pygame.key.get_pressed()[K_w] and player.isGrounded):
        player.vel_y -= player.speed * 100
        player.isGrounded = False
    if(pygame.key.get_pressed()[K_DOWN] | pygame.key.get_pressed()[K_s]):
        player.vel_y += player.speed

    # This code handles velocity.
    acceleration = 15
    deceleration = 15

    if(player.vel_x != 0):
        player.x += player.vel_x / acceleration
        player.vel_x -= player.vel_x / deceleration
        if(player.vel_x < 0.5 and player.vel_x > -0.5):
            player.vel_x = 0
    if(player.isGrounded == False):
        player.y += player.vel_y / acceleration
        player.vel_y -= player.vel_y / deceleration + GRAVITY
    
    # Moves the picked-up object to the player's centre.
    if(player.holding != None):
        player.holding.x = player.x
        player.holding.y = player.y
    
    pygame.draw.circle(DISPLAYSURF, GRAY, CoordinatesToScreen(player), 10, 3)

def Renderer(Obj: GameObject):
    '''Renders everything, unless they should be rendered seperately.'''
    special_cases = ["player"]
    if(id not in special_cases):
        # Scalar X and Y are used to ensure stuff scales with resolution.
        ScalarX = (DISPLAYSURF.get_width() / worldSizeX) / 4
        ScalarY = (DISPLAYSURF.get_height() / worldSizeY) / 3
        x_size = Obj.x_size * ScalarX
        y_size = Obj.y_size * ScalarY
        
        # Renders an object as a box.
        if(Obj.shape == "box"):
            x,y = CoordinatesToScreen(Obj)
            box_rect = Rect(x-x_size/2, y-y_size/2, x_size, y_size)
            pygame.draw.rect(DISPLAYSURF, Obj.color, box_rect)
            pygame.draw.circle(DISPLAYSURF, PURE_RED, (x,y), 1, 1)
        
        # Renders an object as a circle. Uses the object's X or Y value, whichever is larger.
        elif(Obj.shape == "circle"):
            x,y = CoordinatesToScreen(Obj)
            if(Obj.y > Obj.x):
                pygame.draw.circle(DISPLAYSURF, Obj.color, (x,y), x_size/2)
            else:
                pygame.draw.circle(DISPLAYSURF, Obj.color, (x,y), y_size/2)

def CoordinatesToScreen(Obj):
    '''Converts a GameObject's co-ordinates to a screen location. Takes the GameObject as a parameter.'''
    ScalarX = DISPLAYSURF.get_width() / worldSizeX
    ScalarY = DISPLAYSURF.get_height() / worldSizeY
    x = round(Obj.x * ScalarX)
    y = round(Obj.y * ScalarY)
    return((x,y))

def CompareCoordinates(Obj1, Obj2, allowed_distance):
    '''Uses the objects' X and Y values to check if they are close to each other.'''
    point1 = (Obj1.x, Obj1.y)
    point2 = (Obj2.x, Obj2.y)
    if math.dist(point1, point2) < allowed_distance:
        return(True)
    else:
        return(False)
    
def CheckBounds(Obj):
    '''Prevents things going offscreen.'''
    BorderX = 0
    BorderY = 0

    # When in wall teleport to other wall.
    if(Obj.x < BorderX):
        Obj.x = worldSizeX - BorderX
    if(Obj.x > worldSizeX - BorderX):
        Obj.x = BorderX
    if(Obj.y < BorderY):
        Obj.y = BorderY
    if(Obj.y > worldSizeY - BorderY):
        Obj.y = worldSizeY - BorderY
    
def CheckForID(id):
    '''Checks every GameObject to see if any of them match a given ID.'''
    FoundMatch = None
    for Obj in GameObjects:
        if(Obj.id == id):
            FoundMatch = Obj
            break
    return(FoundMatch)

def WriteLog():
    '''Writes a log, containing a lot of runtime data, such as each GameObject.'''
    with open("last.log", "+w") as log:
        log.write("--------------------\nPlayer Details:\n\n")
        log.write(f"Player Collider: {str(player.collider)}\n")
        log.write("\n--------------------\nAll GameObjects:\n\n")
        for x in GameObjects:
            log.write(f"{str(x.id)}: {str(x)}\n")
        
def SnapToGrid(Obj):
    Obj.x = round(Obj.x)
    Obj.y = round(Obj.y)

def GenNewGameObject():
    global GameObjects, Boxes
    size = random.randint(5,50)
    this_id = random.randint(-2147483647,2147483647)
    this_color = (random.randint(1,255), random.randint(1,255), random.randint(1,255))
    loc_x = random.randint(0, worldSizeX)
    loc_y = random.randint(0, worldSizeY)
    genned_go = GameObject(size,size, id=this_id, shape="circle", color=this_color, x=loc_x, y=loc_y, isGround=True)
    GameObjects.append(genned_go)
    Boxes.append(genned_go)

def GenNewArrow():
    global GameObjects
    this_id = random.randint(-2147483647,2147483647)
    genned_arrow = GameObject(50,10, id="arrow", shape="box", color=CRIMSON, x=worldSizeX, y=worldSizeY, isGround=False, isHostile=True)
    GameObjects.append(genned_arrow)

def MoveArrow(arrow):
    arrow.x += 1

def Wiggle(tbox):
    tbox.x += random.random() * random.choice([-1,1])
    tbox.y += random.random() * random.choice([-1,1])

# Player must always exist - you can change its properties to suit your needs, however.
player = GameObject(10, 10, id="player")