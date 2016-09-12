# 6.00 Problem Set 11
# Name: Matt Graffunder
# Collaborators: None 
# Time Spent: 8:00
#
# ps11.py
#
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
from graph import Digraph, CampusDigraph, CampusEdge, Edge, Node

#
# Problem 2: Building up the Campus Map
#
# Write a couple of sentences describing how you will model the
# problem as a graph)
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    print "Loading map from file..."
    campusMap = CampusDigraph()

    campusMapFile = open(mapFilename, 'r')

    for line in campusMapFile:
        parts = line.split(' ')
        src = parts[0]
        dest = parts[1]

        if not campusMap.hasNode(src):
            campusMap.addNode(src)

        if not campusMap.hasNode(dest):
            campusMap.addNode(dest)

        edge = CampusEdge(src, dest, int(parts[2]), int(parts[3]))
        campusMap.addEdge(edge)
        
    return campusMap

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and the constraints
#

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
        
    shortest = shortestPath(digraph, start, end, maxTotalDist, maxDistOutdoors, [start], 0)

    if shortest == None:
        raise ValueError("No Path Found")
    
    return shortest

def pathLength(campusDigraph, path):
    dist = 0
    for i in xrange(len(path)-1):
        edge = campusDigraph.getEdge(path[i], path[i+1])
        dist += edge.getDist()

    return dist

def pathOutdoorLength(campusDigraph, path):
    dist = 0
    for i in xrange(len(path)-1):
        edge = campusDigraph.getEdge(path[i], path[i+1])
        dist += edge.getOutdoorDist()

    return dist
                           
def shortestPath(digraph, start, end, maxTotalDist, maxDistOutdoors, visited = [], depth = 0):
    raiseValueErrorIfNodeNotInGraph(digraph, start, end)
    
    path = [str(start)] #Create new List containing startNode

    #Found the goal node, return a list of one node
    if start == end:
        return path

    #Store the shortest path found so far
    shortest = None
    shortestPathLength = 1000000

    #Get the shortest path to the goal node for each child node
    for node in digraph.childrenOf(start):
        if (str(node) not in visited): #avoid cycles

            childrenVisited = visited + [str(node)] #Add to Visited to prevent cycling

            newPath = shortestPath(digraph, node, end, maxTotalDist, maxDistOutdoors, childrenVisited, depth +1)

            #Couldn't find a path to the goal node, keep checking the remaining children
            if newPath == None:
                continue

            #Prepend path to check the whole legnth
            newPath = path + newPath           

            #Found a path to the goal node, check if it's the shortest path found
            newPathLength = pathLength(digraph, newPath)
            newPathOutdoorLength = pathOutdoorLength(digraph, newPath)

            if ((shortest == None or newPathLength < shortestPathLength) and newPathLength <= maxTotalDist and newPathOutdoorLength <= maxDistOutdoors):                
                shortest = newPath
                shortestPathLength = newPathLength

    #if we found a path to the goal, return the startNode + shortest path
    if shortest != None:
        path = shortest        
    else:
        path = None #Couldn't find a path from any child node, return None

    return path

def raiseValueErrorIfNodeNotInGraph(graph, start, end):
    if not (graph.hasNode(start) and graph.hasNode(end)):
        raise ValueError('Start or end not in graph.')
#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #TODO
    pass

    shortest = shortestPathDirected(digraph, start, end, maxTotalDist, maxDistOutdoors, [start], 0)

    if shortest == None:
        raise ValueError("No Path Found")
    
    return shortest

def shortestPathDirected(digraph, start, end, maxTotalDist, maxDistOutdoors, visited = [], depth = 0, currentPath = [], bestPathLength = 100000):
    raiseValueErrorIfNodeNotInGraph(digraph, start, end)
    
    path = [str(start)] #Create new List containing startNode

    #Found the goal node, return a list of one node
    if start == end:
        return path

    #Store the shortest path found so far
    shortest = None
    shortestPathLength = 1000000

    #Check if current Path is longer than the best path
    currentPath = currentPath + path

    if pathLength(digraph, currentPath) > bestPathLength:
        #Return None if the current checked path is longer than the best found path.        
        return None

    #Get the shortest path to the goal node for each child node
    for node in digraph.childrenOf(start):
        if (str(node) not in visited): #avoid cycles

            childrenVisited = visited + [str(node)] #Add to Visited to prevent cycling

            newPath = shortestPathDirected(digraph, node, end, maxTotalDist, maxDistOutdoors, childrenVisited, depth +1, currentPath, bestPathLength)

            #Couldn't find a path to the goal node, keep checking the remaining children
            if newPath == None:
                continue

            #Prepend path to check the whole length
            newPath = path + newPath           

            #Found a path to the goal node, check if it's the shortest path found
            newPathLength = pathLength(digraph, newPath)
            newPathOutdoorLength = pathOutdoorLength(digraph, newPath)

            if ((shortest == None or newPathLength < shortestPathLength) and newPathLength <= maxTotalDist and newPathOutdoorLength <= maxDistOutdoors):                
                shortest = newPath
                shortestPathLength = newPathLength

                if newPath[0] == start and newPath[-1] == end:
                    bestPathLength = shortestPathLength

    #if we found a path to the goal, return the startNode + shortest path
    if shortest != None:
        path = shortest        
    else:
        path = None #Couldn't find a path from any child node, return None

    return path


# Uncomment below when ready to test
if __name__ == '__main__':
    # Test cases
    digraph = load_map("mit_map.txt")

    LARGE_DIST = 1000000

    # Test case 1
    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    brutePath1 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
    dfsPath1 = directedDFS(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath1
    print "Brute-force: ", brutePath1
    print "DFS: ", dfsPath1

    # Test case 2
    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    brutePath2 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, 0)
    dfsPath2 = directedDFS(digraph, '32', '56', LARGE_DIST, 0)
    print "Expected: ", expectedPath2
    print "Brute-force: ", brutePath2
    print "DFS: ", dfsPath2

    # Test case 3
    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    brutePath3 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
    dfsPath3 = directedDFS(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
    print "Brute-force: ", brutePath3
    print "DFS: ", dfsPath3

    # Test case 4
    print "---------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
    brutePath4 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, 0)
    dfsPath4 = directedDFS(digraph, '2', '9', LARGE_DIST, 0)
    print "Expected: ", expectedPath4
    print "Brute-force: ", brutePath4
    print "DFS: ", dfsPath4

    # Test case 5
    print "---------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
    brutePath5 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
    dfsPath5 = directedDFS(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath5
    print "Brute-force: ", brutePath5
    print "DFS: ", dfsPath5

    # Test case 6
    print "---------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    brutePath6 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, 0)
    dfsPath6 = directedDFS(digraph, '1', '32', LARGE_DIST, 0)
    print "Expected: ", expectedPath6
    print "Brute-force: ", brutePath6
    print "DFS: ", dfsPath6

    # Test case 7
    print "---------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(digraph, '8', '50', LARGE_DIST, 0)
    except ValueError:
        bruteRaisedErr = 'Yes'
    
    try:
        directedDFS(digraph, '8', '50', LARGE_DIST, 0)
    except ValueError:
        dfsRaisedErr = 'Yes'
    
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

    # Test case 8
    print "---------------"
    print "Test case 8:"
    print "Find the shortest-path from Building 10 to 32 without walking"
    print "more than 100 meters in total"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(digraph, '10', '32', 100, LARGE_DIST)
    except ValueError:
        bruteRaisedErr = 'Yes'
    
    try:
        directedDFS(digraph, '10', '32', 100, LARGE_DIST)
    except ValueError:
        dfsRaisedErr = 'Yes'
    
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

