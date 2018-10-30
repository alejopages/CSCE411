
def main():
    # data = loadData("data3.txt")
    # data = loadData("data2.txt")
    data = loadData("data.txt")

    for entry in data:
        print(entry["id"] + ": " + entry["name"])
        if "state" in entry:
            print(entry["state"] + " - " + entry["city"])
            # for message in entry["messages"]:
                # print(message)

    return

def loadData(filepath):
    people = list()

    sections = _loadSections(filepath)
    for section in sections:
        # print("section:")
        # print(section)
        person = dict()
        person["id"] = _extractValue(section[0])
        person["name"] = _extractValue(section[1])

        # print(_extractValue(section[2]))
        locationTokens = _extractValue(section[2]).split(",")
        # print(locationTokens)

        if len(locationTokens) == 3:
            if locationTokens[1].strip() != "":
                person["state"] = locationTokens[1].strip()
                person["city"] = locationTokens[0].strip()

        person["messages"] = _buildMessages(section)
        people.append(person)

    return people

def _buildMessages(section):
    messages = list()
    message = dict()

    isFirstMessage = True
    for i in range(3, len(section)):
        line = section[i]
        value = _extractValue(line)
        # print(value)
        if _isTimestamp(i):
            # print("Timestamp Line")
            tokens = value.split(" ")
            if not isFirstMessage:
                # print("Not first message")
                messages.append(message)
                message = dict()
            message["date"] = _convertDateFormat(tokens[0])
            message["time"] = tokens[1]
            isFirstMessage = False
        else:
            # print("Message Line")
            message["value"] = value

    if "date" in message:
        messages.append(message)
    return messages

def _convertDateFormat(date):
    newDate = ""
    tokens = date.split("/")
    newDate += tokens[2] + "-"
    newDate += tokens[0] + "-"
    newDate += tokens[1]

    return newDate

def _extractValue(line):
    start = line.index(":") + 2
    return line[start : len(line)]

def _isTimestamp(number):
    return not (number % 2 == 0)

def _loadSections(filepath):
    f = open(filepath, 'r')
    NEW_SECTION_HEADER = "ID:"

    sections = list()
    section = list()
    isFirstSection = True
    for line in list(f):
        strippedLine = line.strip()
        if _lineIsIrrelevant(strippedLine):
            continue

        linePrefix = line[0:3]
        if linePrefix == NEW_SECTION_HEADER:
            if isFirstSection:
                section.append(strippedLine)
                isFirstSection = False
            elif not isFirstSection:
                sections.append(section)
                section = list()
                section.append(strippedLine)
        else:
            section.append(strippedLine)

    if section[0] != "":
        sections.append(section)

    return sections

def _lineIsIrrelevant(line):
    return (line == "") or (line[0:12] == "Process time")

if __name__ == "__main__":
    main()
