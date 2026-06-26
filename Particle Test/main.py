import pygame, sys, random, math, datetime
from pygame.locals import *
from dataclasses import dataclass, fields
from typing import Optional

# Global Constants

# Reduce to 30 if performance is very poor.
TICK_RATE = 60
BLACK = (0,0,0)
WHITE = (255,255,255)
SUNSET = (250, 100, 10)
NIGHT_SKY_BLUE = (10,20,140)
CANVAS_SIZE = 100

zoom = 0.25
offset_x = -CANVAS_SIZE/2
offset_y = -CANVAS_SIZE/2

@dataclass
class Element:
    name: str
    mass: float
    reactions: list
    color: tuple

@dataclass
class Reaction:
    reactant_1: str
    reactant_2: str

    product_1: str
    product_2: str

    energy_needed: float
    is_exothermic: bool

    quantity_1: int
    quantity_2: int

@dataclass
class Particle:
    # The xz location values.
    x: float
    y: float

    internal_energy: float

    x_speed: float
    y_speed: float

    element: Element
    

# Setup stuff.
pygame.init()
DISPLAYSURF = pygame.display.set_mode((CANVAS_SIZE, CANVAS_SIZE), RESIZABLE)
pygame.display.set_caption("Langton's Ant")
fpsClock = pygame.time.Clock()

# Loads and sets fonts.
pygame.font.init()
my_font = pygame.font.SysFont("Agency FB", 30)

co_react = Reaction("c", "o", "co", "o", 500, True, 1, 0)
co2_react = Reaction("co", "o", "co2", "o", 1000, True, 1, 0)

c = Element("c", 12, [co_react], BLACK)
o = Element("o", 8, [], WHITE)
co = Element("co", 20, [co2_react], (255,0,0))
co2 = Element("co2", 20, [], (255,255,0))

elements = [c,o,co]

selectable_elements = [c,o,o]

active_particles = []

for i in range(100):
    x = random.randint(0, CANVAS_SIZE)
    y = random.randint(0, CANVAS_SIZE)
    internal_energy = random.random()*1000
    x_speed = random.random() * random.choice([-1,1])
    y_speed = random.random() * random.choice([-1,1])
    element = random.choice(selectable_elements)
    this_particle = Particle(x,y,internal_energy,x_speed,y_speed,element)
    active_particles.append(this_particle)

while True: # Main game loop.
    DISPLAYSURF.fill(NIGHT_SKY_BLUE)
    for particle in active_particles:
        this_element = particle.element
        x = round(particle.x)
        y = round(particle.y)
        DISPLAYSURF.set_at((x, y), this_element.color)
        if(particle.x > DISPLAYSURF.get_width() or particle.x < 0):
            particle.x_speed *= -1
        if(particle.y > DISPLAYSURF.get_height() or particle.y < 0):
            particle.y_speed *= -1

        if(particle.x > DISPLAYSURF.get_width()*1.2):
            particle.x = DISPLAYSURF.get_width()
        if(particle.x < 0):
            particle.x = 0
        if(particle.y > DISPLAYSURF.get_height()*1.2):
            particle.y = DISPLAYSURF.get_height()
        if(particle.y < 0):
            particle.y = 0

        particle.x += particle.x_speed*10
        particle.y += particle.y_speed*10
        try:
            for p2 in active_particles:
                if(round(particle.x) == round(p2.x) and round(particle.y) == round(p2.y)):
                    for reaction in this_element.reactions:
                        if(this_element.name == reaction.reactant_1 and p2.element.name == reaction.reactant_2 and particle.internal_energy + p2.internal_energy >= reaction.energy_needed):
                            x = particle.x
                            y = particle.y
                            internal_energy = particle.internal_energy + p2.internal_energy
                            x_speed = (particle.x_speed + p2.x_speed) / 2
                            y_speed = (particle.y_speed + p2.y_speed) / 2
                            for i in elements:
                                if(i.name == reaction.product_1):
                                    element = i
                            this_particle = Particle(x,y,internal_energy,x_speed,y_speed,element)
                            active_particles.append(this_particle)
                            print(len(active_particles))
                            carbon = 0
                            oxygen = 0
                            col = 0
                            co2l = 0
                            unidentified = 0
                            active_particles.remove(p2)
                            active_particles.remove(particle)
                            for x in active_particles:
                                if(x.element.name == "c"):
                                    carbon += 1
                                elif(x.element.name == "o"):
                                    oxygen += 1
                                elif(x.element.name == "co"):
                                    col += 1
                                elif(x.element.name == "co2"):
                                    co2l += 1
                                else:
                                    unidentified += 1
                            print(f"C: {carbon}")
                            print(f"O: {oxygen}")
                            print(f"CO: {col}")
                            print(f"CO2: {co2l}")
                            print(f"???: {unidentified}")
                            del(p2)
                            del(particle)
                    new_x_speed = (abs(particle.x_speed) + abs(p2.x_speed)) / 2
                    new_y_speed = (particle.y_speed + p2.y_speed) / 2
                    if(particle.x_speed < 0):
                        particle.x_speed = new_x_speed
                    else:
                        particle.x_speed = new_x_speed*-1
                    if(p2.x_speed < 0):
                        p2.x_speed = new_x_speed
                    else:
                        p2.x_speed = new_x_speed*-1
                    if(particle.y_speed < 0):
                        particle.y_speed = new_y_speed
                    else:
                        particle.y_speed = new_y_speed*-1
                    if(p2.y_speed < 0):
                        p2.y_speed = new_y_speed
                    else:
                        p2.y_speed = new_y_speed*-1
        except:
            print("reacted")
                        
    pygame.display.update()

    fpsClock.tick(TICK_RATE)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if(event.key == pygame.K_F2):
                pygame.image.save(DISPLAYSURF, f"screenshots/screenshot {str(datetime.datetime.now()).replace(":", "")}.png")
                print(f"Time is {datetime.datetime.now()}")
            if(event.key == pygame.K_F3):
                print("debug")
                