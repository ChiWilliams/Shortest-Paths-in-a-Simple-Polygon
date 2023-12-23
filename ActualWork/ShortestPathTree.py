import tripy
import networkx as nx
from BasicOperations import *
from VertexListOperations import *
from math import *
from treeclass import *



#this method takes a (simple) polygon and a vertex, and returns the tree of vertices
#corresponding to the shortest path tree
#input: polygon (a list of points which are stored as pairs)
#output: a graph
def old_shortest_path_tree(polygon,vertex):
    #we start by triangulating the polygon
    triangles = tripy.earclip(polygon)
    #We now create the dual graph:
    #We start with creating the edges
    T = nx.Graph()
    for i, triangle in enumerate(triangles):
        T.add_node(i)
    #We now use Dijkstra's algorithm to compute the shortest path tree
    for i, triangle1 in enumerate(triangles):
        for j,triangle2 in enumerate(triangles):
            if i!=j:
                shared_edge = set(triangle1).intersection(set(triangle2))
                print(shared_edge)
                if len(shared_edge) == 2:
                    point1 = shared_edge.pop()
                    point2 = shared_edge.pop()
                    weight = ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**0.5
                print(weight)
    return T

#This is a helper function which is quite slow O(n^3) which finds the visible connections graph
#It is a little bit unwieldy
#input: polygon
def visible_connections_graph(polygon):
    G = nx.Graph()
    #first, we add the vertices as nodes
    G.add_nodes_from(polygon)
    #then, we add the edges as nodes
    for i in range(-1,len(polygon)-1):
        G.add_node((polygon[i],polygon[i+1]))
    #now, we loop through all of the vertices and add all visible pairs
    for point1 in polygon:
        for point2 in polygon:
            if point1<point2:
                if is_chord(polygon,point1,point2):
                    G.add_edge(point1,point2,weight=dist(point1,point2))
    shortest_path_tree = nx.algorithms.shortest_paths.weighted.single_source_dijkstra(G, polygon[0])
    #this is the slightly more tricky part
    #we now add edges representing the distance between edges and points visible to that edge
    for i in range(-1,len(polygon)-1):
        edgei = (polygon[i],polygon[i+1])
        p1=polygon[i]
        p2=polygon[i+1]
        for q in polygon:
            projq = proj(p1,p2,q)
            if q==p1 or q == p2:
                G.add_edge(edgei,q,weight=0)
            elif dist(p1,p2) == dist(p1,projq)+dist(p2,projq) and is_chord(polygon,projq,q):
                G.add_edge(edgei,q,weight=dist(q,projq))
                #this method has floating point -- FIX
            elif is_chord(polygon,p1,q) and is_chord(polygon,p2,q):
                G.add_edge(edgei,q,weight=min(dist(p1,q),dist(p2,q)))
            elif is_chord(polygon,p1,q):
                G.add_edge(edgei,q,weight=dist(p1,q))
            elif is_chord(polygon,p2,q):
                G.add_edge(edgei,q,weight=dist(p1,q))
    #print(G.nodes)
    #print(G.edges)
    return G






#shortest_path_tree = nx.algorithms.shortest_paths.weighted.single_source_dijkstra(G, 0)



# Connect two nodes if their corresponding triangles share an edge
#for i, triangle1 in enumerate(triangles):
#    for j, triangle2 in enumerate(triangles):
#        if i != j:
#            shared_edge = set(triangle1).intersection(set(triangle2))
#            if len(shared_edge) == 2:
#                weight = ((shared_edge.pop()[0] - shared_edge.pop()[0]) ** 2 + (shared_edge.pop()[0] - shared_edge.pop()[0]) ** 2) ** 0.5
#                G.add_edge(i, j, weight=weight)

# Compute the shortest path tree using Dijkstra's algorithm
#shortest_path_tree = nx.algorithms.shortest_paths.weighted.single_source_dijkstra(G, 0)

#print(shortest_path_tree)

def triangVertexFromEdge(tri_list,v1,v2):
    vertex_list = []
    for triangle in tri_list:
        if v1 in triangle and v2 in triangle:
            for i in range(3):
                if triangle[i]!=v1 and triangle[i]!=v2:
                    vertex_list.append(triangle[i])
    return vertex_list

def edgeInTriang(polygon,triang,u,v):
    vertices_number = vertex_dict(polygon)
    ui=vertices_number[u]
    vi=vertices_number[v]
    if abs(ui-vi)==1:
        return False
    if (ui==0 and vi==len(polygon)-1) or (ui==len(polygon)-1 and vi==0):
        return False
    for triangle in triang:
        if u in triangle and v in triangle:
            return True
    return False


#This function returns the shortest path from a vertex to the root of a shortest path three
#input: shortest path tree from a specified vertex
#   any vertex in the tree
#return: a list of vertices starting from the old vertex
def shortestPath(path_tree,vertex):
    return_list = [vertex]
    current_vertex=vertex
    while current_vertex!=path_tree.get_root():
        current_vertex=current_vertex.getParent()
        return_list.append(current_vertex)
    return return_list



#Cute little helper function which finds the cusp between two PathTreeVertices
#input: v1,v2 are pathTree vertices (in *constructed* shortest path tree)
#output: the cusp of their funnel (pathTreeVertex)
def findCusp(path_tree,v1,v2):
    v1_path=shortestPath(path_tree,v1)
    #maybe make set if have time? Runtime is currently o(n^2)
    v2_path=shortestPath(path_tree,v2)
    for vert in v1_path:
        if vert in v2_path:
            return vert

#This method returns the funnel between two PathTreeVertices 
#input: two PathTreeVertices from *constructed PathTree*
#   (They should be in counterclockwise order)
#output: list of PathTree Vertices
def findFunnel(path_tree,v1,v2):
    funnel = []
    cusp = findCusp(path_tree,v1,v2)
    v1_point = v1
    while v1_point!=cusp:
       funnel.append(v1_point)
       v1_point=v1_point.parent
    funnel.append(cusp)
    v2_list = []
    v2_point=v2
    while v2_point!=cusp:
       v2_list.append(v2_point)
       v2_point=v2_point.parent
    v2_list.reverse()
    funnel.extend(v2_list)
    return funnel

#This function adds all of the edges of the polygon to the shortest path tree
#Inputs:
    # polygon: a *counterclockwise* list of vertices (x,y)
    # path_tree: a shortest path tree from a source vertex
#Outputs: none
#Side effects: adds edges to the path_tree, updates pathTreeVertices with their edgeList (child edges)   
def addEdges(polygon,path_tree):
    for i in range(-1,len(polygon)-1):
        v1 = polygon[i]
        v2 = polygon[i+1]
        dict=path_tree.makeDictionary()
        v1vert = dict[v1]
        v2vert = dict[v2]
        cusp = findCusp(path_tree,v1vert,v2vert)
        funnel= findFunnel(path_tree,v1vert,v2vert)
        edgeParent(path_tree,v1vert,v2vert,funnel,cusp)    

#This function updates the tree to add a PathTreeEdge into it:
#Inputs:
#   path_tree (unecessary?) a pathTree object
#   v1, v2 (maybe cut) are pathTreeVertices corresponding to the endpoints of the edge
#   funnel: list of pathTreeVertices which compose the edge which compose the funnel   
#   cusp: pathTreeVertex which is the cusp of the funnel 
def edgeParent(path_tree,v1,v2,funnel,cusp):
    edge = PathTreeEdge(v1,v2) 
    funnel_indices = vertex_dict(funnel)
    cusp_index = find_index(funnel,cusp)
    cusp_proj=proj(v1.cds(),v2.cds(),cusp.cds())
    if cusp_index == 0 or cusp_index == len(funnel)-1:
        dupl_vertex = PathTreeVertex(cusp.cds())
        dupl_vertex.parent = cusp
        cusp.childlist.append(dupl_vertex)
        dupl_vertex.edgeList.append(edge)
        edge.parent = dupl_vertex
    elif not ccw(funnel[cusp_index-1].cds(),cusp.cds(),cusp_proj) and ccw(funnel[cusp_index+1].cds(),
                                                                          cusp.cds(),cusp_proj):
        cusp_proj_vert=PathTreeVertex(cusp_proj)
        cusp_proj_vert.parent = cusp
        cusp_proj_vert.edgeList.append(edge)
        cusp.childlist.append(cusp_proj_vert)
        edge.parent = cusp_proj_vert
        #cusp.edgeList.append(edge)
        #edge.parent = cusp
    elif ccw(funnel[cusp_index-1].cds(),cusp.cds(),cusp_proj):
        flag = True
        index = cusp_index-1
        while flag:
            if index==0:
                #we are going to create a duplicate vertex: this way our endpoints which hit edges
                #are all distinct from vertices of the simple vertex
                dupl_vertex = PathTreeVertex(funnel[index].cds())
                dupl_vertex.parent = funnel[index]
                funnel[index].childlist.append(dupl_vertex)
                dupl_vertex.edgeList.append(edge)
                edge.parent=dupl_vertex
                flag = False
            elif ccw(funnel[index].cds(),funnel[index-1].cds(),
                         proj(v1.cds(),v2.cds(),funnel[index].cds())):
                proj_vert = PathTreeVertex(proj(v1.cds(),v2.cds(),funnel[index].cds()))
                proj_vert.parent = funnel[index]
                proj_vert.edgeList.append(edge)
                edge.parent = proj_vert
                funnel[index].childlist.append(proj_vert)
                #funnel[index].edgeList.append(edge)
                #edge.parent=funnel[index]
                flag = False
            index = index-1
    else:
        flag = True
        index = cusp_index+1
        while flag:
            #print("Funnel:",funnel)
            #print("Funnel len:",len(funnel)-1,"Index=",index)
            if index==len(funnel)-1:
                dupl_vertex = PathTreeVertex(funnel[index].cds())
                dupl_vertex.parent = funnel[index]
                funnel[index].childlist.append(dupl_vertex)
                dupl_vertex.edgeList.append(edge)
                edge.parent=dupl_vertex
                flag = False
            elif not ccw(funnel[index].cds(),funnel[index+1].cds(),
                         proj(v1.cds(),v2.cds(),funnel[index].cds())):
                proj_vert = PathTreeVertex(proj(v1.cds(),v2.cds(),funnel[index].cds()))
                proj_vert.parent = funnel[index]
                proj_vert.edgeList.append(edge)
                edge.parent=proj_vert
                funnel[index].childlist.append(proj_vert)
                #funnel[index].edgeList.append(edge)
                #edge.parent=funnel[index]
                flag = False
            index = index+1

def shortest_path_tree(polygon,source):
    visited_vertices=[]
    makeCCW(polygon)
    source_vertex = PathTreeVertex(source)
    path_tree = PathTree(source_vertex)
    triang = tripy.earclip(polygon)
    vertices_number = vertex_dict(polygon)
    right_of_source = polygon[(vertices_number[source]+1)%len(polygon)]
    right_vertex=PathTreeVertex(right_of_source)
    #print("The source is ",source_vertex.cds(),"and the right is", right_vertex.cds())
    right_vertex.parent=source_vertex
    source_vertex.childlist.append(right_vertex)
    visited_vertices=[source,right_vertex.cds()]
    path(polygon,path_tree,[source_vertex,right_vertex],source_vertex,triang,visited_vertices)
    return path_tree
    

#This function is recursively called to create the shortest path tree
#Our inputs are:
#   polygon: a counterclockwise sorted list of vertices
#   path_tree: the pointer to
#   funnel: a sorted list of PathTreeVertex objects which composes the funnel counterclockwise 
#     sorted list 
#   cusp: a PathTreeVertex that is the cusp
#   triang: a triangulation of the polygon
#No output:
#Side effects:
#   Creates x, a PathTreeVertex
#   Recursively calls other paths to finish the path tree
def path(polygon,path_tree,funnel,cusp,triang,visited_vertices):
    # print("")
    # print("")
    # print("New recursive call!")
    # print("The current funnel is",funnel)
    #first, we find the index of the cusp
    funnel_indices = vertex_dict(funnel)
    cusp_index = funnel_indices[cusp]
    #then, we find the endpoints of our funnel
    u=funnel[0]
    w=funnel[-1]
    #now, we find the point x which we are going to add to the tree
    # print("")
    # print("Potential x values are", triangVertexFromEdge(triang,u.cds(),w.cds()))
    x_coords=triangVertexFromEdge(triang,u.cds(),w.cds())[0]
    if x_coords in visited_vertices:
        x_coords=triangVertexFromEdge(triang,u.cds(),w.cds())[1]
    visited_vertices.append(x_coords)
    # print("X is",x_coords)
    x=PathTreeVertex(x_coords)
    #we now determine v
    #first, we check if x is visible to the cusp
    v=None
    if cusp_index==0:
        if ccw(funnel[cusp_index].cds(),funnel[cusp_index+1].cds(),x.cds()):
            v=cusp
            vi=cusp_index
        else:
            for i in range(1,len(funnel)-1):
                if not ccw(funnel[i-1].cds(),funnel[i].cds(),x.cds()) and ccw(funnel[i].cds(),funnel[i+1].cds(),x.cds()):
                    v=funnel[i]
                    vi=i
            if v==None:
                v=funnel[-1]
                vi=len(funnel)
    elif cusp_index==len(funnel)-1:
        if not ccw(cusp.cds(),funnel[cusp_index-1].cds(),x.cds()):
            v=cusp
            vi=cusp_index
        else:
            for i in reversed(range(1,len(funnel)-1)):
                if ccw(funnel[i+1].cds(),funnel[i].cds(),x.cds()) and not ccw(funnel[i].cds(),funnel[i-1].cds(),x.cds()):
                    v=funnel[i]
                    vi=i
            if v==None:
                v=funnel[0]
                vi=0
    else:
        u1=funnel[cusp_index-1]
        v1=funnel[cusp_index+1]
        if not ccw(x.cds(),cusp.cds(),u1.cds()) and ccw(x.cds(),cusp.cds(),v1.cds()):
            v = cusp
            vi = cusp_index
        #find which side to check:
        if ccw(cusp.cds(),u1.cds(),x.cds()):
            for i in reversed(range(1,len(funnel)-1)):
                if ccw(funnel[i+1].cds(),funnel[i].cds(),x.cds()) and not ccw(funnel[i].cds(),funnel[i-1].cds(),x.cds()):
                    v=funnel[i]
                    vi=i
            if v==None:
                v=funnel[0]
                vi=0
        else:
            for i in range(1,len(funnel)-1):
                if not ccw(funnel[i-1].cds(),funnel[i].cds(),x.cds()) and ccw(funnel[i].cds(),funnel[i+1].cds(),x.cds()):
                    v=funnel[i]
                    vi=i
            if v==None:
                v=funnel[-1]
                vi = len(funnel)-1
        #if not, we check which element of the set the funnel is tangent to
    # print("The value of vi is",vi)
    # print(v.cds())
    F1 = []
    for i in range(0,vi+1):
        # print("We are appending f1 now for i=",i)
        F1.append(funnel[i])
    F1.append(x)
    # print("F1 is",F1)
    F2 = [x]
    for i in range(vi,len(funnel)):
        F2.append(funnel[i])
    if vi <= cusp_index:
        cuspF1=v
        cuspF2=cusp
    else:
        cuspF1=cusp
        cuspF2=v
    v.childlist.append(x)
    x.parent = v
    if edgeInTriang(polygon,triang,u.cds(),x.cds()):
        path(polygon,path_tree,F1,cuspF1,triang,visited_vertices)
    if edgeInTriang(polygon,triang,w.cds(),x.cds()):
        path(polygon,path_tree,F2,cuspF2,triang,visited_vertices)


 
# INFORMAL TESTING SECTION

                           


def printEdges(root):
    print("for", root.cds(),":",root.edgeList)
    for child in root.childlist:
        printEdges(child)

def test():
    polygon = [(0, 0), (0, 3), (1, 3), (1, 1),(3,1),(3,0)]
    # print(tripy.earclip(polygon))


    tree=shortest_path_tree(polygon,(1,1))
    addEdges(polygon,tree)
    tree.print()
    tree.addLengths()
    print(tree.root.childlist)
    print("Root's max dist is",tree.root.far_length)
    print("Root's furthest edge is",tree.root.far_edge)
    printEdges(tree.root)
    dict = tree.makeDictionary()
    edge_dict = tree.makeEdgeDictionary()
    for i in range(-1,len(polygon)-1):
        edge = edge_dict[(polygon[i],polygon[i+1])]
        print("edge:",edge,"parent:",edge.parent)
    print(tree.root.getChildren())
    print("")
    print("The final tree is:")
    tree.print()

    visible_connections_graph(polygon)


    tria=tripy.earclip(polygon)
    #hopefully false
    print(edgeInTriang(polygon,tria,(1,3),(3,1)))
    print(edgeInTriang(polygon,tria,(0,0),(3,0)))
    # hopefully true
    print(edgeInTriang(polygon,tria,(0,0),(3,1)))



    print(triangVertexFromEdge(tripy.earclip(polygon),(0,0),(0,3)))
    print(triangVertexFromEdge(tripy.earclip(polygon),(0,0),(1,1)))

#test()
