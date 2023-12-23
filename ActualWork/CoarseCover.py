from ShortestPathTree import *
from CoarseCoverDataStructs import *
import numpy as np
import statistics as stat
import random

#We want to create a coarse cover of an interval K with endpoints a and b
#Our input is going to be that interval
#And our output is going to be a list of elements (I,f,H) with properties

#inputs: polygon is a *counterclockwise* list of vertices (which are just (float,float))
#   a and b are vertices (float,float)
#returns: list of triples
def coarseCover(polygon,a,b):
    # We use a data structure to help organize our helper methods (probably a bad decision, but whatevs)
    # cch is short for "Coarse Cover Helper"
    cch = CoarseHelper(polygon,a,b)
    final_cover = []
    # we now iterate through both trees:
    for i in range(-1,len(polygon)-1):
        edge = (polygon[i],polygon[i+1])
        edge_a = cch.edgeVert(edge,a)
        edge_b = cch.edgeVert(edge,b)
        #print("Edge_b is",edge_b,"while its parent is",edge_b.parent)
        t_a = edge_a.parent
        t_b = edge_b.parent
        if t_a.cds()!=t_b.cds():
            perp_vec = perp_tuple(*edge)
            linea1 = (t_a.cds(),tuple_minus(t_a.cds(),perp_vec))
            lineb1 = (t_b.cds(),tuple_minus(t_b.cds(),perp_vec))
            line2 = (a,b)
            I = [line_intersection(linea1,line2),line_intersection(lineb1,line2)]
            f = CoarseFunct(2,edge,0)
            H = edge
            #print("We used this case")
            final_cover.append((I,f,H))
        elif t_a.parent.cds() == t_b.parent.cds():
            u = t_a.parent.cds()
            if u != a and u!= b:
                if cch.isVisible(u):
                    #print("v is",t_a.cds(),"u is",u)
                    I = [cch.X_a(u,a),cch.X_a(u,b)]
                    f = CoarseFunct(1,u,dist(u,t_a.cds()))
                    H = edge
                    final_cover.append((I,f,H))
    for point in polygon:
        v_a = cch.dict_a[point]
        if not point == a and not point ==b:
            if not cch.isVisible(point):
                u = v_a.parent.cds()
                if cch.isVisible(u):
                    I = [cch.X_a(u,a),cch.X_a(u,b)]
                    f = CoarseFunct(1,u,dist(u,v_a.cds())+v_a.far_length)
                    H = v_a.far_edge.cds()
                    final_cover.append((I,f,H))
            else:
                #We add the a-side triangle first
                u_a = v_a.parent.cds()
                if u_a!=a and v_a.far_length!=-inf:
                    Ia = [cch.X_a(u_a,a),cch.X_a(point,a)]
                    fa = CoarseFunct(1,u_a,dist(u_a,point)+v_a.far_length)
                    try:
                        Ha = v_a.far_edge.cds()
                    except:
                        print("We have v_a:",v_a,"and edges:",v_a.edgeList)
                        raise ValueError("We have v_a:",v_a,"and edges:",v_a.edgeList)
                    final_cover.append((Ia,fa,Ha))
                #Now, we repeat the same steps for the b-side triangle
                v_b = cch.dict_b[point]
                u_b = v_b.parent.cds()
                if u_b!=b and v_b.far_length!=-inf:
                    Ib = [cch.X_a(point,b),cch.X_a(u_b,b)]
                    fb = CoarseFunct(1,u_b,dist(u_b,point)+v_b.far_length)
                    Hb = v_b.far_edge.cds()
                    final_cover.append((Ib,fb,Hb)) 
    return final_cover

def wrong_intervals(cover):
    final = []
    for co in cover:
        if co[0][0][0] > co[0][1][0]:
            final.append(co[0])
    return final



# Our goal: find relative minimum (happens at an extended intersection point)
# We have n triples (H_i,f_i,H_i), and are seeking to find a point x*
# We will reduce this problem consistently
# outputs a point
# def find_rel_min(cand_triples,interval):
#     if len(cand_triples) < 2:
#         raise ValueError("Cand_triples too short (I think)")
#     if len(cand_triples) == 2:
#         return func_intersections(cand_triples[0][1],cand_triples[1][1],*interval[0],*interval[1])
#     else:
#         ext_ints_list = []
#         pair_inters = {}
#         for i in range(len(cand_triples)//2):
#             ext_ints = ext_intersections(cand_triples[2*i],cand_triples[2*i+1])
#             pair_inters[i] = ext_ints
#             ext_ints_list.extend(ext_ints)
#         ext_ints_list.sort(key=lambda element:element[0])
#         for i in range(3):
#             median = ext_ints_list[len(ext_ints_list)//2]
#             if isRelMean():
#                 return median
#             else:
#                 if relMeanDirection==-1:
#                     ext_ints_list = ext_ints_list[:len(ext_ints_list)//2-1]
#                 else:
#                     ext_ints_list = ext_ints_list[len(ext_ints_list)//2+1:]











def find_extended_intersections(cover):
    intersect_list = []

    for i in range(len(cover)/2):
        intersect_list.append(cover[2*i],cover[2*i+1])

def ext_intersections(triple1,triple2):
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
    print("Ia is",Ia,"and Ib is",Ib)
    part_intersect = func_intersections(fa, fb,*Ha,*Hb)
    if Ia[1][0]<Ib[0][0]:
        points.append((stat.fmean(Ia[1][0],Ib[0][0]),stat.fmean(Ia[1][1],Ib[0][1])))
    elif Ia[1][0]<Ib[1][0]:
        if fa.eval(Ib[0]) < fb.eval(Ib[0]):
            points.append(Ib[0])
    return [*Ia,*Ib]
        

def func_intersections(fa,fb,Ha_0,Ha_1,Hb_0,Hb_1):
    return [Ha_0]


    

polygon = [(450, 273), (361, 163), (588, 177), (446, 215), (593, 306), (420, 336)]
polygon2 = [(342, 338), (411, 281), (401, 244), (354, 221), (255, 205), (351, 185),
             (391, 151), (419, 125), (445, 151), (515, 179), (621, 204), (521, 214),
               (494, 245), (493, 295), (548, 337)]
tree = shortest_path_tree(polygon,(446, 215))
addEdges(polygon,tree)
#printEdges(tree.root)

#makeCCW(polygon)
cc = coarseCover(polygon2,(255, 205), (621, 204))
print(wrong_intervals(cc))
print(cc)
print(CoarseHelper(polygon2,(255, 205), (621, 204)).find_rel_min(cc,[(255, 205), (621, 204)]))