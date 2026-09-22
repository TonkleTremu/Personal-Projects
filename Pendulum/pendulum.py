import pygame, sys, math, random
from pygame.locals import *

# Stuff used for recording.
record_screen = False
images_produced = 0

# Set to true for screensaver distributions.
screensaver = False

# Asks what base should be used, and other setup stuff.
base = input("1. Screensaver-esque Pattern\n2. Randomly Moving Circle\n3. Curly Venn Diagram\n4. Tuple Pendulum\n")
render_lines = False
render_circle = False
after_images = False

pendulums = int(input("How many pendulums should be used? (800 is nice for screensavers.)\n"))

if(base == "4"):
    rot_speed = float(input("How fast should the circle move? (Lower speed gives smoother result - 0.05 is a nice number to use.)\n"))

after_images = input("Would you like after-images? (They work nicely for screensavers, but make it difficult to see what's happening.) Y/N\n").lower()[0] == "y"

# Setup stuff.
pygame.init()
if(screensaver):
    DISPLAYSURF = pygame.display.set_mode((0, 0), RESIZABLE)
else:
    DISPLAYSURF = pygame.display.set_mode((1080, 720))
res_x = DISPLAYSURF.get_width()
res_y = DISPLAYSURF.get_height()
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
pendulum_ends = [(res_x/2,res_y/2)]
pendulum_rotations = [0]
pendulum_speeds = [0]

# Loads and sets fonts.
pygame.font.init()
my_font = pygame.font.SysFont("Agency FB", 30)

for pendulum in range(1,pendulums+1):
    pendulum_ends.append((0,0))
    pendulum_rotations.append(0)
    match base:
        case "1":
            render_lines = True
            if(pendulum%2==0):
                pendulum_speeds.append(random.random()/10)
            else:
                pendulum_speeds.append(-random.random()/10)
        case "2":
            render_circle = True
            if(pendulum%2==0):
                pendulum_speeds.append(random.random()/20)
            else:
                pendulum_speeds.append(-random.random()/20)
        case "3":
            render_lines = True
            if(pendulum%2==0):
                pendulum_speeds.append((pendulum/10)-0.05)
            else:
                pendulum_speeds.append(-0.05 + (pendulum/10))
        case "4":
            render_lines = True
            render_circle = True
            if(pendulum%2==0):
                pendulum_speeds.append(rot_speed)
            else:
                pendulum_speeds.append(-rot_speed)

DISPLAYSURF.fill(NIGHT_SKY_BLUE)
uni_color = (255,255,255)
directions = [0,0,0]


while True: # Main game loop.
    if(after_images == False):
        DISPLAYSURF.fill(NIGHT_SKY_BLUE)
    pygame.mouse.set_visible(False)
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
        if(render_lines):
            pygame.draw.line(DISPLAYSURF, uni_color, pendulum_ends[p], pendulum_ends[p-1], 10)
    if(render_circle):
        pygame.draw.circle(DISPLAYSURF, (uni_color), pendulum_ends[-1], 20)
    pygame.display.update()
    if(record_screen):
        pygame.image.save(DISPLAYSURF, f"tempvideofolder/image{images_produced}.png")
        images_produced += 1
    fpsClock.tick(60)
    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            if(pygame.mouse.get_rel() != (0,0) and screensaver):
                pygame.quit()
                sys.exit()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()