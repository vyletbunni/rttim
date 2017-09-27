#from SZHoodAI import SZHoodAI
from toontown.hood import HoodAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedPicnicBasketAI import DistributedPicnicBasketAI
from toontown.safezone.DistributedPicnicTableAI import DistributedPicnicTableAI
from toontown.distributed.DistributedTimerAI import DistributedTimerAI
from toontown.election import DistributedFlippyStandAI
from toontown.election import DistributedToonfestBalloonAI
from toontown.election import DistributedToonfestTowerBaseAI
from toontown.election import DistributedToonfestCogAI
from direct.fsm.FSM import FSM
from pandac.PandaModules import *

from toontown.toonfest import DistributedToonFestAI
from toontown.toonfest import DistributedDuckTankAI

class TFHoodAI(HoodAI.HoodAI):
    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.ToonFest,
                               ToontownGlobals.ToonFest)

        self.trolley = None
        self.classicChar = None
        self.HOOD = ToontownGlobals.ToonFest

        self.startup()
        
    def startup(self):
        HoodAI.HoodAI.startup(self)
        self.timer = DistributedTimerAI(self.air)
        self.timer.generateWithRequired(self.HOOD)
        self.flippyStand = DistributedFlippyStandAI.DistributedFlippyStandAI(self.air)
        self.flippyStand.generateWithRequired(self.HOOD)
        self.toonfestTower = DistributedToonfestTowerBaseAI.DistributedToonfestTowerBaseAI(self.air)
        self.toonfestTower.generateWithRequired(self.HOOD)
        self.balloon = DistributedToonfestBalloonAI.DistributedToonfestBalloonAI(self.air)
        self.balloon.generateWithRequired(self.HOOD)
        self.balloon.b_setState('Waiting')
        
        self.toonfest = DistributedToonFestAI.DistributedToonFestAI(self.air)
        self.toonfest.generateWithRequired(self.HOOD)

        self.duckTank = DistributedDuckTankAI.DistributedDuckTankAI(self.air)
        self.duckTank.generateWithRequired(self.HOOD)
        
        #filename = self.air.lookupDNAFileName(self.HOOD)
        #self.air.dnaSpawner.spawnObjects(filename, self.HOOD)
        
    def createZone(self):
        #SZHoodAI.createTreasurePlanner(self)
        #SZHoodAI.createZone(self, False)
        self.spawnObjects()
        self.timer = DistributedTimerAI(self.air)
        self.timer.generateWithRequired(self.HOOD)
        #self.flippyStand = DistributedFlippyStandAI.DistributedFlippyStandAI(self.air)
        #self.flippyStand.generateWithRequired(self.HOOD)
        #self.toonfestTower = DistributedToonfestTowerAI.DistributedToonfestTowerAI(self.air)
        #self.toonfestTower.generateWithRequired(self.HOOD)
        #self.toonfestTower = DistributedToonfestTowerBaseAI.DistributedToonfestTowerBaseAI(self.air)
        #self.toonfestTower.generateWithRequired(self.HOOD)
        #self.balloon = DistributedToonfestBalloonAI.DistributedToonfestBalloonAI(self.air)
        #self.balloon.generateWithRequired(self.HOOD)
        #self.balloon.b_setState('Waiting')

        self.toonfest = DistributedToonFestAI.DistributedToonFestAI(self.air)
        self.toonfest.generateWithRequired(self.HOOD)

        self.duckTank = DistributedDuckTankAI.DistributedDuckTankAI(self.air)
        self.duckTank.generateWithRequired(self.HOOD)

        self.cogs = []
        #self.createCogs()

    def createCogs(self):
        # [x, y, z, id]
        posList = [[224, -146, 4.597, 1]]
        for pos in posList:
            self.cog = DistributedToonfestCogAI.DistributedToonfestCogAI(self.air)
            self.cog.generateWithRequired(self.HOOD)
            self.cog.setPos(pos[0], pos[1], pos[2])
            self.cog.setId(pos[3])
            self.cogs.append(self.cog)
