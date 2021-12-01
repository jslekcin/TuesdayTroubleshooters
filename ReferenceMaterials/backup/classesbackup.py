import pygame
import objects
from objects import *
import random
import math

# Creating Player Class
class Player:
    # Player Setup
    def __init__(self):
        self.image = pygame.image.load("Pixel Images/Player.png")
        #self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect()
        self.chunk = (0,0)
        self.currentHealth = 100
        self.last_valid_postion = self.rect.center
        # self.xpos = self.rect[0]+50
        # self.ypos = self.rect[1]+50
        self.type = "player"
    # Function to draw player to screen
    def render(self):
        # pygame.draw.rect(objects.screen, "#000000", self.rect)
        objects.screen.blit(self.image, self.rect)

        pygame.draw.rect(objects.screen, (255,0,0), pygame.Rect(250,0,200,20))
        pygame.draw.rect(objects.screen, (0,255,0), pygame.Rect(250,0,objects.player.currentHealth/100*200,20))
    def move(self, x, y): 
        #self.last_valid_position = self.rect.center
        self.rect = self.rect.move(x,y)
    def update(self):
        pass
    #def NPCHeal(self):
        #if()
    def fireProjectile(self):
        if objects.currentChunk == None:
            return
        
        mousePos = pygame.mouse.get_pos()
        mouseX = mousePos[0]
        mouseY = mousePos[1]
        xGap = mouseX - self.rect.center[0] 
        yGap = mouseY - self.rect.center[1] 
        distance = (xGap**2+yGap**2)**(1/2)
        if distance != 0:
            factor = distance/10
            moveX = xGap / factor
            moveY = yGap / factor
            rotation =  math.degrees(math.atan(xGap / yGap)) + 90
            if yGap > 0:
                rotation += 180
            objects.currentChunk.contents.append(Arrow((moveX, moveY), rotation))
        
# Chunks of the map
class Chunk: 
    def __init__(self, location, image, size):
        self.location = location
        self.contents = []
        self.image = image
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
    def render(self):
        objects.screen.blit(self.image, self.rect)
        for resource in self.contents: 
            resource.render()
    def update(self): 
        for thing in self.contents: 
            thing.update()
    
# Resource Class
class Resource: 
    def __init__(self, item, quantity, image, location):
        self.item = item
        self.quantity = quantity
        self.image = pygame.image.load("Pixel Images/Gold Coin.png")
        #self.image = pygame.transform.scale(self.image, (10,10))
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = "resource"
    def render(self): 
        objects.screen.blit(self.image, self.rect)
    def update(self):
        if objects.player.rect.colliderect(self.rect):
            objects.currentChunk.contents.remove(self)
            objects.resourceAmounts["coins"] += 10
            print(objects.resourceAmounts["coins"])

class Enemy: 
    def __init__(self, location): 
        self.rect = None
        self.health = None
        self.image = None
        self.attackDamage = None
        self.speed = None
        self.location = location
        self.type = None
    def render(self): 
        objects.screen.blit(self.image, self.rect)
    def update(self): 
        pass

class Ghost(Enemy):
    def __init__(self, location): 
        self.health = 20
        self.image = pygame.image.load("Pixel Images/Ghost Enemy.png")
        self.speed = 2
        self.attackDamage = 10
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = "enemy"
    def update(self):
        playerX = objects.player.rect.center[0] 
        playerY = objects.player.rect.center[1]
        xGap = playerX - self.rect.center[0] 
        yGap = playerY - self.rect.center[1] 
        distance = (xGap**2+yGap**2)**(1/2)
        if distance != 0:
            factor = distance/self.speed
            moveX = xGap / factor
            moveY = yGap / factor
        self.rect = (self.rect.move((moveX, moveY)))
        if self.rect.colliderect(objects.player.rect): 
            objects.player.currentHealth -= self.attackDamage
            while self.rect.colliderect(objects.player.rect): 
                self.rect.center = (random.randint(0,objects.width), random.randint(0, objects.height))
        for projectile in objects.currentChunk.contents:
            if projectile.type == "arrow" and self.rect.colliderect(projectile.rect):
                self.health -= projectile.attackDamage
                objects.currentChunk.contents.remove(projectile)
            if self.health <= 0: 
                objects.currentChunk.contents.remove(self)
                return

class FireGhostBoss(Enemy):
    def __init__(self):
        self.image = pygame.image.load("Pixel Images/Fire Boss.png")
        self.rect =  self.image.get_rect()
        self.rect.center = (250,250)
        self.attackDamage = 25
        self.speed = 10
        self.type = "enemy"
        self.direction = 0
        self.counter = 0
        self.health = 200
    def render(self): 
        objects.screen.blit(self.image, self.rect)
        pygame.draw.rect(objects.screen, (255,0,0), pygame.Rect(150,25,200,20))
        pygame.draw.rect(objects.screen, (0,255,0), pygame.Rect(150,25,self.health,20))
        
    def update(self):
        # Changing directions after bouncing
        if self.rect.left < 0: 
            self.direction = random.random() * math.pi - math.pi/2
        if self.rect.right > objects.width: 
            self.direction = random.random() * math.pi + math.pi/2
        if self.rect.top < 0: 
            self.direction = random.random() * math.pi + math.pi
        if self.rect.bottom > objects.height: 
            self.direction = random.random() * math.pi
        # Moving
        self.rect.center = (self.rect.centerx + self.speed*math.cos(self.direction), self.rect.centery - self.speed*math.sin(self.direction))
        # Checking for collision with player
        if self.rect.colliderect(objects.player.rect): 
            objects.player.currentHealth = objects.player.currentHealth - self.attackDamage
            while self.rect.colliderect(objects.player.rect): 
                self.rect.center = (random.randint(0,objects.width), random.randint(0, objects.height))
        # Shooting fireballs on a timer
        self.counter = self.counter + 1
        if self.counter == 10:
            print("shootFireball")
            playerPos = objects.player.rect.center
            xGap = playerPos[0] - self.rect.center[0]
            yGap = playerPos[1] - self.rect.center[1] 
            distance = (xGap**2+yGap**2)**(1/2)
            if distance != 0:
                factor = distance/10
                moveX = xGap / factor
                moveY = yGap / factor
                rotation =  math.degrees(math.atan(xGap / yGap)) + 90
            if yGap > 0:
                rotation += 180
            objects.currentChunk.contents.append(EnemyFireball((moveX, moveY), rotation, self.rect.center))
            self.counter = 0
        # Getting hit by arrows
        for projectile in objects.currentChunk.contents:
            if projectile.type == "arrow" and self.rect.colliderect(projectile.rect):
                self.health -= projectile.attackDamage
                objects.currentChunk.contents.remove(projectile)
            if self.health <= 0: 
                objects.currentChunk.contents.remove(self)
                return
            
class Arrow:
    def __init__(self,direction,rotationAngle):
        self.image = pygame.image.load("Pixel Images/Arrow.png")
        self.image = pygame.transform.rotate(self.image, rotationAngle)
        self.rect = self.image.get_rect()
        self.rect.center = objects.player.rect.center
        self.direction = direction
        self.attackDamage = 10
        self.type = "arrow"
    def render(self):
        pygame.draw.rect(objects.screen, "#000000", self.rect) 
        objects.screen.blit(self.image, self.rect)
    def update(self):
        self.rect = self.rect.move(self.direction)
        if not objects.screen.get_rect().contains(self.rect):
            objects.currentChunk.contents.remove(self)            
            
class EnemyFireball:
    def __init__(self,direction,rotationAngle,spawnPos):
        self.image = pygame.image.load("Pixel Images/Fireball.png")
        self.image = pygame.transform.rotate(self.image, rotationAngle)
        self.rect = self.image.get_rect()
        self.rect.center = spawnPos
        self.direction = direction
        self.attackDamage = 10
        self.type = "enemyProjectile"
    def render(self):
        # pygame.draw.rect(objects.screen, "#000000", self.rect) 
        objects.screen.blit(self.image, self.rect)
    def update(self):
        self.rect = self.rect.move(self.direction)
        if self.rect.colliderect(objects.player.rect): 
            objects.player.currentHealth = objects.player.currentHealth - self.attackDamage 
            objects.currentChunk.contents.remove(self)


        if not objects.screen.get_rect().contains(self.rect):
            objects.currentChunk.contents.remove(self)

class Obstacle: 
    def __init__(self, image, location): 
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = "obstacle"
        self.interact = ["player", "arrow"]
    def render(self):
        objects.screen.blit(self.image, self.rect)
    def update(self):
        for obj in objects.currentChunk.contents:
            if obj.type in self.interact: 
                if self.rect.colliderect(obj.rect): 
                    if obj.type == "arrow": 
                        objects.currentChunk.contents.remove(obj)
        if self.rect.colliderect(objects.player.rect): 
            objects.player.rect.center = objects.player.last_valid_position

class Button: 
    def __init__(self, image, location, effects):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.effects = effects
    def render(self): 
        objects.screen.blit(self.image, self.rect)
    def update(self): 
        if pygame.mouse.get_pressed(): 
            mousePos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mousePos): 
                for action in self.effects:
                    exec(action)

class NPC: 
    def __init__(self, image, location, effects):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.effects = effects
        self.type = "NPC"
    def render (self): 
        objects.screen.blit(self.image, self.rect)
    def update(self): 
        if pygame.mouse.get_pressed(3)[0]:
            mousePos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mousePos): 
                for action in self.effects:
                    exec(action)

class Building:
    def __init__(self, image, location, subchunk, doorSize):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.subchunk = subchunk
        self.type = "building"
        self.doorRect = pygame.Rect((0,0), doorSize)
        self.doorRect.midbottom = self.rect.midbottom
    def render(self):
        objects.screen.blit(self.image, self.rect)
    def update(self):
        if objects.player.rect.colliderect(self.doorRect): 
            objects.player.chunk = (self.subchunk,objects.mapWidth)
            objects.player.rect.center = (250, 425)
            
        
        #for obj in objects.currentChunk.contents:
        #    if obj.type in self.interact: 
        #        if self.rect.colliderect(obj.rect): 
        #            if obj.type == "projectile": 
        #                objects.currentChunk.contents.remove(obj)
        #if self.rect.colliderect(objects.player.rect): 
        #    if objects.player.rect.center = objects.player.last_valid_position

class CollisionButton: 
    def __init__(self, image, location, effects): 
        self.effects = effects
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = "collisionButton"
    def render(self): 
        objects.screen.blit(self.image, self.rect)
    def update(self): 
        if objects.player.rect.colliderect(self.rect): 
            for effect in self.effects: 
                exec(effect)