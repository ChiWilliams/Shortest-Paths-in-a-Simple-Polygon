#Here, we make a tree class for the shortest path tree
from math import *


class PathTree:
    def __init__(self,root):
        self.root=root
    def get_root(self):
        return self.root
    def print(self):
        self.root.printSubtree()
    def makeDictionary(self):
        dict = {}
        self.root.addDictionary(dict)
        return dict
    def makeEdgeDictionary(self):
        dict = {}
        self.root.addEdgeDictionary(dict)
        return dict
    #this method adds the values of self.far_edge and self.far_length to the entire tree
    #input: self (the tree object)
    #output: none
    #side effects: every vertex in the tree will gain a self.far_length value (and self.far_edge)
    #warning: EDGES NEED TO BE ADDED FIRST
    def addLengths(self):
        self.root.addLengths()


class PathTreeVertex:
    def __init__(self,coordinates):
        #print("the coordinates are",coordinates)
        self.childlist = []
        self.edgeList = []
        self.parent = None
        self.far_edge = None
        self.far_length = None
        self.coordinates=coordinates
        self.x=coordinates[0]
        self.y=coordinates[1]
    def __str__(self):
        return "TREEVertex at "+str(self.coordinates)
    def __repr__(self):
        return str(self)
    #this method returns the coordinates
    def cds(self):
        return self.coordinates
    def printSubtree(self):
        print(self)
        for node in self.childlist:
            node.printSubtree()
    def getChildren(self):
        return self.childlist
    def getEdges(self):
        return self.edgeList
    def getParent(self):
        return self.parent
    def isLeaf(self):
        if self.childlist == []:
            return True
        else:
            return False
    def childDict(self):
        dict = {}
        for child in self.childlist:
            dict[child.cds()]=child
        return dict
    def addDictionary(self,dict):
        dict[self.coordinates]=self
        for child in self.childlist:
            child.addDictionary(dict)
    def addEdgeDictionary(self,dict):
        for edge in self.edgeList:
            dict[edge.cds()] = edge
        for child in self.childlist:
            child.addEdgeDictionary(dict)
    #this method is the Vertex equivalent of the Tree Method
    #it recursively calls itself on the nodes children 
    #inputs: self (the current vertex we are at)
    #output: self.far_length (an int): the updated value of the farthest length in the tree
    #side effects: every member of the subtree whose root is this node will gain this value
    def addLengths(self):
        if self.edgeList == []:
            #choose negative infinity
            self.far_length = -inf
        else:
            self.far_edge=self.edgeList[0]
            self.far_length=0
        if self.isLeaf():
            return self.far_length
        else:
            compare_list = [(self,self.far_length)]
            for child in self.childlist:
                #something subtle here: in computing the far_length, we also recursively call this fnct
                #So child.addLengths will update the subtree
                compare_list.append((child,dist(self.cds(),child.cds())+child.addLengths()))
            max_vert = max(compare_list, key=lambda vert: vert[1])[0]
            #print("At",self,"farthest vert is",max_vert)
            self.far_length = max_vert.far_length+dist(self.cds(),max_vert.cds())
            self.far_edge = max_vert.far_edge
            return self.far_length

class PathTreeEdge:
    def __init__(self,v1,v2):
        self.v1=v1
        self.v2=v2
        self.coordinates = (v1.cds(),v2.cds())
        self.parent = None
    def __str__(self):
        return "Edge btw "+str(self.v1.cds())+" and "+str(self.v2.cds())
    def __repr__(self):
        return str(self)
    def cds(self):
        return self.coordinates

#This was for testing

# top = PathTreeVertex((0,0))
# tree = PathTree(top)
# top2 = PathTreeVertex(top.cds())
# top2.parent = top
# top.childlist.append(top2)
# tree.print()

# row1 = []
# row2 = []
# for i in range(0,4):
#     row1.append(PathTreeVertex((1,i)))
#     row2.append(PathTreeVertex((2,i)))
#     row1[i].childlist.append(row2[i])  
# edge1 = PathTreeEdge(top,row1[0])
# print(edge1) 
# for vertex in row1:
#     top.childlist.append(vertex)
# top.printSubtree()

# tree = PathTree(top)
# print("")
# print("")
# tree.print()