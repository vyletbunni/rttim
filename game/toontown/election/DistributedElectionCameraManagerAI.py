from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.election.DistributedElectionCameraAI import DistributedElectionCameraAI
from direct.distributed.ClockDelta import *
from otp.ai.MagicWordGlobal import *

class DistributedElectionCameraManagerAI(DistributedObjectAI):
    def __init__(self, air):
    
        DistributedObjectAI.__init__(self, air)
        self.air.cameraManager = self
        
        self.mainCamera = 0

    def spawnManager(self):
        cameras = []
        for cameraId in range(5):
            cam = DistributedElectionCameraAI(simbase.air)
            cam.setState('Waiting', globalClockDelta.getRealNetworkTime(), 31, -5, 8, -80, -5, 0)
            cam.generateWithRequired(2000)
            cam.b_setPosHpr(0, 0, 10, 0, 0, 0)
            cameras.append(cam.getDoId())
        self.setMainCamera(cameras[0])
        self.setCameraIds(cameras)
        self.generateWithRequired(2000)
 
    def getMainCamera(self):
        return self.mainCamera
        
    def d_setMainCamera(self, cam):
        self.sendUpdate('setMainCamera', [cam])
        
    def b_setMainCamera(self, cam):
        self.setMainCamera(cam)
        self.d_setMainCamera(cam)
        
    def setMainCamera(self, cam):
        self.mainCamera = cam
    
    def getCameraIds(self):
        return self.ids
    
    def setCameraIds(self, ids):
        self.ids = ids
        
    def d_setCameraIds(self, ids):
        self.sendUpdate('setCameraIds', [ids])
        
    def b_setCameraIds(self, ids):
        self.setCameraIds(ids)
        self.d_setCameraIds(ids)
