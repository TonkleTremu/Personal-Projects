from physicslib import *

# Initiates the pygame loop.
pygame.init()

# The FPS clock. Lets the game know how fast your game should be, so it doesn't fluctuate.
fpsClock = pygame.time.Clock()

# Sets the window's name. For example, if your game is called "Bastille Jour", you would put that here.
pygame.display.set_caption("Test")

# Overrides the default values - if you want to change world size, do it here.
worldSizeX = 100
worldSizeY = 100

# Some GameObjects for testing. Remove them as needed, or add new ones.
box = GameObject(10,10, id="test-box", shape="box", color=MINT, x=50, y=70, isGround=True)
box2 = GameObject(10,10, id="test-box2", shape="box", color=DELICIOUS_BLUE, x=30, y=30, isGround=True)

# GameObject lists. Want to iterate through everything? Do that here.
GameObjects = [player, box, box2]
Boxes = [box,box2]

while True: # Main game loop - like Unity's "update" void thing.
    DISPLAYSURF.fill(NIGHT_SKY_BLUE) # Background color.

    PlayerMovementHandler() # Default player movement.
    random.shuffle(GameObjects) # Prevents objects being hidden behind others, at the cost of Z-fighting. Remove this if Z-fighting bothers you.
    
    for Obj in GameObjects: # Applies various behaviours to GOs.
        Renderer(Obj) # Displays the object to the screen, unless they should be handled differently (like the player GO.)
        CheckBounds(Obj) # You don't want stuff going off screen. That's why this is here.
        if(Obj.id not in ["player", "arrow"]):
            Wiggle(Obj) # Boxes wiggle.
        if(Obj.id == "arrow"):
            MoveArrow(Obj) # Arrows slide.
        try:
            if(not(CompareCoordinates(Obj, Obj.collider, Obj.x_size/2))):
                Obj.collider = None # Removes an object's collider if they are no longer colliding.
        except:
            pass # I still don't get why python always needs an except to a try, its annoying.
    
    # If two objects are next to eachother, this marks them as colliding.
    for Obj1 in GameObjects:
        for Obj2 in GameObjects:
            if(not Obj1 == Obj2):
                if(CompareCoordinates(Obj1, Obj2, Obj1.x_size/2) and Obj1.id == "player"):
                    Obj1.collider = Obj2 # collision system really needs reworking...
                    if(Obj1.id == "arrow" or Obj2.id == "arrow"):
                        pygame.quit() # If the player is hit by an arrow, the game shuts down.

    # Re-renders everything.
    pygame.display.update()
    
    # This takes a screenshot.
    if(pygame.key.get_pressed()[K_F2]):
        pygame.image.save(DISPLAYSURF, "screenshot.png")

            
    fpsClock.tick(TICK_RATE)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            # Grabbing boxes? Lovely!
            if(event.key == pygame.K_g):
                if(player.holding == None):
                    player.holding = player.collider
                else:
                   player.holding = None
            if(DEBUG):
                # Provides various debug information.
                if(event.key == pygame.K_z):
                    WriteLog()
                if(event.key == pygame.K_p):
                    GenNewArrow()