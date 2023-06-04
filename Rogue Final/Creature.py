#Imports de classe
from Element import Element

#Imports de module
import theGame

class Creature(Element):
    """A creature that occupies the dungeon.
        Is an Element. Has hit points and strength."""

    def __init__(self, name, hp, abbrv="", strength=1,toxicite=0,deplacement=1):
        Element.__init__(self, name, abbrv)
        self.hp = hp
        self.strength = strength
        self.toxicite = toxicite        #nombre de mouvement ou le poison va agir
        self.empoisonne = 0             #nombre de mouvement ou on est empoisoné
        self.protection = 0             #barre de protection
        self.deplacement = deplacement  #nombre de deplacement que fera une creature par tour 
        self._arme = []         #espace d'armemement
        self.hpmax = hp         #ajout des hp max

    def description(self):
        """Description of the creature"""
        if self.empoisonne > 0:     #si le poison est effectif alors le nombre de mouvements empoisonés apparait dans la description, mais non sinon
            b="(Empoisonnement:"+str(self.empoisonne)+")"
        else:
            b=""
        return Element.description(self) + "(" + str(self.hp) + ")"+ "(Strength:" + str(self.strength) + ")"+ "(P:" + str(self.protection) + ")"+b


    def poison(self):
        "effet du poison si la créature est protégée ou non"
        if self.empoisonne > 0:
            if self.protection > 0:
                self.protection -= 1
                self.empoisonne -= 1
                theGame.theGame().addMessage("Le poison vous fait perdre 1 protection")
            else:
                self.hp -= 1
                self.empoisonne -= 1
                theGame.theGame().addMessage("Le poison vous fait perdre 1 hp")

    def derenforcement(self,arme):
        self.strength-=arme.level

    def soliditeArme(self,other):
        "se faire attaquer par un ennemi armé"
        if other._arme!=[]:
            other._arme[0].solidite-=1
            if other._arme[0].solidite<=0:
                    other.derenforcement(other._arme[0])
                    other._arme=[]                       
            
    def meet(self, other):
        """The creature is encountered by an other creature.
        The other one hits the creature. Return True if the creature is dead."""
        if other.toxicite > 0:      #le coup d'une creature toxic empoisone
            self.empoisonne += other.toxicite
        if other.empoisonne > 0:
            other.poison()
        x = 1
        while x <= other.strength:    #le x permet de retirer le bon nombre de hp dans le cas ou 0<self.protection<other.strength
            if self.protection > 0:
                self.protection -= other.strength
                x += 1
            else:
                self.hp -= other.strength
                x += 1
        self.soliditeArme(other)  
        theGame.theGame().addMessage("The " + other.name + " hits the " + self.description())

        if self.hp > 0:
            return False
        return True
