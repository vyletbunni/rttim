from pandac.PandaModules import *
from SafeZoneLoader import SafeZoneLoader
import TFPlayground
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.effects import Bubbles
from toontown.toon import NPCToons
from toontown.election import ElectionGlobals
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from toontown.election import DistributedFlippyStand
from toontown.election import ToonfestCog
from otp.nametag.NametagConstants import *
from toontown.pets import Pet
from toontown.pets import PetDNA
from toontown.char import Char
from toontown.char import CharDNA
from toontown.suit import Suit
from toontown.suit import SuitDNA
from toontown.suit import BossCog

from direct.interval.IntervalGlobal import *
import random
import math

from toontown.battle import BattleParticles

class TFSafeZoneLoader(SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = TFPlayground.TFPlayground
        self.musicFile = 'phase_6/audio/bgm/TF_SZ_1.ogg'
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.ogg' # Temporary
        self.dnaFile = 'phase_6/dna/toonfest_sz.dna'
        self.safeZoneStorageDNAFile = 'phase_6/dna/storage_TF.dna'
        self.restockSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_pies_restock.ogg')
        self.flippyBlatherSequence = Sequence()
        self.fluffy = None
        self.clouds = []
        self.cloudSwitch = 0
        self.cloudTrack = None

    def load(self):
        SafeZoneLoader.load(self)
        # Flippy
        self.flippy = NPCToons.createLocalNPC(2001)
        self.flippy.reparentTo(render)
        self.flippy.setPickable(0)
        self.flippy.setPos(178.6, -265.6, 5.2)
        self.flippy.setH(100)
        self.flippy.initializeBodyCollisions('toon')
        self.flippy.addActive()
        self.flippy.startBlink()
        
        self.flippyBlatherSequence = Sequence(
            Wait(10),
            Func(self.flippy.setChatAbsolute, 'Hey, how\'s it going?', CFSpeech|CFTimeout),
            Wait(5),
            Func(self.flippy.setChatAbsolute, "I'm fine myself, given how I've had to code ToonFest into RTTIM.", CFSpeech|CFTimeout),
            Wait(8),
            Func(self.flippy.setChatAbsolute, "Thanks, Bill.", CFSpeech|CFTimeout),
            Wait(5),
            Func(self.flippy.setChatAbsolute, "Anyway, I hope you enjoy it.", CFSpeech|CFTimeout),
            Wait(7),
            Func(self.flippy.setChatAbsolute, 'I didn\'t do it for nothing.', CFSpeech|CFTimeout)
        )
        self.flippyBlatherSequence.start()
        
        # Fluffy
        self.mickey = Char.Char()
        self.mickeyDNA = CharDNA.CharDNA()
        self.mickeyDNA.newChar('mk')
        self.mickey.setDNA(self.mickeyDNA)
        self.mickey.addActive()
        self.mickey.startEarTask()
        self.mickey.reparentTo(render)
        self.mickey.setPos(180.382, -271.073, 5.621)
        self.mickey.setH(67.684)
        
        # Bill
        self.bill = NPCToons.createLocalNPC(2001)
        self.bill.reparentTo(render)
        self.bill.setPickable(0)
        self.bill.setPos(112.799, -19.293, 4.597)
        self.bill.setH(-164.953)
        self.bill.initializeBodyCollisions('toon')
        self.bill.addActive()
        self.bill.startBlink()
        
        self.billRun = Sequence(
            Func(self.bill.loop, 'run'),
            self.bill.posInterval(8.1, (154.792, -175.501, 4.597)),
            Func(self.bill.loop, 'walk'),
            self.bill.hprInterval(1.0, (-344.953, 0, 0)),
            Func(self.bill.loop, 'run'),
            self.bill.posInterval(8.1, (112.799, -19.293, 4.597)),
            Func(self.bill.loop, 'walk'),
            self.bill.hprInterval(1.0, (-164.953, 0, 0)))
            
        self.billRun.loop()
        
        self.bfs = Suit.Suit()
        self.bfsDNA = SuitDNA.SuitDNA()
        self.bfsDNA.newSuit('bfs')
        self.bfs.setDNA(self.bfsDNA)
        self.bfs.setPickable(0)
        self.bfs.addActive()
        self.bfs.reparentTo(render)
        self.bfs.initializeBodyCollisions('suit')
        self.bfs.setPos(207, -164, 4.597)
        self.bfs.setH(-240.097)
        
        self.bfs.pingpong('slip-forward', 30, 40)

        #BossCog
        self.vp = BossCog.BossCog()
        self.vpDNA = SuitDNA.SuitDNA()
        self.vpDNA.newBossCog('s')
        self.vp.setDNA(self.vpDNA)
        self.vp.addActive()
        self.vp.reparentTo(render)
        self.vp.initializeBodyCollisions('bosscog')
        self.vp.setPos(302.777, -370.352, 14.446)
        self.vp.setH(-126.356)
        self.vp.happy = 0
        self.vp.doAnimate(self.vp.getAnim(None))

        # Find the bases - base1 is largest
        try:
            self.towerGeom = self.geom.find('**/toonfest_tower_DNARoot')
            self.towerGeom.find('**/itsclosed').removeNode()
            self.base1 = self.towerGeom.find('**/base1')
            self.base2 = self.towerGeom.find('**/base2')
            self.base3 = self.towerGeom.find('**/base3')
        except:
            self.notify.warning("Something messed up loading the tower bases!")

        self.confetti = None
        self.confettiRender = None
        self.confettiFade = None
        self.loadConfetti()

    def loadConfetti(self):
        self.confetti = BattleParticles.loadParticleFile('confetti.ptf')
        self.confetti.setPos(0, 0, 5)
        self.confettiRender = self.geom.attachNewNode('snowRender')
        self.confettiRender.setDepthWrite(0)
        self.confettiRender.setBin('fixed', 1)
        self.confettiFade = None

    def unload(self):
        SafeZoneLoader.unload(self)
        self.flippyBlatherSequence.finish()
        del self.confetti
        del self.confettiRender
        if self.flippy:
            self.flippy.stopBlink()
            self.flippy.removeActive()
            self.flippy.cleanup()
            self.flippy.removeNode()
            del self.flippy
        if self.mickey:
            self.mickey.removeActive()
            self.mickey.stopEarTask()
            self.mickey.delete()
            del self.mickey
        if self.bill:
            self.bill.stopBlink()
            self.bill.removeActive()
            self.billRun.finish()
            self.bill.cleanup()
            self.bill.removeNode()
            del self.bill
        if self.bfs:
            self.bfs.removeActive()
            self.bfs.cleanup()
            self.bfs.removeNode()
            del self.bfs
        if self.vp:
            self.vp.removeActive()
            self.vp.cleanup()
            self.vp.removeNode()
            del self.vp


    def enter(self, requestStatus):
        SafeZoneLoader.enter(self, requestStatus)
        if self.confetti is not None:
            self.confetti.start(camera, self.confettiRender)

    def exit(self):
        SafeZoneLoader.exit(self)

    def startCloudPlatforms(self):
        return
        if len(self.clouds):
            self.cloudTrack = self.__cloudTrack()
            self.cloudTrack.loop()

    def stopCloudPlatforms(self):
        if self.cloudTrack:
            self.cloudTrack.pause()
            del self.cloudTrack
            self.cloudTrack = None
        return

    def loadClouds(self):
        self.loadCloudPlatforms()
        if base.cloudPlatformsEnabled and 0:
            self.setCloudSwitch(1)
        if self.cloudSwitch:
            self.setCloudSwitch(self.cloudSwitch)

    def loadCloud(self, version, radius, zOffset):
        self.notify.debug('loadOnePlatform version=%d' % version)
        cloud = NodePath('cloud-%d%d' % (radius, version))
        cloudModel = loader.loadModel('phase_5.5/models/estate/bumper_cloud')
        cc = cloudModel.copyTo(cloud)
        colCube = cc.find('**/collision')
        colCube.setName('cloudSphere-0')
        dTheta = 2.0 * math.pi / self.numClouds
        cloud.reparentTo(self.cloudOrigin)
        axes = [Vec3(1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, 1)]
        cloud.setPos(radius * math.cos(version * dTheta), radius * math.sin(version * dTheta), 4 * random.random() + zOffset)
        cloud.setScale(4.0)
        cloud.setTag('number', '%d%d' % (radius, version))
        x, y, z = cloud.getPos()
        cloudIval = Parallel(cloud.hprInterval(4.0, (360, 0, 0)))
        if version % 2 == 0:
            cloudIval.append(Sequence(cloud.posInterval(2.0, (x, y, z + 4), startPos=(x, y, z), blendType='easeInOut'), cloud.posInterval(2.0, (x, y, z), startPos=(x, y, z + 4), blendType='easeInOut')))
        else:
            cloudIval.append(Sequence(cloud.posInterval(2.0, (x, y, z), startPos=(x, y, z + 4), blendType='easeInOut'), cloud.posInterval(2.0, (x, y, z + 4), startPos=(x, y, z), blendType='easeInOut')))
        cloudIval.loop()
        self.clouds.append([cloud, random.choice(axes)])

    def loadSkyCollision(self):
        plane = CollisionPlane(Plane(Vec3(0, 0, -1), Point3(0, 0, 350)))
        plane.setTangible(0)
        planeNode = CollisionNode('sky_collision')
        planeNode.addSolid(plane)
        self.cloudOrigin.attachNewNode(planeNode)

    def loadCloudPlatforms(self):
        self.cloudOrigin = self.geom.attachNewNode('cloudOrigin')
        self.cloudOrigin.setPos(216, -68, 55)
        self.loadSkyCollision()
        self.numClouds = 18
        for i in range(self.numClouds):
            self.loadCloud(i, 110, 0)

        for i in range(self.numClouds):
            self.loadCloud(i, 130, 30)

        for i in range(self.numClouds):
            self.loadCloud(i, 110, 60)

        self.cloudOrigin.stash()

    def __cleanupCloudFadeInterval(self):
        if hasattr(self, 'cloudFadeInterval'):
            self.cloudFadeInterval.pause()
            self.cloudFadeInterval = None
        return

    def fadeClouds(self, on):
        self.__cleanupCloudFadeInterval()
        self.cloudOrigin.setTransparency(1)
        self.cloudFadeInterval = self.cloudOrigin.colorInterval(0.5, Vec4(1, 1, 1, int(on)), blendType='easeIn')
        if on:
            self.cloudOrigin.setColor(Vec4(1, 1, 1, 0))
            self.setCloudSwitch(1)
        else:
            self.cloudFadeInterval = Sequence(self.cloudFadeInterval, Func(self.setCloudSwitch, 0), Func(self.cloudOrigin.setTransparency, 0))
        self.cloudFadeInterval.start()

    def setCloudSwitch(self, on):
        self.cloudSwitch = on
        if hasattr(self, 'cloudOrigin'):
            if on:
                self.cloudOrigin.unstash()
            else:
                self.cloudOrigin.stash()