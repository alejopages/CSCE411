from sys import argv, exit
import dataLoader
from math import ceil
import json
from timeit import default_timer as timer

if len(argv) != 2:
    exit("ERROR: Invalid # of arguments provided")

if argv[1] == "10":
    FAN = 10
    FILEPATH_LEADER = "persons/fan10/"
elif argv[1] == "200":
    FAN = 200
    FILEPATH_LEADER = "persons/fan200/"
else:
    exit("ERROR: Provide either '10' or '200' as an argument")

NODE_LEADER = "person_node_"
LEAF_LEADER = "person_leaf_"

def main():

    start = timer()

    # IMPORT DATA
    # ======================================
    print("LOADING DATA" \
        + "\n======================================")
    data = dataLoader.importPersons()
    processData(data)

    end = timer()
    print("Processing Time: " + str(end - start))
    return

def processData(data):
    NUM_ITEMS = len(data)

    # DETERMINE ENTRY RESULTS
    # ======================================
    entryResults = getEntryResults(NUM_ITEMS, FAN)
    print("PROCESSING ENTRY RESULTS" \
        + "\n======================================")
    for item in entryResults:
        print(item)

    # BUILD LEAVES
    # ======================================
    print("BUILDING LEAVES" \
        + "\n======================================")
    lvl0Results = entryResults[0]
    leaves = buildLeaves(data, FAN, \
             lvl0Results["entriesPerFile"], LEAF_LEADER)
    writeLeavesToFiles(leaves, FILEPATH_LEADER + LEAF_LEADER)


    # BUILD LVL 1 NODES
    # ======================================
    print("BUILDING NODE LVL: 1" \
        + "\n======================================")
    lvl1Results = entryResults[1]
    lvl1Nodes = buildLvl1Nodes(leaves, lvl1Results, \
                               LEAF_LEADER, NODE_LEADER)
    writeNodesToFiles(lvl1Nodes, FILEPATH_LEADER + NODE_LEADER, lvl1Results["startingFileNumber"])

    # BUILD LVL 2 NODES
    # ======================================
    # lvl2Results = entryResults[2]
    # lvl2Nodes = buildHigherNodes(lvl1Nodes, lvl1Results["startingFileNumber"], entryResults[2], PERSON_NODE_LEADER)
    # writeNodesToFiles(lvl2Nodes, FILEPATH_LEADER + PERSON_NODE_LEADER, lvl2Results["startingFileNumber"])

    # BUILD LVL 3 NODES
    # ======================================
    # lvl3Results = entryResults[3]
    # lvl3Nodes = buildHigherNodes(lvl2Nodes, lvl2Results["startingFileNumber"], entryResults[3], PERSON_NODE_LEADER)
    # writeNodesToFiles(lvl3Nodes, FILEPATH_LEADER + PERSON_NODE_LEADER, lvl3Results["startingFileNumber"])

    # BUILD ALL NODES
    # ======================================
    allNodes = list()
    allNodes = allNodes + lvl1Nodes
    prevNodes = lvl1Nodes
    for i in range(2, len(entryResults)):
        print("BUILDING NODE LVL: " + str(i) \
            + "\n======================================")
        prevLvlResults = entryResults[i-1]
        lvlResults = entryResults[i]
        lvlNodes = buildHigherNodes(prevNodes, \
                   prevLvlResults["startingFileNumber"], \
                   lvlResults, NODE_LEADER)
        writeNodesToFiles(lvlNodes, FILEPATH_LEADER + NODE_LEADER, lvlResults["startingFileNumber"])
        allNodes = lvlNodes + allNodes
        prevNodes = lvlNodes

    return

def writeLeavesToFiles(LEAVES, LEADER):
    for i in range(0, len(LEAVES)):
        writeLeafToFile(LEAVES[i], LEADER + str(i))
    return

def writeNodesToFiles(NODES, LEADER, STARTING_NUMBER):
    start = 0
    end = len(NODES)
    for i in range(start, end):
        # print(i)
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
        if i >= len(leaves):
            break
        leaf = leaves[i]
        # smallestleaf["values"].split(",")[1].split(";")[0]
        addition = leaf["lowestValue"] \
                 + "," + LEADER + str(i) + ","
        node["values"] = node["values"] + addition

    node["values"] = node["values"][0 : len(node["values"]) - 1]
    return node

def buildLeaves(data, FAN, ENTRIES_PER_LEAF, LEADER):
    # ENTRIES_PER_LEAF = determineEntriesPerLeafFile(len(data), FAN)
    # ENTRIES_PER_LEAF = determineEntriesPerLeafFile(len(data), FAN)

    leaves = list()

    firstLeaf = getFirstLeaf(data, ENTRIES_PER_LEAF, LEADER)
    leaves.append(firstLeaf)

    getInnerLeaves(leaves, data, ENTRIES_PER_LEAF, FAN, LEADER)

    lastLeaf = getLastLeaf(data, ENTRIES_PER_LEAF, len(leaves) - 1, LEADER)
    leaves.append(lastLeaf)

    return leaves

def getLastLeaf(data, ENTRIES_PER_LEAF, leafNumber, LEADER):
    leafEntries = getLeafEntries(data, ENTRIES_PER_LEAF)
    # lastLeaf = wrapLastLeafEntryInLeafPointers(lastLeaf, leafNumber)
    leaf = {"values": leafEntries, "lowestValue": leafEntries.split(";")[0], "leftPointer": LEADER + str(leafNumber), "rightPointer": ""}
    return leaf

def getInnerLeaves(leaves, data, ENTRIES_PER_LEAF, FAN, LEADER):
    leafNumber = 0
    while len(data) > FAN:
        entries = getLeafEntries(data, ENTRIES_PER_LEAF)
        # leaf = wrapLeafEntriesInLeafPointers(entries, count)
        leaf = {"values": entries, "lowestValue": entries.split(";")[0], "leftPointer": LEADER + str(leafNumber), "rightPointer": LEADER + str(leafNumber+2)}
        leaves.append(leaf)
        leafNumber += 1

    return

def getFirstLeaf(data, ENTRIES_PER_LEAF, LEADER):
    leafEntries = getLeafEntries(data, ENTRIES_PER_LEAF)
    # firstLeaf = wrapFirstLeafEntryInLeafPointers(firstLeaf)
    leaf = {"values": leafEntries, "lowestValue": leafEntries.split(";")[0], "leftPointer": "", "rightPointer": LEADER + "1"}
    return leaf

def wrapLastLeafEntryInLeafPointers(leafEntries, leafNumber):
    line = LEAF_LEADER + str(leafNumber) + ","
    line += leafEntries
    line += ","

    return line

def wrapFirstLeafEntryInLeafPointers(leafEntries):
    line = ","
    line += leafEntries
    line += "," + LEAF_LEADER + "1"

    return line

def wrapLeafEntriesInLeafPointers(leafEntries, leafNumber):
    line = LEAF_LEADER + str(leafNumber) + ","
    line += leafEntries
    line += "," + LEAF_LEADER + str(leafNumber + 2)

    return line

def getLeafEntries(data, entriesPerLeaf):
    s = ""
    for i in range(entriesPerLeaf):
        if len(data) != 0:
            s += personToString(data.pop(0)) + ","

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

def determineNumberOfItemsToPutInFile(numItemsLeft, numPointersLeft):
    return int(numItemsLeft/numPointersLeft)

if __name__ == "__main__":
    main()
