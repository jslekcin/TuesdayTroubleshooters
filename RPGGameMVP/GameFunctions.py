import pygame
import Classes
import objects
import random
import MapLoader
import quests
import time

pygame.init()

buttons = {
    "game": [], 
    "menu": [Classes.Button(pygame.transform.scale(pygame.image.load("Pixel Images/StartButton.png"), (500,100)),(250,450), ['objects.gamestate = 1','objects.Reset()']), Classes.Button(pygame.image.load("Pixel Images/AboutUsButton.png"),(250,350), ['webbrowser.open("https://docs.google.com/presentation/d/1fCRW8VGcp_BtFYz1E_SCKFJo4uPcnhw9mEK5d6gdftc/edit?usp=sharing")'])],
    "shop": [
    Classes.Button(pygame.transform.scale(pygame.image.load("Pixel Images/Purple Potion.png"),(50,50)),(175,175), ['if objects.resourceAmounts["coins"] >= 25: objects.potions["purple"] += 1;objects.resourceAmounts["coins"] -= 25;print("Bought Purple Potion")', "time.sleep(0.5)"]),
    Classes.Button(pygame.transform.scale(pygame.image.load("Pixel Images/Red Potion.png"), (50,50)),(225,175), ['if objects.resourceAmounts["coins"] >= 50: objects.potions["red"] += 1;objects.resourceAmounts["coins"] -= 50;print("Bought Red Potion")', "time.sleep(0.5)"]),
    Classes.Button(pygame.transform.scale(pygame.image.load("Pixel Images/Blue Potion.png"),(50,50)),(275,175), ['if objects.resourceAmounts["coins"] >= 50: objects.potions["blue"] += 1;objects.resourceAmounts["coins"] -= 50;print("Bought Blue Potion")', "time.sleep(0.5)"]),
    Classes.Button(pygame.transform.scale(pygame.image.load("Pixel Images/Gold Potion.png"),(50,50)),(325,175), ['if objects.resourceAmounts["coins"] >= 100: objects.potions["gold"] += 1;objects.resourceAmounts["coins"] -= 100;print("Bought Gold Potion")', "time.sleep(0.5)","objects.FindQuest('Potion Critic').data += 1"]),
    Classes.Button(pygame.Surface((200,50)),(250,325), ['objects.shopShowing = False'])]
}
objects.player = Classes.Player()

def DebugCode():
    if pygame.key.get_pressed()[pygame.K_SPACE]: 
        objects.player.currentHealth -= 10
    #if pygame.key.get_pressed()[pygame.K_p]:
       # print(pygame.mouse.get_pos())

def NightEvent():
    # Spawning normal ghosts in empty chunks
    for y in range(objects.mapHeight): 
        for x in range(objects.mapWidth): 
            chunk = objects.chunks[x][y]
            enemies = False
            for thing in chunk.contents: 
                if thing.type == "enemy": 
                    enemies = True
            if enemies is False: 
                if chunk != objects.chunks[0][0] and chunk != objects.currentChunk: 
                    for i in range(random.randint(1,5)):
                        chunk.contents.append(Classes.Ghost((random.randint(0,500),random.randint(0,500))))
    print("REPORT: Ghosts have appeared in uninhabited areas.")
    # Spawning a large ghost in uninhabited chunks
    chunk = objects.chunks[random.randint(0,objects.mapWidth-1)][random.randint(0,objects.mapHeight-1)]
    while chunk == objects.chunks[0][0] or chunk == objects.currentChunk:
        chunk = objects.chunks[random.randint(0,objects.mapWidth-1)][random.randint(0,objects.mapHeight-1)]
    print(f"REPORT: A powerful ghost has appeared in chunk {chunk.location}.")
    chunk.contents.append(Classes.LargeGhost((250,250)))

dayNightCounter = 0
def GameplayUpdate():
    for quest in objects.quests:
        quest.update()

    # INPUT (Getting stuff that player is doing ex: pressing keys moving keyboard)
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
    if keys[pygame.K_i]: # Game Information
        print("INFORMATION: ")
        print("Current Quest: "+objects.quests[objects.currentQuest]) 
        print("Ghost Energy: "+str(objects.resourceAmounts["ghost energy"]))
        print("Coins: "+str(objects.resourceAmounts["coins"]))
        print("Potions: "+str(objects.potions)) 
        print("Health: "+str(objects.player.currentHealth))
        print("")
    # Pressing Keys
    for event in pygame.event.get(pygame.KEYDOWN):
        if event.key == pygame.K_1 and objects.abilities[0] != None:
            objects.player.currentAbility = 0
        if event.key == pygame.K_2 and objects.abilities[1] != None:  
            objects.player.currentAbility = 1
        if event.key == pygame.K_3 and objects.abilities[2] != None:  
            objects.player.currentAbility = 2
        if event.key == pygame.K_4 and objects.abilities[3] != None:  
            objects.player.currentAbility = 3
        if event.key == pygame.K_5 and objects.abilities[4] != None:  
            objects.player.currentAbility = 4
        if event.key == pygame.K_6 and objects.abilities[5] != None:  
            objects.player.currentAbility = 5
        if event.key == pygame.K_7 and objects.abilities[6] != None:  
            objects.player.currentAbility = 6
        if event.key == pygame.K_8 and objects.abilities[7] != None:  
            objects.player.currentAbility = 7
        if event.key == pygame.K_9 and objects.abilities[8] != None:  
            objects.player.currentAbility = 8
        if event.key == pygame.K_0 and objects.abilities[9] != None:  
            objects.player.currentAbility = 9
    # Using Scrollwheel
    for event in pygame.event.get(pygame.MOUSEWHEEL): 
        if event.y > 0:
            objects.player.currentAbility += 1
            while objects.player.currentAbility > 9 or objects.abilities[objects.player.currentAbility] == None:
                objects.player.currentAbility += 1
                if objects.player.currentAbility > 9: 
                    objects.player.currentAbility = 0
        if event.y < 0: 
            objects.player.currentAbility -= 1
            while objects.player.currentAbility < 0 or objects.abilities[objects.player.currentAbility] == None:
                objects.player.currentAbility -= 1
                if objects.player.currentAbility < 0: 
                    objects.player.currentAbility = 9

    # UPDATE (Doing checks in the background ex: checking if something is colliding)
    global dayNightCounter
    dayNightCounter += 1
    if dayNightCounter / objects.framerate >= objects.dayLength: 
        objects.daytime = not objects.daytime
        if objects.daytime:
            print("REPORT: It is now daytime.")
        else:
            print("REPORT: It is now nighttime")
            NightEvent()
        dayNightCounter = 0
    
    if objects.player.rect.center[0] < 0: # Moving off left of screen
        if objects.player.chunk[0] == -1 or objects.player.chunk[0] == 0: # If in subchunk or leftmost chunk and boss fights.
            objects.player.rect.centerx = 0 # Move flush to wall
        else:
            objects.player.chunk = (objects.player.chunk[0]-1, objects.player.chunk[1])
            print(f'REPORT: Current chunk is {objects.player.chunk}')
            objects.player.rect.centerx = objects.width
            #objects.player.move(objects.width, 0)
    
    if objects.player.rect.center[0] > objects.width: # Moving off right of screen
        if objects.player.chunk[0] == -1  or objects.player.chunk[0] == objects.mapWidth-1:
            objects.player.rect.centerx = objects.width 
        else:
            objects.player.chunk = (objects.player.chunk[0]+1, objects.player.chunk[1])
            print(f'REPORT: Current chunk is {objects.player.chunk}')
            objects.player.rect.centerx = 0
    
    if objects.player.rect.center[1] < 0: # Moving off top of screen
        if objects.player.chunk[0] == -1  or objects.player.chunk[1] == 0:
            objects.player.rect.centery = 0
        else:
            objects.player.chunk = (objects.player.chunk[0],objects.player.chunk[1]-1)
            print(f'REPORT: Current chunk is {objects.player.chunk}')
            objects.player.rect.centery = objects.height
         
    if objects.player.rect.center[1] > objects.width: # Moving off bottom of screen
        if objects.player.chunk[0] == -1  or objects.player.chunk[1] == objects.mapHeight-1:
            objects.player.rect.centery = objects.height
        else:  
            objects.player.chunk = (objects.player.chunk[0],objects.player.chunk[1]+1)
            print(f'REPORT: Current chunk is {objects.player.chunk}')
            objects.player.rect.centery = 0
    
    objects.currentChunk = objects.chunks[objects.player.chunk[0]][objects.player.chunk[1]]
    if objects.freeze == True: 
        for thing in objects.currentChunk.contents: 
            if thing.type != 'enemy': 
                thing.update()
        Classes.Freeze.freezeCD()
    else: 
        objects.currentChunk.update()
    objects.player.update()
    if objects.player.currentHealth <= 0: 
        objects.gamestate = 2
    if objects.resourceAmounts["ghostEnergy"] >= objects.player.maxEnergy: 
        objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
        
freezeOverlay = pygame.Surface(objects.size)
freezeOverlay.fill((255,255,255))
freezeOverlay.set_alpha(100)


def ShopUpdate():
    for button in buttons["shop"]: 
        button.update()

shopImage = pygame.image.load("Pixel Images/ShopInv.png")
def ShopRender():
    objects.screen.blit(shopImage, (150, 150))
    #for button in buttons["shop"]: 
    #    button.render()

'''
shopImage = pygame.Surface((200,200))
def generateShop(): # P.S. I know this is not efficient
    shopImage.fill((200,200,200))
    #Potion = pygame.image.load("Pixel Images/Purple Potion.png")
    #PotionRect = Potion.get_rect()
    #PotionRect.center = (50,50)
    RedPotion = pygame.image.load("Pixel Images/Red Potion.png")
    RedPotionRect = RedPotion.get_rect()
    RedPotionRect.center = (150,50)
    BluePotion = pygame.image.load("Pixel Images/Blue Potion.png")
    BluePotionRect = BluePotion.get_rect()
    BluePotionRect.center = (50,150)
    GoldPotion = pygame.image.load("Pixel Images/Gold Potion.png")
    GoldPotionRect = GoldPotion.get_rect()
    GoldPotionRect.center = (150,150)
    #shopImage.blit(Potion, PotionRect)
    shopImage.blit(RedPotion, RedPotionRect)
    shopImage.blit(BluePotion, BluePotionRect)
    shopImage.blit(GoldPotion, GoldPotionRect)
generateShop()
'''

objects.abilityPanel = [pygame.image.load("Pixel Images/Arrow Icon.png"),
                pygame.image.load("Pixel Images/Fireball Icon.png"),
                pygame.image.load("Pixel Images/Freeze Icon.png"),
                pygame.image.load("Pixel Images/Speed Icon.png"),
                pygame.image.load("Pixel Images/Poison Icon.png"),
                pygame.image.load("Pixel Images/Summoning Icon.png"),
                pygame.image.load("Pixel Images/Shield Icon.png"),
                pygame.image.load("Pixel Images/Laser Icon.png"),
                pygame.image.load("Pixel Images/Wave Icon.png"),
                pygame.image.load("Pixel Images/Potion Icon.png")]

def GameplayRender(): 
    # RENDER (Putting stuff on the screen)
    objects.currentChunk.render()
    if objects.freeze == True: 
        global freezeOverlay
        objects.screen.blit(freezeOverlay, (0,0))
    objects.player.render()
    
    # UI Rendering
    objects.screen.blit(objects.myFont.render("Coins: "+ str(objects.resourceAmounts["coins"]), True, (0,0,0)), (0,0))
    # Draw healthbar
    pygame.draw.rect(objects.screen, (15,15,15), pygame.Rect(300,0,200,20))
    pygame.draw.rect(objects.screen, (0,255,0), pygame.Rect(300,0,objects.player.currentHealth/objects.player.maxHealth*200,20))
    objects.screen.blit(objects.myFont.render(f"Health: {objects.player.currentHealth} / {objects.player.maxHealth}", True, (0,0,0)),(100,0))
    # Draw energybar
    pygame.draw.rect(objects.screen, (15,15,15), pygame.Rect(300,20,200,20))
    pygame.draw.rect(objects.screen, (0,0,255), pygame.Rect(300,20,objects.resourceAmounts["ghostEnergy"]/objects.player.maxEnergy*200,20))
    objects.screen.blit(objects.myFont.render(f"Ghost Energy: {objects.resourceAmounts['ghostEnergy']} / {objects.player.maxEnergy}", True, (0,0,0)),(100,25))
    # Draw equipped
    for i in range(len(objects.abilityPanel)):
        if i == objects.player.currentAbility:
            objects.abilityPanel[i].set_alpha(255)
        elif objects.abilities[i] != None:
            objects.abilityPanel[i].set_alpha(100)
        else:
            objects.abilityPanel[i].set_alpha(25)
        objects.screen.blit(objects.abilityPanel[i], (50 * i, 450))

def MenuRender(): 
    objects.screen.fill((255,255,255))
    titleScreen = pygame.image.load("Pixel Images/StartScreen.png")
    
    objects.screen.blit(titleScreen, (0, 0))
    for button in buttons["menu"]: 
        button.render()
    pygame.display.flip()

def MenuUpdate():

    for button in buttons["menu"]: 
        button.update()

def GameOverUpdate(): 
    pygame.event.pump()
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_c]: 
        #print("C recieved")
        objects.gamestate = 0

def GameOverRender(): 
    objects.screen.fill((0,0,0))
    objects.screen.blit(objects.announcementFont.render("Game Over", True, (255,0,0)), (100,50))
    objects.screen.blit(objects.myFont.render("Press C to continue to the main menu.", True, (255, 0, 0)), (100, 300))

# Create list of buttons
if objects.difficulty <= 2: 
    problems = objects.mathQuestions[(objects.difficulty*400):((objects.difficulty+1)*400)]
else: 
    problems = objects.mathQuestions
a = [pygame.Rect(20, 110,100,100),"1",True]
b = [pygame.Rect(140,110,100,100),"2",True]
c = [pygame.Rect(260,110,100,100),"3",True]
d = [pygame.Rect(380,110,100,100),"4",True]
plus = [pygame.Rect(20,250,100,100),"+"]
minus = [pygame.Rect(140,250,100,100),"-"]
times = [pygame.Rect(260,250,100,100),"*"]
divide = [pygame.Rect(20,370,100,100),"/"]
startparen = [pygame.Rect(140,370,100,100),"("]
endparen = [pygame.Rect(260,370,100,100),")"]
backspace = pygame.Rect(380,250,100,100)
enter = pygame.Rect(380,370,100,100)

numbers = [a,b,c,d]
operations = [plus,minus,times,divide] 
parentheses = [startparen,endparen]
answerString = ""
values = ["1","2","3","4","5","6","7","8","9","0"]
def MathUpdate(): 
    a[1] = objects.currentProblem[0]
    b[1] = objects.currentProblem[1]
    c[1] = objects.currentProblem[2]
    d[1] = objects.currentProblem[3]
    global answerString
    for event in pygame.event.get(): 
        if event.type == pygame.MOUSEBUTTONDOWN: 
            mousePos = pygame.mouse.get_pos()
            if answerString != "" and answerString[-1] in values: 
                pass
            else: 
                for i in numbers: 
                    if i[2] and i[0].collidepoint(mousePos): 
                        answerString += i[1]
                        i[2] = False
            for i in operations: 
                if answerString != "" and (answerString[-1] in values or answerString[-1] == endparen[1]) and i[0].collidepoint(mousePos): 
                    answerString += i[1]
            for i in parentheses: 
                if i[0].collidepoint(mousePos): 
                    answerString += i[1]
            if backspace.collidepoint(mousePos) and len(answerString) > 0:
                answerString = ""
                for i in numbers: 
                    i[2] = True
            if answerString != "" and enter.collidepoint(mousePos):
                if eval(answerString) == 24 or eval(answerString) == 23.99999999999999:
                    Classes.QuestionCube.randBoost()
                objects.gamestate = 1 # no boost
                answerString = ""
                
            #    if eval(answerString) in results: 
            #        gamestate = 3
            #    else: 
            #        gamestate = 4

panelImage = pygame.image.load("Pixel Images/MathPanel.png")
panelRect = panelImage.get_rect()
def MathRender():
    # Display our background
    objects.screen.fill((0,255,0))
    objects.screen.blit(panelImage, panelRect)
    # Display the numbers
    submissionText = objects.mathFont.render(answerString, False, (0,0,0))
    objects.screen.blit(submissionText, (10,25))
    aText = objects.mathFont.render(a[1], False, (0,0,0))
    objects.screen.blit(aText, (45, 135))
    bText = objects.mathFont.render(b[1], False, (0,0,0))
    objects.screen.blit(bText, (165, 135))
    cText = objects.mathFont.render(c[1], False, (0,0,0))
    objects.screen.blit(cText, (285, 135))
    dText = objects.mathFont.render(d[1], False, (0,0,0))
    objects.screen.blit(dText, (405, 135))