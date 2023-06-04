#Imports de classe
from Creature import Creature

#Imports de modules
import theGame

class Piege(Creature):  #création d'une classe Piege heritière de la classe Creature
    def __init__(self, name="Piege", hp=0,abbrv=".", strength=1 ):
        Creature.__init__(self,name, hp, abbrv, strength)
    def meet(self,hero):
        hero.hp-=self.strength
        theGame.theGame().addMessage("You just passed on a trap" + str(self.strength) + " hp " )
        return True