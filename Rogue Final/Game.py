#Imports de classe
from Equipment import Equipment
from Arme import Arme
from Creature import Creature
from Coord import Coord
from Hero import Hero
from Map import Map
from Stairs import Stairs

#Imports de modules
from handler import heal, teleport, throw ,protect,renforcement1,renforcement2,renforcement3, amulette, restaureFaim
from utils import getch
import theGame

import random, copy

class Game(object):
    """ Class representing game state """

    """ available equipments """
    equipments = {0: [Equipment("potion", "!",2, usage=lambda self, hero: heal(hero)), \
                      Equipment("gold", "o"), \
                      Equipment("pomme", "P", usage=lambda self, hero: restaureFaim(hero, 4))],
                  2: [Arme("epée","/",level=3,solidite=4, usage=lambda self, hero: renforcement3(hero))], \
                  3: [Equipment("portoloin", "w", usage=lambda self, hero: teleport(hero, False))], \
                  4: [Equipment("bouclier", "#", usage=lambda self, hero: protect(hero))], \
                  5: [Arme("couteau","-",level=1,solidite=2, usage=lambda self, hero: renforcement1(hero))], \
                  6: [Arme("lance","|",level=2,solidite=3, usage=lambda self, hero: renforcement2(hero))], \
                  7: [Equipment("amulettes","a",usage=lambda self, hero: amulette(hero))]\
                  }

    """ available monsters """
    monsters = {0: [Creature("Goblin", 4), Creature("Bat", 2, "W")],
                1: [Creature("Ork", 6, strength=2), Creature("Blob", 10)], 5: [Creature("Dragon", 20, strength=3)]}


    """ available actions """
    _actions = {'z': lambda h: theGame.theGame()._floor.move(h, Coord(0, -1)), \
                'q': lambda h: theGame.theGame()._floor.move(h, Coord(-1, 0)), \
                's': lambda h: theGame.theGame()._floor.move(h, Coord(0, 1)), \
                'd': lambda h: theGame.theGame()._floor.move(h, Coord(1, 0)), \
                'i': lambda h: theGame.theGame().addMessage(h.fullDescription()), \
                'k': lambda h: h.__setattr__('hp', 0), \
                'u': lambda h: h.use(theGame.theGame().select(h._inventory)), \
                't': lambda h: h.detruit(theGame.theGame().select(h._inventory)),\
                ' ': lambda h: None, \
                'h': lambda h: theGame.theGame().addMessage("Actions disponibles : " + str(list(Game._actions.keys()))), \
                'b': lambda h: theGame.theGame().addMessage("I am " + h.name), \
                'a': lambda h: theGame.theGame()._floor.move(h, Coord(-1, -1)),     #joueur se déplace en diagonale
                'e': lambda h: theGame.theGame()._floor.move(h, Coord(1, -1)),
                'c': lambda h: theGame.theGame()._floor.move(h, Coord(1, 1)),
                'w': lambda h: theGame.theGame()._floor.move(h, Coord(-1, 1))
                }

    def __init__(self, level=1, hero=None):
        self._level = level
        self._messages = []
        if hero == None:
            hero = Hero()
        self._hero = hero
        self._floor = None
        self.hungloop = 0  #compteurs d'actions pour la faim et la réduction d'hp liée à la faim
        self.hploop = 0

    def buildFloor(self):
        """Creates a map for the current floor."""
        self._floor = Map(hero=self._hero)
        self._floor.put(self._floor._rooms[-1].center(), Stairs())
        self._level += 1

    def addMessage(self, msg):
        """Adds a message in the message list."""
        self._messages.append(msg)

    def readMessages(self):
        """Returns the message list and clears it."""
        s = ''
        for m in self._messages:
            s += m + '. '
        self._messages.clear()
        return s

    def randElement(self, collect):
        """Returns a clone of random element from a collection using exponential random law."""
        x = random.expovariate(1 / self._level)
        for k in collect.keys():
            if k <= x:
                l = collect[k]
        return copy.copy(random.choice(l))

    def randEquipment(self):
        """Returns a random equipment."""
        return self.randElement(Game.equipments)

    def randMonster(self):
        """Returns a random monster."""
        return self.randElement(Game.monsters)

    def select(self, l):
        print("Choose item> " + str([str(l.index(e)) + ": " + e.name for e in l]))
        c = getch()
        if c.isdigit() and int(c) in range(len(l)):
            return l[int(c)]
            
    def play(self):
        """Main game loop"""
        self.buildFloor()
        print("--- Welcome Hero! ---")
        while self._hero.hp > 0:
            print()
            print(self._floor)
            print(self._hero.description())
            print(self.readMessages())
            c = getch()
            if c in Game._actions:
                Game._actions[c](self._hero)
            self._hero.reduireLaFaim()  #lors que chaque action les compteurs sont vérifiés et incrémentés ou remis à zéro en plus de réduire la satiété ou la faim en fonction des circonstances
            self._floor.moveAllMonsters()
        print("--- Game Over ---")
