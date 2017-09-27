from pandac.PandaModules import *
from otp.nametag.NametagConstants import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from toontown.toon import NPCToons
from toontown.toonbase import ToontownGlobals
from direct.task import Task

class DistributedDuckTank(DistributedObject):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

        # I'm debating whether to make this class depend on FSM

        # Let's create the ducktank
        self.ducktank = loader.loadModel('phase_6/models/events/ttr_m_tf_ducktank')
        self.ducktank.reparentTo(base.render)
        self.ducktank.setPos(170.29, -332.146, 8)
        self.ducktank.setH(180)

        self.target = self.ducktank.find('**/target')

        # A Different Toon XD
        self.Slappy = NPCToons.createLocalNPC(99996)
        self.Slappy.reparentTo(self.ducktank.find('**/tank_seat'))
        self.Slappy.setH(180)
        self.Slappy.setPos(0, -1.80, -0.40)
        self.Slappy.loop('periscope')

        # This is to ensure no Z-Fighting takes place 
        self.Slappy.getGeomNode().setDepthWrite(1)
        self.Slappy.getGeomNode().setDepthTest(1)

        # This is so that pies can hit the target
        self.target.setTag('pieCode', str(ToontownGlobals.PieCodeNotBossCog))
        self.accept('pieSplat', self.__hitTarget)

    def delete(self):
        self.ducktank.removeNode()
        self.ignore('pieSplat')
        DistributedObject.delete(self)
        if self.Slappy:
            self.Slappy.stopBlink()
            self.Slappy.removeActive()
            self.Slappy.cleanup()
            self.Slappy.removeNode()

    def __hitTarget(self, toon, pieCode):
        if pieCode == ToontownGlobals.PieCodeNotBossCog:
            Sequence(self.target.hprInterval(.4, (0, -43, 0)),
                self.target.hprInterval(.9, (0, 20, 0)), self.target.hprInterval(1.2, (0, 0, 0)),
                Wait(1),
                Func(self.beginTankSeq)
            ).start()

    def beginTankSeq(self):
        tankSeat = self.ducktank.find("**/tank_pole")
        x, y, z = tankSeat.getPos()

        Sequence2 = Sequence(tankSeat.posInterval(1.5, (x, y, z + 2)),
            tankSeat.posInterval(.4, (x, y, z - 8)), Wait(3),
            tankSeat.posInterval(2, (-15.7391004562, 1.21719002724, 0)))
        Sequence2.start()

