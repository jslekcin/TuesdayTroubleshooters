import Classes
import objects

# 2 Steps
# 1) Append the quests
# 2) Add the active code to update data to the quest item

objects.quests.append(
    Classes.Quest("Defeat the Fire Boss!","self.data == True","The Fire Boss")
)
objects.quests.append(
    Classes.Quest("Defeat the Ice Boss!","self.data == True","The Ice Boss")
)
objects.quests.append(
    Classes.Quest("Defeat the Lightning Boss!","self.data == True","The Lightning Boss")
)
objects.quests.append(
    Classes.Quest("Defeat the Poison Boss!","self.data == True","The Poison Boss")
)
objects.quests.append(
    Classes.Quest("Defeat the Summoning Boss!","self.data == True","The Summoning Boss")
)
objects.quests.append(
    Classes.Quest("Defeat the Shield Boss!","self.data == True","The Shield Boss")
)
objects.quests.append(
    Classes.Quest("Defeat the Laser Boss!","self.data == True","The Laser Boss")
)
objects.quests.append(
    Classes.Quest("Defeat the Water Boss!","self.data == True","The Water Boss")
)
objects.quests.append(
    Classes.Quest("Buy 3 Gold Potions!","self.data == 3","Potion Critic")
) # Whenever we buy a potion: self.data += 1