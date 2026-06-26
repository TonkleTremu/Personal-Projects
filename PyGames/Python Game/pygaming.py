# The library stackalbry.
import pygame, sys, random, math
from pygame.locals import *
from gamelib import *

# Setup stuff. Should be mostly self-explanatory.
pygame.init()
DISPLAYSURF = pygame.display.set_mode((res_x, res_y))
pygame.display.set_caption(game_name)
fpsClock = pygame.time.Clock()

# Dynamic Player Data
player_x = 10
player_y = 10
player_velocity = [0,0]

# World Data
CreatureCount = 7 # If 3 preset creatures exist, this should be 4.
GlobalCreatures = {1: [(0,0,127), (0,0), (15, 150)],
             2: [(127,0,0), (0,0), (20, 200)],
             3: [(0,127,0), (0,0), (25, 250)],
             4: [(0,0,127), (0,0), (15,15)],
             5: [(127,0,0), (0,0), (20, 20)],
             6: [(0,127,0), (0,0), (25, 25)]
             } # Creatures are stored as {ID: [Colour, Parents, Position]} Colour determines traits - Red: Hostility, Green: Breed rate, Blue: Mitosis rate

def PlayerMovementHandler():
    '''Handles player inputs and such.'''
    global player_x
    global player_y
    # Basic movement script. Accepts either WASD or arrow key inputs.
    if(pygame.key.get_pressed()[K_RIGHT] | pygame.key.get_pressed()[K_d]):
        player_x += 1
    if(pygame.key.get_pressed()[K_LEFT] | pygame.key.get_pressed()[K_a]):
        player_x -= 1
    if(pygame.key.get_pressed()[K_UP] | pygame.key.get_pressed()[K_w]):
        player_y -= 1
    if(pygame.key.get_pressed()[K_DOWN] | pygame.key.get_pressed()[K_s]):
        player_y += 1

    # When in wall teleport to other wall.
    if(player_x < PLAYER_WIDTH):
        player_x = res_x - PLAYER_WIDTH
    if(player_x > res_x - PLAYER_WIDTH):
        player_x = 10
    if(player_y < PLAYER_HEIGHT):
        player_y = res_y - PLAYER_HEIGHT
    if(player_y > res_y - PLAYER_HEIGHT):
        player_y = 10
    
    pygame.draw.circle(DISPLAYSURF, MINT, (player_x, player_y), 10, 3)

def DrawPattern():
    x = 0
    while(x <= res_x):
        pygame.draw.line(DISPLAYSURF, LIGHT_BLUE, (x, 0), (x+10, res_y), 15)
        x += 30
    
def CheckNeighbours():
    '''A creature will check its neighbours, then identify if they are compatible species. If they are, they produce an offspring. If not, they may fight.'''
    global CreatureCount
    Creatures = GlobalCreatures
    for x in list(GlobalCreatures.keys()):
        for i in list(GlobalCreatures.keys()):
            if(not(x == i)):
                if(random.randint(1,3) == 1):
                    try:
                        # Checks if the creatures are next to each other.
                        if((GlobalCreatures[x][2][0]+GlobalCreatures[i][2][0])/2 in [-1,0,1]):
                            # Checks if the creatures are similar species. If so, a new cretin will spawn.
                            # If all colour values are within 30, they may breed.
                            print(sum(GlobalCreatures[x][0])-sum(GlobalCreatures[i][0]))
                            if((sum(GlobalCreatures[x][0])-sum(GlobalCreatures[i][0]) <= 30) or (sum(GlobalCreatures[x][0])-sum(GlobalCreatures[i][0]) >= -30)):
                                if((x in GlobalCreatures[i][1]) or (i in GlobalCreatures[x][1])):
                                    pass
                                else:
                                    # Creating the new creature.
                                    if((GlobalCreatures[x][0][1] + GlobalCreatures[i][0][1])/2 <= random.randint(0,256)):
                                        NewRed = round((GlobalCreatures[x][0][0] + GlobalCreatures[i][0][0])/2) + random.randint(-5,5)
                                        if(NewRed < 0):
                                            NewRed = 0
                                        elif(NewRed > 255):
                                            NewRed = 255
                                        NewGreen = round((GlobalCreatures[x][0][1] + GlobalCreatures[i][0][1])/2) + random.randint(-5,5)
                                        if(NewGreen < 0):
                                            NewGreen = 0
                                        elif(NewGreen > 255):
                                            NewGreen = 255
                                        NewBlue = round((GlobalCreatures[x][0][2] + GlobalCreatures[i][0][2])/2) + random.randint(-5,5)
                                        if(NewBlue < 0):
                                            NewBlue = 0
                                        elif(NewBlue > 255):
                                            NewBlue = 255
                                        GlobalCreatures.update({CreatureCount: [(NewRed, NewGreen, NewBlue), (x,i), (random.randint(0,res_x), random.randint(0,res_y))]})
                                        CreatureCount += 1
                            elif((GlobalCreatures[x][0][1] + GlobalCreatures[i][0][1])/2 >= random.randint(0,127)):
                                        if(random.randint(0, GlobalCreatures[x][0][0]) <= random.randint(0, GlobalCreatures[i][0][0])):
                                            GlobalCreatures.pop(x)
                                        else:
                                            GlobalCreatures.pop(i)
                    except:
                        print("stop! its already dead...")
def ShowCreatures():
    for x in GlobalCreatures:
        pygame.draw.circle(DISPLAYSURF, GlobalCreatures[x][0], GlobalCreatures[x][2], 1, 1)    

def MoveCreatures():
    for x in GlobalCreatures:
        NewPos = (GlobalCreatures[x][2][0] + random.randint(-5,5),GlobalCreatures[x][2][1] + random.randint(-5,5))
        if(NewPos[0] < 0):
            NewPos = (0, NewPos[1])
        elif(NewPos[0] > res_x):
            NewPos = (res_x, NewPos[1])
        if(NewPos[1] < 0):
            NewPos = (NewPos[0], 0)
        elif(NewPos[1] > res_y):
            NewPos = (NewPos[0], res_y)
        GlobalCreatures.update({x: [GlobalCreatures[x][0], GlobalCreatures[x][1], NewPos]})        

while True: # Main game loop - like Unity's "update" void thing.
    DISPLAYSURF.fill(WHITE)
    #DrawPattern()
    #PlayerMovementHandler()

    ShowCreatures()
    MoveCreatures()
    CheckNeighbours()

    pygame.display.update()
    fpsClock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()