from direct.stdpy import threading

import DNALoader
from DNAStorage import DNAStorage
from DNASuitPoint import DNASuitPoint
from DNAGroup import DNAGroup
from DNAVisGroup import DNAVisGroup
from DNADoor import DNADoor

import xml.sax

elementRegistry = {}

def registerElement(element):
    elementRegistry[element.TAG] = element

class DNABulkLoader:
    def __init__(self, storage, files):
        self.dnaStorage = storage
        self.dnaFiles = files

    def loadDNAFiles(self):
        for file in self.dnaFiles:
            print 'Reading DNA file...', file
            loadDNABulk(self.dnaStorage, file)
        del self.dnaStorage
        del self.dnaFiles
        
class DNASaxHandler(xml.sax.ContentHandler):

    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.stack = []
        self.root = None
        return

    def startElement(self, tag, attrs):
        if self.stack:
            parent = self.stack[-1]
            parentTag = parent.TAG
        else:
            parent = None
            parentTag = None
        element = elementRegistry.get(tag)
        if not element:
            raise DNAParseError('Unknown element type: ' + tag)
        if parentTag not in element.PARENTS:
            raise DNAParseError('Cannot put %s below %s element' % (tag, parentTag))
        element = element(**attrs)
        self.stack.append(element)
        element.reparentTo(parent)
        if not self.root:
            self.root = element
        return

    def endElement(self, tag):
        self.stack.pop(-1)

    def characters(self, chars):
        if not self.stack:
            return
        self.stack[-1].handleText(chars)

class DNAError(Exception):
    pass


class DNAParseError(DNAError):
    pass

def loadDNABulk(dnaStorage, file):
    dnaLoader = DNALoader.DNALoader()
    if __debug__:
        file = '../resources/' + file
    else:
        file = '/' + file
    dnaLoader.loadDNAFile(dnaStorage, file)
    dnaLoader.destroy()

def loadDNAFile(dnaStorage, file):
    print 'Reading DNA file...', file
    dnaLoader = DNALoader.DNALoader()
    if __debug__:
        file = '../resources/' + file
    else:
        file = '/' + file
    node = dnaLoader.loadDNAFile(dnaStorage, file)
    dnaLoader.destroy()
    if node.node().getNumChildren() > 0:
        return node.node()
    return None

def loadDNAFileAI(dnaStorage, file):
    dnaLoader = DNALoader.DNALoader()
    if __debug__:
        file = '../resources/' + file
    else:
        file = '/' + file
    data = dnaLoader.loadDNAFileAI(dnaStorage, file)
    dnaLoader.destroy()
    return data

def loadDNAFileXML(stream):
    handler = DNASaxHandler()
    xml.sax.parse(stream, handler)
    return handler.root

