from otp.ai.AIBaseGlobal import *
from DistributedNPCToonBaseAI import *
from ToonDNA import *
from DistributedNPCToonAI import *
import random

class DistributedNPCSecretAI(DistributedNPCToonBaseAI):

    def __init__(self, air, npcId, questCallback=None, hq=0):
        DistributedNPCToonBaseAI.__init__(self, air, npcId, questCallback)
        self.air = air

    def avatarEnter(self):
        chatPhraseId = random.randrange(6)
        self.sendUpdate('createBot', [chatPhraseId])
        dna = ToonDNA()
        dna.newToonRandom()
        newToon = DistributedNPCToonAI(self.cr)
        newToon.b_setDNAString(dna.makeNetString())
        x = (random.random()*10) + 10
        y = (random.random()*10) + 10
        z = 4
        newToon.sendUpdate('setPositionIndex', [x, y, z])