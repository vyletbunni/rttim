from direct.task import Task
import math
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence
from pandac.PandaModules import Point3
from pandac.PandaModules import *
  
import direct.directbase.DirectStart
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
 
Robo = Actor('phase_3.5/models/char/suitA-mod.bam', {'Anim' : 'phase_4/models/char/suitA-neutral.bam'})
Robo.reparentTo(render)
Robo.loop('Anim')
TorsoTex = loader.loadTexture('phase_3.5/maps/cm_blazer.jpg')
ArmTex = loader.loadTexture('phase_3.5/maps/cm_sleeve.jpg')
LegTex = loader.loadTexture('phase_3.5/maps/cm_leg.jpg')
Robo.find('**/torso').setTexture(TorsoTex, 1)
Robo.find('*/arms').setTexture(ArmTex, 1) 
Robo.find('**/legs').setTexture(LegTex, 1)
Robo.find('**/hands').setColor(0.25, 0.25, 0.25)
Head = Actor('phase_3/models/char/tt_a_chr_dgm_skirt_head_1000.bam', {'anim':'phase_3/models/char/tt_a_chr_dgm_skirt_head_neutral.bam'})
Head.setPlayRate(1.05, 'anim')
Head.loop('anim')
Head.reparentTo(Robo.find('**/joint_head'))
Head.setY(-0.32)
Head.setZ(0.19)
Head.setColor(0, 0.498, 0,054)
Head.find('**/ears').setColor(0)
Head.find('**/muzzle').hide()
Head.find('**/nose').setColor(1, 1, 1)
Head.find('**/eyes').setColor(0.99, 0.99, 0.99)
EyeTex = loader.loadTexture('phase_3/maps/eyesAngry.jpg', 'phase_3/maps/eyesAngry_a.rgb')
Head.find('**/eyes').setTexture(EyeTex, 1)
Head.find('**/eyes').reparentTo(Head)
Muzzle = loader.loadModel('phase_3/models/char/dogMM_Skirt-headMuzzles-500.bam').find('**/muzzle-short-angry')
Muzzle.reparentTo(render)
Muzzle.reparentTo(Head)
Muzzle.setColor(1, 1, 1)
#eye
eye = loader.loadModel('phase_9/models/cogHQ/PaintMixer.bam')
eye.reparentTo(Head)
eye.setScale(0.03)
eye.setPos(-0.18, 0.48, 0.41)
eye.setP(272.64)
eye.setColor(1, 1, 1)
#gear 
from direct.interval.IntervalGlobal import *
gear = loader.loadModel('phase_9/models/char/gearProp.bam')
gear.reparentTo(render)
gear.reparentTo(Head)
gearInt3 = gear.hprInterval(9.0, Vec3(360, 95.36, 0))
gearInt3.loop()
gear.setColor(0.99, 0.99, 0.99)
gear.setScale(0.06)
gear.setX(-0.13)
gear.setY(0.06)
gear.setZ(0.57)
gear.setH(90)
gear.setR(270)
Rotate = gear.hprInterval(1, Vec3(90, -360, 270)).loop()
#cigar
cigar = loader.loadModel('phase_5/models/props/cigar.bam')
cigar.reparentTo(render)
cigar.reparentTo(Head)
cigar.setColor(0.99, 0.99, 0.99)
cigar.setX(0.81)
cigar.setY(1.00)
cigar.setZ(-0.16)
cigar.setH(315.00)
cigar.setScale(7.44)
#smoke
from direct.particles.ParticleEffect import ParticleEffect
base.enableParticles()
Smoke = ParticleEffect()
Smoke.loadConfig('phase_2/models/misc/smoke.ptf')
Smoke.start(parent = cigar, renderParent = render)
Smoke.setScale(0.1)
Smoke.setPos(0.00, 0.00, 0.03)

camera.hide()
base.oobe()
base.run()


