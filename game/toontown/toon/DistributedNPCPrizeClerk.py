from pandac.PandaModules import *
from DistributedNPCToonBase import *
from toontown.minigame import ClerkPurchase
from toontown.shtiker.PurchaseManagerConstants import *
import NPCToons
from direct.task.Task import Task
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil
from toontown.toontowngui import TeaserPanel
from otp.nametag.NametagConstants import *

class DistributedNPCPrizeClerk(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.purchase = None
        self.isLocalToon = 0
        self.av = None
        return

    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('lerpCamera'))
        self.av = None
        base.localAvatar.posCamera(0, 0)
        DistributedNPCToonBase.disable(self)
        return

    def initToonState(self):
        self.setAnimState('neutral', 1.05, None, None)
        npcOrigin = self.cr.playGame.hood.loader.geom.find('**/npc_prizeclerk_origin_%s;+s' % self.posIndex)
        if not npcOrigin.isEmpty():
            self.reparentTo(npcOrigin)
            self.clearMat()
        else:
            self.notify.warning('announceGenerate: Could not find npc_prizeclerk_origin_' + str(self.posIndex))
        return

    def allowedToEnter(self):
        if hasattr(base, 'ttAccess') and base.ttAccess and base.ttAccess.canAccess():
            return True
        return False

    def handleOkTeaser(self):
        self.dialog.destroy()
        del self.dialog
        place = base.cr.playGame.getPlace()
        if place:
            place.fsm.request('walk')

    def handleCollisionSphereEnter(self, collEntry):
        if self.allowedToEnter():
            base.cr.playGame.getPlace().fsm.request('purchase')
            self.sendUpdate('avatarEnter', [])
        else:
            place = base.cr.playGame.getPlace()
            if place:
                place.fsm.request('stopped')
            self.dialog = TeaserPanel.TeaserPanel(pageName='otherGags', doneFunc=self.handleOkTeaser)

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None
        return

    def setMovie(self, mode, npcId, avId, timestamp):
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.remain = NPCToons.CLERK_COUNTDOWN_TIME - timeStamp
        self.isLocalToon = avId == base.localAvatar.doId
        if mode == NPCToons.PURCHASE_MOVIE_CLEAR:
            return
        else:
            if mode == NPCToons.PURCHASE_MOVIE_START:
                self.av = base.cr.doId2do.get(avId)
                if self.av is None:
                    self.notify.warning('Avatar %d not found in doId' % avId)
                    return
                self.accept(self.av.uniqueName('disable'), self.__handleUnexpectedExit)
                self.setupAvatars(self.av)
                if self.isLocalToon:
                    camera.wrtReparentTo(render)
                    self.cameraLerp = LerpPosQuatInterval(camera, 1, Point3(-4, 16, self.getHeight() - 0.5), Point3(-150, -2, 0), other=self, blendType='easeInOut')
                    self.cameraLerp.start()
                self.setChatAbsolute(TTLocalizer.TF_GREETING, CFSpeech|CFTimeout)
                if self.isLocalToon:
                    taskMgr.doMethodLater(1.0, self.revealToonFestGui, self.uniqueName('revealToonFestGui'))
            elif mode == NPCToons.PURCHASE_MOVIE_TIMEOUT:
                self.setChatAbsolute(TTLocalizer.TF_TOOKTOOLONG, CFSpeech | CFTimeout)
                self.resetClerk()
            elif mode == NPCToons.PURCHASE_MOVIE_COMPLETE:
                self.setChatAbsolute(TTLocalizer.TF_GOODBYE, CFSpeech | CFTimeout)
                self.resetClerk()
            return

    def revealToonFestGui(self, task):
        self.accept(DONE_EVENT, self.__handleGuiDone)
        self.gui = TFPrizeScreen.TFPrizeScreen(npc=self, random=self.rng, doneEvent=DONE_EVENT)
        self.gui.show()
        return Task.done

    def resetClerk(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('lerpCamera'))
        self.clearMat()
        self.startLookAround()
        self.detectAvatars()
        if self.isLocalToon:
            self.freeAvatar()
        return Task.done

