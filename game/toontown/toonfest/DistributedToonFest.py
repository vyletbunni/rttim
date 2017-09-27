from pandac.PandaModules import *
from direct.task.Task import Task
from direct.distributed.ClockDelta import *
from direct.task.Task import Task
from direct.actor.Actor import Actor
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import NodePath
from toontown.toonbase import TTLocalizer
import random

import ToonfestGlobals

class DistributedToonFest(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonFest')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.geom = base.cr.playGame.hood.loader.geom
        self.generate()

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        #Toon.loadMinigameAnims()
        self.defaultSignModel = loader.loadModel('phase_13/models/parties/eventSign')
        self.activityIconsModel = loader.loadModel('phase_4/models/parties/eventSignIcons')
        #self.initializeCogDummies()

        # Cog holes
        for hole in ToonfestGlobals.CogHolePopupPoints:
            holeGeom = loader.loadModel('phase_13/models/parties/cogPinataHole')
            holeGeom.setTransparency(True)
            holeGeom.setPos(hole[0])
            holeGeom.setP(-90)
            holeGeom.setScale(3.2)
            holeGeom.setBin('ground', 3)
            holeGeom.reparentTo(render)

    def disable(self):
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        DistributedObject.DistributedObject.delete(self)
        return
