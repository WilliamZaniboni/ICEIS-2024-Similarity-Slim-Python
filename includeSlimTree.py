import models
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from math import radians, cos, sin, asin, sqrt


class IncludeSlim():
    root: str
    maxOccupation: int
    height: int
    objectCount: int
    nodeCount: int
    nodes: dict
    writeCount: int
    readCount: int
    distancesCount: int

    def setRoot(self, value):
        self.root = value

    def toMap(self):
        return {"root": self.root, "maxOccupation": self.maxOccupation, "height": self.height, "objectCount": self.objectCount, "nodeCount": self.nodeCount, "writeCount": self.writeCount, "nodeCount": self.nodeCount, "readCount": self.readCount,  "distancesCount": self.distancesCount}

    def distributeLeaf(self, node0: models.Node, rep0: models.SlimObject, node1: models.Node, rep1: models.SlimObject, logicNode: models.Node):

        matrix = []

        for row in range(len(logicNode.entries)):
            a = []
            for column in range(len(logicNode.entries)):
                a.append(0)
            matrix.append(a)

        for i in range(0, len(logicNode.entries)):
            matrix[i][i] = 0
            for j in range(i):
                matrix[i][j] = self.getDistance(
                    logicNode.entries[i], logicNode.entries[j])
                matrix[j][i] = matrix[i][j]

        X = csr_matrix(matrix)

        Tcsr = minimum_spanning_tree(X).toarray().astype(float)

        maxEdgeValue = -1

        limit1 = 0
        limit2 = 0

        for row in range(len(logicNode.entries)):
            for column in range(len(logicNode.entries)):
                Tcsr[column][row] = Tcsr[row][column]
                if Tcsr[row][column] >= maxEdgeValue:
                    maxEdgeValue = Tcsr[row][column]
                    limit1 = row
                    limit2 = column

        Tcsr[limit1][limit2] = 0
        Tcsr[limit2][limit1] = 0

        cluster1 = []
        cluster2 = []

        cluster1.append(limit1)

        checkList = []

        checkList.append(limit1)

        while len(checkList) != 0:

            value = checkList.pop()

            for i in range(len(logicNode.entries)):
                if Tcsr[i][value] != 0:
                    if cluster1.count(i) == 0:
                        checkList.append(i)
                        cluster1.append(i)

        for i in range(len(logicNode.entries)):
            if cluster1.count(i) == 0:
                cluster2.append(i)

        maximumDistance = []

        for i in range(len(logicNode.entries)):
            if cluster1.count(i) != 0:
                # i is on cluster1
                maxValue = 0
                for j in cluster1:
                    if matrix[i][j] > maxValue:
                        maxValue = matrix[i][j]
                maximumDistance.append(maxValue)
            else:
                # i is on cluster2
                maxValue = 0
                for j in cluster2:
                    if matrix[i][j] > maxValue:
                        maxValue = matrix[i][j]
                maximumDistance.append(maxValue)

        rep1Index = 0
        rep2Index = 0

        maxValue = 1000000000000000

        for i in cluster1:
            if maximumDistance[i] < maxValue:
                maxValue = maximumDistance[i]
                rep1Index = i

        maxValue = 1000000000000000

        for i in cluster2:
            if maximumDistance[i] < maxValue:
                maxValue = maximumDistance[i]
                rep2Index = i

        node0.entries.append(logicNode.entries[rep1Index])
        node0.occupation = 1
        subTree0 = models.SubTreeInfos()
        subTree0.distance = 0
        node0.subtrees.append(subTree0)

        node1.entries.append(logicNode.entries[rep2Index])
        node1.occupation = 1
        subTree1 = models.SubTreeInfos()
        subTree1.distance = 0
        node1.subtrees.append(subTree1)

        for i in cluster1:
            if i != rep1Index:
                node0.entries.append(logicNode.entries[i])
                node0.occupation += 1
                subTree = models.SubTreeInfos()
                subTree.distance = matrix[rep1Index][i]
                node0.subtrees.append(subTree)

        for i in cluster2:
            if i != rep2Index:
                node1.entries.append(logicNode.entries[i])
                node1.occupation += 1
                subTree = models.SubTreeInfos()
                subTree.distance = matrix[rep2Index][i]
                node1.subtrees.append(subTree)

        rep0.oid = logicNode.entries[rep1Index].oid
        rep0.includeAttribute = logicNode.entries[rep1Index].includeAttribute
        rep0.complexAttribute = logicNode.entries[rep1Index].complexAttribute

        rep1.oid = logicNode.entries[rep2Index].oid
        rep1.includeAttribute = logicNode.entries[rep2Index].includeAttribute
        rep1.complexAttribute = logicNode.entries[rep2Index].complexAttribute

    def distributeIndex(self, node0: models.Node, rep0: models.SlimObject, node1: models.Node, rep1: models.SlimObject, logicNode: models.Node):

        matrix = []

        for row in range(len(logicNode.entries)):
            a = []
            for column in range(len(logicNode.entries)):
                a.append(0)
            matrix.append(a)

        for i in range(0, len(logicNode.entries)):
            matrix[i][i] = 0
            for j in range(i):
                matrix[i][j] = self.getDistance(
                    logicNode.entries[i], logicNode.entries[j])
                matrix[j][i] = matrix[i][j]

        X = csr_matrix(matrix)

        Tcsr = minimum_spanning_tree(X).toarray().astype(float)

        maxEdgeValue = -1

        limit1 = 0
        limit2 = 0

        for row in range(len(logicNode.entries)):
            for column in range(len(logicNode.entries)):
                Tcsr[column][row] = Tcsr[row][column]
                if Tcsr[row][column] >= maxEdgeValue:
                    maxEdgeValue = Tcsr[row][column]
                    limit1 = row
                    limit2 = column

        Tcsr[limit1][limit2] = 0
        Tcsr[limit2][limit1] = 0

        cluster1 = []
        cluster2 = []

        cluster1.append(limit1)

        checkList = []

        checkList.append(limit1)

        while len(checkList) != 0:

            value = checkList.pop()

            for i in range(len(logicNode.entries)):
                if Tcsr[i][value] != 0:
                    if cluster1.count(i) == 0:
                        checkList.append(i)
                        cluster1.append(i)

        for i in range(len(logicNode.entries)):
            if cluster1.count(i) == 0:
                cluster2.append(i)

        maximumDistance = []

        for i in range(len(logicNode.entries)):
            if cluster1.count(i) != 0:
                # i is on cluster1
                maxValue = 0
                for j in cluster1:
                    if matrix[i][j] > maxValue:
                        maxValue = matrix[i][j]
                maximumDistance.append(maxValue)
            else:
                # i is on cluster2
                maxValue = 0
                for j in cluster2:
                    if matrix[i][j] > maxValue:
                        maxValue = matrix[i][j]
                maximumDistance.append(maxValue)

        rep1Index = 0
        rep2Index = 0

        maxValue = 1000000000000000

        for i in cluster1:
            if maximumDistance[i] < maxValue:
                maxValue = maximumDistance[i]
                rep1Index = i

        maxValue = 1000000000000000

        for i in cluster2:
            if maximumDistance[i] < maxValue:
                maxValue = maximumDistance[i]
                rep2Index = i

        node0.entries.append(logicNode.entries[rep1Index])
        node0.occupation = 1
        subTree0 = models.SubTreeInfos()
        subTree0.nEntries = logicNode.subtrees[rep1Index].nEntries
        subTree0.pageID = logicNode.subtrees[rep1Index].pageID
        subTree0.radius = logicNode.subtrees[rep1Index].radius
        subTree0.distance = 0
        node0.subtrees.append(subTree0)

        node1.entries.append(logicNode.entries[rep2Index])
        node1.occupation = 1
        subTree1 = models.SubTreeInfos()
        subTree1.distance = 0
        subTree1.nEntries = logicNode.subtrees[rep2Index].nEntries
        subTree1.pageID = logicNode.subtrees[rep2Index].pageID
        subTree1.radius = logicNode.subtrees[rep2Index].radius
        node1.subtrees.append(subTree1)

        for i in cluster1:
            if i != rep1Index:
                node0.entries.append(logicNode.entries[i])
                node0.occupation += 1
                subTree = models.SubTreeInfos()
                subTree.distance = matrix[i][rep1Index]
                subTree.nEntries = logicNode.subtrees[i].nEntries
                subTree.pageID = logicNode.subtrees[i].pageID
                subTree.radius = logicNode.subtrees[i].radius
                node0.subtrees.append(subTree)

        for i in cluster2:
            if i != rep2Index:
                node1.entries.append(logicNode.entries[i])
                node1.occupation += 1
                subTree = models.SubTreeInfos()
                subTree.distance = matrix[i][rep2Index]
                subTree.nEntries = logicNode.subtrees[i].nEntries
                subTree.pageID = logicNode.subtrees[i].pageID
                subTree.radius = logicNode.subtrees[i].radius
                node1.subtrees.append(subTree)

        rep0.oid = logicNode.entries[rep1Index].oid
        rep0.includeAttribute = logicNode.entries[rep1Index].includeAttribute
        rep0.complexAttribute = logicNode.entries[rep1Index].complexAttribute

        rep1.oid = logicNode.entries[rep2Index].oid
        rep1.includeAttribute = logicNode.entries[rep2Index].includeAttribute
        rep1.complexAttribute = logicNode.entries[rep2Index].complexAttribute

    def chooseSubTree(self, oldNode: models.Node,  newObj: models.SlimObject):

        index = 0
        minoccup = 1000000000000

        containsNewObj = []

        for i in range(len(oldNode.entries)):
            if self.getDistance(newObj, oldNode.entries[i]) <= oldNode.subtrees[i].radius:
                containsNewObj.append(i)

        if len(containsNewObj) == 0:
            for j in range(len(oldNode.entries)):
                if oldNode.subtrees[j].nEntries < minoccup:
                    minoccup = oldNode.subtrees[j].nEntries
                    index = j

        else:
            for j in containsNewObj:
                if oldNode.subtrees[j].nEntries < minoccup:
                    minoccup = oldNode.subtrees[j].nEntries
                    index = j

        return index

    def splitLeaf(self, oldNode: models.Node, newNode: models.Node, newObj: models.SlimObject,  prevRep: models.SlimObject, promo1: models.SubtreeInfo, promo2: models.SubtreeInfo):

        lRep:  models.SlimObject
        lRep = models.SlimObject()
        rRep:  models.SlimObject
        rRep = models.SlimObject()
        numberOfEntries = oldNode.occupation

        logicNode = models.Node()
        logicNode.entries = []

        for i in oldNode.entries:
            logicNode.entries.append(i)

        logicNode.entries.append(newObj)

        self.objectCount += 1

        oldNode.entries = []
        oldNode.occupation = 0
        oldNode.subtrees = []

        self.distributeLeaf(oldNode, lRep, newNode, rRep, logicNode)

        if prevRep == None:

            promo1.rep = models.SlimObject()
            promo1.rep.oid = lRep.oid
            promo1.rep.complexAttribute = lRep.complexAttribute
            promo1.rep.includeAttribute = lRep.includeAttribute
            promo1.radius = self.getMinimumRadiusLeaf(oldNode)
            promo1.rootID = oldNode.pageID
            promo1.nObjects = oldNode.occupation
            promo2.rep = models.SlimObject()
            promo2.rep.oid = rRep.oid
            promo2.rep.complexAttribute = rRep.complexAttribute
            promo2.rep.includeAttribute = rRep.includeAttribute
            promo2.radius = self.getMinimumRadiusLeaf(newNode)
            promo2.rootID = newNode.pageID
            promo2.nObjects = newNode.occupation

        else:

            if prevRep.oid == lRep.oid:

                promo1.rep = None
                promo1.radius = self.getMinimumRadiusLeaf(oldNode)
                promo1.rootID = oldNode.pageID
                promo1.nObjects = oldNode.occupation
                promo2.rep = models.SlimObject()
                promo2.rep.oid = rRep.oid
                promo2.rep.complexAttribute = rRep.complexAttribute
                promo2.rep.includeAttribute = rRep.includeAttribute
                promo2.radius = self.getMinimumRadiusLeaf(newNode)
                promo2.rootID = newNode.pageID
                promo2.nObjects = newNode.occupation

            elif prevRep.oid == rRep.oid:

                promo2.rep = models.SlimObject()
                promo2.rep.oid = lRep.oid
                promo2.rep.complexAttribute = lRep.complexAttribute
                promo2.rep.includeAttribute = lRep.includeAttribute
                promo2.radius = self.getMinimumRadiusLeaf(oldNode)
                promo2.rootID = oldNode.pageID
                promo2.nObjects = oldNode.occupation
                promo1.rep = None
                promo1.radius = self.getMinimumRadiusLeaf(newNode)
                promo1.rootID = newNode.pageID
                promo1.nObjects = newNode.occupation

            else:
                promo1.rep = models.SlimObject()
                promo1.rep.oid = lRep.oid
                promo1.rep.complexAttribute = lRep.complexAttribute
                promo1.rep.includeAttribute = lRep.includeAttribute
                promo1.radius = self.getMinimumRadiusLeaf(oldNode)
                promo1.rootID = oldNode.pageID
                promo1.nObjects = oldNode.occupation
                promo2.rep = models.SlimObject()
                promo2.rep.oid = rRep.oid
                promo2.rep.complexAttribute = rRep.complexAttribute
                promo2.rep.includeAttribute = rRep.includeAttribute
                promo2.radius = self.getMinimumRadiusLeaf(newNode)
                promo2.rootID = newNode.pageID
                promo2.nObjects = newNode.occupation

    def splitIndex(self, oldNode: models.Node, newNode: models.Node, newObj1: models.SlimObject,  newRadius1: float, newNodeID1: str,  newNEntries1: int, newObj2: models.SlimObject, newRadius2: float, newNodeID2: str, newNEntries2: int, prevRep: models.SlimObject, promo1: models.SubtreeInfo, promo2: models.SubtreeInfo):

        lRep:  models.SlimObject
        lRep = models.SlimObject()
        rRep:  models.SlimObject
        rRep = models.SlimObject()
        numberOfEntries = oldNode.occupation

        logicNode = models.Node()
        logicNode.entries = []
        logicNode.subtrees = []

        for i in oldNode.entries:
            logicNode.entries.append(i)

        for i in oldNode.subtrees:
            logicNode.subtrees.append(i)

        oldNode.entries = []
        oldNode.occupation = 0
        oldNode.subtrees = []

        logicNode.entries.append(newObj1)

        subTreeInfos = models.SubTreeInfos()
        subTreeInfos.radius = newRadius1
        subTreeInfos.nEntries = newNEntries1
        subTreeInfos.pageID = newNodeID1

        logicNode.subtrees.append(subTreeInfos)

        if newObj2 != None:
            logicNode.entries.append(newObj2)
            subTreeInfos2 = models.SubTreeInfos()
            subTreeInfos2.radius = newRadius2
            subTreeInfos2.nEntries = newNEntries2
            subTreeInfos2.pageID = newNodeID2

            logicNode.subtrees.append(subTreeInfos2)

        self.distributeIndex(oldNode, lRep, newNode, rRep, logicNode)

        if prevRep == None:
            promo1.rep = models.SlimObject()
            promo1.rep.oid = lRep.oid
            promo1.rep.complexAttribute = lRep.complexAttribute
            promo1.rep.includeAttribute = lRep.includeAttribute
            promo1.radius = self.getMinimumRadiusIndex(oldNode)
            promo1.rootID = oldNode.pageID
            promo1.nObjects = self.getTotalObjectCount(oldNode)
            promo2.rep = models.SlimObject()
            promo2.rep.oid = rRep.oid
            promo2.rep.complexAttribute = rRep.complexAttribute
            promo2.rep.includeAttribute = rRep.includeAttribute
            promo2.radius = self.getMinimumRadiusIndex(newNode)
            promo2.rootID = newNode.pageID
            promo2.nObjects = self.getTotalObjectCount(newNode)

        else:

            if prevRep.oid == lRep.oid:
                promo1.rep = None
                promo1.radius = self.getMinimumRadiusIndex(oldNode)
                promo1.rootID = oldNode.pageID
                promo1.nObjects = self.getTotalObjectCount(oldNode)
                promo2.rep = models.SlimObject()
                promo2.rep.oid = rRep.oid
                promo2.rep.complexAttribute = rRep.complexAttribute
                promo2.rep.includeAttribute = rRep.includeAttribute
                promo2.radius = self.getMinimumRadiusIndex(newNode)
                promo2.rootID = newNode.pageID
                promo2.nObjects = self.getTotalObjectCount(newNode)

            elif prevRep.oid == rRep.oid:
                promo2.rep = models.SlimObject()
                promo2.rep.oid = lRep.oid
                promo2.rep.complexAttribute = lRep.complexAttribute
                promo2.rep.includeAttribute = lRep.includeAttribute
                promo2.radius = self.getMinimumRadiusIndex(oldNode)
                promo2.rootID = oldNode.pageID
                promo2.nObjects = self.getTotalObjectCount(oldNode)
                promo1.rep = None
                promo1.radius = self.getMinimumRadiusIndex(newNode)
                promo1.rootID = newNode.pageID
                promo1.nObjects = self.getTotalObjectCount(newNode)

            else:

                promo1.rep = models.SlimObject()
                promo1.rep.oid = lRep.oid
                promo1.rep.complexAttribute = lRep.complexAttribute
                promo1.rep.includeAttribute = lRep.includeAttribute
                promo1.radius = self.getMinimumRadiusIndex(oldNode)
                promo1.rootID = oldNode.pageID
                promo1.nObjects = self.getTotalObjectCount(oldNode)

                promo2.rep = models.SlimObject()
                promo2.rep.oid = rRep.oid
                promo2.rep.complexAttribute = rRep.complexAttribute
                promo2.rep.includeAttribute = rRep.includeAttribute
                promo2.radius = self.getMinimumRadiusIndex(newNode)
                promo2.rootID = newNode.pageID
                promo2.nObjects = self.getTotalObjectCount(newNode)

    def insertRecursive(self, currNodeID: str, newObj: models.SlimObject, repObj: models.SlimObject, promo1: models.SubtreeInfo, promo2: models.SubtreeInfo):

        currNode: models.Node
        newIndexNode: models.Node
        newLeafNode: models.Node
        insertIdx: int
        result: str
        dist: float
        subtree: int
        subRep: models.SlimObject

        currNode = self.readNode(currNodeID)

        if currNode.type == "INDEX":

            subtree = self.chooseSubTree(currNode, newObj)

            subRep = currNode.entries[subtree]

            op = self.insertRecursive(
                currNode.subtrees[subtree].pageID, newObj, subRep, promo1, promo2)

            if op == "NO_ACT":
                currNode.subtrees[subtree].nEntries += 1
                currNode.subtrees[subtree].radius = promo1.radius

                promo1.nObjects = self.getTotalObjectCount(currNode)

                promo1.radius = self.getMinimumRadiusIndex(currNode)
                result = "NO_ACT"

                # 1285

            elif op == "CHANGE_REP":

                self.removeEntry(currNode, subtree)

                insertIdx = self.addEntryIndex(promo1.rep, currNode)

                if insertIdx >= 0:

                    subTreeInfos = models.SubTreeInfos()
                    subTreeInfos.radius = promo1.radius
                    subTreeInfos.nEntries = promo1.nObjects
                    subTreeInfos.pageID = promo1.rootID

                    currNode.subtrees.append(subTreeInfos)

                    if ((repObj != None) and (repObj.oid == subRep.oid)):
                        self.getIndexEntry(currNode, insertIdx).distance = 0

                        promo1.rootID = currNodeID

                        self.updateDistances(currNode, promo1.rep, insertIdx)

                        result = "CHANGE_REP"
                        # 1314
                    else:
                        if (repObj != None):
                            self.getIndexEntry(currNode, insertIdx).distance = self.getDistance(
                                repObj, promo1.rep)

                        else:
                            self.getIndexEntry(
                                currNode, insertIdx).distance = 0

                        promo1.rep = None

                        result = "NO_ACT"
                        # 1330

                    promo1.radius = self.getMinimumRadiusIndex(currNode)
                    promo1.nObjects = self.getTotalObjectCount(currNode)

                    # 1333

                else:

                    newIndexNode = models.Node()
                    self.nodeCount += 1
                    newIndexNode.type = "INDEX"
                    newIndexNode.generatePageID()
                    newIndexNode.occupation = 0
                    newIndexNode.entries = []
                    newIndexNode.subtrees = []

                    self.splitIndex(currNode, newIndexNode, promo1.rep, promo1.radius,
                                    promo1.rootID, promo1.nObjects, None, 0, 0, 0, repObj, promo1, promo2)

                    self.writeNode(newIndexNode)

                    result = "PROMOTION"

                    # 1352

            elif op == "PROMOTION":

                if promo1.rep == None:

                    self.getIndexEntry(
                        currNode, subtree).nEntries = promo1.nObjects
                    self.getIndexEntry(
                        currNode, subtree).radius = promo1.radius
                    self.getIndexEntry(
                        currNode, subtree).pageID = promo1.rootID

                    insertIdx = self.addEntryIndex(promo2.rep, currNode)

                    # 1363
                    if insertIdx >= 0:

                        subTreeInfos = models.SubTreeInfos()
                        subTreeInfos.radius = promo2.radius
                        subTreeInfos.nEntries = promo2.nObjects
                        subTreeInfos.pageID = promo2.rootID

                        currNode.subtrees.append(subTreeInfos)

                        if repObj != None:

                            self.getIndexEntry(currNode, insertIdx).distance = self.getDistance(
                                repObj, promo2.rep)
                            # 1374
                        else:
                            self.getIndexEntry(
                                currNode, insertIdx).distance = 0

                        promo1.radius = self.getMinimumRadiusIndex(currNode)
                        promo1.nObjects = self.getTotalObjectCount(currNode)

                        promo2.rep = None

                        result = "NO_ACT"
                        # 1386
                    else:
                        newIndexNode = models.Node()
                        self.nodeCount += 1
                        newIndexNode.type = "INDEX"
                        newIndexNode.generatePageID()
                        newIndexNode.occupation = 0
                        newIndexNode.entries = []
                        newIndexNode.subtrees = []

                        self.splitIndex(currNode, newIndexNode, promo2.rep, promo2.radius,
                                        promo2.rootID, promo2.nObjects, None, 0, 0, 0, repObj, promo1, promo2)

                        self.writeNode(newIndexNode)

                        result = "PROMOTION"

                        # 1405
                else:

                    self.removeEntry(currNode, subtree)

                    insertIdx = self.addEntryIndex(promo1.rep, currNode)

                    # 1412
                    if insertIdx >= 0:

                        subTreeInfos = models.SubTreeInfos()
                        subTreeInfos.radius = promo1.radius
                        subTreeInfos.nEntries = promo1.nObjects
                        subTreeInfos.pageID = promo1.rootID

                        currNode.subtrees.append(subTreeInfos)

                        if (repObj != None) and repObj.oid == subRep.oid:
                            self.getIndexEntry(
                                currNode, insertIdx).distance = 0

                            promo1.rootID = currNodeID

                            self.updateDistances(
                                currNode, promo1.rep, insertIdx)

                            result = "CHANGE_REP"

                            # 1434
                        else:

                            if repObj != None:
                                self.getIndexEntry(currNode, insertIdx).distance = self.getDistance(
                                    repObj, promo1.rep)
                            else:
                                self.getIndexEntry(
                                    currNode, insertIdx).distance = 0

                            promo1.rep = None

                            result = "NO_ACT"

                            # 1450

                        insertIdx = self.addEntryIndex(
                            promo2.rep, currNode)

                        if insertIdx >= 0:
                            # 1457

                            subTreeInfos = models.SubTreeInfos()
                            subTreeInfos.radius = promo2.radius
                            subTreeInfos.nEntries = promo2.nObjects
                            subTreeInfos.pageID = promo2.rootID

                            currNode.subtrees.append(subTreeInfos)

                            if promo1.rep != None:

                                self.getIndexEntry(currNode, insertIdx).distance = self.getDistance(
                                    promo1.rep, promo2.rep)

                            else:
                                if repObj != None:
                                    self.getIndexEntry(currNode, insertIdx).distance = self.getDistance(
                                        repObj, promo2.rep)
                                else:
                                    self.getIndexEntry(
                                        currNode, insertIdx).distance = 0

                            # 1479

                            promo2.rep = None

                            promo1.nObjects = self.getTotalObjectCount(
                                currNode)
                            promo1.radius = self.getMinimumRadiusIndex(
                                currNode)

                            # 1488
                        else:

                            newIndexNode = models.Node()
                            self.nodeCount += 1
                            newIndexNode.type = "INDEX"
                            newIndexNode.generatePageID()
                            newIndexNode.occupation = 0
                            newIndexNode.subtrees = []
                            newIndexNode.entries = []

                            if promo1.rep != None:
                                promo1.rep = None

                            self.splitIndex(currNode, newIndexNode, promo2.rep, promo2.radius,
                                            promo2.rootID, promo2.nObjects, None, 0, 0, 0, repObj, promo1, promo2)

                            self.writeNode(newIndexNode)

                            result = "PROMOTION"
                            # 1514
                    else:
                        newIndexNode = models.Node()
                        self.nodeCount += 1
                        newIndexNode.type = "INDEX"
                        newIndexNode.generatePageID()
                        newIndexNode.occupation = 0
                        newIndexNode.subtrees = []
                        newIndexNode.entries = []

                        self.splitIndex(currNode, newIndexNode, promo1.rep, promo1.radius,
                                        promo1.rootID, promo1.nObjects, promo2.rep, promo2.radius, promo2.rootID, promo2.nObjects, repObj, promo1, promo2)

                        self.writeNode(newIndexNode)

                        result = "PROMOTION"

                        # 1533

            subRep = None
        else:

            insertIdx = self.addEntryLeaf(newObj, currNode)

            if insertIdx >= 0:
                # Don't split

                if (repObj == None):
                    dist = 0
                else:
                    dist = self.getDistance(newObj, repObj)

                subTreeInfos = models.SubTreeInfos()
                subTreeInfos.distance = 0
                currNode.subtrees.append(subTreeInfos)

                self.getLeafEntry(currNode, insertIdx).distance = dist

                self.writeNode(currNode)

                promo1.rep = None
                promo1.radius = self.getMinimumRadiusLeaf(currNode)
                promo1.rootID = currNodeID
                promo1.nObjects = currNode.occupation
                result = "NO_ACT"
            else:
                # split it

                newLeafNode = models.Node()
                self.nodeCount += 1
                newLeafNode.type = "LEAF"
                newLeafNode.generatePageID()
                newLeafNode.occupation = 0
                newLeafNode.subtrees = []
                newLeafNode.entries = []

                self.splitLeaf(currNode, newLeafNode, newObj,
                               repObj, promo1, promo2)

                self.writeNode(newLeafNode)

                result = "PROMOTION"

        self.writeNode(currNode)

        return result

    def removeEntry(self, node: models.Node, index: int):
        node.occupation = node.occupation - 1

        obj = node.entries[index]

        node.entries.remove(obj)

        subtree = node.subtrees[index]
        node.subtrees.remove(subtree)

    def addEntryLeaf(self, object: models.SlimObject, node: models.Node):

        if node.occupation == self.maxOccupation:
            return -1

        node.entries.append(object)
        node.occupation += 1
        self.objectCount += 1

        return node.entries.index(object)

    def addEntryIndex(self,  object: models.SlimObject, node: models.Node):

        if node.occupation == self.maxOccupation:
            return -1

        node.entries.append(object)
        node.occupation += 1

        return node.entries.index(object)

    def addNewRoot(self, obj1: models.SlimObject, radius1: float, nodeID1: str, nEntries1: int, obj2: models.SlimObject, radius2: float, nodeID2: str, nEntries2: int):

        newRoot = models.Node()
        self.nodeCount += 1
        newRoot.type = "INDEX"
        newRoot.generatePageID()
        newRoot.occupation = 0
        newRoot.entries = []
        newRoot.subtrees = []

        idx = self.addEntryIndex(obj1, newRoot)
        subTreeInfos = models.SubTreeInfos()
        subTreeInfos.radius = radius1
        subTreeInfos.nEntries = nEntries1
        subTreeInfos.pageID = nodeID1
        subTreeInfos.distance = 0

        newRoot.subtrees.append(subTreeInfos)

        idx = self.addEntryIndex(obj2, newRoot)
        subTreeInfos = models.SubTreeInfos()
        subTreeInfos.radius = radius2
        subTreeInfos.nEntries = nEntries2
        subTreeInfos.pageID = nodeID2
        subTreeInfos.distance = 0

        newRoot.subtrees.append(subTreeInfos)

        self.height += 1
        self.root = newRoot.pageID
        self.writeNode(newRoot)

    def add(self,  object: models.SlimObject):

        promo1 = models.SubtreeInfo()
        promo1.rep = models.SlimObject()
        promo2 = models.SubtreeInfo()
        promo2.rep = models.SlimObject()

        if self.root == "NULL":

            node = models.Node()
            node.type = "LEAF"
            node.generatePageID()
            node.occupation = 0
            node.entries = []
            node.subtrees = []
            self.setRoot(node.pageID)

            insertIdx = self.addEntryLeaf(object, node)

            if insertIdx == -1:
                return False
            else:
                self.height += 1
                subTreeInfos = models.SubTreeInfos()
                subTreeInfos.distance = 0
                node.subtrees.append(subTreeInfos)

                self.writeNode(node)
                self.nodeCount += 1
        else:

            if self.insertRecursive(self.root, object, None, promo1, promo2) == "PROMOTION":

                self.addNewRoot(promo1.rep, promo1.radius, promo1.rootID,
                                promo1.nObjects, promo2.rep, promo2.radius, promo2.rootID, promo2.nObjects)
                promo1.rep = None
                promo2.rep = None

    def readNode(self, nodeID: str):
        self.readCount += 1
        return self.nodes[nodeID]

    def getLeafEntry(self, currNode: models.Node, insertIdx: int):
        return currNode.subtrees[insertIdx]

    def getIndexEntry(self, currNode: models.Node, insertIdx: int):
        return currNode.subtrees[insertIdx]

    def getTotalObjectCount(self, node: models.Node):
        count = 0

        for i in node.subtrees:
            count += i.nEntries

        return count

    def getTotalObjectCount(self, node: models.Node):
        count = 0

        for i in node.subtrees:
            count += i.nEntries

        return count

    def getMinimumRadiusLeaf(self, node: models.Node):
        radius = 0

        for i in node.subtrees:
            if radius < i.distance:
                radius = i.distance

        return radius

    def getMinimumRadiusIndex(self, node: models.Node):
        minRadius = 0

        for i in node.subtrees:
            distance = i.distance + i.radius
            if minRadius < distance:
                minRadius = distance

        return minRadius

    def haversine(self, lat1, lon1, lat2, lon2):

        R = 6372.8  # this is in miles.  For Earth radius in kilometers use 6372.8 km

        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
        c = 2*asin(sqrt(a))

        return R * c

    
    def manhattan(self, list1, list2):

        sum = 0

        for i in range(len(list1)):
            sum = sum + abs(float(list1[i])-float(list2[i]))

        return sum

    def jaccard(self, list1, list2):

        s1 = set(list1)
        s2 = set(list2)

        return 1 - float(len(s1.intersection(s2)) / len(s1.union(s2)))

    def debug(self, a, b):

        return abs(a-b)

    def getDistance(self, obj1: models.SlimObject, obj2: models.SlimObject):
        self.distancesCount += 1

        #return self.jaccard(obj1.complexAttribute["features"], obj2.complexAttribute["features"])
        #return self.manhattan(obj1.complexAttribute["features"], obj2.complexAttribute["features"])

        #return self.debug(float(obj1.complexAttribute["value"]), float(obj2.complexAttribute["value"]))
        return self.haversine(float(obj1.complexAttribute["lat"]), float(obj1.complexAttribute["lon"]), float(obj2.complexAttribute["lat"]), float(obj2.complexAttribute["lon"]))

    def writeNode(self, node: models.Node):
        self.writeCount += 1
        self.nodes[node.pageID] = node

    def updateDistances(self, node: models.Node, repObj: models.SlimObject, repObjIdx: int):
        for i in range(len(node.subtrees)):

            node.subtrees[i].distance = self.getDistance(
                repObj, node.entries[i])
