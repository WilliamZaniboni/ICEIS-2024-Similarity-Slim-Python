import models
import includeSlimTree
import bisect
from queue import PriorityQueue


class PriorityQueueData:
    queue: PriorityQueue

    def add(self, distance: float, pageID: str, radius: float):
        elem = PriorityQueueElement()
        elem.pageID = pageID
        elem.radius = radius
       
        self.queue.put((distance, elem))


class PriorityQueueElement:
    pageID: str
    radius: float

    def __gt__(self, other):
        return self.radius > other.radius

    def __lt__(self, other):
        return self.radius < other.radius


class ResultElement:
    similarity: float
    element: models.SlimObject

    def __lt__(self, other):
        return self.similarity < other.similarity


class QueryResult:
    entries: list[ResultElement] = []

    def addPair(self, element: models.SlimObject, distance: float):
        resultElement = ResultElement()
        resultElement.similarity = distance
        resultElement.element = element

        self.addEntry(resultElement)

    def addEntry(self, resultElement: ResultElement):
        bisect.insort(self.entries, resultElement)


class SimilarityRetrievalOperators():


    def KnnQueryDummy(self, includeSlim: includeSlimTree.IncludeSlim, collection:  models.SlimObject(),  sample: models.SlimObject, k: int):

        result:  QueryResult
        result = QueryResult()
        result.entries = []

        includeSlim.readCount = 0
        includeSlim.writeCount = 0
        includeSlim.distancesCount = 0

        for document in collection:

            distance = includeSlim.getDistance(document, sample)

            result.addPair(document, distance)
            if len(result.entries) > k:
                result.entries.pop()

        return result


    def RangeQuery(self, includeSlim: includeSlimTree.IncludeSlim, sample: models.SlimObject, rangeValue: float):

        includeSlim.readCount = 0
        includeSlim.writeCount = 0
        includeSlim.distancesCount = 0

        result:  QueryResult
        result = QueryResult()
        result.entries = []

        currNode: models.Node

        numberOfEntries: int
        distance: float

        if includeSlim.root != "NULL":
            currNode = includeSlim.readNode(includeSlim.root)

            if currNode.type == "INDEX":
                numberOfEntries = len(currNode.entries)

                for i in range(numberOfEntries):
                    distance = includeSlim.getDistance(
                        currNode.entries[i], sample)

                    if distance <= (rangeValue + currNode.subtrees[i].radius):

                        self.RangeQueryRecursive(
                            includeSlim, currNode.subtrees[i].pageID, result, sample, rangeValue, distance)

            else:
                numberOfEntries = len(currNode.entries)

                for i in range(numberOfEntries):
                    distance = includeSlim.getDistance(
                        numberOfEntries[i], sample)
                    if distance <= rangeValue:
                        result.addPair(currNode.entries[i], distance)

        return result

    def RangeQueryRecursive(self, includeSlim: includeSlimTree.IncludeSlim, pageID: str, result:  QueryResult, sample: models.SlimObject, rangeValue: float, distanceRepres: float):

        currNode: models.Node

        numberOfEntries: int
        distance: float

        if pageID != "NULL":
            currNode = includeSlim.readNode(pageID)

            if currNode.type == "INDEX":
                numberOfEntries = len(currNode.entries)
                for i in range(numberOfEntries):

                    if abs(distanceRepres - currNode.subtrees[i].distance) <= (rangeValue + currNode.subtrees[i].radius):
                        distance = includeSlim.getDistance(
                            currNode.entries[i], sample)

                        if distance <= (rangeValue + currNode.subtrees[i].radius):

                            self.RangeQueryRecursive(
                                includeSlim, currNode.subtrees[i].pageID, result, sample, rangeValue, distance)

            else:

                numberOfEntries = len(currNode.entries)
                for i in range(numberOfEntries):
                    if abs(distanceRepres - currNode.subtrees[i].distance) <= rangeValue:
                        distance = includeSlim.getDistance(
                            currNode.entries[i], sample)
                        if distance <= rangeValue:
                            result.addPair(currNode.entries[i], distance)

    def KnnQuery(self, includeSlim: includeSlimTree.IncludeSlim,  sample: models.SlimObject, k: int):

        includeSlim.readCount = 0
        includeSlim.writeCount = 0
        includeSlim.distancesCount = 0

        result:  QueryResult
        result = QueryResult()
        result.entries = []

        if includeSlim.root != "NULL":
            self.KnnQueryLoop(includeSlim, result, sample, 10000000000000, k)

        return result

    def KnnQueryLoop(self, includeSlim: includeSlimTree.IncludeSlim, result:  QueryResult, sample: models.SlimObject, rangeK: float, k: int):

        queue = PriorityQueueData()
        queue.queue = PriorityQueue()

        currNode: models.Node
        numberOfEntries: int
        distance: float
        distanceRepres: float
        distanceRepres = 0

        pqCurrValuePageID: str
        pqCurrValueRadius: float

        pqTmpValuePageID: str
        pqTmpValueRadius: float

        pqCurrValuePageID = includeSlim.root
        pqCurrValueRadius = 0

        while pqCurrValuePageID != "NULL":
            currNode = includeSlim.readNode(pqCurrValuePageID)

            if currNode.type == "INDEX":
                numberOfEntries = len(currNode.entries)

                for i in range(numberOfEntries):
                    if abs(distanceRepres - currNode.subtrees[i].distance) <= (rangeK + currNode.subtrees[i].radius):
                        distance = includeSlim.getDistance(
                            currNode.entries[i], sample)
                        if distance <= (rangeK + currNode.subtrees[i].radius):
                            pqTmpValuePageID = currNode.subtrees[i].pageID
                            pqTmpValueRadius = currNode.subtrees[i].radius

                            queue.add(distance, pqTmpValuePageID,
                                      pqTmpValueRadius)
            else:
                numberOfEntries = len(currNode.entries)
                for i in range(numberOfEntries):
                    if (abs(distanceRepres - currNode.subtrees[i].distance) <= rangeK):
                        distance = distance = includeSlim.getDistance(
                            currNode.entries[i], sample)
                        if distance <= rangeK:
                            result.addPair(currNode.entries[i], distance)
                            if len(result.entries) > k:
                                result.entries.pop()
                                rangeK = result.entries[k-1].similarity

            stop = False

            while True:
                if queue.queue.empty() == False:
                    elem = queue.queue.get()
                    distance = elem[0]
                    pqCurrValuePageID = elem[1].pageID
                    pqCurrValueRadius = elem[1].radius

                    if distance <= (rangeK + pqCurrValueRadius):
                        distanceRepres = distance
                        stop = True

                else:
                    pqCurrValuePageID = "NULL"
                    stop = True

                if stop == True:
                    break
