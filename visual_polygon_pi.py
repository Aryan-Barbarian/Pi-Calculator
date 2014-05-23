import pi_calculator
import Geometry
import pygame, sys
from pygame.locals import *
import math
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("monospace", 18)

FPS = 1 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
scale = 650
DISPLAYSURF = pygame.display.set_mode((scale+200, scale), 0, 32)
pygame.display.set_caption('Pi Calculator')

a = pi_calculator.pi_polygon_generator(scale)


WHITE = (150,150,150)
RED = (75,0,0)
BLACK = (0,0,0)
GREEN = (0,150,0)
generate = False
pygame.draw.circle(DISPLAYSURF, WHITE, (0,0),scale,1)
shape = next(a)
calc = True
num_sides = 0

while True: # the main game loop
    
    """this handles events.
    "w" will enable generate, which allows the program to keep improving the shape. 
    "s" pauses this.
    "a" enables the program to calculate area
    "d" disables calculation
    "q" slows down the FPS Clock
    "e" speeds up the FPS Clock """
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                pygame.draw.circle(DISPLAYSURF, BLACK, (0,0),scale,1)
                flag = False
                generate = True
            if event.key == pygame.K_s:
                generate = False
            if event.key == pygame.K_a:
                calc = True
            if event.key == pygame.K_d:
                calc = False
            if event.key == pygame.K_q:
                FPS = FPS/2.0 + 0.1
            if event.key == pygame.K_e:
                FPS = FPS*2.0

    if generate:
        num_sides += 1
        DISPLAYSURF.fill(BLACK)
        shape = next(a)
        color = WHITE
        points = shape.to_tuple()

        if calc:
            """The following displays text using text labels.
            This library comes with Pygame. The text is rendered
            to the font surface and these surfaces are all combined and
            rendered onto the main game surface."""

            val = shape.gen_area()*4.0/scale/scale #the actual calculated value of pi
            txt_our_pi = font.render("Our PI: " + str(val),False,WHITE)
            txt_real_pi = font.render("Real PI: " + str(math.pi),False,WHITE)
            txt_difference = font.render("Difference: " + str(math.fabs(val-math.pi)),False,WHITE)
            txt_num_sides = font.render("Sides: " + str(len(shape.points)),False,WHITE )
            text = pygame.Surface((400,500))
            text.fill(BLACK)

            text.blit(txt_real_pi, (0,0))
            text.blit(txt_our_pi, (0,50))
            text.blit(txt_difference, (0,100))
            text.blit(txt_num_sides, (0,150))

            DISPLAYSURF.blit(text,(scale-150,scale -200))

    #This draws our Polygon and the red circle behind it
    pygame.draw.circle(DISPLAYSURF, RED, (0,0),scale)
    pygame.draw.polygon(DISPLAYSURF,GREEN,shape.to_tuple())

    pygame.display.update()

    """uncomment this to slow the program down to the FPS defined at the
    beginning of the program or comment it out to let the program go full speed"""
    fpsClock.tick(FPS)