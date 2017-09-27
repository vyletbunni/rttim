from pandac.PandaModules import *
from otp.nametag.NametagConstants import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM
from toontown.toon import NPCToons
from toontown.toonbase import ToontownGlobals
from direct.task import Task
from random import choice
import ToonfestBalloonGlobals

class DistributedToonfestBalloon(DistributedObject, FSM):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'ToonfestBalloonFSM')
        self.avId = 0
        self.flightPathIndex = 0

        # Create the balloon
        self.balloon = loader.loadModel('phase_6/models/events/tf_balloon')
        self.balloon.reparentTo(base.render)
        self.balloon.setPos(*ToonfestBalloonGlobals.BalloonBasePosition)
        self.balloon.setH(250)
        self.balloon.setScale(ToonfestBalloonGlobals.BalloonScale)
        # So we can reparent toons to the balloon so they don't fall out
        self.cr.parentMgr.registerParent(ToontownGlobals.SPToonfestBalloon, self.balloon)
        # This code was taken from Flippy's stand.
        cs = CollisionSphere(0, 0, 0, 9)
        cs.setTangible(False)
        # Balloon collision NodePath (outside)
        self.collisionNP = self.balloon.find('**/basket_wall_collision')
        self.collisionNP.node().addSolid(cs)
        self.alec = NPCToons.createLocalNPC(99995)
        self.alec.setPos(0.7, 0.7, 0.4)
        self.alec.setH(150)
        self.alec.setScale((1/ToonfestBalloonGlobals.BalloonScale)) # We want a normal sized Slappy
        self.alec.initializeBodyCollisions('toon')
        self.alec.setPickable(0)
        self.alec.addActive()
        self.alec.startBlink()
        self.alec.loop('neutral')

        # Create balloon flight paths and Slappy speeches. It's important we do this AFTER we load everything
        # else as this requires both the balloon and Slappy.
        self.flightPaths = ToonfestBalloonGlobals.generateFlightPaths(self)
        self.toonFlightPaths = ToonfestBalloonGlobals.generateToonFlightPaths(self)
        self.speechSequence = ToonfestBalloonGlobals.generateSpeechSequence(self)

    def delete(self):
        # Clean up after our mess...
        self.demand('Off')
        self.ignore('enter' + self.collisionNP.node().getName())
        self.cr.parentMgr.unregisterParent(ToontownGlobals.SPToonfestBalloon)
        self.balloon.removeNode()
        if self.alec:
            self.alec.delete()
        DistributedObject.delete(self)

    def setState(self, state, timestamp, avId):
        if avId != self.avId:
            self.avId = avId
        self.demand(state, globalClockDelta.localElapsedTime(timestamp))

    def enterWaiting(self, offset):
        # Move alec back in the balloon (in case the waiting state was entered after the NotReady state)
        self.alec.reparentTo(self.balloon)
        self.alec.setPos(0.7, 0.7, 0.4)
        self.alec.setH(150)
        self.alec.setScale((1/ToonfestBalloonGlobals.BalloonScale)) # We want a normal sized Slappy
        # Wait for a collision...
        self.accept('enter' + self.collisionNP.node().getName(), self.__handleToonEnter)
        # Mini animation for the balloon hovering near the floor
        self.balloonIdle = Sequence(
            Wait(0.3),
            self.balloon.posInterval(3, (274, -263, 26)),
            Wait(0.3),
            self.balloon.posInterval(3, (274, -263, 25)),
        )
        self.balloonIdle.loop()
        self.balloonIdle.setT(offset)

    def enterNotReady(self, offset):
        # Render Alec outside the balloon
        self.alec.reparentTo(render)
        self.alec.setPos(255, -259, 22.366)
        self.alec.setH(80)
        self.alec.setScale(1) # Otherwise we get a teeny tiny alec

        # Wait for a collision...
        self.accept('enter' + self.collisionNP.node().getName(), self.__handleToonEnterNotReady)
        # Mini animation for the balloon hovering near the floor
        self.balloonIdle = Sequence(
            Wait(0.3),
            self.balloon.posInterval(3, (274, -263, 26)),
            Wait(0.3),
            self.balloon.posInterval(3, (274, -263, 25)),
        )
        self.balloonIdle.loop()
        self.balloonIdle.setT(offset)

    def enterElectionIdle(self, offset):
        # This isn't the elections, silly!
        self.notify.warning('Someone tried to put the ToonFest balloon in election idle state!')
        # Simulate NotReady
        self.alec.reparentTo(render)
        self.alec.setPos(255, -259, 22.366)
        self.alec.setH(80)
        self.alec.setScale(1) # Otherwise we get a teeny tiny alec

        # Wait for a collision...
        self.accept('enter' + self.collisionNP.node().getName(), self.__handleToonEnterNotReady)
        # Mini animation for the balloon hovering near the floor
        self.balloonIdle = Sequence(
            Wait(0.3),
            self.balloon.posInterval(3, (274, -263, 26)),
            Wait(0.3),
            self.balloon.posInterval(3, (274, -263, 25)),
        )
        self.balloonIdle.loop()
        self.balloonIdle.setT(offset)

    def enterElectionCrashing(self, offset):
        # This isn't the elections, silly!
        self.notify.warning('Someone tried to put the ToonFest balloon in election crashing state!')
        # Simulate NotReady
        self.alec.reparentTo(render)
        self.alec.setPos(255, -259, 22.366)
        self.alec.setH(80)
        self.alec.setScale(1) # Otherwise we get a teeny tiny alec

        # Wait for a collision...
        self.accept('enter' + self.collisionNP.node().getName(), self.__handleToonEnterNotReady)
        # Mini animation for the balloon hovering near the floor
        self.balloonIdle = Sequence(
            Wait(0.3),
            self.balloon.posInterval(3, (274, -263, 26)),
            Wait(0.3),
            self.balloon.posInterval(3, (274, -263, 25)),
        )
        self.balloonIdle.loop()
        self.balloonIdle.setT(offset)

    def __handleToonEnter(self, collEntry):
        if self.avId != 0:
            # Someone is already occupying the balloon
            return
        if self.state != 'Waiting':
            # The balloon isn't waiting for a toon
            return
        self.sendUpdate('requestEnter', [])

    def __handleToonEnterNotReady(self, collEntry):
        if self.alec.nametag.getChat() == '':
            # Alec's not saying anything, make him blab
            self.alec.setChatAbsolute("Hey there! Come back later for a ride to the top of the tower!", CFSpeech|CFTimeout)

    def exitWaiting(self):
        self.balloonIdle.finish()
        self.ignore('enter' + self.collisionNP.node().getName())

    def exitNotReady(self):
        self.balloonIdle.finish()

    def exitElectionIdle(self):
        self.balloonIdle.finish()

    def exitElectionCrashing(self):
        self.balloonIdle.finish()

    def enterOccupied(self, offset):
        if self.avId == base.localAvatar.doId:
            # This is us! We need to reparent to the balloon and position ourselves accordingly.
            base.localAvatar.disableAvatarControls()

            self.hopOnAnim = Sequence(Parallel(
                Func(base.localAvatar.b_setParent, ToontownGlobals.SPToonfestBalloon), # Required to put the toon in the basket
                Func(base.localAvatar.b_setAnimState, 'jump', 1.0)), 
                base.localAvatar.posInterval(0.6, (0, 0, 2)), 
                base.localAvatar.posInterval(0.4, (0, 0, 0.7)), 
                Func(base.localAvatar.enableAvatarControls),
                Parallel(Func(base.localAvatar.b_setParent, ToontownGlobals.SPRender))) # Unparent the toon and balloon

            self.hopOnAnim.start()
        try:
            self.speechSequence = self.speechSequence
            self.speechSequence.start()
            self.speechSequence.setT(offset)
        except Exception, e:
            self.notify.debug('Exception: %s' % e)

    def exitOccupied(self):
        try:
            self.hopOnAnim.finish()
        except Exception, e:
            self.notify.debug('Exception: %s' % e)

    def setFlightPath(self, flightPathIndex):
        self.flightPathIndex = flightPathIndex

    def enterStartRide(self, offset):
        # Try and get the flightPath from the AI
        try:
            self.rideSequence = self.flightPaths[self.flightPathIndex]
            self.rideSequence.start()
            self.rideSequence.setT(offset)
        except Exception, e:
            self.notify.debug('Exception: %s' % e)

        if self.avId == base.localAvatar.doId:
            try:
                self.toonRideSequence = self.toonFlightPaths[self.flightPathIndex]
                self.toonRideSequence.start()
                self.toonRideSequence.setT(offset)
            except Exception, e:
                self.notify.debug('Exception: %s' % e)            

    def exitStartRide(self):
        try:
            self.rideSequence.finish()
            self.speechSequence.finish()
        except Exception, e:
            self.notify.debug('Exception: %s' % e) 

    def enterRideOver(self, offset):
        if self.avId == base.localAvatar.doId:
            # We were on the ride! Better reparent to the render and get out of the balloon...
            base.localAvatar.disableAvatarControls()

            self.hopOffAnim = Sequence(
                Parallel(Func(base.localAvatar.b_setParent, ToontownGlobals.SPRender), Func(base.localAvatar.b_setAnimState, 'jump', 1.0)), 
                Wait(0.3),
                base.localAvatar.hprInterval(0.4, (-24, 0, 0)),
                base.localAvatar.posInterval(0.3, (197, -133, 209)), 
                base.localAvatar.posInterval(0.7, (209, -112, 204.936)), 
                Wait(0.3), 
                Func(base.localAvatar.b_setAnimState, 'neutral'),
                Wait(0.3), 
                Func(base.localAvatar.enableAvatarControls),
                Wait(5),
                self.balloon.posHprInterval(15.0, Point3(274, -263, 26), (0, 0, 0)),
                #to fix a bug
                self.balloon.posHprInterval(0.1, Point3(274, -263, 25), (0, 0, 0))
                )

            self.hopOffAnim.start()
