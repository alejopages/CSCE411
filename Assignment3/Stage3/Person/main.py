from sys import argv, exit
import tests
import dataLoader
from math import ceil

NODE_HEADER = "person_node_"
LEAF_HEADER = "person_leaf_"

def main():
    FAN = 10
    # FAN = 200
    # NUM_ITEMS = 1999
    # messages = dataLoader.importMessages()
    persons = dataLoader.importPersons()
    NUM_ITEMS = len(persons)
    entryResults = getEntryResults(NUM_ITEMS, FAN)
    for item in entryResults:
        print(item)

    leaves = buildLeaves(persons, FAN, entryResults[0]["entriesPerFile"])
    # print(len(leaves))

    lvl1Nodes = buildLvl1Nodes(leaves, FAN, \
            entryResults[1]["entriesPerFile"], \
            entryResults[1]["startingFileNumber"], "person_leaf_")
    # print(len(lvl1Nodes))
    # for node in lvl1Nodes:
        # print(node)

    lvl2Nodes = buildLvl1Nodes(lvl1Nodes, FAN, \
            entryResults[2]["entriesPerFile"], \
            entryResults[2]["startingFileNumber"], "person_node_")
    print(len(lvl2Nodes))
    for node in lvl2Nodes:
        print(node)


    return

def getEntryResults(NUM_ITEMS, FAN):
    entryResults = determineEntriesPerFileAmounts(NUM_ITEMS, FAN)
    determineStartingFileNumbers(entryResults)
    return entryResults

def determineStartingFileNumbers(entryResults):
    count = 0
    for i in range(len(entryResults)-1, 0, -1):
        entry = entryResults[i]
        entry["startingFileNumber"] = count
        count += entry["numFiles"]

    return

def determineEntriesPerFileAmounts(NUM_ITEMS, FAN):
    entryResults = list()

    numEntriesPerFile = determineEntriesPerLeafFile(NUM_ITEMS, FAN)
    numFiles = ceil(NUM_ITEMS/numEntriesPerFile)
    entryResults.append({"entriesPerFile": numEntriesPerFile, "numFiles": numFiles, "startingFileNumber": 0})

    while numFiles > 1:
        numEntriesPerFile = determineEntriesPerNode(numFiles, FAN)
        numFiles = ceil(numFiles/numEntriesPerFile)
        entryResults.append({"entriesPerFile": numEntriesPerFile, "numFiles": numFiles, "startingFileNumber": -1})

    return entryResults

def buildLvl1Nodes(leaves, FAN, LEAVES_PER_NODE, FIRST_NODE_NUMBER, HEADER):
    # LEAVES_PER_NODE = determineEntriesPerNode(len(leaves), FAN)

    lvl1Nodes = list()
    count = 0
    while len(leaves) > 0:
        node = buildNode(leaves, LEAVES_PER_NODE, \
                         FIRST_NODE_NUMBER + (count*10), HEADER)
        lvl1Nodes.append(node)
        count += 1

    return lvl1Nodes

def buildNode(leaves, LEAVES_PER_NODE, FIRST_NODE_NUMBER, HEADER):
    leaves.pop(0)
    node = HEADER + str(FIRST_NODE_NUMBER) + ","
    for i in range(1, LEAVES_PER_NODE):
        if len(leaves) == 0:
            break
        addition = leaves.pop(0).split(",")[1].split(";")[0] \
                 + "," + HEADER + str(FIRST_NODE_NUMBER + i) + ","
        node += addition

    return node[0 : len(node) - 1]

def buildLeaves(persons, FAN, ENTRIES_PER_LEAF):
    # ENTRIES_PER_LEAF = determineEntriesPerLeafFile(len(persons), FAN)
    # ENTRIES_PER_LEAF = determineEntriesPerLeafFile(len(persons), FAN)

    leaves = list()

    firstLeaf = getFirstLeaf(persons, ENTRIES_PER_LEAF)
    leaves.append(firstLeaf)

    getInnerLeaves(leaves, persons, ENTRIES_PER_LEAF, FAN)

    lastLeaf = getLastLeaf(persons, ENTRIES_PER_LEAF, len(leaves) - 1)
    leaves.append(lastLeaf)

    return leaves

def getLastLeaf(persons, ENTRIES_PER_LEAF, leafNumber):
    lastLeaf = getLeafEntries(persons, ENTRIES_PER_LEAF)
    lastLeaf = wrapLastLeafEntryInLeafPointers(lastLeaf, leafNumber)
    return lastLeaf

def getInnerLeaves(leaves, persons, ENTRIES_PER_LEAF, FAN):
    count = 0
    while len(persons) > FAN:
        entries = getLeafEntries(persons, ENTRIES_PER_LEAF)
        leaf = wrapLeafEntriesInLeafPointers(entries, count)
        leaves.append(leaf)
        count += 1

    return

def getFirstLeaf(persons, ENTRIES_PER_LEAF):
    firstLeaf = getLeafEntries(persons, ENTRIES_PER_LEAF)
    firstLeaf = wrapFirstLeafEntryInLeafPointers(firstLeaf)
    return firstLeaf

def wrapLastLeafEntryInLeafPointers(leafEntries, leafNumber):
    line = LEAF_HEADER + str(leafNumber) + ","
    line += leafEntries
    line += ","

    return line

def wrapFirstLeafEntryInLeafPointers(leafEntries):
    line = ","
    line += leafEntries
    line += "," + LEAF_HEADER + "1"

    return line

def wrapLeafEntriesInLeafPointers(leafEntries, leafNumber):
    LEAF_HEADER = "person_leaf_"
    line = LEAF_HEADER + str(leafNumber) + ","
    line += leafEntries
    line += "," + LEAF_HEADER + str(leafNumber + 2)

    return line

def getLeafEntries(persons, entriesPerLeaf):
    s = ""
    for i in range(entriesPerLeaf):
        if len(persons) != 0:
            s += personToString(persons.pop(0)) + ","

    return s[0 : len(s) - 1]

def determineEntriesPerLeafFile(numItems, fan):
    for tentativeNumEntriesPerLeaf in range(fan - 1, 0, -1):
        if entriesPerLeafAmountIsValid(numItems, tentativeNumEntriesPerLeaf):
            return tentativeNumEntriesPerLeaf

    exit("ERROR: No viable number of entries")
    return

def determineEntriesPerNode(numItems, fan):
    if numItems < fan:
        return numItems

    for tentativeNumEntriesPerLeaf in range(fan, 0, -1):
        if entriesPerLeafAmountIsValid(numItems, tentativeNumEntriesPerLeaf):
            return tentativeNumEntriesPerLeaf

    exit("ERROR: No viable number of entries")
    return

def entriesPerLeafAmountIsValid(numItems, numEntriesPerFile):
    remainder = (numItems/numEntriesPerFile) % 1
    return (remainder >= 0.5) or (remainder == 0)

def personToString(tuple):
    s = ""
    for item in tuple:
        s += str(item) + ";"

    return s[0: len(s) - 1]

def printPersons():
    persons = dataLoader.importPersons()

    print(len(persons))
    print("stateId, id, idStr, name, cityId")

    for person in persons:
        print(person)

    return

def determineNumberOfItemsToPutInFile(numItemsLeft, numPointersLeft):
    return int(numItemsLeft/numPointersLeft)

if __name__ == "__main__":
    main()
