from re import finditer
from typing import Optional, List


class Step:
    def __init__(self, desc: Optional[str], imgurl: str):
        self.desc = desc
        self.imgurl = imgurl

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return f'Step(desc={self.desc}, imgurl={self.imgurl})'


# tt in ttt returns [0] instead of [0,1]
def getPositionsOf(needle: str, haystack: str) -> List[int]:
    return [m.start() for m in finditer(needle, haystack)]


# ex: !a in '!a hi !a bi !a' -> [[0,6]]
# ex !a in '!a hi !a bi !a si !a' -> [[0,6],[12,18]
def getPairsOfPositionsOf(needle: str, haystack: str) -> List[List[int]]:
    needlePositions = getPositionsOf(needle, haystack)
    out = []

    if len(needlePositions) % 2 == 1:
        needlePositions.pop()

    for i in range(len(needlePositions) - 1):
        out.append([needlePositions[i], needlePositions[i + 1]])

    return out


def extractSteps(text: str) -> List[Step]:
    imgPrefix = '<img src="'
    descPrefix = '!stepd'
    imgPositions = getPositionsOf(imgPrefix, text)
    allDescPosPairs = getPairsOfPositionsOf(descPrefix, text)
    descPosPairs: List[Optional[List[int]]] = [None] * len(imgPositions)
    descs: List[Optional[str]] = [None] * len(imgPositions)
    imgUrls: List[str] = []

    for i in range(len(imgPositions)):
        imgPos = imgPositions[i]
        toRemove = []

        for descPosPair in allDescPosPairs:
            if descPosPair[0] < imgPos and descPosPair[1] < imgPos:
                descPosPairs[i] = descPosPair
                toRemove.append(descPosPair)

        for descPosPair in toRemove:
            allDescPosPairs.remove(descPosPair)

    for i in range(len(descPosPairs)):
        descPosPair = descPosPairs[i]
        if descPosPair is not None:
            a = descPosPair[0] + len(descPrefix)
            descs[i] = text[a: descPosPair[1]].strip()

    for imgPos in imgPositions:
        endQuote = text.find('"', imgPos + len(imgPrefix))
        imgUrls.append(text[imgPos + len(imgPrefix): endQuote])

    return [Step(descs[i], imgUrls[i]) for i in range(len(imgPositions))]
