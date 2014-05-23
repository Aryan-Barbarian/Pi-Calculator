import pi_calculator
import Geometry
import pygame, sys
from pygame.locals import *
import math

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("monospace", 16)

FPS = 90000 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
scale = 650
DISPLAYSURF = pygame.display.set_mode((scale+200, scale), 0, 32)
pygame.display.set_caption('Pi Calculator')

a = pi_calculator.pi_rand_generator()


WHITE = (150,150,150)
RED = (255,0,0)
BLACK = (0,0,0)
GREEN = (0,255,0)
generate = False
pygame.draw.circle(DISPLAYSURF, WHITE, (0,0),scale,1)
flag = True
while True: # the main game loop
    #DISPLAYSURF.fill(BLACK)
    
    """this handles events.
    "w" will enable generate, which allows the program to keep improving the shape. 
    "s" pauses this.
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
            if event.key == pygame.K_q:
                FPS = FPS/2.0 + 0.1
            if event.key == pygame.K_e:
                FPS = FPS*2.0

        
    if generate:

        val,point,in_circle = next(a)
        if in_circle:
        	color = GREEN
        else:
        	color = RED
        coor = (int(point.x*scale),int(point.y*scale))
        pygame.draw.circle(DISPLAYSURF,color,coor,0)

        """The following displays text using text labels.
            This library comes with Pygame. The text is rendered
            to the font surface and these surfaces are all combined and
            rendered onto the main game surface."""
        txt_our_pi = font.render(str(val),False,WHITE)
        txt_real_pi = font.render(str(math.pi),False,WHITE)
        txt_difference = font.render(str(math.fabs(val-math.pi)),False,WHITE)

        text = pygame.Surface((200,500))
        text.fill(BLACK)

        text.blit(txt_real_pi, (0,0))
        text.blit(txt_our_pi, (0,50))
        text.blit(txt_difference, (0,100))

        DISPLAYSURF.blit(text,(scale,0))
          

    pygame.display.update()
    fpsClock.tick(FPS)