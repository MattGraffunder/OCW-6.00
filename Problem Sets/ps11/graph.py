# 6.00 Problem Set 11
#
# graph.py
#
# A set of data structures to represent graphs
#

class Node(object):
   def __init__(self, name):
       self.name = str(name)
   def getName(self):
       return self.name
   def __str__(self):
       return self.name
   def __repr__(self):
      return self.name
   def __eq__(self, other):
      return not other == None and self.name == other.name
   def __ne__(self, other):
      return not self.__eq__(other)

class Edge(object):
   def __init__(self, src, dest):
       self.src = src
       self.dest = dest
   def getSource(self):
       return self.src
   def getDestination(self):
       return self.dest
   def __str__(self):
       return str(self.src) + '->' + str(self.dest)

class CampusEdge(Edge):
   def __init__(self, src, dest, dist, outdoorDist):
      Edge.__init__(self, src, dest)
      self.dist = dist
      self.outdoorDist = outdoorDist
   def getDist(self):
      return self.dist
   def getOutdoorDist(self):
      return self.outdoorDist
   def __str__(self):
      return Edge.__str__(self) + ", Dist: " + str(self.dist) + " Outside: " + str(self.outdoorDist)

class Digraph(object):
   """
   A directed graph
   """
   def __init__(self):
       self.nodes = set([])
       self.edges = {}
   def addNode(self, node):
       if node in self.nodes:
           raise ValueError('Duplicate node')
       else:
           self.nodes.add(node)
           self.edges[node] = []
   def addEdge(self, edge):
       src = edge.getSource()
       dest = edge.getDestination()
       if not(src in self.nodes and dest in self.nodes):
           raise ValueError('Node not in graph')
       self.edges[src].append(dest)
   def childrenOf(self, node):
       return self.edges[node]
   def hasNode(self, node):
       return node in self.nodes
   def __str__(self):
       res = ''
       print len(self.edges)
       print len(self.nodes)
       for k in self.edges:
           for d in self.edges[k]:
               res = res + str(k) + '->' + str(d) + '\n'
       return res[:-1]

class CampusDigraph(Digraph):
   def __init__(self):
      Digraph.__init__(self)
      self.nodeEdges = {}
   def addNode(self, node):
      Digraph.addNode(self, node)
      self.nodeEdges[node] = {}
      #print "Add node: ", node
   def getNodeByName(self, nodeName):
      for node in self.nodes:
         if node == nodeName:
            return node

      return None
   def addEdge(self, edge):
      Digraph.addEdge(self, edge)
      self.nodeEdges[edge.getSource()][edge.getDestination()] = edge
      #print edge.getSource(), " ", self.nodeEdges[edge.getSource()]
      #print edge.getSource(), ' ', edge.getDestination()
   def getEdges(self, node):
      return self.nodeEdges[node]
   def getEdge(self, fromNode, toNode):
      return self.nodeEdges[fromNode][toNode]
##      for dests in self.nodeEdges[fromNode]:
##         if dests.getName() == nodeName:
##            return node
##
##      return None
   def __str__(self):
      res = ''
      nodes = list(self.nodes)
      nodes.sort()
##      for k in self.nodeEdges:
      for k in nodes:
           for d in self.nodeEdges[k]:
               res = res + str(self.nodeEdges[k][d]) + '\n'
      return res[:-1]
      
