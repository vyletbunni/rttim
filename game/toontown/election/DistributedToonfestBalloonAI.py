from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM
from direct.task import Task
import ToonfestBalloonGlobals
from random import randint
from otp.ai.MagicWordGlobal import *

class DistributedToonfestBalloonAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedToonfestBalloonAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'ToonfestBalloonFSM')
        self.avId = 0
        self.stateTime = globalClockDelta.getRealNetworkTime()
        self.flightPathIndex = 0
        
    def b_setState(self, state, avId=0):
        if avId != self.avId:
            self.avId = avId
        self.setState(state)
        self.d_setState(state)
    
    def setState(self, state):
        self.demand(state)
        
    def d_setState(self, state):
        self.stateTime = globalClockDelta.getRealNetworkTime()
        self.sendUpdate('setState', [state, self.stateTime, self.avId])

    def getState(self):
        return (self.state, self.stateTime, self.avId)

    def enterOff(self):
        self.requestDelete()

    def enterWaiting(self):
        # We don't need to do anything on the AI...
        pass

    def enterNotReady(self):
        # We don't need to do anything on the AI...
        pass

    def enterElectionIdle(self):
        pass
        
    def enterElectionCrashing(self):
        pass

    def requestEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if self.state != 'Waiting':
            self.notify.warning('Received unexpected requestEnter from avId %d!' % avId)
            return
        if self.avId == avId:
            return # Duplicate request?
        self.b_setState('Occupied', avId)

    def enterOccupied(self):
        # Generate a flight path while we wait for the toon to hop in
        self.b_setFlightPath(randint(0, ToonfestBalloonGlobals.NumBalloonPaths-1))
        # After 3.5 seconds, we take off!
        taskMgr.doMethodLater(3.5, self.b_setState, 'balloon-startride-task', extraArgs=['StartRide', self.avId])
        
    def b_setFlightPath(self, flightPathIndex):
        self.setFlightPath(flightPathIndex)
        self.d_setFlightPath(flightPathIndex)
        
    def setFlightPath(self, flightPathIndex):
        self.flightPathIndex = flightPathIndex
        
    def d_setFlightPath(self, flightPathIndex):
        self.sendUpdate('setFlightPath', [flightPathIndex])
        
    def getFlightPath(self):
        return self.flightPathIndex
        
    def enterStartRide(self):
        # After 105 seconds, the ride is over!
        taskMgr.doMethodLater(85, self.b_setState, 'balloon-riding-task', extraArgs=['RideOver', self.avId])
        
    def enterRideOver(self):
        # So that the client can handle events without instantly switching to the "Waiting" state...
        taskMgr.doMethodLater(30, self.b_setState, 'balloon-cleaningup-task', extraArgs=['Waiting'])
        
@magicWord(category=CATEGORY_MODERATOR, types=[str])
def balloon(state):
    event = simbase.air.doFind('ToonfestBalloon')
    if event is None:
        return "There is no ToonFest Balloon here!"

    if not hasattr(event, 'enter'+state):
        return 'Invalid state'

    event.b_setState(state)

    return 'Balloon now in %r state' % state