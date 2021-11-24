import pygame
import objects
import random
import math
import time
import webbrowser

# Quest System Steps

# 1) Somewhere to remember all of our quests - List
# 2) A format to save our quests that has the completions state and the instructions - Class
#    Things the quests need to know: Instructions, Quest complete state
# 3) A way to display our quests, either in pause menu or on the UI - A part of gameFunctions
# 4) Creating all of our quests main and side - A document/file or somthing

# Reset Main Boss Functionality
# 1) Pause our other functionality - State machine
# 2) Setup a 


# Creating Player Class
class Player:
    # Player Setup
    def __init__(self):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Player.png")
        self.rect = self.image.get_rect()
        self.chunk = (0,0)
        self.currentHealth = 100
        self.maxEnergy = 100
        self.maxHealth = 100
        self.last_valid_postion = self.rect.center
        self.type = "player"
        self.currentAbility = 0
        self.invulnerability = False
        objects.abilities[0] = FireArrow()
        #objects.abilities[1] = LaunchFireball() 
        #objects.abilities[2] = Freeze()
        #objects.abilities[3] = ElectroDash()
        #objects.abilities[4] = PoisonField()
        #objects.abilities[5] = SummonAbility()
        #objects.abilities[6] = MagicalShield()
        #objects.abilities[7] = FireLaserArrow()
        #objects.abilities[8] = LaunchWave()
        objects.abilities[9] = PotionAbility()

        #objects.resourceAmounts["ghostEnergy"] = objects.maxEnergys
    # Function to draw player to screen
    def render(self):
        # pygame.draw.rect(objects.screen, "#000000", self.rect)
        objects.screen.blit(self.image, self.rect)
        objects.abilities[objects.player.currentAbility].render()
        if self.currentHealth > self.maxHealth: 
            self.currentHealth = self.maxHealth
        if objects.resourceAmounts["ghostEnergy"] > self.maxEnergy: 
            objects.resourceAmounts["ghostEnergy"] = self.maxEnergy
    def move(self, x, y): 
        #self.last_valid_position = self.rect.center
        self.rect = self.rect.move(x,y)
    def update(self):
        objects.abilities[objects.player.currentAbility].update()

class FireArrow(): # Ability 1: Fires an arrow projectile
    def __init__(self):
        self.fireRate = .5 * objects.framerate
        self.cooldown = 0

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        if objects.currentChunk == None:
            return

        if pygame.mouse.get_pressed(3)[0]:
            mousePos = pygame.mouse.get_pos()
            mouseX = mousePos[0]
            mouseY = mousePos[1]
            xGap = mouseX - objects.player.rect.centerx 
            yGap = mouseY - objects.player.rect.centery
            if yGap == 0:
                yGap = 0.01 
            distance = (xGap**2+yGap**2)**(1/2)
            if distance != 0:
                factor = distance/20
                moveX = xGap / factor
                moveY = yGap / factor
                rotation =  math.degrees(math.atan(xGap / yGap)) + 90
                if yGap > 0:
                    rotation += 180
                objects.currentChunk.contents.append(Arrow((moveX, moveY), rotation))
            self.cooldown = self.fireRate
    
    def render(self):
        return

class Arrow:
    def __init__(self,direction,rotationAngle):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Arrow.png")
        self.image = pygame.transform.rotate(self.image, rotationAngle)
        self.rect = self.image.get_rect()
        self.rect.center = objects.player.rect.center
        self.direction = direction
        self.attackDamage = 10
        self.type = "arrow"
    def render(self):
        #pygame.draw.rect(objects.screen, "#000000", self.rect) 
        objects.screen.blit(self.image, self.rect)
    def update(self):
        self.rect = self.rect.move(self.direction)
        if not objects.screen.get_rect().contains(self.rect):
            objects.currentChunk.contents.remove(self)
        for enemy in objects.currentChunk.contents:
            if enemy.type == "enemy" and self.rect.colliderect(enemy.rect):
                enemy.health -= self.attackDamage
                try:
                    objects.currentChunk.contents.remove(self)
                except ValueError:
                    print(f"something with the arrow {self} is wrong")
                break

class LaunchFireball:
    def __init__(self):
        self.fireRate = .1 * objects.framerate
        self.cooldown = 0
        self.cost = 10

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        if objects.currentChunk == None:
            return

        if pygame.mouse.get_pressed(3)[0] and objects.resourceAmounts["ghostEnergy"] >= self.cost:
            mousePos = pygame.mouse.get_pos()
            mouseX = mousePos[0]
            mouseY = mousePos[1]
            xGap = mouseX - objects.player.rect.centerx 
            yGap = mouseY - objects.player.rect.centery
            if yGap == 0:
                yGap = 0.01 
            distance = (xGap**2+yGap**2)**(1/2)
            if distance != 0:
                factor = distance/10
                moveX = xGap / factor
                moveY = yGap / factor
                rotation =  math.degrees(math.atan(xGap / yGap)) + 90
                if yGap > 0:
                    rotation += 180
                objects.currentChunk.contents.append(Fireball("large", (moveX, moveY), rotation, None))
            self.cooldown = self.fireRate
            objects.resourceAmounts["ghostEnergy"] = objects.resourceAmounts["ghostEnergy"] - self.cost

    def render(self):
        return

class Fireball:
    def __init__(self,size,direction,rotationAngle, position):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Fireball.png")
        self.size = size
        self.attackDamage = 20
        if self.size == "small": 
            self.image = pygame.transform.scale(self.image, (20,10))
            self.attackDamage = 10
        self.image = pygame.transform.rotate(self.image, rotationAngle)
        self.rect = self.image.get_rect()
        self.rect.center = objects.player.rect.center
        if self.size == "small": 
            self.rect.center = position
        self.direction = direction
        self.type = "fireball"
    def render(self):
        #pygame.draw.rect(objects.screen, "#000000", self.rect) 
        objects.screen.blit(self.image, self.rect)
    def update(self):
        self.rect = self.rect.move(self.direction)
        if not objects.screen.get_rect().contains(self.rect):
            objects.currentChunk.contents.remove(self)
        for enemy in objects.currentChunk.contents:
            if enemy.type == "enemy" and self.rect.colliderect(enemy.rect):
                enemy.health -= self.attackDamage
                objects.currentChunk.contents.remove(self)
                if self.size != "small": 
                    objects.currentChunk.contents.append(Fireball("small", (10,0), 0, self.rect.center))
                    objects.currentChunk.contents.append(Fireball("small", (-10,0), 180, self.rect.center))
                    objects.currentChunk.contents.append(Fireball("small", (0,-10), 90, self.rect.center))
                    objects.currentChunk.contents.append(Fireball("small", (0,10), 270, self.rect.center))

class Freeze: 
    def __init__(self):
        self.cost = 25 
    def update(self):
        if objects.resourceAmounts["ghostEnergy"] < self.cost:
            return
        if pygame.mouse.get_pressed(3)[0] and Freeze.timer == Freeze.cooldown:
            objects.resourceAmounts["ghostEnergy"] = objects.resourceAmounts["ghostEnergy"] - self.cost
            objects.freeze = True

    cooldown = 100
    timer = 100
    def freezeCD():
        if Freeze.timer == 0:
            Freeze.timer = Freeze.cooldown
            objects.freeze = False
            return
        Freeze.timer -= 1
    
    def render(self):
        return # TODO: Move freeze overlay to here

class ElectroDash:
    def __init__(self):
        self.fireRate = .1 * objects.framerate
        self.cooldown = 0
        self.cost = 15
        self.dashSpeed = 25
        self.damage = 25
        self.dashPositions = []

    def update(self):
        if len(self.dashPositions) != 0:
            # Move to first postition in list
            objects.player.rect.center = self.dashPositions[0]
            # Remove position
            self.dashPositions.remove(self.dashPositions[0])
            # Remember any enemies that we collide with
            collided = []
            for enemy in objects.currentChunk.contents: 
                if enemy.type == "enemy": 
                    if objects.player.rect.colliderect(enemy.rect): 
                        collided.append(enemy)
            # Damage collided enemies
            for enemy in collided: 
                enemy.health = enemy.health - self.damage
            if len(self.dashPositions) == 0:
                objects.player.invulnerability = False
                

        if self.cooldown > 0:
            self.cooldown -= 1
            return

        if objects.currentChunk == None:
            return

        if len(self.dashPositions) == 0 and pygame.mouse.get_pressed(3)[0] and objects.resourceAmounts["ghostEnergy"] >= self.cost:
            mousePos = pygame.mouse.get_pos()
            # Find the incremental amount to get there
            totalXdist = mousePos[0]-objects.player.rect.centerx
            totalYdist = mousePos[1]-objects.player.rect.centery
            totaldist  = (totalXdist**2+totalYdist**2)**.5
            ratio = totaldist/self.dashSpeed
            if ratio == 0:
                return
            # Find future positions
            if ratio > 1:
                xdist = totalXdist/ratio
                ydist = totalYdist/ratio
                x = objects.player.rect.centerx
                y = objects.player.rect.centery
                self.dashPositions.append((x + xdist, y + ydist))
                ratio -= 1
                while ratio > 1:
                    self.dashPositions.append((self.dashPositions[-1][0]+ xdist, self.dashPositions[-1][1]+ ydist))
                    ratio -= 1
            self.dashPositions.append(mousePos)
            self.cooldown = self.fireRate
            objects.player.invulnerability = True

    def render(self):
        return

class PoisonField: 
    def __init__(self): 
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Poison Effect.png")
        self.image.set_alpha(150)
        self.cooldown = 0
        self.duration = 5 * objects.framerate
        self.cost = 0
        self.damage = 1
        self.rect = self.image.get_rect()
    def update(self): 
        if self.cooldown == 0 and pygame.mouse.get_pressed(3)[0] and objects.resourceAmounts["ghostEnergy"] >= self.cost:
            self.cooldown = self.duration
            objects.resourceAmounts["ghostEnergy"]-=self.cost
        if self.cooldown != 0:
            # Check for enemies and damage them
            self.rect.center = objects.player.rect.center
            for thing in objects.currentChunk.contents: 
                if thing.type == "enemy" and thing.rect.colliderect(self.rect): 
                    thing.health -= 1
            self.cooldown -= 1

    def render(self):
        if self.cooldown != 0:
            # render image # TODO: make a render method for all of our abilities so that this can render after our map
            objects.screen.blit(self.image, self.rect)

class SummonAbility:
    def __init__(self): 
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Ghost Enemy.png")
        self.speed = 10
        self.attackDamage = 20
        self.rect = self.image.get_rect()
        self.rect.center = (250,250)
        self.type = "projectile"
        self.active = False
        self.counter = 0
        self.lastChunk = (0,0)
    def render(self): 
        if self.active: 
            self.image.set_alpha(((objects.framerate * 10) - self.counter)/(objects.framerate * 10)*200+55)
            objects.screen.blit(self.image, self.rect)
    def update(self): 
        # Check if the currentchunk is different
        # if it is move the position back to player
        if objects.currentChunk != self.lastChunk:
            self.rect.center = objects.player.rect.center

        if pygame.mouse.get_pressed(3)[0]: 
            self.active = True
            self.rect.center = objects.player.rect.center
        if self.active:
            mousePos = pygame.mouse.get_pos()
            xGap = mousePos[0] - self.rect.center[0] 
            yGap = mousePos[1] - self.rect.center[1] 
            distance = (xGap**2+yGap**2)**(1/2)
            if distance != 0:
                factor = distance/self.speed
                moveX = xGap / factor
                moveY = yGap / factor
                self.rect = self.rect.move((moveX, moveY))
            for enemy in objects.currentChunk.contents: 
                if enemy.type == "enemy" and self.rect.colliderect(enemy.rect): 
                    enemy.health -= self.attackDamage 
                    self.rect.center = objects.player.rect.center
            if self.counter >= objects.framerate * 10: 
                self.counter = 0
                self.active = False    
            self.counter += 1

class MagicalShield: 
    def __init__(self): 
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Magical Shield.png")
        self.rect = self.image.get_rect() 
        self.cooldown = 0
        self.duration = 5 * objects.framerate
        self.cost = 0
        self.active = False
    def render(self): 
        if self.active: 
            objects.screen.blit(self.image, self.rect)
    def update(self): 
        self.rect.center = objects.player.rect.center
        if pygame.mouse.get_pressed(3)[0] and objects.resourceAmounts["ghostEnergy"] >= self.cost:
            self.active = True
            objects.resourceAmounts["ghostEnergy"]-=self.cost
        if self.active: 
            objects.player.invulnerability = True 
            self.cooldown += 1
        if self.cooldown == self.duration: 
            self.active = False 
            objects.player.invulnerability = False 

class FireLaserArrow(): # Ability 8: Fires a laser arrow projectile
    def __init__(self):
        self.fireRate = .5 * objects.framerate
        self.cooldown = 0

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        if objects.currentChunk == None:
            return

        if pygame.mouse.get_pressed(3)[0]:
            mousePos = pygame.mouse.get_pos()
            mouseX = mousePos[0]
            mouseY = mousePos[1]
            xGap = mouseX - objects.player.rect.centerx 
            yGap = mouseY - objects.player.rect.centery
            if yGap == 0:
                yGap = 0.01 
            distance = (xGap**2+yGap**2)**(1/2)
            if distance != 0:
                factor = distance/20
                moveX = xGap / factor
                moveY = yGap / factor
                rotation =  math.degrees(math.atan(xGap / yGap)) + 90
                if yGap > 0:
                    rotation += 180
                objects.currentChunk.contents.append(LaserArrow((moveX*2, moveY*2), rotation))
            self.cooldown = self.fireRate
    
    def render(self):
        return

class LaserArrow:
    def __init__(self,direction,rotationAngle):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Laser Arrow.png")
        self.image = pygame.transform.scale(self.image, (40,10))
        self.image = pygame.transform.rotate(self.image, rotationAngle)
        
        self.rect = self.image.get_rect()
        self.rect.center = objects.player.rect.center
        self.direction = direction
        self.attackDamage = 25
        self.type = "laserarrow"
    def render(self):
        #pygame.draw.rect(objects.screen, "#000000", self.rect) 
        objects.screen.blit(self.image, self.rect)
    def update(self):
        self.rect = self.rect.move(self.direction)
        if not objects.screen.get_rect().contains(self.rect):
            objects.currentChunk.contents.remove(self)
        for enemy in objects.currentChunk.contents:
            if enemy.type == "enemy" and self.rect.colliderect(enemy.rect):
                enemy.health -= self.attackDamage

class LaunchWave(): # Ability 9: Fires a wave projectile with knockback
    def __init__(self):
        self.fireRate = .5 * objects.framerate
        self.cooldown = 0

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        if objects.currentChunk == None:
            return

        if pygame.mouse.get_pressed(3)[0]:
            mousePos = pygame.mouse.get_pos()
            mouseX = mousePos[0]
            mouseY = mousePos[1]
            xGap = mouseX - objects.player.rect.centerx 
            yGap = mouseY - objects.player.rect.centery
            if yGap == 0:
                yGap = 0.01 
            distance = (xGap**2+yGap**2)**(1/2)
            if distance != 0:
                factor = distance/20
                moveX = xGap / factor
                moveY = yGap / factor
                rotation =  math.degrees(math.atan(xGap / yGap)) + 90
                if yGap > 0:
                    rotation += 180
                objects.currentChunk.contents.append(Wave((moveX, moveY), rotation))
                objects.currentChunk.contents.append(Wave((moveX*-1, moveY*-1), rotation+180))
                objects.currentChunk.contents.append(Wave((moveY, moveX*-1), rotation+90))
                objects.currentChunk.contents.append(Wave((moveY*-1, moveX), rotation+270))
            self.cooldown = self.fireRate
    
    def render(self):
        return

class Wave:
    def __init__(self,direction,rotationAngle):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Wave.png")
        if rotationAngle > 360: 
            rotationAngle -= 360
        self.image = pygame.transform.scale(self.image, (100,200))
        self.image = pygame.transform.rotate(self.image, rotationAngle)
    
        self.rect = self.image.get_rect()
        self.rect.center = objects.player.rect.center
        self.direction = direction
        self.attackDamage = 1
        self.type = "wave"
    def render(self):
        #pygame.draw.rect(objects.screen, "#000000", self.rect) 
        objects.screen.blit(self.image, self.rect)
    def update(self):
        self.rect = self.rect.move(self.direction)
        if not self.rect.colliderect(pygame.Rect(0,0,500,500)):
            objects.currentChunk.contents.remove(self)
        for enemy in objects.currentChunk.contents:
            if enemy.type == "enemy" and self.rect.colliderect(enemy.rect):
                if type(enemy) == Ghost or type(enemy) == LargeGhost: 
                    enemy.knocked = True 
                    enemy.direction = self.direction
                enemy.health -= self.attackDamage

class PotionAbility: 
    types = ["purple","red","blue","gold"]
    images = [pygame.transform.scale(pygame.image.load("RPGGameMVP\Pixel Images\Purple Potion.png"),(50,50)),pygame.transform.scale(pygame.image.load("RPGGameMVP\Pixel Images\Red Potion.png"),(50,50)),pygame.transform.scale(pygame.image.load("RPGGameMVP\Pixel Images\Blue Potion.png"),(50,50)),pygame.transform.scale(pygame.image.load("RPGGameMVP\Pixel Images\Gold Potion.png"),(50,50))]
    number = 0
    def __init__(self): 
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Poison Effect.png")
        self.mousePressed = False
        self.cooldown = 0
        self.duration = objects.framerate
    def update(self): 
        if pygame.mouse.get_pressed(3)[2] and self.mousePressed == False: 
            self.mousePressed = True
            PotionAbility.number += 1
            if PotionAbility.number == 4: 
                PotionAbility.number = 0
            objects.abilityPanel[9] = PotionAbility.images[PotionAbility.number]
        if not pygame.mouse.get_pressed(3)[2]: 
            self.mousePressed = False
        
        if self.cooldown == 0 and pygame.mouse.get_pressed(3)[0] and objects.potions[PotionAbility.types[PotionAbility.number]] >= 1:
            self.cooldown = self.duration
            objects.potions[PotionAbility.types[PotionAbility.number]] -= 1
            for i in objects.potionEffects[PotionAbility.types[PotionAbility.number]]: 
                exec(i)

        if self.cooldown > 0:
            self.cooldown -= 1
            
    def render(self):
        potionText = objects.myFont.render("Amount of Equipped Potion ["+PotionAbility.types[PotionAbility.number]+"]: "+str(objects.potions[PotionAbility.types[PotionAbility.number]]),False,(0,0,0))
        objects.screen.blit(potionText, (0,50))

# Chunks of the map
class Chunk: 
    def __init__(self, location, image, size, chunk_type: str):
        self.location = location
        self.contents = []
        self.image = image
        self.image = pygame.transform.scale(self.image, size)
        if self.location[0] != 7: 
            for i in range(10): 
                self.image.blit(pygame.image.load("RPGGameMVP\Pixel Images\TallGrass.png"), (random.randint(0,500),random.randint(0,500)))
                
        self.rect = self.image.get_rect()
        self.nightOverlay = pygame.Surface(objects.size)
        self.nightOverlay.fill((0,0,50))
        self.chunk_type = chunk_type
    def render(self):
        objects.screen.blit(self.image, self.rect)
        for resource in self.contents: 
            resource.render()
        if self.location[0] is not objects.mapWidth and objects.daytime is False:
            self.nightOverlay.set_alpha(100)
            objects.screen.blit(self.nightOverlay, (0,0))
    def update(self): 
        for thing in self.contents:
            thing.update()
    
    def __repr__(self):
        return f"{self.location} {self.chunk_type}"
        
class Quest:
    def __init__(self, text, condition, name): # all inputs are strings
        self.text = text 
        self.condition = condition 
        self.name = name 
        self.data = 0
        self.complete = False
    def render(self):
        pass

    def update(self):
        if eval(self.condition): 
            self.complete = True

# Resource Class
class Resource: 
    def __init__(self, item, quantity, image, location):
        self.item = item
        self.quantity = quantity
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Gold Coin.png")
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
        self.maxHealth = 20
        self.health = self.maxHealth
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Ghost Enemy.png")
        self.speed = 2
        self.attackDamage = 10
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = "enemy"
        self.drops = 5
        self.knocked = False
        self.direction = (0,0)
    def render(self): 
        self.image.set_alpha((self.health/self.maxHealth)*255)
        objects.screen.blit(self.image, self.rect)
        
        pygame.draw.rect(objects.screen, (0,0,0), pygame.Rect(self.rect.left,self.rect.top-self.rect[3]*.1,self.rect[2],self.rect[3]*.1))
        pygame.draw.rect(objects.screen, (255,0,0), pygame.Rect(self.rect.left,self.rect.top-self.rect[3]*.1,self.rect[2]*(self.health/self.maxHealth),self.rect[3]*.1))
    def update(self):
        if not self.knocked: 
            playerX = objects.player.rect.center[0] 
            playerY = objects.player.rect.center[1]
            xGap = playerX - self.rect.center[0] 
            yGap = playerY - self.rect.center[1] 
            distance = (xGap**2+yGap**2)**(1/2)
            if distance != 0:
                factor = distance/self.speed
                moveX = xGap / factor
                moveY = yGap / factor
                self.direction = (moveX, moveY)
        self.rect = (self.rect.move(self.direction))
        # Check which side of the screen we are off and then move us back on
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 500:
            self.rect.right = 500
        if self.rect.top > 500:
            self.rect.top = 500
        if self.rect.bottom < 0:
            self.rect.bottom = 0;

            #self.rect = self.rect.move((-self.direction[0],-self.direction[1])) 
            self.knocked = False
        
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability:      
                objects.player.currentHealth -= self.attackDamage
            while self.rect.colliderect(objects.player.rect): 
                self.rect.center = (random.randint(100,objects.width-100), random.randint(100, objects.height-100))
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            if objects.currentChunk.location[0]+1 != len(objects.chunks): 
                objects.resourceAmounts["ghostEnergy"] = objects.resourceAmounts["ghostEnergy"] + self.drops
                objects.currentChunk.contents.append(QuestionCube(self.rect.center))
            return

class LargeGhost(Ghost): 
    def __init__(self, location): 
        self.maxHealth = 50
        self.health = self.maxHealth
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Large Ghost.png")
        self.speed = 5
        self.attackDamage = 20
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = "enemy"
        self.drops = 25
        self.knocked = False

class FireGhostBoss(Enemy):
    def __init__(self):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Fire Boss.png")
        self.rect =  self.image.get_rect()
        self.rect.center = (250,250)
        self.attackDamage = 25
        self.speed = 5
        self.type = "enemy"
        self.angle = 0
        self.counter = 0
        self.maxHealth = 200
        self.health = self.maxHealth
    def render(self): 
        self.image.set_alpha((self.health/self.maxHealth)*255)
        objects.screen.blit(self.image, self.rect)
        objects.screen.blit(self.image, self.rect)
        pygame.draw.rect(objects.screen, (15,15,15), pygame.Rect(300,50 ,200,20))
        pygame.draw.rect(objects.screen, (255,0,0), pygame.Rect(300,50,self.health,20))
        
    def update(self):
        # Changing directions after bouncing
        if self.rect.left < 0: 
            self.angle = random.random() * math.pi - math.pi/2
        if self.rect.right > objects.width: 
            self.angle = random.random() * math.pi + math.pi/2
        if self.rect.top < 0: 
            self.angle = random.random() * math.pi + math.pi
        if self.rect.bottom > objects.height: 
            self.angle = random.random() * math.pi
        # Moving
        
        self.rect.center = (self.rect.centerx + self.speed*math.cos(self.angle), self.rect.centery - self.speed*math.sin(self.angle))
        # Checking for collision with player
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability:
                objects.player.currentHealth = objects.player.currentHealth - self.attackDamage
            while self.rect.colliderect(objects.player.rect): 
                self.rect.center = (random.randint(0,objects.width), random.randint(0, objects.height))
        # Shooting fireballs on a timer
        self.counter = self.counter + 1
        if self.counter == 10:
            playerPos = objects.player.rect.center
            xGap = playerPos[0] - self.rect.center[0]
            yGap = playerPos[1] - self.rect.center[1] 
            distance = (xGap**2+yGap**2)**(1/2)
            if yGap == 0:
                yGap = .01
            if distance != 0:
                factor = distance/5
                moveX = xGap / factor
                moveY = yGap / factor
                rotation =  math.degrees(math.atan(xGap / yGap)) + 90 # y/x
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
                objects.player.maxHealth = objects.player.maxHealth + 25
                objects.player.maxEnergy = objects.player.maxEnergy + 25
                objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
                objects.player.currentHealth = objects.player.maxHealth
                objects.abilities[1] = LaunchFireball()
                objects.player.chunk = (0,0)
                objects.player.rect.center = (400,400)
                print("REPORT: You have defeated the fire ghost.")
                print("NEW ABILITY: FIREBALL")
                print("Ability Information: The fireball ability allows you to launch a fireball that does high damage and explodes upon contact, launching 4 smaller fireballs in different directions. This ability uses up 10 ghost energy per use. Press 2 to switch to the fireball ability from another ability.")
                objects.FindQuest("The Fire Boss").data = True
                for i in objects.chunks[1][0].contents: 
                    if type(i) == CollisionButton: 
                        objects.chunks[1][0].contents.remove(i)
                return

class IceGhostBoss(Ghost): 
    def __init__(self):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Ice Boss.png")
        self.rect = self.image.get_rect()
        self.rect.center = (250,250)
        self.type = "enemy"
        self.speed = 5
        self.maxHealth = 400
        self.health = 400
        self.attackDamage = 10
        self.direction = 90
        self.counter = 0

    def render(self):
        self.image.set_alpha((self.health/self.maxHealth)*255)
        objects.screen.blit(self.image, self.rect)
        objects.screen.blit(self.image, self.rect)
        pygame.draw.rect(objects.screen, (15,15,15), pygame.Rect(150,25,200,20))
        pygame.draw.rect(objects.screen, (255,0,0), pygame.Rect(150,25,self.health/self.maxHealth*200,20))

    def update(self):
        # Changing directions after bouncing
        if self.rect.left < 0 or self.rect.right > objects.width or self.rect.top < 0 or self.rect.bottom > objects.height:
            playerPos = objects.player.rect.center
            xGap = playerPos[0] - self.rect.centerx
            yGap = playerPos[1] - self.rect.centery
            if yGap == 0:
                yGap = .01
            self.direction = math.atan(yGap / xGap)
            if xGap < 0:
                self.direction += math.pi
        # Moving
        self.rect.center = (self.rect.centerx + self.speed*math.cos(self.direction), self.rect.centery + self.speed*math.sin(self.direction))
        # Checking for collision with player
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth = objects.player.currentHealth - self.attackDamage
            while self.rect.colliderect(objects.player.rect): 
                self.rect.center = (random.randint(0,objects.width), random.randint(0, objects.height))
        # Shooting icicles on a timer
        self.counter = self.counter + 1
        if self.counter == 60:
            playerPos = objects.player.rect.center
            xGap = playerPos[0] - self.rect.center[0]
            yGap = playerPos[1] - self.rect.center[1] 
            distance = (xGap**2+yGap**2)**(1/2)
            if yGap == 0:
                yGap = .01
            if distance != 0:
                factor = distance/5
                moveX = xGap / factor * 2
                moveY = yGap / factor * 2
                rotation =  math.degrees(math.atan(xGap / yGap)) + 90
            if yGap > 0:
                rotation += 180
            objects.currentChunk.contents.append(EnemyIcicle((moveX, moveY), rotation, self.rect.center))
            self.counter = 0
        # Getting hit by arrows
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            objects.player.maxHealth = objects.player.maxHealth + 25
            objects.player.maxEnergy = objects.player.maxEnergy + 25
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
            objects.player.currentHealth = objects.player.maxHealth
            objects.abilities[2] = Freeze()
            objects.player.chunk = (0,0)
            objects.player.rect.center = (400,400)
            
            print("REPORT: You have defeated the ice ghost.")
            print("NEW ABILITY: FREEZE")
            print("Ability Information: The freeze ability allows you to freeze all enemies on the screen for 3 seconds. This ability uses up 25 ghost energy per use. Press 3 to switch to the freeze ability from another ability.")
            objects.FindQuest("The Ice Boss").data = True
            for i in objects.chunks[0][1].contents: 
                if i.type == "collisionButton": 
                    objects.chunks[0][1].contents.remove(i)
            return

class LightningGhostBoss(Enemy):
    def __init__(self):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Lightning Boss.png")
        self.shadowImage = pygame.image.load("RPGGameMVP\Pixel Images\Lightning Boss Shadow.png")
        self.shadowRect = self.shadowImage.get_rect()
        self.rect =  self.image.get_rect()
        self.rect.center = (250,250)
        self.attackDamage = 50
        self.speed = 25
        self.type = "enemy"
        self.nextLocation = (250,250)
        self.shadowRect.center = self.nextLocation
        self.counter = 0
        self.maxHealth = 600
        self.health = self.maxHealth
        self.moving = False
    def render(self): 
        self.image.set_alpha((self.health/self.maxHealth)*255)
        objects.screen.blit(self.image, self.rect)
        objects.screen.blit(self.image, self.rect)
        pygame.draw.rect(objects.screen, (15,15,15), pygame.Rect(150,25,200,20))
        pygame.draw.rect(objects.screen, (255,0,0), pygame.Rect(150,25,self.health/self.maxHealth*200,20))
        if self.counter >= objects.framerate/2: 
            objects.screen.blit(self.shadowImage, self.shadowRect)
    def update(self):
        # Changing directions after reaching targeted location
        #print(self.counter)
        if self.rect.center == self.nextLocation:
            self.nextLocation = (random.randint(0,500),random.randint(0,500))
            self.shadowRect.center = self.nextLocation
            self.counter = 0
            self.moving = False

        if not self.moving: 
            self.counter += 1
            if self.counter == objects.framerate:
                self.moving = True
        else: 
            # Moving
            xDist = self.nextLocation[0] - self.rect.center[0]
            yDist = self.nextLocation[1] - self.rect.center[1]
            totalDist = (xDist**2 + yDist**2)**.5
            if self.speed > totalDist:
                self.rect.center = self.nextLocation
            else:
                xSpeed = xDist / totalDist * self.speed
                ySpeed = yDist / totalDist * self.speed
                self.rect = self.rect.move(xSpeed, ySpeed)
        # Checking for collision with player
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability:
                objects.player.currentHealth = objects.player.currentHealth - self.attackDamage
            while self.rect.colliderect(objects.player.rect): 
                self.rect.center = (random.randint(0,objects.width), random.randint(0, objects.height))
            self.counter = 0
            self.moving = False
        # Dying
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            objects.player.maxHealth = objects.player.maxHealth + 25
            objects.player.maxEnergy = objects.player.maxEnergy + 25
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
            objects.player.currentHealth = objects.player.maxHealth
            objects.abilities[3] = ElectroDash()
            objects.player.chunk = (0,0)
            objects.player.rect.center = (400,400)
            print("REPORT: You have defeated the lightning ghost.")
            print("NEW ABILITY: ELECTRODASH")
            print("Ability Information: The electrodash ability allows you to dash quickly to a spot on the screen, doing damage to everything in your path and not taking damage at all. This ability uses up 25 ghost energy per use. Press 4 to switch to the electrodash ability from another ability.")
            objects.FindQuest("The Lightning Boss").data = True
            for i in objects.chunks[1][1].contents: 
                if i.type == "collisionButton": 
                    objects.chunks[1][1].contents.remove(i)
                return

class PoisonGhostBoss(Enemy):
    def __init__(self):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Poison Boss.png")
        self.rect =  self.image.get_rect()
        self.rect.center = (50,50)
        self.type = "enemy"
        self.maxHealth = 800
        self.health = self.maxHealth
        self.moving = False
        self.attackDamage = 20
        self.counter = 0
        self.pools = [(50,50),(450,50),(50,450),(450,450)]
        self.waitTime = 5
    def render(self): 
        objects.screen.blit(self.image, self.rect)
        pygame.draw.rect(objects.screen, (15,15,15), pygame.Rect(150,25,200,20))
        pygame.draw.rect(objects.screen, (255,0,0), pygame.Rect(150,25,self.health/self.maxHealth*200,20))
    def update(self):
        # if boss is appearing we want him to fire and then wait around (Yuan)
        if self.counter < 6: 
            y = (self.counter/5)
            self.image.set_alpha(y*((self.health/self.maxHealth)*255))

        elif self.counter == 6:
            objects.currentChunk.contents.append(PoisonDrop(self.rect.center, objects.player.rect.center))
            objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
            objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))

        # waiting around count down till moves again (Max)
        elif self.counter < objects.framerate*self.waitTime:
            pass
        # disappearing then reappear somewhere else
        else:
            y = 255-((self.counter-objects.framerate*self.waitTime)/5)*255
            self.image.set_alpha(y)

        if self.counter == objects.framerate*self.waitTime + 5:
            self.counter = 0
            self.rect.center = random.choice(self.pools)
            #print(self.rect.center)
        else:
            self.counter += 1
            
        # Dying
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            objects.player.maxHealth = objects.player.maxHealth + 25
            objects.player.maxEnergy = objects.player.maxEnergy + 25
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
            objects.player.currentHealth = objects.player.maxHealth
            objects.abilities[4] = PoisonField()
            objects.player.chunk = (0,0)
            objects.player.rect.center = (400,400)
            print("REPORT: You have defeated the poison ghost.")
            print("NEW ABILITY: POISON FIELD")
            print("Ability Information: The poison field ability deals damage over time to enemies near you. This ability uses up 25 ghost energy per use. Press 5 to switch to the poison field ability from another ability.")
            objects.FindQuest("The Poison Boss").data = True
            for i in objects.chunks[2][0].contents: 
                if i.type == "collisionButton": 
                    objects.chunks[2][0].contents.remove(i)
                return

class SummoningGhostBoss(Enemy):
    def __init__(self):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Summoning Boss.png")
        self.rect =  self.image.get_rect()
        self.rect.center = (250,250)
        self.type = "enemy"
        self.maxHealth = 1000
        self.health = self.maxHealth
        self.attackDamage = 75
        self.speed = 2
        self.counter = 0
    def render(self): 
        objects.screen.blit(self.image, self.rect)
        pygame.draw.rect(objects.screen, (15,15,15), pygame.Rect(150,25,200,20))
        pygame.draw.rect(objects.screen, (255,0,0), pygame.Rect(150,25,self.health/self.maxHealth*200,20))
    def update(self):
        # Movement
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
            if not objects.player.invulnerability: 
                objects.player.currentHealth -= self.attackDamage
            while self.rect.colliderect(objects.player.rect): 
                self.rect.center = (random.randint(0,objects.width), random.randint(0, objects.height))
        # Spawning
        if self.counter == objects.framerate * 1.5: 
            newGhost = Ghost(self.rect.center)
            newGhost.speed = 4
            objects.currentChunk.contents.append(newGhost)
            self.counter = 0
        else:
            self.counter += 1
        # Dying
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            objects.player.maxHealth = objects.player.maxHealth + 25
            objects.player.maxEnergy = objects.player.maxEnergy + 25
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
            objects.player.currentHealth = objects.player.maxHealth
            objects.abilities[5] = SummonAbility()
            
            objects.player.chunk = (0,0)
            objects.player.rect.center = (400,400)
            print("REPORT: You have defeated the summoning ghost.")
            print("NEW ABILITY: GHOST SUMMONING")
            print("Ability Information: The summoning ability summons a ghost that follows your mouse around the screen. This ability uses up 25 ghost energy per use. Press 6 to switch to the summoning ability from another ability.")
            objects.FindQuest("The Summoning Boss").data = True
            for i in objects.chunks[3][0].contents: 
                if i.type == "collisionButton": 
                    objects.chunks[3][0].contents.remove(i)
                return

class ShieldGhostBoss(Enemy):
    def __init__(self):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Summoning Boss.png")
        self.rect =  self.image.get_rect()
        self.rect.center = (250,50)
        self.type = "enemy"
        self.maxHealth = 1200
        self.health = self.maxHealth
        self.counter = 0
        self.cooldown = objects.framerate*3
        self.direction = (5,0)
        self.attackDamage = 25
    def render(self): 
        objects.screen.blit(self.image, self.rect)
        pygame.draw.rect(objects.screen, (15,15,15), pygame.Rect(150,25,200,20))
        pygame.draw.rect(objects.screen, (255,0,0), pygame.Rect(150,25,self.health/self.maxHealth*200,20))
    def update(self):
        # Movement
        self.rect = self.rect.move(self.direction)
        if not pygame.Rect(0,0,500,500).contains(self.rect): 
            self.direction = (-self.direction[0],0)
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth -= self.attackDamage
            while self.rect.colliderect(objects.player.rect): 
                self.rect.center = (random.randint(50,objects.width-50), 50)
        if self.counter % self.cooldown == 0: 
            objects.currentChunk.contents.append(Shield(self.rect.centerx))
        self.counter += 1

        # Dying
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            objects.player.maxHealth = objects.player.maxHealth + 25
            objects.player.maxEnergy = objects.player.maxEnergy + 25
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
            objects.player.currentHealth = objects.player.maxHealth
            objects.abilities[6] = MagicalShield()
            objects.player.chunk = (0,0)
            objects.player.rect.center = (400,400)
            print("REPORT: You have defeated the shield ghost.")
            print("NEW ABILITY: MAGICAL SHIELD")
            print("Ability Information: The magical shield ability makes you immune to taking damage. This ability uses up 25 ghost energy per use. Press 7 to switch to the poison field ability from another ability.")
            objects.FindQuest("The Shield Boss").data = True
            for i in objects.chunks[0][0].contents: 
                if i.type == "collisionButton": 
                    objects.chunks[0][0].contents.remove(i)
                return



class LaserGhostBoss(Enemy): 
    def __init__(self):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Laser Boss.png")
        self.rect =  self.image.get_rect()
        self.rect.center = (50,50)
        self.type = "enemy"
        self.maxHealth = 1400
        self.health = self.maxHealth
        self.moving = False
        self.attackDamage = 50
        self.counter = 0
        self.targets = [(50,50),(450,50),(50,450),(450,450)]
        self.target = (450,450)
        self.waitTime = 5
        self.direction = None
        self.speed = 25
        self.laserMoveX = 0
        self.laserMoveY = 0 
        self.laserRotation = 0
    def render(self): 
        
        objects.screen.blit(self.image, self.rect)
        pygame.draw.rect(objects.screen, (15,15,15), pygame.Rect(150,25,200,20))
        pygame.draw.rect(objects.screen, (255,0,0), pygame.Rect(150,25,self.health/self.maxHealth*200,20))
    def update(self):
        # if boss is appearing we want him to fire and then wait around 
        '''if self.counter < 6: 
            pass # don't do anything

        elif self.counter == 6:
            pass # shoot laser'''
        if self.counter == objects.framerate: 
            playerPos = objects.player.rect.center
            xGap = playerPos[0] - self.rect.center[0]
            yGap = playerPos[1] - self.rect.center[1] 
            distance = (xGap**2+yGap**2)**(1/2)
            if yGap == 0:
                yGap = .01
            if distance != 0:
                factor = distance/50 # note: the divisor here is the speed of the laser (for future changes)
                self.laserMoveX = xGap / factor
                self.laserMoveY = yGap / factor
                self.laserRotation =  math.degrees(math.atan(xGap / yGap)) + 90 # y/x
            if yGap > 0:
                self.laserRotation += 180
        # waiting around count down till moves again 
        if self.counter < objects.framerate*(self.waitTime-3) and self.counter > objects.framerate:
            
            objects.currentChunk.contents.append(EnemyLaser((self.laserMoveX, self.laserMoveY), self.laserRotation, self.rect.center))



        # disappearing then reappear somewhere else
        elif self.counter == objects.framerate*self.waitTime:
            while self.target == self.rect.center: 
                self.target = random.choice(self.targets)
            location = self.rect.center 
            xGap = self.target[0]-self.rect.centerx
            yGap = self.target[1]-self.rect.centery 
            distance = (xGap**2+yGap**2)**(1/2)
            if distance != 0:
                factor = distance/self.speed
                moveX = xGap / factor
                moveY = yGap / factor
                self.direction = (moveX, moveY)
                self.moving = True 
        else: 
            pass 
        if self.moving: 
            self.rect = self.rect.move(self.direction[0],self.direction[1])
            if self.rect.center == self.target: 
                self.moving = False 
                self.counter = 0
                self.direction = (0,0)
        else: 
            self.counter += 1
        
        #going diagonally 
        if self.rect.left < 0: 
            self.rect.left = 0 
            self.moving = False
            self.counter = 0
            self.direction = (0,0)
        if self.rect.right > 500: 
            self.rect.right = 500 
            self.moving = False
            self.counter = 0
            self.direction = (0,0)
        if self.rect.top < 0: 
            self.rect.top = 0  
            self.moving = False
            self.counter = 0
            self.direction = (0,0)
        if self.rect.bottom > 500: 
            self.rect.bottom = 500 
            self.moving = False 
            self.counter = 0
            self.direction = (0,0)

        # Dying
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            objects.player.maxHealth = objects.player.maxHealth + 25
            objects.player.maxEnergy = objects.player.maxEnergy + 25
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
            objects.player.currentHealth = objects.player.maxHealth
            objects.abilities[7] = FireLaserArrow()
            objects.player.chunk = (0,0)
            objects.player.rect.center = (400,400)
            print("REPORT: You have defeated the laser ghost.")
            print("NEW ABILITY: LASER ARROW")
            print("Ability Information: The laser arrow ability allows you to shoot a large arrow that passes through enemies, dealing high damage. This ability uses up 25 ghost energy per use. Press 8 to switch to the laser arrow ability from another ability.")
            objects.FindQuest("The Laser Boss").data = True
            for i in objects.chunks[0][0].contents: 
                if type(i) == CollisionButton: 
                    objects.chunks[0][0].contents.remove(i)
                return

class WaterGhostBoss: 
    def __init__(self):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Ice Boss.png")
        self.rect =  self.image.get_rect()
        self.rect.center = (250,250)
        self.type = "enemy"
        self.maxHealth = 1600
        self.health = self.maxHealth
        self.moving = False
        self.counter = 0
        self.waitTime = 5
    def render(self): 
        objects.screen.blit(self.image, self.rect)
        pygame.draw.rect(objects.screen, (15,15,15), pygame.Rect(150,25,200,20))
        pygame.draw.rect(objects.screen, (255,0,0), pygame.Rect(150,25,self.health/self.maxHealth*200,20))
    def update(self):
        # if boss is appearing we want him to fire and then wait around (Yuan)
        if self.counter < 6: 
            y = (self.counter/5)
            self.image.set_alpha(y*(self.health/self.maxHealth)*255)

        elif self.counter == 6:
            playerPos = objects.player.rect.center
            xGap = playerPos[0] - self.rect.center[0]
            yGap = playerPos[1] - self.rect.center[1] 
            distance = (xGap**2+yGap**2)**(1/2)
            if yGap == 0:
                yGap = .01
            if distance != 0:
                factor = distance/10 # note: the divisor here is the speed of the wave (for future changes)
                moveX = xGap / factor
                moveY = yGap / factor
                rotationAngle =  math.degrees(math.atan(xGap / yGap)) + 90 # y/x
            if yGap > 0:
                rotationAngle += 180
            objects.currentChunk.contents.append(EnemyWave((moveX, moveY), rotationAngle, self.rect.center))

        # waiting around count down till moves again (Max)
        elif self.counter < objects.framerate*self.waitTime:
            pass
        # disappearing then reappear somewhere else
        else:
            y = 255-((self.counter-objects.framerate*self.waitTime)/5)*255
            self.image.set_alpha(y)

        if self.counter == objects.framerate * self.waitTime + 5:
            self.counter = 0
            self.rect.center = (random.randint(150,350),random.randint(150,350))
            #print(self.rect.center)
        else:
            self.counter += 1
            
        # Dying
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            objects.player.maxHealth = objects.player.maxHealth + 25
            objects.player.maxEnergy = objects.player.maxEnergy + 25
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
            objects.player.currentHealth = objects.player.maxHealth
            objects.abilities[8] = LaunchWave()
            objects.player.chunk = (0,0)
            objects.player.rect.center = (400,400)
            print("REPORT: You have defeated the water ghost.")
            print("NEW ABILITY: WAVE")
            print("Ability Information: The wave ability launches 4 large waves in different directions. These waves deal damage over time to enemies that they collide with, and pull/push non-boss enemies along with them (dealing more damage). This ability uses up 25 ghost energy per use. Press 9 to switch to the wave ability from another ability.")
            objects.FindQuest("The Water Boss").data = True
            for i in objects.chunks[0][0].contents: 
                if i.type == "collisionButton": 
                    objects.chunks[0][0].contents.remove(i)
                return

class FinalBossGhost(Enemy):
    def __init__(self): 
        self.neutralImage = pygame.image.load("RPGGameMVP\Pixel Images\NeutralFB.png")
        self.fireImage = pygame.image.load("RPGGameMVP\Pixel Images\FireFB.png")
        self.iceImage = pygame.image.load("RPGGameMVP\Pixel Images\IceFB.png")
        self.lightningImage = pygame.image.load("RPGGameMVP\Pixel Images\LightningFB.png")
        self.poisonImage = pygame.image.load("RPGGameMVP\Pixel Images\PoisonFB.png")
        self.summoningImage = pygame.image.load("RPGGameMVP\Pixel Images\SummoningFB.png")
        self.shieldImage = pygame.image.load("RPGGameMVP\Pixel Images\ShieldFB.png")
        self.laserImage = pygame.image.load("RPGGameMVP\Pixel Images\LaserFB.png")
        self.waterImage = pygame.image.load("RPGGameMVP\Pixel Images\WaterFB.png")
        self.images = [self.neutralImage, self.fireImage, self.iceImage, self.lightningImage, self.poisonImage,self.summoningImage,self.shieldImage, self.laserImage, self.waterImage]
        self.currentState = 0
        self.rect = pygame.Rect(0,0,100,100)
        self.rect.center = (250,150)
        self.maxHealth = 3000 
        self.health = self.maxHealth 
        self.type = "enemy" 
        self.counter = 0
        self.waitTime = 3 
        self.image = self.neutralImage
        self.direction = (0,0)
        self.moving = False
        self.attackDamage = 1
        self.angle = 0
        self.iceDir = 0
        self.shadowImage = pygame.image.load("RPGGameMVP\Pixel Images\Lightning Boss Shadow.png")
        self.shadowRect = pygame.Rect(0,0,100,100)
        self.nextLocation = (250,150)
        self.lightningCounter = 0
    def render(self): 
        objects.screen.blit(self.image, self.rect)
        pygame.draw.rect(objects.screen, (15,15,15), pygame.Rect(150,50,200,20))
        pygame.draw.rect(objects.screen, (255,0,0), pygame.Rect(150,50,self.health/self.maxHealth*200,20))

        if self.lightningCounter >= objects.framerate/2 and self.currentState == 3: 
            objects.screen.blit(self.shadowImage, self.shadowRect)
    def update(self): 
        self.counter += 1
        if self.counter == objects.framerate * self.waitTime: 
            if self.rect.center == (250,150): 
                self.currentState = random.randint(1,8)
                self.image = self.images[self.currentState] 
                self.counter = 0
            else: 
                self.currentState = 0 
                self.image = self.images[0]
                xDist = 250 - self.rect.center[0]
                yDist = 150 - self.rect.center[1]
                totalDist = (xDist**2 + yDist**2)**.5
                if 25 > totalDist:
                    self.rect.center = (250,150)
                else:
                    xSpeed = xDist / totalDist * 25
                    ySpeed = yDist / totalDist * 25
                    self.direction = (xSpeed, ySpeed)
        if self.currentState == 1: #Fire 
            if self.rect.left < 0: 
                self.angle = random.random() * math.pi - math.pi/2
            if self.rect.right > objects.width: 
                self.angle = random.random() * math.pi + math.pi/2
            if self.rect.top < 0: 
                self.angle = random.random() * math.pi + math.pi
            if self.rect.bottom > objects.height: 
                self.angle = random.random() * math.pi
            # Moving
            self.rect.center = (self.rect.centerx + 4*math.cos(self.angle), self.rect.centery - 4*math.sin(self.angle))

            if self.counter % objects.framerate == 0:
                playerPos = objects.player.rect.center
                xGap = playerPos[0] - self.rect.center[0]
                yGap = playerPos[1] - self.rect.center[1] 
                distance = (xGap**2+yGap**2)**(1/2)
                if yGap == 0:
                    yGap = .01
                if distance != 0:
                    factor = distance/5
                    moveX = xGap / factor
                    moveY = yGap / factor
                    rotation =  math.degrees(math.atan(xGap / yGap)) + 90 # y/x
                if yGap > 0:
                    rotation += 180
                objects.currentChunk.contents.append(EnemyFireball((3*moveX, 3*moveY), rotation, self.rect.center))
        if self.currentState == 2: #Ice 
            
            # Changing directions after bouncing
            if self.rect.left < 0 or self.rect.right > objects.width or self.rect.top < 0 or self.rect.bottom > objects.height:
                playerPos = objects.player.rect.center
                xGap = playerPos[0] - self.rect.centerx
                yGap = playerPos[1] - self.rect.centery
                if yGap == 0:
                    yGap = .01
                self.iceDir = math.atan(yGap / xGap)
                if xGap < 0:
                    self.iceDir += math.pi
            # Moving
            self.rect.center = (self.rect.centerx + 5*math.cos(self.iceDir), self.rect.centery + 5*math.sin(self.iceDir))
            
            # Shooting icicles on a timer
            if self.counter % objects.framerate == 0:
                playerPos = objects.player.rect.center
                xGap = playerPos[0] - self.rect.center[0]
                yGap = playerPos[1] - self.rect.center[1] 
                distance = (xGap**2+yGap**2)**(1/2)
                if yGap == 0:
                    yGap = .01
                if distance != 0:
                    factor = distance/5
                    moveX = xGap / factor * 2
                    moveY = yGap / factor * 2
                    rotation =  math.degrees(math.atan(xGap / yGap)) + 90
                if yGap > 0:
                    rotation += 180
                objects.currentChunk.contents.append(EnemyIcicle((4*moveX, 4*moveY), rotation, self.rect.center))
        if self.currentState == 3: #Lightning 
            if self.rect.center == self.nextLocation:
                self.nextLocation = (random.randint(0,500),random.randint(0,500))
                self.shadowRect.center = self.nextLocation
                self.moving = False
                self.lightningCounter = 0
            self.lightningCounter += 1
            if not self.moving: 
                if self.lightningCounter == objects.framerate:
                    self.moving = True
            else: 
                # Moving
                xDist = self.nextLocation[0] - self.rect.center[0]
                yDist = self.nextLocation[1] - self.rect.center[1]
                totalDist = (xDist**2 + yDist**2)**.5
                if 25 > totalDist:
                    self.rect.center = self.nextLocation
                else:
                    xSpeed = xDist / totalDist * 25
                    ySpeed = yDist / totalDist * 25
                    self.rect = self.rect.move(xSpeed, ySpeed) 
        if self.currentState == 4: #Poison 
            if self.counter == objects.framerate:
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, objects.player.rect.center))
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400)))) 
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
        if self.currentState == 5: #Summoning
            playerX = objects.player.rect.center[0] 
            playerY = objects.player.rect.center[1]
            xGap = playerX - self.rect.center[0] 
            yGap = playerY - self.rect.center[1] 
            distance = (xGap**2+yGap**2)**(1/2)
            if distance != 0:
                factor = distance/2
                moveX = xGap / factor
                moveY = yGap / factor
            self.rect = (self.rect.move((moveX, moveY)))
            if self.rect.colliderect(objects.player.rect): 
                if not objects.player.invulnerability: 
                    objects.player.currentHealth -= self.attackDamage
                while self.rect.colliderect(objects.player.rect): 
                    self.rect.center = (random.randint(0,objects.width), random.randint(0, objects.height))
            # Spawning
            if self.counter % objects.framerate == 0: 
                newGhost = LargeGhost(self.rect.center)
                newGhost.speed = 5
                objects.currentChunk.contents.append(newGhost)
        if self.currentState == 6: #Shield 
            if self.rect.colliderect(objects.player.rect): 
                if not objects.player.invulnerability: 
                    objects.player.currentHealth -= self.attackDamage
            if self.counter % objects.framerate == 0: 
                objects.currentChunk.contents.append(Shield(self.rect.centerx))
        if self.currentState == 7: #Laser 
            if self.counter == objects.framerate: 
                playerPos = objects.player.rect.center
                xGap = playerPos[0] - self.rect.center[0]
                yGap = playerPos[1] - self.rect.center[1] 
                distance = (xGap**2+yGap**2)**(1/2)
                if yGap == 0:
                    yGap = .01
                if distance != 0:
                    factor = distance/50 # note: the divisor here is the speed of the laser (for future changes)
                    self.laserMoveX = xGap / factor
                    self.laserMoveY = yGap / factor
                    self.laserRotation =  math.degrees(math.atan(xGap / yGap)) + 90 # y/x
                if yGap > 0:
                    self.laserRotation += 180
            # waiting around count down till moves again 
            if self.counter < objects.framerate*(self.waitTime-1) and self.counter > objects.framerate:
                playerPos = objects.player.rect.center
                xGap = playerPos[0] - self.rect.center[0]
                yGap = playerPos[1] - self.rect.center[1] 
                distance = (xGap**2+yGap**2)**(1/2)
                if yGap == 0:
                    yGap = .01
                if distance != 0:
                    factor = distance/15 # note: the divisor here is the speed of the laser (for future changes)
                    self.laserMoveX = xGap / factor
                    self.laserMoveY = yGap / factor
                    self.laserRotation =  math.degrees(math.atan(xGap / yGap)) + 90 # y/x
                if yGap > 0:
                    self.laserRotation += 180
                objects.currentChunk.contents.append(EnemyLaser((self.laserMoveX, self.laserMoveY), self.laserRotation, self.rect.center))
        if self.currentState == 8: #Water 
            if self.counter == objects.framerate:
                playerPos = objects.player.rect.center
                xGap = playerPos[0] - self.rect.center[0]
                yGap = playerPos[1] - self.rect.center[1] 
                distance = (xGap**2+yGap**2)**(1/2)
                if yGap == 0:
                    yGap = .01
                if distance != 0:
                    factor = distance/10 # note: the divisor here is the speed of the wave (for future changes)
                    moveX = xGap / factor
                    moveY = yGap / factor
                    rotationAngle =  math.degrees(math.atan(xGap / yGap)) + 90 # y/x
                if yGap > 0:
                    rotationAngle += 180
                objects.currentChunk.contents.append(EnemyWave((3*moveX, 3*moveY), rotationAngle, self.rect.center))

        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth = objects.player.currentHealth - self.attackDamage
        
        if self.counter > objects.framerate * self.waitTime: 
            self.rect = self.rect.move(self.direction)
            if self.rect.contains(pygame.Rect(210,110,80,80)): 
                self.rect.center = (250,150)
                self.currentState = random.randint(1,8)
                self.image = self.images[self.currentState] 
                self.counter = 0
                self.direction = (0,0)
            

        # Dying
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
            objects.player.currentHealth = objects.player.maxHealth
            objects.player.chunk = (0,0)
            objects.player.rect.center = (400,400)
            print("REPORT: You have defeated the dark ghost.")
            print("GAME COMPLETE!")
            for i in objects.chunks[0][0].contents: 
                if type(i) == CollisionButton: 
                    objects.chunks[0][0].contents.remove(i)
                return

class EnemyWave:
    def __init__(self,direction,rotationAngle,location):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Wave.png")
        if rotationAngle > 360: 
            rotationAngle -= 360
        self.image = pygame.transform.scale(self.image, (100,200))
        self.image = pygame.transform.rotate(self.image, rotationAngle)
    
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.direction = direction
        self.attackDamage = 1
        self.type = "wave"
    def render(self):
        #pygame.draw.rect(objects.screen, "#000000", self.rect) 
        objects.screen.blit(self.image, self.rect)
    def update(self):
        self.rect = self.rect.move(self.direction)
        if not self.rect.colliderect(pygame.Rect(0,0,500,500)):
            objects.currentChunk.contents.remove(self)
        if self.rect.colliderect(objects.player.rect): 
            objects.player.knocked = True 
            objects.player.rect = objects.player.rect.move(self.direction[0],self.direction[1])
            objects.player.currentHealth -= self.attackDamage

class EnemyLaser: 
    def __init__(self,direction,rotationAngle,spawnPos):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Fireball.png")
        self.image = pygame.transform.rotate(self.image, rotationAngle)
        # self.image = pygame.transform.scale(self.image, (20,10))
        self.rect = self.image.get_rect()
        self.rect.center = spawnPos
        self.direction = direction
        self.attackDamage = 5
        self.type = "enemyProjectile"
    def render(self):
        # pygame.draw.rect(objects.screen, "#000000", self.rect) 
        objects.screen.blit(self.image, self.rect)
    def update(self):
        self.rect = self.rect.move(self.direction)
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth = objects.player.currentHealth - self.attackDamage 
            objects.currentChunk.contents.remove(self)

        elif not objects.screen.get_rect().colliderect(self.rect):
            objects.currentChunk.contents.remove(self)

class Shield: 
    def __init__(self,xPos): 
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Silver Coin.png")
        self.image = pygame.transform.scale(self.image, (100,25))
        self.rect = self.image.get_rect() 
        self.rect.top = 100
        self.type = "enemy"
        self.direction = (5,1)
        self.damage = 10
        self.rect.centerx = xPos
        self.maxHealth = 50
        self.health = self.maxHealth
    def render(self): 
        self.image.set_alpha((self.health/self.maxHealth)*255)
        objects.screen.blit(self.image, self.rect)
        
        pygame.draw.rect(objects.screen, (0,0,0), pygame.Rect(self.rect.left,self.rect.top-self.rect[3]*.1,self.rect[2],self.rect[3]*.1))
        pygame.draw.rect(objects.screen, (255,0,0), pygame.Rect(self.rect.left,self.rect.top-self.rect[3]*.1,self.rect[2]*(self.health/self.maxHealth),self.rect[3]*.1))
    def update(self): 
        self.rect = self.rect.move(self.direction)
        if not pygame.Rect(0,0,500,500).contains(self.rect): 
            self.direction = (self.direction[0]*(-1),1)
        if self.rect.bottom > objects.height: 
            objects.currentChunk.contents.remove(self) 
        elif self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth -= self.damage 
            objects.currentChunk.contents.remove(self)
        elif self.health <= 0: 
            objects.currentChunk.contents.remove(self)
    
class PoisonDrop: 
    def __init__(self, start, target): 
        self.start = start
        self.target = target
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Poison Drop.png")
        self.rect = self.image.get_rect()
        self.rect.center = self.start
        self.speed = 15
        self.direction = 0
        xGap = self.target[0] - self.start[0]
        yGap = self.target[1] - self.start[1]
        self.direction = math.degrees(math.atan2(yGap,xGap))
        self.image = pygame.transform.rotate(self.image, self.direction + 90)
        self.type = "enemyProjectile"
    def render(self):
        
        objects.screen.blit(self.image, self.rect)
        
    def update(self):
        self.rect = self.rect.move(self.speed*math.cos(math.radians(self.direction)), self.speed*math.sin(math.radians(self.direction)))
        if self.rect.colliderect(objects.player.rect) or self.rect.collidepoint(self.target): 
            objects.currentChunk.contents.append(PoisonPool(self.rect.center))
            objects.currentChunk.contents.remove(self)
        if not objects.screen.get_rect().contains(self.rect):
            objects.currentChunk.contents.remove(self)

class PoisonPool:
    def __init__(self,pos):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Poison Puddle.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.timer = 0
        self.damage = 1
        self.type = "enemy projectile"
    def update(self):
        # If collide with player do 1 damage
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth -= self.damage
        # If timer is 5s delete self
        if self.timer == objects.framerate*10: 
            objects.currentChunk.contents.remove(self)
        # Increase timer
        self.timer += 1
    def render(self):
        objects.screen.blit(self.image, self.rect)

class EnemyIcicle:
    def __init__(self,direction,rotationAngle,spawnPos):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Icicle.png")
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
            if not objects.player.invulnerability: 
                objects.player.currentHealth = objects.player.currentHealth - self.attackDamage 
            objects.currentChunk.contents.remove(self)


        if not objects.screen.get_rect().contains(self.rect):
            objects.currentChunk.contents.remove(self)


class EnemyFireball:
    def __init__(self,direction,rotationAngle,spawnPos):
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\Fireball.png")
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
            if not objects.player.invulnerability: 
                objects.player.currentHealth = objects.player.currentHealth - self.attackDamage 
            objects.currentChunk.contents.remove(self)

        elif not objects.screen.get_rect().contains(self.rect):
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

class MovementBarrier: 
    def __init__(self, image, location): 
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = "obstacle"
    def render(self):
        objects.screen.blit(self.image, self.rect)
    def update(self):
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
        if pygame.mouse.get_pressed(3)[0]:
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
        self.type = "NPC" #TODO: wait till up before being pressed down
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
            objects.player.chunk = (objects.mapWidth, self.subchunk)
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

class QuestionCube: 
    boosts = [["objects.player.currentHealth += 25", 25], ["objects.resourceAmounts['ghostEnergy'] += 25", 50], ["objects.moveSpeed = 10", 60],["objects.resourceAmountsr['purple']", 65],["objects.resourceAmounts['red']", 67],["objects.resourceAmounts['blue']", 69],["objects.resourceAmounts['gold']", 70],["print('10s infinite health')", 80], ["print('10s infinite energy')", 90], ["print('key')"]]

    def __init__(self, location): 
        self.image = pygame.image.load("RPGGameMVP\Pixel Images\QuestionCube.png")
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = "qcube"
    def render(self): 
        objects.screen.blit(self.image, self.rect)
    def update(self): 
        if objects.player.rect.colliderect(self.rect): 
            objects.currentChunk.contents.remove(self)
            objects.gamestate = 3
            objects.currentProblem = random.choice(objects.problems)
    def randBoost(): 
        choice = random.randint(1,100)
        for boost in QuestionCube.boosts:
            if choice <= boost[1]:
                exec(boost[0])
                return
