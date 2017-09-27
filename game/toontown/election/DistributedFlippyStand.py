from pandac.PandaModules import *
from otp.nametag.NametagConstants import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM
from direct.actor import Actor
from direct.task import Task
from toontown.toon import NPCToons
from toontown.suit import DistributedSuitBase, SuitDNA
from toontown.toonbase import ToontownGlobals
from toontown.battle import BattleProps
from otp.margins.WhisperPopup import *
import ElectionGlobals
from direct.directnotify import DirectNotifyGlobal
from random import choice

# Interactive Flippy
from otp.speedchat import SpeedChatGlobals

class DistributedFlippyStand(DistributedObject, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFlippyStand")

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'FlippyStandFSM')
        #Campaign stands
        self.flippyStand = Actor.Actor('phase_4/models/events/election_flippyStand-mod', {'idle': 'phase_4/models/events/election_flippyStand-idle'})
        #self.standNode = base.render.attachNewNode('standOrigin')
        #self.standNode.setPos(344, -201, 15.909)
        self.flippyStand.reparentTo(render)
        self.flippyStand.setPosHprScale(172, -254, 4.85, -55, 1, -8, 0.55, 0.55, 0.55) 
        self.flippyStand.exposeJoint(None,"modelRoot", "LInnerShoulder")
        flippyTable = self.flippyStand.find('**/LInnerShoulder')
        self.flippyStand.exposeJoint(None,"modelRoot", "Box_Joint")
        wheelbarrowJoint = self.flippyStand.find('**/Box_Joint').attachNewNode('Pie_Joint')
        wheelbarrow = self.flippyStand.find('**/Box')
        wheelbarrow.setPosHprScale(-2.39, 0.00, 1.77, 0.00, 0.00, 6.00, 1.14, 1.54, 0.93)
        # Let's give FlippyStand a bunch of pies.
        # Pies on/around the stand.
        pie = loader.loadModel('phase_3.5/models/props/tart')
        pieS = pie.copyTo(flippyTable)
        pieS.setPosHprScale(-2.61, -0.37, -1.99, 355.60, 90.00, 4.09, 1.6, 1.6, 1.6)
        # Pies in the wheelbarrow.
        for pieSettings in ElectionGlobals.FlippyWheelbarrowPies:
            pieModel = pie.copyTo(wheelbarrowJoint)
            pieModel.setPosHprScale(*pieSettings)
        wheelbarrowJoint.setPosHprScale(3.94, 0.00, 1.06, 270.00, 344.74, 0.00, 1.43, 1.12, 1.0)
        self.restockSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_pies_restock.ogg')
        cs = CollisionBox(Point3(7, 0, 0), 12, 5, 18)
        self.pieCollision = self.flippyStand.attachNewNode(CollisionNode('wheelbarrow_collision'))
        self.pieCollision.node().addSolid(cs)
        self.accept('enter' + self.pieCollision.node().getName(), self.handleWheelbarrowCollisionSphereEnter)
        self.flippyStand.loop('idle')
        self.flippyStand.setBlend(frameBlend=True)

    def delete(self):
        self.demand('Off')
        self.ignore('enter' + self.pieCollision.node().getName())
        self.flippyStand.removeNode()
        DistributedObject.delete(self)

    def handleWheelbarrowCollisionSphereEnter(self, collEntry):
        if base.localAvatar.numPies >= 0 and base.localAvatar.numPies < 20:
            # We need to give them more pies! Send a request to the server.
            self.sendUpdate('wheelbarrowAvatarEnter', [])
            self.restockSfx.play()
