import pi_calculator
import Geometry
import pygame, sys
from pygame.locals import *
import math
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("monospace", 16)

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
scale = 650
DISPLAYSURF = pygame.display.set_mode((scale+200, scale), 0, 32)
pygame.display.set_caption('Pi Calculator')

a = pi_calculator.pi_polygon_generator(scale)


WHITE = (150,150,150)
RED = (255,0,0)
BLACK = (0,0,0)
GREEN = (0,255,0)
generate = False


shape = next(a)

pointer_x = 0
pointer_scale = -100

while True: # the main game loop
    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
        	if event.key == pygame.K_w:
        		generate = True
        	if event.key == pygame.K_s:
        		pointer_scale*= 10

    if generate:
        shape = next(a)
        val = shape.gen_area()*4.0/scale/scale
        diff = math.pi - val
        pointer_y = diff*pointer_scale+500
        print("y: ", pointer_y)
        pygame.draw.circle(DISPLAYSURF,WHITE, (pointer_x,int(pointer_y)),0)
        pygame.draw.circle(DISPLAYSURF,GREEN, (pointer_x,20),0)
        pointer_x += 1

        if pointer_x >= scale:
            DISPLAYSURF.fill(BLACK)
            pointer_x = 0

        txt_scale = font.render("Scale: " + str(pointer_scale),False,WHITE )
        txt_difference = font.render("Difference: " + str(diff),False,WHITE )
        text = pygame.Surface((400,500))
        text.fill(BLACK)

        text.blit(txt_scale, (0,0))
        text.blit(txt_difference, (0,50))
        DISPLAYSURF.blit(text,(scale-150,scale -200))
        

   
    pygame.display.update()
    fpsClock.tick(FPS)