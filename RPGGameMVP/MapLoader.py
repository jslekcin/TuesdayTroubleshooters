import Classes
import objects
import pygame
import random
import time

file = {
    "chunks":
    {
        "chunk00": {
            "obstacles": [(250, 250)]
        },
        "chunk33": {
            "obstacles": [(100, 200)]
        }
    }
}

def createDungeon(index, boss, location, chunk, background, portal_image, name):
    objects.chunks[chunk[0]][chunk[1]].contents.append(
        Classes.CollisionButton(portal_image, location,
        ["objects.player.chunk = (-1,"+str(index)+")","objects.player.rect.center = (250,450)"]))
    objects.chunks[-1].append(Classes.Chunk((objects.mapWidth,0),
    background,
      (500,500),
      name))
    objects.chunks[-1][index].contents.append(boss)

# Creating List
for x in range(objects.mapWidth): 
    objects.chunks.append(list())
    for y in range(objects.mapHeight):
        objects.chunks[-1].append(Classes.Chunk((x,y), pygame.image.load("Pixel Images/Grass.png"), (500,500), "Overworld"))
        enemyNum = random.randint(1,5)
        coinNum = 2
        if x == 3 and y == 3:
            coinNum = 4
        if x != 0 or y != 0: 
            for e in range(enemyNum): 
                objects.chunks[x][y].contents.append(Classes.Ghost((random.randint(100,400),random.randint(100,400))))
        for coin in range(coinNum): 
            objects.chunks[x][y].contents.append(Classes.Resource("coins", 10, pygame.transform.scale(pygame.image.load("Pixel Images/Gold Coin.png"), (15,15)), (random.randint(0,500),random.randint(0,500))))

# Manual addition of objects to chunks
#objects.chunks[0][1].contents.append(
#            Classes.Obstacle(pygame.transform.scale(pygame.image.load("TestImage.png"), (50,50)), (250, 250))
#            )
objects.chunks[0][0].contents.append(
    Classes.NPC(pygame.image.load("Pixel Images/Player.png"), (100,100), [
        "if objects.resourceAmounts['coins'] >= 50: objects.player.currentHealth = objects.player.maxHealth;objects.resourceAmounts['coins'] -= 50"]))

objects.chunks[0][0].contents.append(Classes.Building(pygame.image.load("Pixel Images/House.png"), (100,0), 0, (24,50)))

objects.chunks[0][0].contents.append(Classes.NPC(pygame.image.load("Pixel Images/Shop.png"), (400,400), ["objects.shopShowing = not objects.shopShowing", "time.sleep(0.1)"])) #TODO: Fix glitching and freeze game

# Subchunk list
objects.chunks.append(list())

# House in spawn area
objects.chunks[-1].append(Classes.Chunk((objects.mapWidth,0), pygame.image.load("Pixel Images/HouseBackground.png"), (500,500), "Shop"))
objects.chunks[-1][0].contents.append(Classes.CollisionButton(pygame.image.load("Pixel Images/DoorFromInside.png"), (250, 475), ["objects.player.chunk = (0,0)","objects.player.rect.center = (400,200)"]))

# Fire Boss Dungeon
createDungeon(1, Classes.FireGhostBoss(), (450, 350), (objects.mapWidth,0), 
pygame.image.load("Pixel Images/FireBossBackground.png"), pygame.image.load("Pixel Images/FirePortal.png"), "fire dungeon")

# Ice Boss Dungeon
createDungeon(2, Classes.IceGhostBoss(), (450,250), (objects.mapWidth,0), pygame.image.load("Pixel Images/Ice Boss Background.png"), pygame.image.load("Pixel Images/Ice Portal.png"), "ice dungeon")


# Lightning Boss Dungeon
createDungeon(3, Classes.LightningGhostBoss(), (450, 150), (objects.mapWidth,0), 
pygame.image.load("Pixel Images/Lightning Boss Background.png"), pygame.image.load("Pixel Images/Lightning Portal.png"), "lightning dungeon")

# Poison boss
createDungeon(4, Classes.PoisonGhostBoss(), (450, 50), (objects.mapWidth, 0),
pygame.image.load("Pixel Images/Poison Boss Background.png"), pygame.image.load("Pixel Images/Poison Portal.png"), "poison dungeon")

# Summoning Boss 
createDungeon(5, Classes.SummoningGhostBoss(), (50,50),(objects.mapWidth,0),pygame.image.load("Pixel Images/Grass.png"), pygame.image.load("Pixel Images/Summoning Portal.png"), "summoning dungeon")

# Shield Boss 
createDungeon(6, Classes.ShieldGhostBoss(), (50,150),(objects.mapWidth,0),pygame.image.load("Pixel Images/Grass.png"), pygame.image.load("Pixel Images/Summoning Portal.png"), "shield dungeon")
objects.chunks[7][6].contents.append(Classes.MovementBarrier(pygame.transform.scale(pygame.image.load("Pixel Images/WaterBase.png"), (500,100)),(250,250)))

# Laser Boss 
createDungeon(7, Classes.LaserGhostBoss(), (50,250),(objects.mapWidth,0),pygame.image.load("Pixel Images/Grass.png"), pygame.image.load("Pixel Images/FirePortal.png"), "laser dungeon")

# Water Boss 
createDungeon(8, Classes.WaterGhostBoss(), (50,350),(objects.mapWidth,0),pygame.image.load("Pixel Images/Grass.png"), pygame.image.load("Pixel Images/Ice Portal.png"), "water dungeon")
image = pygame.transform.scale(pygame.image.load("Pixel Images/WaterBase.png"), (300,300))
image.set_alpha(10)
objects.chunks[7][8].contents.append(Classes.MovementBarrier(image,(250,250)))

# Final Boss 
createDungeon(9, Classes.FinalBossGhost(), (250,250),(objects.mapWidth,0),pygame.image.load("Pixel Images/Grass.png"), pygame.image.load("Pixel Images/Summoning Portal.png"), "final dungeon")

# Chaotic Fun
objects.chunks[0][2].contents.append(Classes.FireGhostBoss())
objects.chunks[0][2].contents.append(Classes.IceGhostBoss())
objects.chunks[0][2].contents.append(Classes.LightningGhostBoss())
objects.chunks[0][2].contents.append(Classes.PoisonGhostBoss())
objects.chunks[0][2].contents.append(Classes.SummoningGhostBoss())
objects.chunks[0][2].contents.append(Classes.ShieldGhostBoss())
objects.chunks[0][2].contents.append(Classes.LaserGhostBoss())






def load():
    position = file["chunks"]["chunk33"]["obstacles"][0]
    #objects.chunks[3][3].contents.append(
        #Classes.Obstacle(pygame.transform.scale(pygame.image.load("TestImage.png"), (50,50)), position)
        #)