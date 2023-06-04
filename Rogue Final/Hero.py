#Imports de classe
from Creature import Creature
from Equipment import Equipment
from Arme import Arme

#Imports de module
import theGame

class Hero(Creature):
    """The hero of the game.
        Is a creature. Has an inventory of elements. """

    def __init__(self, name="Hero", hp=10, abbrv="@", strength=2,toxicite=0,empoisonne=0):
        Creature.__init__(self, name, hp, abbrv, strength,toxicite,empoisonne)
        self.gold=0             #or n'est plus dans l'iventaire
        self._inventory = []
        self._arme=[]           #inventaire qui comprendra qu'un element, l'arme que le héros a équipé
        self.killCreature = 0
        self.hpmax=hp
        self.xp=0               #le nombre d'xp est initialisé à 0
        self.hungermax = 20
        self.hunger = self.hungermax  #au debut le hero n'as pas faim
        self.poisoned=0         #au debut le hero n'est pas empoisoné


    def description(self):
        """Description of the hero"""
        return Creature.description(self) +"(Gold:" + str(self.gold) + ")"+ "(Arme:"+str(self._arme)+")"+ str(self._inventory)

    def fullDescription(self):
        """Complete description of the hero"""
        res = ''
        for e in self.__dict__:
            if e[0] != '_':
                res += '> ' + e + ' : ' + str(self.__dict__[e]) + '\n'
        res += '> INVENTORY : ' + str([x.name for x in self._inventory])
        res += "> Max HP : " + str(self.hpmax) + '\n'  #ajout de l'hp max et de l'xp dans la description
        return res

    def checkEquipment(self, o):
        """Check if o is an Equipment."""
        if not isinstance(o, Equipment):
            raise TypeError('Not a Equipment')

    def take(self, elem):
        """The hero takes adds the equipment to its inventory"""
        self.checkEquipment(elem)
        if elem.name == "gold":             #l'or ne vas plus dans l'inventaire,
            self.gold = self.gold + 1
            return True
        elif len(self._inventory) < 10:     #l'inventaire est limitée a 10 element si le hero
                                            #cherche a en ramasser un 11éme il ne pourras pas le prendre
            self._inventory.append(elem)    
            return True
        else:
            theGame.theGame().addMessage(" pour utiliser cet équipement utilisez le ou détruisez le")
            return False

    def detruit(self,elem):      
        self._inventory.remove(elem)
        theGame.theGame().addMessage(elem.name+ "est détruit")

    def use(self, elem):
        """Use a piece of equipment"""
        if elem is None:
            return
        self.checkEquipment(elem)
        if elem not in self._inventory:
            raise ValueError('Equipment ' + elem.name + 'not in inventory')
        if elem.use(self):
            if isinstance(elem,Arme):
                if len(self._arme)>0:       #si le hero utilise une arme(2) alors qu’il porte déjà une arme(1)
                    self._inventory.append(self._arme[0])   #l'arme(1) qu'il portait retourne dans son inventaire
                    self.derenforcement(self._arme[0])      #l'effet de l'arme(1) est annulé
                    self._arme=[]                           #on remplace l'arme(1)  
                    self._arme.append(elem)                 #par l'arme (2) dans l'espace d'armement
                    self._inventory.remove(elem)            #on retire l'arme(2) de l'inventaire
                else:                                       #si le hero utilise une arme(2) qu’il n'en porte pas deja.l'arme passe de l'inventaire a l'espace d'armement
                    self._arme.append(elem)
                    self._inventory.remove(elem)
            else:                                   #dans le cas ou l'equipment n'est pas une arme la solidité baissent apres une utilisation
                elem.solidite-=1
                if elem.solidite<=0:
                   self._inventory.remove(elem)

    def reduireLaFaim(self):  # fait baisser la fain tout les 3 deplacement, si la faim est à 0,
        #ça baisse la barre d'hp tout les 2 deplacement jusqu'à ce que la faim soi> 0
        if self.hunger > 0:
            if theGame.theGame().hungloop == 2:
                self.hunger = self.hunger - 1
                theGame.theGame().hungloop = 0
            else:
                theGame.theGame().hungloop = theGame.theGame().hungloop + 1
        else:
            if theGame.theGame().hploop == 1:
                self.hp = self.hp - 1
                theGame.theGame().hploop = 0
            else:
                theGame.theGame().hploop = theGame.theGame().hploop + 1
                
