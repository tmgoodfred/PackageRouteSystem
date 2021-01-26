class Truck:
    def __init__(self):
        self.speed = 18
        self.speedInSeconds = 0.005
        self.capacity = 16
        self.cargo = []
        self.distanceTraveled = 0
        self.startTime = 0

    def insertPackage(self, packageID):
        if not self.isAtMaxCap():
           self.cargo.append(packageID)
        else:
            print("Nope", packageID)

    def removePackage(self, packageID):
        self.cargo.remove(packageID)

    def getSize(self):
        return len(self.cargo)

    def maxCap(self):
        return self.capacity

    def getCargoInfo(self):
        return self.cargo

    def isAtMaxCap(self):
        if len(self.cargo) < self.capacity:
            return False
        else:
            return True

    def returnSinglePackage(self,n):
        return self.cargo[n]

    def increaseDistance(self,distance):
        self.distanceTraveled += distance

    def setDistance(self,distance):
        self.distanceTraveled = distance

    def getDistance(self):
        return self.distanceTraveled

    def setStartTime(self,seconds):
        self.startTime = seconds

    def getStartTime(self):
        return self.startTime