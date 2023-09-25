import models
import includeSlimTree
import similarityOperators
import time
import os
import random

def geonames1M():
    myCollection: list[models.DocumentObject]

    myCollection = []

    with open("inputs/geonames10k.txt", "r") as f:
        for line in f:
            list = line.split()
            documentObject = models.DocumentObject()
            documentObject.oid = list[0]
            documentObject.data = {"name":  list[1], "lat": list[2], "lon": list[3], "type": list[4], "typeDetail": list[5],
                                   "country": list[6], "pop": list[7], "dem": list[8], "contin": list[9], "currency": list[10]}
            myCollection.append(documentObject)

    includeSlim = includeSlimTree.IncludeSlim()
    includeSlim.maxOccupation = 5
    includeSlim.height = 0
    includeSlim.objectCount = 0
    includeSlim.nodeCount = 0
    includeSlim.nodes = {}
    includeSlim.root = "NULL"
    includeSlim.writeCount = 0
    includeSlim.readCount = 0
    includeSlim.distancesCount = 0

    for document in myCollection:

        slimObject = models.SlimObject()
        slimObject.oid = document.oid
        slimObject.complexAttribute = {
            "lat": document.data["lat"], "lon": document.data["lon"]}
        slimObject.includeAttribute = {"type": document.data["type"]}

        includeSlim.add(slimObject)
    
    myQueryList: list[models.DocumentObject]

    myQueryList = []

    with open("inputs/geonames1MQuery.txt", "r") as f:
        for line in f:
            list = line.split()
            documentObject = models.DocumentObject()
            documentObject.oid = list[0]
            documentObject.data = {"name":  list[1], "lat": list[2], "lon": list[3], "type": list[4], "typeDetail": list[5],
                                "country": list[6], "pop": list[7], "dem": list[8], "contin": list[9], "currency": list[10]}
            myQueryList.append(documentObject)


    rangeList = [0, 1, 2, 3, 5, 10, 15, 20, 25, 30]

    for range in rangeList:

        print("RANGE: " + str(range))

        avgTime = 0
        avgReadDocuments = 0
        avgDistanceCalculations = 0
        avgTuples = 0

        for center in myQueryList:
            slimObject = models.SlimObject()
            slimObject.oid = center.oid
            slimObject.complexAttribute = {
                "lat": center.data["lat"], "lon": center.data["lon"]}
            slimObject.includeAttribute = {"type": center.data["type"]}


            query = similarityOperators.SimilarityRetrievalOperators()
            start = time.time()
            result = query.RangeQuery(includeSlim, slimObject, range)
            end = time.time()
            avgTime = avgTime + (end - start)
            avgReadDocuments = avgReadDocuments + includeSlim.readCount
            avgDistanceCalculations = avgDistanceCalculations + includeSlim.distancesCount
            avgTuples = avgTuples + len(result.entries)

          
geonames1M()

