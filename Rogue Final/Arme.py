#Imports de classe
from Equipment import Equipment

#Imports de modules
import theGame

class Arme(Equipment):          #sert a trier les arme parmit les equipment
    def __init__(self, name, abbrv="",level=1,solidite=3, usage=None):
        Equipment.__init__(self, name, abbrv, solidite)
        self.level = level      #nombre de point que l'arme rapporte sur la force,on utilse cette variable pour la fonction derenforcement(en classe Creature)
        self.usage = usage

    def use(self, creature):    #on change le message d'utilisation
        """Utilise l'équipement. A un effet sur le héros selon son utilisation.
             Renvoie True si l'objet est consommé."""
        if self.usage is None:
            theGame.theGame().addMessage(self.name + " n'est pas utilisable")
            return False
        else:
            theGame.theGame().addMessage(creature.name + " s'est équipé de " + self.name)
            return self.usage(self, creature)