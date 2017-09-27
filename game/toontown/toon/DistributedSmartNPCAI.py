from otp.ai.AIBaseGlobal import *
from DistributedNPCToonBaseAI import *
from ToonDNA import *
from DistributedNPCToonAI import *
import random

class DistributedSmartNPCAI(DistributedNPCToonBaseAI):

    def __init__(self, air, npcId, questCallback=None, hq=0):
        DistributedNPCToonBaseAI.__init__(self, air, npcId, questCallback)
        self.air = air

#    def avatarEnter(self):
#        chatPhraseId = random.randrange(6)
#        print ':DistributedSmartNPCAI: %d' % chatPhraseId
#        #self.sendUpdate('createBot', [chatPhraseId])
#        dna = ToonDNA()
#        dna.newToonRandom()
#        newToon = DistributedNPCToonAI(self.air, random.randrange(1211,1306,1))
#        #newToon.b_setDNAString(dna.makeNetString())
#        x = (random.random()*10) + 10
#        y = (random.random()*10) + 10
#        z = 4
#        newToon.sendUpdate('setPos', [x, y, z])