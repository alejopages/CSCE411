import main

def runTests():
    determineNumberOfItemsToPutInFile1()
    determineNumberOfItemsToPutInFile2()
    determineNumberOfItemsToPutInFile3()
    determineNumberOfItemsToPutInFile4()
    determineNumberOfItemsToPutInFile5()
    determineNumberOfItemsToPutInFile6()
    return

def printTestResults(leader, passedTest):

    if passedTest:
        print(leader + "Passed")
    else:
        print(leader + "Failed")

    return

def determineNumberOfItemsToPutInFile1():
    leader = "Determine number of items to put in file - Test 1: "
    answer = main.determineNumberOfItemsToPutInFile(10, 6)
    CORRECT_ANSWER = 1

    printTestResults(leader, answer == CORRECT_ANSWER)

    return

def determineNumberOfItemsToPutInFile2():
    leader = "Determine number of items to put in file - Test 2: "
    answer = main.determineNumberOfItemsToPutInFile(9, 5)
    CORRECT_ANSWER = 1

    printTestResults(leader, answer == CORRECT_ANSWER)

    return

def determineNumberOfItemsToPutInFile3():
    leader = "Determine number of items to put in file - Test 3: "
    answer = main.determineNumberOfItemsToPutInFile(8, 4)
    CORRECT_ANSWER = 2

    printTestResults(leader, answer == CORRECT_ANSWER)

    return

def determineNumberOfItemsToPutInFile4():
    leader = "Determine number of items to put in file - Test 4: "
    answer = main.determineNumberOfItemsToPutInFile(6, 3)
    CORRECT_ANSWER = 2

    printTestResults(leader, answer == CORRECT_ANSWER)

    return

def determineNumberOfItemsToPutInFile5():
    leader = "Determine number of items to put in file - Test 5: "
    answer = main.determineNumberOfItemsToPutInFile(4, 2)
    CORRECT_ANSWER = 2

    printTestResults(leader, answer == CORRECT_ANSWER)

    return

def determineNumberOfItemsToPutInFile6():
    leader = "Determine number of items to put in file - Test 6: "
    answer = main.determineNumberOfItemsToPutInFile(2, 1)
    CORRECT_ANSWER = 2

    printTestResults(leader, answer == CORRECT_ANSWER)

    return

