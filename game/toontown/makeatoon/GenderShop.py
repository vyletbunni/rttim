from pandac.PandaModules import *
from direct.fsm import StateData
from direct.gui.DirectGui import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.toon import ToonDNA
from toontown.toon import Toon
from MakeAToonGlobals import *
from direct.directnotify import DirectNotifyGlobal
import random

class GenderShop(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('GenderShop')
    
    def __init__(self, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.shopsVisited = []
        self.toon = None
        self.gender = 'm'
        return None

    
    def enter(self):
        base.disableMouse()
        return None

    
    def showButtons(self):
        return None

    
    def exit(self):
        return None

    
    def load(self):
        return None

    
    def unload(self):
        return None

    
    def setGender(self, choice):
        self._GenderShop__setGender(choice)

    
    def _GenderShop__setGender(self, choice):
        if choice == -1:
            self.gender = 'm'
        else:
            self.gender = 'f'
        messenger.send(self.doneEvent)