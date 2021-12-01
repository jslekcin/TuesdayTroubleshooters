import pygame
import objects
from pygame import *
import FileLoader

import GameFunctions

pygame.init()

clock = pygame.time.Clock()

# load everything
FileLoader.load()
# Game Loop

# Game Name: Spirits of Darkness

while 1: 
    objects.screen.fill((200,200,200))

    if objects.debugging: # Debugging code
      GameFunctions.DebugCode()
    
    if objects.gamestate == 0: # Menu Code
        GameFunctions.MenuInput()
        GameFunctions.MenuUpdate()
        GameFunctions.MenuRender()
    
    if objects.gamestate == 1: # Gameplay
        GameFunctions.GameplayInput()
        GameFunctions.GameplayUpdate()
        GameFunctions.GameplayRender()
        '''
        # Day
        if subgamestate == 1:
            dodaystuff()
            dogamestuff()
        # Night
        if subgamestate == 2:
            donightstuff()
            dogamestuff()
        '''
    if objects.gamestate == 2: # Game Over
        GameFunctions.GameOverInput()
        GameFunctions.GameOverUpdate()
        GameFunctions.GameOverRender()
    objects.screen.fill((0,0,0))
    clock.tick(30)