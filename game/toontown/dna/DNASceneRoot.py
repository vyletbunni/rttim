from DNASceneElement import DNASceneElement
from DNASceneData import DNASceneData
from DNAParser import *
from panda3d.core import *

class DNASceneRoot(DNASceneElement):
    TAG = 'scene'
    PARENTS = [None]

    def __init__(self, zone = None):
        DNASceneElement.__init__(self)
        if zone is not None:
            self.zone = int(zone)
        else:
            self.zone = None
        return

    def generate(self, storage):
        scene = NodePath('scene')
        for child in self.children:
            child._generate(storage, scene)

        return scene.node()

    def generateData(self):
        data = DNASceneData()
        for child in self.children:
            child._getData(data)

        data.update()
        return data


registerElement(DNASceneRoot)
