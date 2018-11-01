from sys import argv, exit
import tests
import dataLoader
from math import ceil
import json

NODE_HEADER = "person_node_"
LEAF_HEADER = "person_leaf_"

def main():
    FAN = 10
    # FAN = 200
    # NUM_ITEMS = 1999
    PERSON_LEAF_LEADER = "person_leaf_"
    PERSON_NODE_LEADER = "person_node_"

    # messages = dataLoader.importMessages()

    persons = dataLoader.importPersons()
    NUM_ITEMS = len(persons)
    entryResults = getEntryResults(NUM_ITEMS, FAN)
    for item in entryResults:
        print(item)

    lvl0Results = entryResults[0]
    leaves = buildLeaves(persons, FAN, \
             lvl0Results["entriesPerFile"], PERSON_LEAF_LEADER)
    print(len(leaves))

    lvl1Results = entryResults[1]
    lvl1Nodes = buildLvl1Nodes(leaves, lvl1Results, \
                               PERSON_LEAF_LEADER, PERSON_NODE_LEADER)
    # print(json.dumps(lvl1Nodes, indent=4))
    # for node in lvl1Nodes:
        # print(node)

    # TODO: Consider removing the person_node_4 label thing from this -
    # I think the label might make it harder to iterate for the next
    # node levels - don't think it'll be necessary to have that either
    # since it's still stored in the entryResults
    # CAn just do entryREsults["starintgthingy"] + i when iterating
    # over them

    # lvl2Results = entryResults[2]
    # lvl2Nodes = buildLvl2Nodes(lvl1Nodes, lvl2Results, PERSON_NODE_LEADER)
    # for node in lvl2Nodes:
        # print(node)

    return

def buildLvl2Nodes(lvl1Nodes, lvlEntryResults, NODE_LEADER):
    # nodes = dict()
    nodes = list()
    count = 0
    for i in range(0, len(lvl1Nodes), 10):
        # nodeNumber = count + lvl1EntryResults["startingFileNumber"]
        # nodeFilename = NODE_LEADER + str(nodeNumber)
        # nodes[nodeFilename] = buildNode(leaves, \
                              # lvl1EntryResults["entriesPerFile"], \
                              # i, LEAF_LEADER)

        node = buildHigherNode(lvl1Nodes, lvlEntryResults["entriesPerFile"], \
                         i, NODE_LEADER)

        nodes.append(node)
        count += 1

    return nodes

def buildHigherNode(leaves, , STARTING_LEAF_NUMBER, LEADER):
    node = dict()
    node["values"] = LEADER + str(STARTING_LEAF_NUMBER) + ","
    node["leftmostTreeValue"] = leaves[STARTING_LEAF_NUMBER]["lowestValue"]
    for i in range(STARTING_LEAF_NUMBER+1, \
                   STARTING_LEAF_NUMBER + LEAVES_PER_NODE):
        leaf = leaves[i]
        # smallestleaf["values"].split(",")[1].split(";")[0]
        addition = leaf["lowestValue"] \
                 + "," + LEADER + str(i) + ","
        node["values"] = node["values"] + addition

    node["values"] = node["values"][0 : len(node["values"]) - 1]
    return node


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

def buildLvl1Nodes(leaves, lvl1EntryResults, LEAF_LEADER, NODE_LEADER):
    # nodes = dict()
    nodes = list()
    count = 0
    for i in range(0, len(leaves), 10):
        # nodeNumber = count + lvl1EntryResults["startingFileNumber"]
        # nodeFilename = NODE_LEADER + str(nodeNumber)
        # nodes[nodeFilename] = buildNode(leaves, \
                              # lvl1EntryResults["entriesPerFile"], \
                              # i, LEAF_LEADER)

        nodes.append(buildNode(leaves, \
                              lvl1EntryResults["entriesPerFile"], \
                              i, LEAF_LEADER))
        count += 1

    return nodes

def buildNode(leaves, LEAVES_PER_NODE, STARTING_LEAF_NUMBER, LEADER):
    node = dict()
    node["values"] = LEADER + str(STARTING_LEAF_NUMBER) + ","
    node["leftmostTreeValue"] = leaves[STARTING_LEAF_NUMBER]["lowestValue"]
    for i in range(STARTING_LEAF_NUMBER+1, \
                   STARTING_LEAF_NUMBER + LEAVES_PER_NODE):
        leaf = leaves[i]
        # smallestleaf["values"].split(",")[1].split(";")[0]
        addition = leaf["lowestValue"] \
                 + "," + LEADER + str(i) + ","
        node["values"] = node["values"] + addition

    node["values"] = node["values"][0 : len(node["values"]) - 1]
    return node

def buildLeaves(persons, FAN, ENTRIES_PER_LEAF, LEADER):
    # ENTRIES_PER_LEAF = determineEntriesPerLeafFile(len(persons), FAN)
    # ENTRIES_PER_LEAF = determineEntriesPerLeafFile(len(persons), FAN)

    leaves = list()

    firstLeaf = getFirstLeaf(persons, ENTRIES_PER_LEAF, LEADER)
    leaves.append(firstLeaf)

    getInnerLeaves(leaves, persons, ENTRIES_PER_LEAF, FAN, LEADER)

    lastLeaf = getLastLeaf(persons, ENTRIES_PER_LEAF, len(leaves) - 1, LEADER)
    leaves.append(lastLeaf)

    return leaves

def getLastLeaf(persons, ENTRIES_PER_LEAF, leafNumber, LEADER):
    leafEntries = getLeafEntries(persons, ENTRIES_PER_LEAF)
    # lastLeaf = wrapLastLeafEntryInLeafPointers(lastLeaf, leafNumber)
    leaf = {"values": leafEntries, "lowestValue": leafEntries.split(";")[0], "leftPointer": "", "rightPointer": LEADER + str(leafNumber)}
    return leaf

def getInnerLeaves(leaves, persons, ENTRIES_PER_LEAF, FAN, LEADER):
    leafNumber = 0
    while len(persons) > FAN:
        entries = getLeafEntries(persons, ENTRIES_PER_LEAF)
        # leaf = wrapLeafEntriesInLeafPointers(entries, count)
        leaf = {"values": entries, "lowestValue": entries.split(";")[0], "leftPointer": LEADER + str(leafNumber), "rightPointer": LEADER + str(leafNumber+2)}
        leaves.append(leaf)
        leafNumber += 1

    return

def getFirstLeaf(persons, ENTRIES_PER_LEAF, LEADER):
    leafEntries = getLeafEntries(persons, ENTRIES_PER_LEAF)
    # firstLeaf = wrapFirstLeafEntryInLeafPointers(firstLeaf)
    leaf = {"values": leafEntries, "lowestValue": leafEntries.split(";")[0], "leftPointer": "", "rightPointer": LEADER + "1"}
    return leaf

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
