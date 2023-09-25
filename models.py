import random
import string
import json

class SlimObject():
    oid: str
    complexAttribute: dict
    includeAttribute: dict

    def encodeComplete(self):
        return {"oid": self.oid, "complexAttribute": self.complexAttribute, "includeAttribute": self.includeAttribute}

    def encodeShort(self):
        return {"oid": self.oid, "complexAttribute": self.complexAttribute}


class DocumentObject():
    oid: str
    data: dict


class SubTreeInfos():
    pageID: str
    occupation: int
    distance: float
    nEntries: int
    radius: float

    def encode(self):
        return vars(self)


class Node():
    pageID: str
    type: str
    occupation: int
    entries: list[SlimObject] = []
    subtrees: list[SubTreeInfos] = []

    def generatePageID(self):
        self.pageID = ''.join(random.choice(string.ascii_lowercase)
                              for i in range(10))

    def convertEntries(self):
        dict = []

        for i in self.entries:
            if self.type == "INDEX":
                dict.append(i.encodeShort())
            else:
                dict.append(i.encodeComplete())

        return dict

    def convertSubtrees(self):
        dict = []

        for i in self.subtrees:
            dict.append(i.encode())

        return dict

    def toMap(self):
       
        return {"type": self.type, "occupation": self.occupation, "entries": self.convertEntries(), "subtrees": self.convertSubtrees()}
      

class SubtreeInfo():
    rep: SlimObject
    radius: float
    rootID: str
    nObjects: int
