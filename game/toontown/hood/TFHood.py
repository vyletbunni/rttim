from ToonHood import ToonHood
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.toonbase import ToontownGlobals
from toontown.safezone.TFSafeZoneLoader import TFSafeZoneLoader
from toontown.town.TTTownLoader import TTTownLoader # Temporary
import SkyUtil

class TFHood(ToonHood):
    notify = directNotify.newCategory('TFHood')
    
    ID = ToontownGlobals.ToonFest
    TOWNLOADER_CLASS = TTTownLoader # Temporary
    SAFEZONELOADER_CLASS = TFSafeZoneLoader
    STORAGE_DNA = 'phase_6/dna/storage_TF.dna'
    SKY_FILE = 'phase_3.5/models/props/TT_sky'
    TITLE_COLOR = (1.0, 0.5, 0.4, 1.0)

    #def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
    #    ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        
    def load(self):
        ToonHood.load(self)
        self.parentFSM.getStateNamed('TFHood').addChild(self.fsm)

    def enter(self, *args):
        ToonHood.enter(self, *args)
        base.camLens.setNearFar(ToontownGlobals.SpeedwayCameraNear, ToontownGlobals.SpeedwayCameraFar)

    def exit(self):
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)
        ToonHood.exit(self)

    def unload(self):
        self.parentFSM.getStateNamed('TFHood').removeChild(self.fsm)
        ToonHood.unload(self)

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)

    def startSky(self):
        SkyUtil.startCloudSky(self)
