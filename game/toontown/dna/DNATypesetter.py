from panda3d.core import *
import math

class DNATypesetter:

    def __init__(self, baseline, dnaStorage):
        self.baseline = baseline
        self.dnaStorage = dnaStorage

    def generate(self, texts, old=0):
        root = NodePath('typesetter')
        if old == 0:
            sx, _, sz = self.baseline.getScale()
            root.setScale(1 / sx, 1, 1 / sz)
            width = self.baseline.width
            height = self.baseline.height
            stumble = self.baseline.stumble
            stomp = self.baseline.stomp
            kern = self.baseline.kern
            wiggle = self.baseline.wiggle
            indent = self.baseline.indent
        x = 0.0
        for i, text in enumerate(texts):
            tn = TextNode('text')
            tn.setText(text)
            if old == 0:
                font = self.dnaStorage.findFont(self.baseline.code)
            else:
                tn.setTextColor(self.baseline.getColor())
                font = self.dnaStorage.findFont(self.baseline.code)
            if font is None:
                font = TextProperties.getDefaultFont()
            tn.setFont(font)
            if i == 0 and 'b' in self.baseline.flags:
                tn.setTextScale(1.5)
            np = root.attachNewNode(tn)
            if old == 0:
                np.setScale(sx, 1, sz)
                np.setDepthWrite(0)
                if i & 1:
                    np.setPos(x + stumble, 0, stomp)
                    np.setR(-wiggle)
                else:
                    np.setPos(x - stumble, 0, -stomp)
                    np.setR(wiggle)
                x += tn.getWidth() * sx + kern
            else:
                np.setScale(self.baseline.scale)
                np.setDepthWrite(0)
                if i & 1:
                    np.setPos(x+self.baseline.stumble, 0, self.baseline.stomp)
                    np.setR(-self.baseline.wiggle)
                else:
                    np.setPos(x-self.baseline.stumble, 0, -self.baseline.stomp)
                    np.setR(self.baseline.wiggle)
                x += tn.getWidth()*np.getSx() + self.baseline.kern

        for child in root.getChildren():
            child.setX(child.getX() - x / 2)
            
        if old == 0:
            if width != 0.0 and height != 0.0:
                ellipse = DNAEllipseFormatter(width, height, indent)
                ellipse.process(root)
        else:
            if self.baseline.width != 0.0 and self.baseline.height != 0.0:
                ellipse = DNAEllipseFormatter(self.baseline)
                ellipse.process(root)
        for np in root.findAllMatches('**/+TextNode'):
            tn = np.node().generate()
            np2 = np.getParent().attachNewNode(tn)
            np2.setTransform(np.getTransform())
            np.removeNode()

        root.flattenStrong()
        if root.getNumChildren():
            return root.getChild(0)
        else:
            return
            return


class DNAEllipseFormatter:

    def __init__(self, width, height, indent):
        self.a = width / 2.0
        self.b = height / 2.0
        self.indent = indent

    def arc(self, x):
        return x / self.b

    def process(self, np):
        for node in np.getChildren():
            theta = self.arc(node.getX())
            deviation = node.getY()
            theta += self.indent * math.pi / 180
            x, y = math.sin(theta) * self.a, (math.cos(theta) - 1) * self.b
            radius = math.sqrt(x * x + y * y)
            if radius > 0.0:
                x *= (radius + deviation) / radius
                y *= (radius + deviation) / radius
            node.setPos(x, 0, y)
            node.setR(node, theta * 180 / math.pi)
