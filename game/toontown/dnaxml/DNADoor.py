from DNANode import DNANode
from DNAParser import *
import DNAUtil
from panda3d.core import *

class DNADoor(DNANode):
    TAG = 'door'
    PARENTS = ['landmark_building']

    def __init__(self, code):
        DNANode.__init__(self, 'door')
        self.code = code

    @staticmethod
    def setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color):
        doorNodePath.setPosHprScale(doorOrigin, (0, 0, 0), (0, 0, 0), (1, 1, 1))
        doorNodePath.setColor(color, 0)
        leftHole = doorNodePath.find('door_*_hole_left')
        leftHole.setName('doorFrameHoleLeft')
        rightHole = doorNodePath.find('door_*_hole_right')
        rightHole.setName('doorFrameHoleRight')
        leftDoor = doorNodePath.find('door_*_left')
        leftDoor.setName('leftDoor')
        rightDoor = doorNodePath.find('door_*_right')
        rightDoor.setName('rightDoor')
        doorFlat = doorNodePath.find('door_*_flat')
        leftHole.wrtReparentTo(doorFlat)
        leftHole.setDepthOffset(DNADoor.DEPTH_OFFSET)
        rightHole.wrtReparentTo(doorFlat)
        rightHole.setDepthOffset(DNADoor.DEPTH_OFFSET)
        rightDoor.wrtReparentTo(parentNode)
        rightDoor.setDepthOffset(DNADoor.DEPTH_OFFSET * 2)
        leftDoor.wrtReparentTo(parentNode)
        leftDoor.setDepthOffset(DNADoor.DEPTH_OFFSET * 2)
        rightDoor.setColor(color, 0)
        leftDoor.setColor(color, 0)
        leftHole.setColor((0, 0, 0, 1), 0)
        rightHole.setColor((0, 0, 0, 1), 0)
        doorTrigger = doorNodePath.find('door_*_trigger')
        doorTrigger.setScale(2, 2, 2)
        doorTrigger.wrtReparentTo(parentNode, 0)
        doorTrigger.setName('door_trigger_%s' % block)

    def _makeNode(self, storage, parent):
        frontNode = parent.find('**/*building*_front')
        if frontNode.isEmpty():
            frontNode = parent.find('**/*_front')
        if not frontNode.getNode(0).isGeomNode():
            frontNode = frontNode.find('**/+GeomNode')
        node = storage.findNode(self.code)
        if node is None:
            pass
        doorNode = node.copyTo(frontNode, 0)
        doorNode.setDepthOffset(self.DEPTH_OFFSET)
        origin = parent.find('**/*door_origin')
        origin.node().setPreserveTransform(ModelNode.PTNet)
        self.setupDoor(doorNode, parent, origin, storage, DNAUtil.getBlockFromName(parent.getName()), self.getColor())
        return doorNode


registerElement(DNADoor)
