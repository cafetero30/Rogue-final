#Imports de modules
import theGame
import random

def heal(creature):
    """Heal the creature"""
    creature.hp += 3
    return True

def renforcement1(creature):
    creature.strength+=1
    return True

def renforcement2(creature):
    creature.strength+=2
    return True

def renforcement3(creature):
    creature.strength+=3
    return True

def protect(creature):
    "protect the creature"
    creature.protection+=4
    return True

def teleport(creature, unique):
    """Teleport the creature"""
    r = theGame.theGame()._floor.randRoom()
    c = r.randEmptyCoord(theGame.theGame()._floor)
    theGame.theGame()._floor.rm(theGame.theGame()._floor.pos(creature))
    theGame.theGame()._floor.put(c, creature)
    return unique

def throw(power, loss):
    """Throw an object"""
    pass

def amulette(hero):
    """Le heros peut porter une amulette parmi un gain d'hp ou une augmentation de la force"""
    nb_choix = [1, 2]
    points = [3, 4, 5, 6]
    a = random.choice(points)
    i = random.choice(nb_choix)

    """bonus de gain d’hp"""
    if i == 1:
        hero.hp += a
        return True
    
    """augmentation de la force"""
    if i == 2:
        hero.strength += a
        return True
    
def restaureFaim(hero, amount):  #ajout de la fonction de restauration de la faim
    """Restores hero's hunger"""
    if hero.hunger + amount <= hero.hungermax:
        hero.hunger = hero.hunger + amount
    else:
        hero.hunger = hero.hungermax
    return True
