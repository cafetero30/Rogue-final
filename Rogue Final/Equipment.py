#Imports de classe
from Element import Element

#Imports de module
import theGame

class Equipment(Element):
    """A piece of equipment"""

    def __init__(self, name, abbrv="",solidite=2, usage=None):
        Element.__init__(self, name, abbrv)
        self.solidite = solidite        #nombre d'usage possible avant destruction
        self.usage = usage


    def descr(self):
        return str(self.abbrv)+"(solidité:"+str(self.solidite)+")"
    
    def meet(self, hero):
        """Makes the hero meet an element. The hero takes the element."""
        if hero.take(self): 
            theGame.theGame().addMessage("You pick up a " + self.name)
            return True
        else: 
            theGame.theGame().addMessage("Sorry, you have reached your maximum item number")


    def use(self, creature):
        """Uses the piece of equipment. Has effect on the hero according usage.
            Return True if the object is consumed."""
        if self.usage is None:
            theGame.theGame().addMessage("The " + self.name + " is not usable")
            return False
        else:
            
            theGame.theGame().addMessage("The " + creature.name + " uses the " + self.name)
            return self.usage(self, creature)

