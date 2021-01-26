# Tyler Goodfred #931149
from HashTableAndMap import HashMap
from Packages import Packages

#The program's overall time complexity is O(nlogn) or O(VlogE)

packageHashTable = HashMap()
truck1 = Packages.truck1
truck2 = Packages.truck2
truck1trip2 = Packages.truck1trip2
packageBacklog = Packages.packageBackLog

#this is a conversion function that takes seconds and returns hours in a HH:MM:SS format
def convertToHours(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def convertToSeconds(time_str):
    h, m, s = time_str.split(':')
    return int(h)*3600+int(m)*60+int(s)

#truck1 goes out immedietely
#truck2 leaves at 9:05
#truck1trip2 goes out after truck1 comes back, at the earliest 10:20

time = 28800
continueCheck = 1
continueCheck2 = 1
continueCheck3 = 1
firstTime = 0
secondTime = 0
print("Total distance travelled: %.1f" % (truck1.getDistance()+truck2.getDistance()+truck1trip2.getDistance()), " miles"
                      "\nTruck 1 with 2 trips travelled:",(truck1.getDistance()+truck1trip2.getDistance()), " miles"
                      "\nTruck 2 with 1 trip travelled: %.1f" % truck2.getDistance(), " miles")

isCorrect = True
#O(n)
#this checks to make sure all packages are delivered on time
for n in Packages.packageBackLog:
    packageDueTime = n[5]
    if packageDueTime != 'EOD':
        deliverTime = convertToSeconds(n[9])
        if int(deliverTime) > convertToSeconds(packageDueTime):
            isCorrect = False
            break

if isCorrect:
    print("All packages delivered on time!")
else:
    print("Some packages not delivered on time")

dataCheck = int(input("\nWhat information would you like to see? (please enter the corresponding number)"
                      "\n1. Look up by package information"
                      "\n2. Look up packages delivered by a certain time"
                      "\n... "))
#O(n)
if dataCheck == 1:
    while continueCheck != 0:
        dataCheck1 = int(input("Please enter a package number (or '0' to stop looking): "))
        if dataCheck1 == 0:
            continueCheck = 0
            break
        for value in packageBacklog:
            if dataCheck1 == int(value[0]):
                print(value)
                break
        else:
            print("Package does not exist, please enter a different number")
            continueCheck = 1
#o(n)
elif dataCheck == 2:
    while continueCheck2 != 0 and continueCheck3 != 0:
        dataCheck2 = str(input("Please enter a first time in 24HR format (10:00:00, 14:00:00, etc): "))
        timeToComp = convertToSeconds(dataCheck2)
        if 28800 <= timeToComp < 61200: #if the time is between 8:00AM and 5:00PM
            firstTime = timeToComp
            continueCheck2 = 0
        else:
            print("This time is outside of business hours (8:00AM to 5:00PM), please enter a different time")
            continueCheck2 = 1

        dataCheck3 = str(input("Please enter a second time after the first in 24HR format (10:00, 14:00, etc): "))
        timeToComp2 = convertToSeconds(dataCheck3)
        if firstTime < timeToComp2 <= 61200:  # if the time is between 8:00AM and 5:00PM
            secondTime = timeToComp2
            continueCheck3 = 0
        elif timeToComp2 < firstTime:
            print("Please enter a time after the first time given")
            continueCheck3 = 1
        else:
            print("This time is outside of business hours (8:00AM to 5:00PM), please enter a different time")
            continueCheck3 = 1

    #this will print all packages and will mark with have been delivered and which haven't
    for n in packageBacklog:
        deliveryTime = n[9]
        deliveryStatus = n[8]
        #if you want to print *only* the packages within a certain amount of time you can do the following:
        #if firstTime < convertToSeconds(str(deliveryTime)) < secondTime:
        #    print(n)
        if convertToSeconds(str(deliveryTime)) > secondTime:
            n[8] = 'NOT DELIVERED'
        print(n)