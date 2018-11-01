from sys import argv, exit
import tests
import dataLoader
from math import ceil
import json

# NODE_HEADER = "person_node_"
LEAF_HEADER = "person_leaf_"
FAN_10_FILEPATH = "persons/fan10/"
FAN_200_FILEPATH = "persons/fan200/"

def main():
    FAN = 10
    # FAN = 200
    # NUM_ITEMS = 1999
    PERSON_LEAF_LEADER = "person_leaf_"
    PERSON_NODE_LEADER = "person_node_"

    # messages = dataLoader.importMessages()

    # IMPORT PERSONS
    # ======================================
    persons = dataLoader.importPersons()
    NUM_ITEMS = len(persons)
    entryResults = getEntryResults(NUM_ITEMS, FAN)
    for item in entryResults:
        print(item)

    # BUILD LEAVES
    # ======================================
    lvl0Results = entryResults[0]
    leaves = buildLeaves(persons, FAN, \
             lvl0Results["entriesPerFile"], PERSON_LEAF_LEADER)
    # writeLeavesToFiles(leaves, FAN_10_FILEPATH + PERSON_LEAF_LEADER)


    # BUILD LVL 1 NODES
    # ======================================
    lvl1Results = entryResults[1]
    lvl1Nodes = buildLvl1Nodes(leaves, lvl1Results, \
                               PERSON_LEAF_LEADER, PERSON_NODE_LEADER)
    # writeNodesToFiles(lvl1Nodes, FAN_10_FILEPATH + PERSON_NODE_LEADER, lvl1Results["startingFileNumber"])

    # BUILD LVL 2 NODES
    # ======================================
    lvl2Results = entryResults[2]
    lvl2Nodes = buildHigherNodes(lvl1Nodes, lvl1Results["startingFileNumber"], entryResults[2], PERSON_NODE_LEADER)
    # writeNodesToFiles(lvl2Nodes, FAN_10_FILEPATH + PERSON_NODE_LEADER, lvl2Results["startingFileNumber"])
    # for node in lvl2Nodes:
        # print(node)

    # BUILD LVL 3 NODES
    # ======================================
    lvl3Results = entryResults[3]
    lvl3Nodes = buildHigherNodes(lvl2Nodes, lvl2Results["startingFileNumber"], entryResults[3], PERSON_NODE_LEADER)
    writeNodesToFiles(lvl2Nodes, FAN_10_FILEPATH + PERSON_NODE_LEADER, lvl3Results["startingFileNumber"])

    # TODO: Seems to basically be working - but I know there's definitely
    # some issues where indices are off by a certain amount. Really need
    # to go through it all with a fine-tooth comb and see what's going on.
    # Might help if I just write it all to files so I have something more
    # tangible to observe

    return

def writeLeavesToFiles(LEAVES, LEADER):
    for i in range(0, len(LEAVES)):
        writeLeafToFile(LEAVES[i], LEADER + str(i))
    return

def writeNodesToFiles(NODES, LEADER, STARTING_NUMBER):
    start = 0
    end = len(NODES)
    for i in range(start, end):
        nodeNameNumber = str(STARTING_NUMBER + i)
        writeNodeToFile(NODES[i], LEADER + nodeNameNumber)
    return

def writeNodeToFile(node, filepath):
    f = open(filepath, "w")
    f.write(node["values"])
    f.close()
    return

def writeLeafToFile(item, filepath):
    f = open(filepath, "w")
    # f.write(item.strip())
    f.write(item["leftPointer"] + "," \
          + item["values"] + "," \
          + item["rightPointer"])

    f.close()
    # print("Writing: " + item["leftPointer"] + "," \
                      # + item["values"] + "," \
                      # + item["rightPointer"] \
                      # + "\nTo FP: " + filepath)
    return

# def buildRootNode(lowerNodes, lvlEntryResults, PREVIOUS_STARTING_NODE_NUMBER, LEADER):
    # STARTING_NODE_NUMBER = lvlEntryResults["startingFileNumber"]
    # node = dict()
    # ENTRIES_PER_FILE = lvlEntryResults["entriesPerFile"]
    # node["values"] = LEADER + str(PREVIOUS_STARTING_NODE_NUMBER) + ","
    # # node["leftmostTreeValue"] = lowerNodes[STARTING_NODE_NUMBER-PREVIOUS_STARTING_NODE_NUMBER]["leftmostTreeValue"]
#
    # start = (STARTING_NODE_NUMBER+1)
    # end = (STARTING_NODE_NUMBER + ENTRIES_PER_FILE)
    # print(start)
    # print(end)
    # for i in range(start, end):
        # # if i-PREVIOUS_STARTING_NODE_NUMBER >= len(lowerNodes):
            # # break
        # lowerNode = lowerNodes[i-PREVIOUS_STARTING_NODE_NUMBER]
        # # smallestleaf["values"].split(",")[1].split(";")[0]
        # addition = lowerNode["leftmostTreeValue"] \
                 # + "," + LEADER + str(i) + ","
        # node["values"] = node["values"] + addition
#
    # node["values"] = node["values"][0 : len(node["values"]) - 1]
#
    # return node

def buildHigherNodes(previousLevelNodes, previousLvlStartingFileNumber, \
                   lvlEntryResults, NODE_LEADER):
# def buildHigherNodes(previousLevelNodes, lvlEntryResults, \
                     # previousLvlStartingFileNumber, NODE_LEADER):
    nodes = list()
    entriesPerFile = lvlEntryResults["entriesPerFile"]
    end = lvlEntryResults["numFiles"]
    for i in range(end):
        # print(i)
        higherNode = buildHigherNode(previousLevelNodes, lvlEntryResults, \
                previousLvlStartingFileNumber + (i*entriesPerFile), \
                previousLvlStartingFileNumber, NODE_LEADER)
        # print(higherNode)
        nodes.append(higherNode)

    return nodes

def buildHigherNode(lowerNodes, lvlEntryResults, STARTING_NODE_NUMBER, PREVIOUS_STARTING_NODE_NUMBER, LEADER):
    # print("StartingNodeNumber: " + str(STARTING_NODE_NUMBER))
    # print("PrevStartNodeNum: " + str(PREVIOUS_STARTING_NODE_NUMBER))
    node = dict()
    ENTRIES_PER_FILE = lvlEntryResults["entriesPerFile"]
    node["values"] = LEADER + str(STARTING_NODE_NUMBER) + ","

    if lvlEntryResults["numFiles"] != 1:
        node["leftmostTreeValue"] = lowerNodes[STARTING_NODE_NUMBER-PREVIOUS_STARTING_NODE_NUMBER]["leftmostTreeValue"]

    start = (STARTING_NODE_NUMBER)+1
    end = (STARTING_NODE_NUMBER + ENTRIES_PER_FILE)
    # print(start)
    # print(end)
    for i in range(start, end):
        numLowerNodes = len(lowerNodes)
        # print("NumLowerNodes: " + str(numLowerNodes))
        # if i >= numLowerNodes:
        if i-PREVIOUS_STARTING_NODE_NUMBER >= numLowerNodes:
            # print("exiting")
            break
        lowerNode = lowerNodes[i-PREVIOUS_STARTING_NODE_NUMBER]
        # smallestleaf["values"].split(",")[1].split(";")[0]
        addition = lowerNode["leftmostTreeValue"] \
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
    entriesPerFile = lvl1EntryResults["entriesPerFile"]
    for i in range(0, len(leaves), entriesPerFile):
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
    leaf = {"values": leafEntries, "lowestValue": leafEntries.split(";")[0], "leftPointer": LEADER + str(leafNumber), "rightPointer": ""}
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
