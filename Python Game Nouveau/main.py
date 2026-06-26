import pygame, sys, random, math, datetime
from pygame.locals import *
from dataclasses import dataclass, fields
from typing import Optional


# Global Variables
res_x = 400
res_y = 300

# Global Constants
TICK_RATE = 60

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

# Setup stuff. Should be mostly self-explanatory.
pygame.init()
DISPLAYSURF = pygame.display.set_mode((res_x, res_y), pygame.RESIZABLE)
pygame.display.set_caption("Test")
fpsClock = pygame.time.Clock()
worldSizeX = 100
worldSizeY = 100


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

    # Collision Stuff.
    holding: Optional[dataclass] = None
    collider: Optional[dataclass] = None

def PlayerMovementHandler():
    '''Handles player inputs and such.'''
    # Basic movement script. Accepts either WASD or arrow key inputs.
    if(pygame.key.get_pressed()[K_RIGHT] | pygame.key.get_pressed()[K_d]):
        player.vel_x += player.speed
    if(pygame.key.get_pressed()[K_LEFT] | pygame.key.get_pressed()[K_a]):
        player.vel_x -= player.speed
    if(pygame.key.get_pressed()[K_UP] | pygame.key.get_pressed()[K_w]):
        player.vel_y -= player.speed
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
    if(player.vel_y != 0):
        player.y += player.vel_y / acceleration
        player.vel_y -= player.vel_y / deceleration
        if(player.vel_y < 0.5 and player.vel_y > -0.5):
            player.vel_y = 0
        

    # When in wall teleport to other wall.
    BorderX = 0
    BorderY = 0
    if(player.x < BorderX):
        player.x = worldSizeX - BorderX
    if(player.x > worldSizeX - BorderX):
        player.x = BorderX
    if(player.y < BorderY):
        player.y = worldSizeY - BorderY
    if(player.y > worldSizeY - BorderY):
        player.y = BorderY
    
    # Moves the picked-up object to the player's centre.
    if(player.holding != None):
        player.holding.x = player.x
        player.holding.y = player.y
    
    pygame.draw.circle(DISPLAYSURF, GRAY, CoordinatesToScreen(player), 10, 3)

def Rigidbody(Obj: GameObject):
    special_cases = ["player"]
    if(id not in special_cases):
        if(Obj.shape == "box"):
            x,y = CoordinatesToScreen(Obj)
            box_rect = Rect(x-Obj.x_size/2, y-Obj.x_size/2, Obj.x_size, Obj.y_size)
            pygame.draw.rect(DISPLAYSURF, Obj.color, box_rect)
            pygame.draw.circle(DISPLAYSURF, PURE_RED, (x,y), 1, 1)
 
def CoordinatesToScreen(Obj):
    '''Converts a GameObject's co-ordinates to a screen location. Takes the GameObject as a parameter.'''
    ScalarX = DISPLAYSURF.get_width() / worldSizeX
    ScalarY = DISPLAYSURF.get_height() / worldSizeY
    x = round(Obj.x * ScalarX)
    y = round(Obj.y * ScalarY)
    return((x,y))

def CompareCoordinates(Obj1, Obj2, allowed_distance):
    point1 = (Obj1.x, Obj1.y)
    point2 = (Obj2.x, Obj2.y)
    if math.dist(point1, point2) < allowed_distance:
        return(True)
    else:
        return(False)
    
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

player = GameObject(10, 10, id="player")
box = GameObject(10,10, id="test-box", shape="box", color=MINT, x=50, y=50)
box2 = GameObject(10,10, id="test-box2", shape="box", color=DELICIOUS_BLUE, x=30, y=30)
GameObjects = [player, box, box2]
Boxes = [box,box2]

while True: # Main game loop - like Unity's "update" void thing.
    DISPLAYSURF.fill(NIGHT_SKY_BLUE)

    PlayerMovementHandler()
    random.shuffle(GameObjects)
    for Obj in GameObjects:
        Rigidbody(Obj)
        try:
            if(not(CompareCoordinates(Obj, Obj.collider, Obj.x_size/2))):
                Obj.collider = None
        except:
            pass
    for Obj1 in GameObjects:
        for Obj2 in GameObjects:
            if(not Obj1 == Obj2):
                if(CompareCoordinates(Obj1, Obj2, Obj1.x_size/2) and Obj1.id == "player"):
                    Obj1.collider = Obj2
    for box in Boxes:
        SnapToGrid(box)

    pygame.display.update()
    
    # This takes a screenshot.
    if(pygame.key.get_pressed()[K_F2]):
        pygame.image.save(DISPLAYSURF, "screenshot.png")

            
    fpsClock.tick(TICK_RATE)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # Grabbing boxes? Lovely!
            if(event.key == pygame.K_g):
                if(player.holding == None):
                    player.holding = player.collider
                else:
                   player.holding = None
            # Provides various debug information.
            if(event.key == pygame.K_z):
                WriteLog()