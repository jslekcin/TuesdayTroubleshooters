# TODAYS TODO:
# 1) --- Finish potion shop
# 1a) --- Freeze the rest of our game
# 1b) --- Make it so that shop buttons work
# 1c) --- Make an obvious way to close the shop

# 2) --- Potion inventory
# 3) --- Summoning boss: normal ai but slower and spawns normal ghosts
# 4) Press I to get info (current health, chunk, energy, quest)
# 5) Make quest information
# 6) Housekeeping

import pygame
import sys
import objects
objects.LoadMath()
import MapLoader
from GameFunctions import *
pygame.init()
# load everything
MapLoader.load()
 
# Game Name: Spirits of the night
print("REPORT: Welcome to the game. Your goal is to find 9 portals on the map and defeat the 9 bosses inside them. Controls: arrow keys to move, click to shoot an arrow towards the mouse. Later in the game, when you have other abilities, you can press 1 to switch back to arrows. ")

# Game Loop
clock = pygame.time.Clock()
while 1: 
    for event in pygame.event.get(pygame.QUIT):
        pygame.quit()
        sys.exit()

    if objects.debugging: # Debugging code
        DebugCode()
    
    if objects.gamestate == 0: # Menu Code
        MenuUpdate()
        MenuRender()
    
    if objects.gamestate == 1: # Gameplay
        if objects.shopShowing:
            ShopUpdate()
        else:
            GameplayUpdate()
            
        GameplayRender()
        if objects.shopShowing:
            ShopRender()

    if objects.gamestate == 2: # Game Over
        GameOverUpdate()
        GameOverRender()

    if objects.gamestate == 3: # Question Cubes
        MathUpdate() 
        MathRender() 
        
    pygame.display.flip()
    clock.tick(objects.framerate)

"""
try - catch
l = ["today", "is", "tuesday"]
l.remove("today")
print(l)
try:
    l.remove("today")
except ValueError:
    # deal with error
    print("can't remove today twice")"""
