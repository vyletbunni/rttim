from DNAElement import DNAElement
from DNAParser import *

class DNAStorageElement(DNAElement):

    def __init__(self):
        DNAElement.__init__(self)
        self.scope = None
        return

    def getScope(self):
        if self.scope is not None:
            return self.scope
        elif self.parent is not None:
            return self.parent
        else:
            raise DNAParseError('No scope defined')
            return

    def store(self, storage):
        self._store(storage)
        for child in self.children:
            child.store(storage)

    def _store(self, storage):
        pass
