import sys
class Graph():

    #This is a graph implementation that uses an adjacency matrix.
    #For all subsequent calls the table uses a list of vertices
    #which are used to specify which vertices in the graph that will be taken into account for working with my algorithms
    #Doing so allows us to use the graph with different sets of data.
    #
    #Dijkstras is a potential algorithm but I needed an algorithm that calculated the shortest path between all points.
    #

    #if I had to do this project again, I would work on my package delivery system traversal first instead of implementing it
    #while doing my sorting of packages beacause I ran into bugs most steps of the way that required more lines of code than
    #if I just did my traversal algorithm and then did my packaged sorting after.

    #as for data structures, I used lists, dictionaries, and hashmaps. I think that a database would be very efficient for storing
    #the data since it can be accessed much easier to pull data without having to store it in so many places.
    #for another alternative of my graph I could have used an adjacenty list instead of a matrix but that would be better used
    #for more sparse graphs or less edges so you can converve space. But since it was fully populated with edges it wouldn't save
    #anything. Matrixes are better for quick look ups but take up more space since it's a 2D array.

    def __init__(self, matrix):
        self.graph = matrix

    #takes in a source point to calculate the shortest distance between a list of potential next destinations
    #O(n)
    def findClosest(self, src, dests):
        currentClosest = -1
        currentClosestDistance = sys.maxsize

        for point in dests:
            distance = self.graph[src][point]
            if distance < currentClosestDistance:
                currentClosest = point
                currentClosestDistance = distance
        return (currentClosest,currentClosestDistance)

    #this is an implementation of the travelling salesman problem
    #it attempts to find the shortest path between the source point and all points in the vertex list
    #a greedy algorithm is easy to implement and can find a fairly optimal solution with a good time complexity
    #however it may not always find the most optimal solution
    #My algorithm is roughly o(VlogE) or roughly o(nlogn)
    #My program's memory complexity is linear
    #if more packages, trucks, or cities gets added,the total time will increase a little more than linearly
    #My algorithm's overhead when going between points is negligable given how simple it is.
    #one alternative could be recursive breadth first search which allows for some back tracking in it's decision making
    #another alternative could be brute-force which would eventually give you the most optimal distance but at the
    #expense of time complexity of O(n!) which is frankly terrible and with expanded data sets could take way too long

    #the following is O(n*the complexity of the findClosest function), so roughly O(nlogn) or O(VlogE)
    #This is the big algorithm of the program
    def travel(self, src, vertices):
        visitQueue = vertices
        dists = {}

        currentDistance = 0
        currentLocation = src
        while(visitQueue):
            closestInfo = self.findClosest(currentLocation, visitQueue)
            currentDistance = currentDistance + closestInfo[1]
            currentLocation = closestInfo[0]
            visitQueue.remove(currentLocation)
            dists[currentLocation] = currentDistance
        return dists

    #O(n)
    def pathLength(dists):
        currentMax = -1
        currentMaxNode = -1
        for node, distance in dists.items():
            if distance > currentMax:
                currentMax = distance
                currentMaxNode = node
        return (node, currentMax)

