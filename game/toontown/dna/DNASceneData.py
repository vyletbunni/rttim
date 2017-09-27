from DNAParser import *
import DNAStoreSuitPoint
try:
    import ctypes
except ImportError:

    class uint16array(object):

        def __init__(self, size, initial = None):
            if initial is None:
                self.__array = bytearray(size * 2)
            else:
                self.__array = bytearray((initial for x in xrange(size * 2)))
            return

        def __getitem__(self, index):
            hi, lo = self.__array[index * 2:index * 2 + 2]
            return hi * 256 + lo

        def __setitem__(self, index, value):
            self.__array[index * 2:index * 2 + 2] = divmod(value, 256)


else:

    def uint16array(size, initial = None):
        array = (ctypes.c_uint16 * size)()
        if initial is not None:
            ctypes.memset(array, initial, ctypes.sizeof(array))
        return array


class DNASuitGraph(object):

    def __init__(self, points, edges):
        self.points = points
        self.edges = edges
        self._pointId2point = {}
        self._point2outboundEdges = {}
        self._point2inboundEdges = {}
        self._table = uint16array(4 * len(points) * len(points), 255)
        if points:
            highestId = max((point.id for point in points))
            self._id2index = uint16array(highestId + 1)
        for i, point in enumerate(points):
            self._pointId2point[point.id] = point
            self._id2index[point.id] = i

        for edge in edges:
            try:
                a = self._pointId2point[edge.a]
                b = self._pointId2point[edge.b]
            except KeyError:
                raise DNAError('Edge connects a nonexistent point!')

            self._point2outboundEdges.setdefault(a, []).append(edge)
            self._point2inboundEdges.setdefault(b, []).append(edge)

        visited = bytearray(len(points))
        for i, point in enumerate(points):
            for neighbor in self.getOriginPoints(point):
                self.addLink(neighbor, point, 1, point, False, visited)

    def addLink(self, point, neighbor, distance, destination, unbounded, visited):
        pointIndex = self._id2index[point.id]
        neighborIndex = self._id2index[neighbor.id]
        destinationIndex = self._id2index[destination.id]
        if visited[pointIndex]:
            unbounded = True
        visited[pointIndex] += 1
        entry = pointIndex * len(self.points) + destinationIndex
        existingDistance = self._table[entry * 4 + 3] if unbounded else self._table[entry * 4 + 1]
        if distance < existingDistance:
            if not unbounded:
                self._table[entry * 4 + 0] = neighborIndex
                self._table[entry * 4 + 1] = distance
            else:
                self._table[entry * 4 + 2] = neighborIndex
                self._table[entry * 4 + 3] = distance
            traversable = point.type in (DNAStoreSuitPoint.STREETPOINT, DNAStoreSuitPoint.COGHQINPOINT, DNAStoreSuitPoint.COGHQOUTPOINT)
            if traversable:
                for neighbor in self.getOriginPoints(point):
                    self.addLink(neighbor, point, distance + 1, destination, unbounded, visited)

        visited[pointIndex] -= 1

    def getEdgeEndpoints(self, edge):
        return (self._pointId2point[edge.a], self._pointId2point[edge.b])

    def getEdgesFrom(self, point):
        return self._point2outboundEdges.get(point, [])

    def getEdgesTo(self, point):
        return self._point2inboundEdges.get(point, [])

    def getPointFromIndex(self, index):
        return self._pointId2point[index]

    def getEdgeZone(self, edge):
        return edge.getVisGroup().getZone()

    def getPointZone(self, point):
        edges = self.getEdgesTo(point)
        return self.getEdgeZone(edges[0])

    def getSuitPath(self, startPoint, endPoint, minPathLen, maxPathLen):
        start = self._id2index[startPoint.id]
        end = self._id2index[endPoint.id]
        at = start
        path = [startPoint]
        while at != end or minPathLen > 0:
            entry = at * len(self.points) + end
            if minPathLen <= self._table[entry * 4 + 1] <= maxPathLen:
                at = self._table[entry * 4 + 0]
            elif self._table[entry * 4 + 3] <= maxPathLen:
                at = self._table[entry * 4 + 2]
            else:
                return None
            path.append(self.points[at])
            minPathLen -= 1
            maxPathLen -= 1

        return path

    def getAdjacentPoints(self, point):
        return [ self.getPointFromIndex(edge.b) for edge in self.getEdgesFrom(point) ]

    def getOriginPoints(self, point):
        return [ self.getPointFromIndex(edge.a) for edge in self.getEdgesTo(point) ]

    def getConnectingEdge(self, pointA, pointB):
        for edge in self.getEdgesFrom(pointA) + self.getEdgesTo(pointA):
            a = self.getPointFromIndex(edge.a)
            b = self.getPointFromIndex(edge.b)
            if a == pointA and b == pointB or a == pointB and b == pointA:
                return edge

        return None

    def getSuitEdgeTravelTime(self, p1, p2, speed):
        pos1 = p1.getPos()
        pos2 = p1.getPos()
        return (pos1 - pos2).length() / speed


class DNABlock:
    index = None
    title = None
    buildingType = None
    zone = None
    node = None

    def __init__(self, index):
        self.index = index


class DNASceneData:

    def __init__(self):
        self.visgroups = []
        self.suitPoints = []
        self.suitEdges = []
        self.suitGraph = None
        self._blocks = {}
        return

    def update(self):
        self.suitGraph = DNASuitGraph(self.suitPoints, self.suitEdges)

    def getBlock(self, block):
        if block not in self._blocks:
            self._blocks[block] = DNABlock(block)
        return self._blocks[block]

    def getBlocks(self):
        return self._blocks.items()
