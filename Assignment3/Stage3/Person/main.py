from sys import argv, exit
import tests
import dataLoader

NODE_HEADER = "person_node_"
LEAF_HEADER = "person_leaf_"

def main():
    FAN = 10
    # FAN = 200
    # tests.runTests()

    # messages = dataLoader.importMessages()
    persons = dataLoader.importPersons()
    leaves = buildLeaves(persons, FAN)

    # for leaf in leaves:
        # print(leaf)
    LEAVES_PER_NODE = determineLeavesPerNode(len(leaves), FAN)
    print(LEAVES_PER_NODE)

    lvl1Nodes = list()
    node = LEAF_HEADER + "0,"
    leaves.pop(0)
    for i in range(1, LEAVES_PER_NODE - 1):
        addition = leaves.pop(0).split(",")[1].split(";")[0] + "," + LEAF_HEADER + str(i+1) + ","
        node += addition

    print(node[0 : len(node) - 1])


    return

def buildLeaves(persons, FAN):
    ENTRIES_PER_LEAF = determineEntriesPerLeaf(len(persons), FAN)

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

def determineEntriesPerLeaf(numItems, fan):
    for tentativeNumEntriesPerLeaf in range(fan - 1, 0, -1):
        if entriesPerLeafAmountIsValid(numItems, tentativeNumEntriesPerLeaf):
            return tentativeNumEntriesPerLeaf

    exit("ERROR: No viable number of entries")
    return

def determineLeavesPerNode(numItems, fan):
    for tentativeNumEntriesPerLeaf in range(fan, 0, -1):
        if entriesPerLeafAmountIsValid(numItems, tentativeNumEntriesPerLeaf):
            return tentativeNumEntriesPerLeaf

    exit("ERROR: No viable number of entries")
    return

def entriesPerLeafAmountIsValid(numItems, numEntriesPerFile):
    remainder = (numItems/numEntriesPerFile) % 1
    return (remainder > 0.5) or (remainder == 0)

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
