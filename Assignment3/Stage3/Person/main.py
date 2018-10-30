from sys import argv, exit
import tests
import dataLoader

def main():
    # tests.runTests()

    persons = dataLoader.importPersons()
    print(len(persons))
    for person in persons:
        print(person)
    # messages = dataLoader.importMessages()


    return

def determineNumberOfItemsToPutInFile(numItemsLeft, numPointersLeft):
    return int(numItemsLeft/numPointersLeft)

if __name__ == "__main__":
    main()
