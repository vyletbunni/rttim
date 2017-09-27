from direct.distributed import DistributedObjectAI
from direct.distributed.ClockDelta import *
from otp.ai.AIBase import *
from toontown.toonbase.ToontownGlobals import *
import time


HEIGHT_DELTA = 0.5
MAX_HEIGHT = 10.0
MIN_HEIGHT = 2.0


class DistributedDGFlowerAI(DistributedObjectAI.DistributedObjectAI):
    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

        self.height = MIN_HEIGHT
        self.avList = []
        self.cooloff = 0

    def delete(self):
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def start(self):
        pass

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.avList:
            self.avList.append(avId)
            if self.height + HEIGHT_DELTA <= MAX_HEIGHT:
                self.height += HEIGHT_DELTA
                self.sendUpdate('setHeight', [self.height])
            else:
                if self.cooloff == 0:
                    self.hereComesTheBOOM()
                else:
                    print ':DistributedDGFlowerAI(warning): Tried to ignite flower when cooldown wasn\'t finished.'

    def avatarExit(self):
        avId = self.air.getAvatarIdFromSender()
        if avId in self.avList:
            self.avList.remove(avId)
            if self.height - HEIGHT_DELTA >= MIN_HEIGHT:
                self.height -= HEIGHT_DELTA
                self.sendUpdate('setHeight', [self.height])

    def hereComesTheBOOM(self):
        self.sendUpdate('readyOrNot', [1])
        self.helpMe()
        taskMgr.doMethodLater(3.0, self.holdUp, 'waitAMinute')
    
    def helpMe(self):
        for x in self.avList:
            toon = simbase.air.doId2do.get(x)
            if toon is not None:
                toon.b_setAnimPlay('slip-backward', 20)
        
    def holdUp(self, name):
        for x in self.avList:
            toon = simbase.air.doId2do.get(x)
            if toon is not None:
                if toon.getHp() > 0: #sanity checks
                    toon.takeDamage(toon.getHp())
        print ':DistributedDGFlowerAI: People just got XD\'d.'
    
    def doCooldown(self, name):
        self.cooloff = 0
        print ':DistributedDGFlowerAI: Flower now ready for use.'