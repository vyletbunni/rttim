from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedDuckTankAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedDuckTankAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
