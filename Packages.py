from HashTableAndMap import HashMap
from Truck import Truck
from PathMap import Graph
from DistanceMap import DistanceMap

import csv
class Packages:
    def convertToHours(seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)

    truck1 = Truck()
    truck2 = Truck()
    truck1trip2 = Truck()
    packageHashTable = HashMap()
    packageBackLog = []
    #this opens the package information and puts the data into my hashmap
    #O(n)
    with open('package_info2.csv') as packageInfo:
        packages = csv.reader(packageInfo, delimiter=',')
        for row in packages:
            packIdNum = row[0]
            delivAdd = row[1]
            delivCity = row[2]
            delivState = row[3]
            delivZip = row[4]
            delivDeadline = row[5]
            packWeight = row[6]
            packNote = row[7]
            delivStatus = "AT_HUB"  # setting the default status to AT_HUB
            delivTime = 0 #standard is 0 because it will need to be increased
            key = packIdNum
            packageData = [packIdNum, delivAdd, delivCity, delivState, delivZip, delivDeadline, packWeight, packNote,
                           delivStatus, delivTime]
            value = packageData
            packageHashTable.insert(key, value)
            packageBackLog.append(packageData)

    packages = 0
    truck1.setStartTime(28800) #set start time to 8:00AM
    truck2.setStartTime(32700) #set start time to 9:05AM

    #this stores the package ID's  for each truck
    truck1listo = []
    truck2listo = []
    truck1trip2listo = []

    #this stores the address of each package for each truck
    truck1add = []
    truck1trip2add = []
    truck2add = []

    #this stores the zip codes of each package for each truck
    truck1zip = []
    truck2zip = []
    truck1trip2zip = []

    #this sorts the packages into each truck
    #O(n)
    for value in packageBackLog:
        #THIS IS IMPORTANT - this takes all the packages with deadlines that DONT have any other requirements
        #and puts them in truck1 to go out ASAP
        if value[5] != 'EOD':
            if 'Must' in value[7] or 'NA' in value[7]:
                truck1.insertPackage(value)
                truck1listo.append(int(value[0]))
                truck1add.append(value[1])
                truck1zip.append(value[4])
        #this takes all packages delayed on flight and puts them on the second truck which will leave when they arrive
        if 'Delayed' in value[7]:
            truck2.insertPackage(value)
            truck2listo.append(int(value[0]))
            truck2add.append(value[1])
            truck2zip.append(value[4])
        #for all packages that specify that they be on truck 2, this puts them on truck 2
        if 'Can only' in value[7]:
            truck2.insertPackage(value)
            truck2listo.append(int(value[0]))
            truck2add.append(value[1])
            truck2zip.append(value[4])
        #this puts the wrong addressed package into the last truck since the package is updated later in the morning
        if 'Wrong' in value[7]:
            value[1] = '410 S State St'
            value[4] = '84111'
            truck1trip2.insertPackage(value)
            truck1trip2listo.append(int(value[0]))
            truck1trip2add.append(value[1])
            truck1trip2zip.append(value[4])
        #this takes all packages that don't have any extra limits and puts them into truck 2 and the 1st truck's 2nd trip
        #at equal rates so they dont fill one truck too fast
        if value not in truck1.getCargoInfo() and value not in truck2.getCargoInfo() and value not in truck1trip2.getCargoInfo():
            check1 = truck2.getSize()
            check2 = truck1trip2.getSize()
            if check1 > check2:
                truck1trip2.insertPackage(value)
                truck1trip2listo.append(int(value[0]))
                truck1trip2add.append(value[1])
                truck1trip2zip.append(value[4])
            else:
                truck2.insertPackage(value)
                truck2listo.append(int(value[0]))
                truck2add.append(value[1])
                truck2zip.append(value[4])

    #these gives me a list of the address indices
    #O(n)
    vertName1 = []
    for n in truck1add:
        vertName1.append(int(DistanceMap.addressDict[n]))

    vertName2 = []
    for n in truck2add:
        vertName2.append(int(DistanceMap.addressDict[n]))

    vertName1trip2 = []
    for n in truck1trip2add:
        vertName1trip2.append(int(DistanceMap.addressDict[n]))

    #this sets the package IDs into a new list of vertices
    truck1vert = truck1listo
    truck2vert = truck2listo
    truck1trip2vert = truck1trip2listo

    #this puts the distance matrix into a list
    truckGraph = Graph(DistanceMap.matrix)
    #this function call gives me an int to int dictionary where the value is the distance from the source node to each index postion in the path
    distancesTruck1 = truckGraph.travel(0, vertName1)
    distancesTruck1trip2 = truckGraph.travel(0, vertName1trip2)

    truck1times = []
    truck2times = []
    truck1trip2times = []
    packageDistance = []

    #this increases the distance each package travels into a variable to track the delivery length
    #O(n)
    for package in truck1.getCargoInfo():
        packageDistance = distancesTruck1[DistanceMap.addressDict[package[1]]]
        # this takes the delivery time in seconds and turns it into the more readable HH:MM:SS time format
        package[9] = convertToHours(int(packageDistance/truck1.speedInSeconds + truck1.startTime))
        package[8] = "DELIVERED" #sets delivery state to delivered
    truck1total = Graph.pathLength(distancesTruck1) #sets the total trip distance of the truck
    truck1roundtrip = truck1total[1] + truckGraph.graph[truck1total[0]][0]
    truck1total = truck1roundtrip/truck1.speedInSeconds
    truck1.setDistance(truck1roundtrip)

    #truck2 is divided up to make sure packages with deadlines get delivered first and then those without deadlines go after
    #O(n)
    priorityPackages = []
    priorityDests = []
    eodPackages = []
    eodDests = []
    for package in truck2.getCargoInfo():
        if package[5] != "EOD":
            priorityDests.append(DistanceMap.addressDict[package[1]])
            priorityPackages.append(package)
        else:
            eodDests.append(DistanceMap.addressDict[package[1]])
            eodPackages.append(package)

    #O(n)
    priorityDistances = truckGraph.travel(0, priorityDests)
    prioTrip = Graph.pathLength(priorityDistances)
    eodDistances = truckGraph.travel(prioTrip[0], eodDests)
    eodTrip = Graph.pathLength(eodDistances)
    truck2times = []
    for package in priorityPackages:
        packageDistance = priorityDistances[DistanceMap.addressDict[package[1]]]
        package[9] = convertToHours(int(packageDistance / truck2.speedInSeconds + truck2.startTime))
        package[8] = "DELIVERED"
    for package in eodPackages:
        packageDistance = eodDistances[DistanceMap.addressDict[package[1]]]
        package[9] = convertToHours(int((packageDistance+prioTrip[1]) / truck2.speedInSeconds + truck2.startTime))
        package[8] = "DELIVERED"
    truck2total = prioTrip[1]+eodTrip[1]
    truck2roundtrip = truck2total + truckGraph.graph[eodTrip[0]][0]
    truck2.setDistance(truck2roundtrip)

    x = max(truck1.getStartTime()+truck1total,37800) #if the time the first truck gets back is earlier than the time the new package's
    truck1trip2.setStartTime(x)                      #address change time, then wait until 10:30AM to take off
    truck1trip2times = []
    for package in truck1trip2.getCargoInfo():
        packageDistance = distancesTruck1trip2[DistanceMap.addressDict[package[1]]]
        package[9] = convertToHours(int(packageDistance / truck1trip2.speedInSeconds + truck1trip2.startTime))
        package[8] = "DELIVERED"
    truck1trip2total = Graph.pathLength(distancesTruck1trip2)
    truck1trip2roundtrip = truck1trip2total[1] + truckGraph.graph[truck1trip2total[0]][0]
    truck1trip2.setDistance(truck1trip2roundtrip)


    def __init__(self):
        self.CloneQueue = []
        self.InitQueue = []

    def addToClone(self,value):
        self.CloneQueue.append(value)

    def addToInit(self,value):
        self.InitQueue.append(value)

    def getInitData(self):
        return self.InitQueue

    def getCloneData(self):
        return self.CloneQueue

    def processRemoval(self, clone, init):
        for n in clone:
            for x in init:
                if n == x:
                    init.remove(x)

    def simpleRemove(self,value):
        self.InitQueue.remove(value)

