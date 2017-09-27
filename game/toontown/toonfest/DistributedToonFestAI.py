from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.task import Task

from toontown.toonbase import ToontownGlobals
from toontown.toonfest import ToonfestGlobals 
from toontown.parties.DistributedPartyCannonActivityAI import DistributedPartyCannonActivityAI
from toontown.parties.DistributedPartyCannonAI import DistributedPartyCannonAI
from toontown.parties.DistributedPartyVictoryTrampolineActivityAI import DistributedPartyVictoryTrampolineActivityAI

class DistributedToonFestAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonFestAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air

        # Future references:
        self.cogDummyTaskName = 'random-cog-dummies'
        self.fireworksTaskName = 'hourly-toonfest-fireworks'
        self.beanBagTaskName = 'bean-bag-treasures'

    def generate(self):
        self.initiateActivities()
        
    def initiateActivities(self):
        #self.TFCannonActivity = DistributedPartyCannonActivityAI(self.air, self.doId, (0, 0, 0, 0))
        #self.TFCannonActivity.generateWithRequired(ToontownGlobals.ToonFest)
        #for ToonfestCannonPos in ToonfestGlobals.CannonPoints:
        #    self.TFCannon = DistributedPartyCannonAI(self.air)
        #    self.TFCannon.setActivityDoId(self.TFCannonActivity.doId)
        #    self.TFCannon.setPosHpr(*ToonfestCannonPos)
        #    self.TFCannon.generateWithRequired(ToontownGlobals.ToonFest)
        #for ToonfestTrampolinePos in ToonfestGlobals.TrampolinePoints:
        #    x = ToonfestTrampolinePos[0]
        #    y = ToonfestTrampolinePos[1]
        #    z = ToonfestTrampolinePos[2]
        #    h = ToonfestTrampolinePos[3]
        #    self.TFTrampolineActivity = DistributedPartyVictoryTrampolineActivityAI(self.air, self.doId, (0, 0, 0, 0))
        #    self.TFTrampolineActivity.generateWithRequired(ToontownGlobals.ToonFest)
        #    self.TFTrampolineActivity.sendUpdate('setX', [x])
        #    self.TFTrampolineActivity.sendUpdate('setY', [y])
        #    self.TFTrampolineActivity.sendUpdate('setZ', [z])
        #    self.TFTrampolineActivity.sendUpdate('setH', [h])
        pass