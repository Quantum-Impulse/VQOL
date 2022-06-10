import csv

while True:
    try:
        fileName = input('Enter the result file you want to read: ')
        file = open(fileName, 'r')
    except:
        print("That is not a valid file, please try again. Be sure to include the .csv at the end of the file name.")
        print()
        continue
    else:
        break
csv_filename = fileName

# returns all the possible cominations of clicks you can get from the detectors
def allCombinations(detIndex, numDet, currPattern, allPatterns):
    if numDet == 0:
        return
    options = ['C', 'N']
    for i in options:
        currPattern[detIndex] = i
        str = ""
        string = str.join(currPattern)
        if not string in allPatterns:
            allPatterns[string] = makeDict(string)
        allCombinations(detIndex + 1, numDet - 1, currPattern, allPatterns)
        currPattern[detIndex] = 'N'
    return allPatterns

# make the dictionary for each possible detector combination outcome
def makeDict(pattern):
    countSpot = []
    for detNum in range(len(pattern)):
        if pattern[detNum] == 'C':
            countSpot.append(detNum + 1)
    dict = {'detectors' : countSpot, 'counts' : 0}
    return dict

def printResultingCounts(allCombs):
    for k in sorted(allCombs, key=lambda i: (len(allCombs[i]["detectors"]), i)):
        detectors = allCombs[k]['detectors']
        countNum = allCombs[k]['counts']
        if len(detectors) == 0:
            pass
        elif len(detectors) == 1:
            print("Detector " + str(detectors[0]) + " only: " + str(countNum))
        else:
            detectorList = "Detectors " + str(detectors[0])
            for x in detectors[1:]:
                detectorList += " & " + str(x)
            print(detectorList + ": " + str(countNum))

header = []
print("RESULTS")
with open(csv_filename, mode='r') as csv_file:
    csvreader = csv.reader(csv_file)
    header = next(csvreader)
    numDetectors = 0
    for num in header[1:]:
        numDetectors += 1
    pattern = []
    for i in range(numDetectors):
        pattern.append('N')
    allCombs = allCombinations(0, numDetectors, pattern, {})
    for row in csvreader:
        time = row[0]
        countPat = ''
        for i in range(1, numDetectors + 1):
            if row[i] == '1':
                countPat += 'C'
            else:
                countPat += 'N'
        counts = allCombs.get(countPat)
        currCount = counts['counts']
        counts['counts'] = currCount + 1
        allCombs[countPat] = counts
    printResultingCounts(allCombs)



