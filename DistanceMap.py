import csv
class DistanceMap:
    #pulls the distance information from my csv file and puts it into a list
    with open('Dest_Dist.csv') as csvfile:
        distanceInfo = csv.reader(csvfile, delimiter=',')
        distanceInfo = list(distanceInfo)
    #pulls the destination names from my csv file
    #O(n)
    with open('Dest_names.csv') as csvfile:
        addressDict = {} #this associates the index number to the string of the address to make associates the package
                         #address to the distance map easier
        nameInfo = csv.reader(csvfile, delimiter=',')
        nameInfo = list(nameInfo)
        for n in nameInfo:
            addressRaw = n[2]
            newString = []
            try:
                parenIndex = addressRaw.index("(")
                newString = addressRaw[0:parenIndex].rstrip()
            except ValueError as Error:
                newString = addressRaw
            addressDict[newString] = int(n[0])

    #O(n^2)
    #this fills out my matrix because the data given is only on the bottom half of the file
    #and this will make getting the distances easier on the program and will scale with more packages easily
    rawMatrix = distanceInfo
    matrix = [[0 for i in range(27)] for j in range(27)]
    for i in range(0, len(rawMatrix)):
        for j in range(0, len(rawMatrix[i])):
            if i >= j:
                parsed = float(rawMatrix[i][j])
                matrix[i][j] = parsed
                matrix[j][i] = parsed