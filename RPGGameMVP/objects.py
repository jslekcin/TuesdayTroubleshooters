import pygame
import os

# all of these values are read only that we want to access everywhere
# this is a box that we never touch but only look at its contents
# to *IMPORTANT read these values you can => from objects import *

size = width, height = 500,500
moveSpeed = 5
mapWidth, mapHeight = 7, 7
debugging = True
dayLength = 5
framerate = 30
difficulty = 0

# Spawn Instructions

# THESE ARE KNOWN AS CONSTANTS
# written with all caps (usually)
# in different languages you might have seen these variables with a "final" keyword

# here are the variables that we can change with functions not set. STATIC variables
# we are puting different things inside the box but its the same box
# you can from objects import * but better practice to objects.variable
pygame.font.init()
myFont = pygame.font.SysFont("Comic Sans", 24)
announcementFont = pygame.font.SysFont("Comic Sans", 72)
mathFont = pygame.font.SysFont("Comic Sans", 50)

gamestate = 0
chunks = []
mathQuestions = None
currentProblem = ['a','b','c','d']
"""
[
    [(0, 0) Overworld, (0, 1) Overworld, (0, 2) Overworld, (0, 3) Overworld, (0, 4) Overworld, (0, 5) Overworld, (0, 6) Overworld],
    [(1, 0) Overworld, (1, 1) Overworld, (1, 2) Overworld, (1, 3) Overworld, (1, 4) Overworld, (1, 5) Overworld, (1, 6) Overworld],
    [(2, 0) Overworld, (2, 1) Overworld, (2, 2) Overworld, (2, 3) Overworld, (2, 4) Overworld, (2, 5) Overworld, (2, 6) Overworld], 
    [(3, 0) Overworld, (3, 1) Overworld, (3, 2) Overworld, (3, 3) Overworld, (3, 4) Overworld, (3, 5) Overworld, (3, 6) Overworld], 
    [(4, 0) Overworld, (4, 1) Overworld, (4, 2) Overworld, (4, 3) Overworld, (4, 4) Overworld, (4, 5) Overworld, (4, 6) Overworld], 
    [(5, 0) Overworld, (5, 1) Overworld, (5, 2) Overworld, (5, 3) Overworld, (5, 4) Overworld, (5, 5) Overworld, (5, 6) Overworld], 
    [(6, 0) Overworld, (6, 1) Overworld, (6, 2) Overworld, (6, 3) Overworld, (6, 4) Overworld, (6, 5) Overworld, (6, 6) Overworld], 
    [(7, 0) Shop, (7, 0) fire dungeon, (7, 0) ice dungeon, (7, 0) lightning dungeon]
]
"""


# we have a 7, 7 map meaning chunks are two dimensional list and 7 by 7
# Every index in the 2D list houses a "Chunk" object
# Every thing displayed on a chunk is housed in the chunks "contents" variable, that is including portals
# Additionally we store our boss rooms in our chunks list by creating another "8th" list as the 7th index

resourceAmounts = {
    "coins": 1000000, 
    "ghostEnergy": 0
    }
potions = {
    "purple": 0, 
    "red": 0, 
    "blue": 0, 
    "gold": 0
}
potionEffects = {
    "purple":["objects.player.currentHealth += objects.player.maxHealth * .2","objects.resourceAmounts['ghostEnergy'] += objects.player.maxHealth * .2"],
    "red":["objects.player.currentHealth = objects.player.maxHealth"],
    "blue":["objects.resourceAmounts['ghostEnergy'] = objects.player.maxEnergy"],
    "gold":["objects.player.currentHealth = objects.player.maxHealth","objects.resourceAmounts['ghostEnergy'] = objects.player.maxEnergy"],
}
screen = pygame.display.set_mode(size)
daytime = True
freeze = False
abilities = [None, None, None, None, None, None, None, None, None, None]
abilityPanel = []
shopShowing = False
quests = []
#"Find the Fire Key! ","Defeat the Fire Ghost! ","Find the Ice Key! ","Defeat the Ice Ghost! ","Find the Lightning Key! ","Defeat the Lightning Ghost! ","Find the Poison Key! ","Defeat the Poison Ghost! ","Find the Summoning Key! ","Defeat the Summoner Ghost! ","Find the Shield Key! ","Defeat the Shield Ghost! ","Find the Laser Key! ","Defeat the Laser Ghost! ","Find the Water Key! ","Defeat the Water Ghost! ","Find the Boss Key! ","Defeat the Dark Ghost! "]
currentQuest = 0
achievements = [
    "Buy 3 gold potions!",
    "Defeat 100 enemies!",
    "Travel the entire map! ",
    "Defeat 5 fire ghosts!",
    "Survive for 10 days!",
    "Take 1000 damage (careful with your health)!",
    "Have infinite health for 3 minutes overall!",
    "Defeat 5 enemies in one electrodash!",
    "Use the laser arrows at least 50 times! ", 
    "Upgrade one aspect of the player to the highest level! ", 
    "Buy the highest level upgrade of every ability! ", 
    "Pick up 100 Question Cubes!", 
    "PLEASE ENTER MORE HERE"
    ]
    
def FindQuest(name):
    for quest in quests:
        if quest.name == name:
            return quest
            break

# all of the following values are read and write.
# we are actually changing out the box sometimes
# for these we want to import objects and then when writing and reading to use =>
# objects.variable (READ)
# objects.variable = (WRITE)

player = None
currentChunk = None

# reset resources
# respawn all entities
# 
def Reset():
    player.currentHealth = player.maxHealth
    resourceAmounts["ghost energy"] = 0
    player.chunk = (0, 0)
    currentChunk = chunks[player.chunk[1]][player.chunk[0]]
    player.rect.topleft = (0,0)
    for chunkList in chunks:
        for chunk in chunkList:
            for thing in chunk.contents:
                if thing.type == "enemy": 
                    thing.health = thing.maxHealth
                    #print(thing.maxHealth)

def LoadMath():
    file_path = '24sets.txt'
    current_path = os.path.dirname(__file__)
    file_loc = os.path.join(current_path, file_path)
    filetxt = open(file_loc, "r")
    data = filetxt.read()
    filetxt.close()

    data = data.split("\n")
    for i in range(len(data)):
        data[i] = data[i].split()

    global mathQuestions
    
    mathQuestions = data
    global problems
    if difficulty <= 2: 
        
        problems = mathQuestions[(difficulty*400):((difficulty+1)*400)]
    else: 
        problems = mathQuestions[1200:]


class Point: 
    def __init__(self, position): 
        self.color = (255,0,0) 
        self.position = position
        self.type = "marker"
    def render(self): 
        pygame.draw.circle(screen, self.color, self.position, 5)
    def update(self): 
        pass