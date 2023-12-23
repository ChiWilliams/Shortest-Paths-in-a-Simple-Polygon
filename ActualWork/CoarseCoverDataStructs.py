from treeclass import *
from ShortestPathTree import *
from math import *
from BasicOperations import proj
from statistics import fmean


class CoarseHelper:
    def __init__(self,polygon,a,b):
        self.polygon = polygon
        self.a = a
        self.b = b
        self.tree_a = shortest_path_tree(polygon,a)
        self.tree_b = shortest_path_tree(polygon,b)
        self.dict_a = self.tree_a.makeDictionary()
        self.dict_b = self.tree_b.makeDictionary()
        self.updateTrees()
        self.edge_dict_a = self.tree_a.makeEdgeDictionary()
        self.edge_dict_b = self.tree_b.makeEdgeDictionary()
    #Helper method to make __init__ cleaner
    def updateTrees(self):
        addEdges(self.polygon,self.tree_a)
        addEdges(self.polygon,self.tree_b)
        self.tree_a.addLengths()
        self.tree_b.addLengths()
        #input a bare pair of coordinates
    def isVisible(self,v):
        v_a = self.dict_a[v]
        v_b = self.dict_b[v]
        return not v_a.parent == v_b.parent
    def X_a(self,v,a_or_b):
        if not self.isVisible(v):
            return False
        else:
            if a_or_b == self.a:
                line1 = [v,self.dict_a[v].parent.cds()]
            elif a_or_b == self.b:
                line1 = [v,self.dict_b[v].parent.cds()]
            else:
                raise ValueError("Second argument must be a or b")
            line2 = [self.a,self.b]
            return line_intersection(line1,line2)
    def edgeVert(self,edge,a_or_b):
        if a_or_b == self.a:
            return self.edge_dict_a[edge]
        elif a_or_b == self.b:
            return self.edge_dict_b[edge]
        else:
            raise ValueError("3rd argument must be a or b")
    #endpoint should be 0 or 1. If it is 0, corresponds to 0
    def addCoarse(self,node,endpoint,finalCover):
        if endpoint == self.a:
            indicator = 0
            dict = self.dict_a
        elif endpoint == self.b:
            indicator = 1
            dict = self.dict_b
        else:
            raise ValueError("Endpoint must be a or b")
        if node.cds() != endpoint and node.parent.cds() != endpoint:
            v = node.cds()
            u_vert = node.parent
            u = u_vert.cds()
            if self.isVisible(v):
                Ia = (self.X_a(u,indicator),self.X_a(v,indicator))
                fa = CoarseFunct(1,u,dist(u+node.far_length))
                Ha = node.far_edge
                finalCover.append(Triple(Ia,fa,Ha))
        for child in node.childlist:
            self.addCoarse(child,endpoint,finalCover)
    def turn(self,funct,point):
        if funct.type ==1: 
            return ccw(point,tuple_minus(point,perp_tuple(self.a,self.b)),funct.object)
        if funct.type == 2:
            return ccw(point,tuple_minus(point,perp_tuple(self.a,self.b)),proj(*funct.object,point))
    def isRelMean(self,median):
        maximal = self.maxFunctions(median)
        funct = maximal.pop()
        turn = self.turn(funct,median)
        for funct in maximal:
            if turn != turn(funct,median):
                return True
        return False
    def relMeanDirection(self,median):
        maximal = self.maxFunctions(median)
        funct = maximal.pop()
        turn = self.turn(funct,median)
        for funct in maximal:
            if turn != turn(funct,median):
                raise ValueError("Should have been caught by RelMean")
        return int(turn)
    def maxFunctions(point):
        return []  
    def find_rel_min(self,cand_triples,interval):
        if len(cand_triples) < 2:
            raise ValueError("Cand_triples too short (I think)")
        if len(cand_triples) == 2:
            return self.func_intersections(cand_triples[0][1],cand_triples[1][1],*interval[0],*interval[1])
        else:
            ext_ints_list = []
            pair_inters = {}
            for i in range(len(cand_triples)//2):
                ext_ints = self.ext_intersections(cand_triples[2*i],cand_triples[2*i+1])
                pair_inters[i] = ext_ints
                ext_ints_list.extend(ext_ints)
            ext_ints_list.sort(key=lambda element:element[0])
            for i in range(3):
                median = ext_ints_list[len(ext_ints_list)//2]
                if self.isRelMean(median):
                    return median
                else:
                    if self.relMeanDirection(median)==-1:
                        ext_ints_list = ext_ints_list[:len(ext_ints_list)//2-1]
                    else:
                        ext_ints_list = ext_ints_list[len(ext_ints_list)//2+1:]
    def ext_intersections(self,triple1,triple2):
        #instantiate the list
        points = []
        #assumes not vertical
        #first, find the endpoints
        Ia, Ib = triple1[0],triple2[0]
        fa, fb = triple1[1],triple2[1]
        Ha, Hb = triple1[2],triple2[2]
        if Ia[0][0] < Ib[0][0]:
            Ia, Ib = Ib, Ia
            fa, fb = fb, fa
            Ha, Hb = Hb, Ha
        if not (Ia[0][0]<Ia[1][0] and Ib[0][0]<Ib[1][0]):
            raise ValueError("One of the intervals is backwards!")
        print("Ia is",Ia,"and Ib is",Ib)
        print(*Ha,*Hb)
        part_intersect = self.func_intersections(fa, fb,*Ha,*Hb)
        if Ia[1][0]<Ib[0][0]:
            points.append((fmean(Ia[1][0],Ib[0][0]),fmean(Ia[1][1],Ib[0][1])))
        elif Ia[1][0]<Ib[1][0]:
            if fa.eval(Ib[0]) < fb.eval(Ib[0]):
                points.append(Ib[0])
            if fa.eval(Ia[1]) > fb.eval(Ia[1]):
                points.append(Ia[1])
        else:
            if fa.eval(Ib[0]) < fb.eval(Ib[0]):
                points.append(Ib[0])
            if fa.eval(Ib[1]) < fb.eval(Ib[1]):
                points.append(Ib[1])

        return [*Ia,*Ib]
        

    def func_intersections(self,fa,fb,Ha_0,Ha_1,Hb_0,Hb_1):
        return 


class Triple:
    def __init__(self,interval,function,edge):
        self.inter = interval
        #The function needs to be a CoarseFunct
        self.function = function
        self.edge = edge

class CoarseFunct:
    def __init__(self,type,object,const):
        self.type=type
        if type == 0:
            self.object = None
            self.const=0
        else:
            self.object = object
            self.const= const
    def eval(self,point):
        if self.type == 0:
            return 0
        if self.type == 1:
            return dist(point,self.object)+self.const
        if self.type == 2:
            return dist(point,proj(*self.object,point))


                 