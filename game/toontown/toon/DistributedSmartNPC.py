from DistributedNPCToonBase import *
from toontown.chat.ChatGlobals import *
from toontown.nametag.NametagGlobals import *


class DistributedSmartNPC(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.window = Sequence(Func(self.setAnimState, 'Squish'), Func(base.playSfx, base.loadSfx('phase_3.5/audio/dial/AV_rabbit_exclaim.ogg'), volume=1, node=self))

    def delayDelete(self):
        DistributedNPCToonBase.delayDelete(self)
        DistributedNPCToonBase.disable(self)
        self.window.finish()

    def handleCollisionSphereEnter(self, collEntry):
        self.window.start()
        
    def initToonState(self):
        self.setAnimState('neutral', 1, None, None)
        self.setPosHpr(101, 15.5, 4, -245, 0, 0)

    def createBot(self, chatPhraseId):
        chatPhrases = [
            "Yo here's a bot.",
            'Don\'t touch me!!!  It makes bots!',
            'Hope you don\'t mind this new bot.',
            "Tell Cheeze to stop using the injector.",
            "Here\'s an L and a bot.",
            "End the createBot process? nah",
            "xd"
        ]
        self.setChatAbsolute(chatPhrases[chatPhraseId], CFSpeech|CFTimeout)