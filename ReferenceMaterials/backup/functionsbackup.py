import pygame
import Classes
import objects
from objects import *
import random

pygame.init()

myFont = pygame.font.SysFont("Comic Sans", 24)
announcementFont = pygame.font.SysFont("Comic Sans", 72)
buttons = {
    "game": [], 
    "menu": [Classes.Button(pygame.image.load("Pixel Images/StartButton.png"),(250,400), ['objects.gamestate = 1','objects.Reset()'])]
}
objects.player = Classes.Player()

# Creating Runtime Variables
for x in range(objects.mapWidth): 
    objects.chunks.append(list())
    for y in range(objects.mapHeight):
        objects.chunks[-1].append(Classes.Chunk((x,y), pygame.image.load("Pixel Images/Grass.png"), (500,500)))
        enemyNum = random.randint(1,5)
        coinNum = 2
        if x == 3 and y == 3:
            coinNum = 4
        for e in range(enemyNum): 
            objects.chunks[x][y].contents.append(Classes.Ghost((random.randint(0,500),random.randint(0,500))))
        for coin in range(coinNum): 
            objects.chunks[x][y].contents.append(Classes.Resource("coins", 10, pygame.transform.scale(pygame.image.load("Pixel Images/Gold Coin.png"), (15,15)), (random.randint(0,500),random.randint(0,500))))

# Manual addition of objects to chunks
objects.chunks[3][3].contents.append(
            Classes.Obstacle(pygame.transform.scale(pygame.image.load("TestImage.png"), (50,50)), (250, 250))
            )
objects.chunks[0][0].contents.append(
    Classes.NPC(pygame.image.load("Pixel Images/Player.png"), (100,100), [
        "if objects.resourceAmounts['coins'] >= 50: objects.player.currentHealth = 100;objects.resourceAmounts['coins'] -= 50"]))
objects.chunks[0][0].contents.append(Classes.Building(pygame.image.load("Pixel Images/House.png"), (400,100),0, (24,50)))
# Subchunk list
objects.chunks.append(list())
objects.chunks[-1].append(Classes.Chunk((objects.mapWidth,0), pygame.image.load("Pixel Images/HouseBackground.png"), (500,500))) # House in spawn area
objects.chunks[-1][0].contents.append(Classes.CollisionButton(pygame.image.load("Pixel Images/DoorFromInside.png"), (250, 475), ["objects.player.chunk = (0,0)","objects.player.rect.center = (400,200)"]))
#objects.chunks[-1].append(Classes.Chunk((objects.mapWidth, 1), pygame.image.load("Pixel Images/Grass.png"), (500,500)))
objects.chunks[-1].append(Classes.Chunk((objects.mapWidth,0), pygame.image.load("Pixel Images/HouseBackground.png"), (500,500))) # House with boss
objects.chunks[-1][0].contents.append(Classes.FireGhostBoss())


def DebugCode():
    if pygame.key.get_pressed()[pygame.K_SPACE]: 
        objects.player.currentHealth -= 10
    if pygame.key.get_pressed()[pygame.K_p]:
        print(pygame.mouse.get_pos())

def GameplayInput(): 
    # INPUT (Getting stuff that player is doing ex: pressing keys moving keyboard)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            objects.player.fireProjectile()
    objects.player.last_valid_position = objects.player.rect.center
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        objects.player.move(0,-objects.moveSpeed)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        objects.player.move(0,objects.moveSpeed)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        objects.player.move(-objects.moveSpeed,0)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: 
        objects.player.move(objects.moveSpeed,0)
    

def GameplayUpdate(): 
    # UPDATE (Doing checks in the background ex: checking if something is colliding)
    if objects.player.rect.center[0] < 0: # Moving off left of screen
        if objects.player.chunk[1] == objects.mapWidth or objects.player.chunk[0] == 0: # If in subchunk or leftmost chunk
            objects.player.rect.centerx = 0 # Move flush to wall
        else:
            objects.player.chunk = (objects.player.chunk[0]-1, objects.player.chunk[1])
            print(objects.player.chunk)
            objects.player.rect.centerx = objects.width
            #objects.player.move(objects.width, 0)
    
    if objects.player.rect.center[0] > objects.width: # Moving off right of screen
        if objects.player.chunk[1] == objects.mapWidth or objects.player.chunk[0] == objects.mapWidth-1:
            objects.player.rect.centerx = objects.width 
        else:
            objects.player.chunk = (objects.player.chunk[0]+1, objects.player.chunk[1])
            print(objects.player.chunk)
            objects.player.rect.centerx = 0

    if objects.player.rect.center[1] < 0: # Moving off top of screen
        if objects.player.chunk[1] == objects.mapWidth or objects.player.chunk[1] == 0:
            objects.player.rect.centery = 0
        else:
            objects.player.chunk = (objects.player.chunk[0],objects.player.chunk[1]-1)
            print(objects.player.chunk)
            objects.player.centery = objects.height
            
    if objects.player.rect.center[1] > objects.width: # Moving off bottom of screen
        if objects.player.chunk[1] == objects.mapWidth or objects.player.chunk[1] == objects.mapHeight-1:
            objects.player.rect.centery = objects.height
        else:  
            objects.player.chunk = (objects.player.chunk[0],objects.player.chunk[1]+1)
            print(objects.player.chunk)
            objects.player.rect.centery = 0
    
    objects.currentChunk = objects.chunks[objects.player.chunk[1]][objects.player.chunk[0]]
    objects.currentChunk.update()
    objects.player.update()
    if objects.player.currentHealth <= 0: 
        objects.gamestate = 2

def GameplayRender(): 
    # RENDER (Putting stuff on the screen)
    objects.currentChunk.render()
    objects.player.render()
    
    objects.screen.blit(myFont.render("Coins: "+ str(objects.resourceAmounts["coins"]), True, (0,0,0)), (0,0))
    objects.screen.blit(myFont.render("Health: "+str(objects.player.currentHealth)+"/100", True, (0,0,0)),(100,0))
    pygame.display.flip()

def MenuRender(): 
    objects.screen.fill((255,255,255))
    objects.screen.blit(announcementFont.render("Troubleshooting", True, (0,0,0)), (10,50))
    objects.screen.blit(myFont.render("Press enter to start the game.", True, (0, 0, 0)), (100, 300))
    for button in buttons["menu"]: 
        button.render()
    pygame.display.flip()

def MenuInput():
    pygame.event.pump()
    keys = pygame.key.get_pressed() 

    if keys[pygame.K_RETURN]: 
        print("enter recieved")
        objects.gamestate = 1
        Reset()
        
def MenuUpdate(): 
    for button in buttons["menu"]: 
        button.update()

def GameOverInput(): 
    pygame.event.pump()
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_c]: 
        print("C recieved")
        objects.gamestate = 0

def GameOverUpdate(): 
    pass

def GameOverRender(): 
    objects.screen.fill((0,0,0))
    objects.screen.blit(announcementFont.render("Game Over", True, (255,0,0)), (100,50))
    objects.screen.blit(myFont.render("Press C to continue to the main menu.", True, (255, 0, 0)), (100, 300))
    pygame.display.flip()