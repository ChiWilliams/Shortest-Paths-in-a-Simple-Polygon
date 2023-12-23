import pyglet
from pyglet import shapes
from ShortestPathTree import *
from math import dist

def drawArrow(x1,y1,x2,y2):
    dx = x2-x1
    dy = y2-y1
    length = (dx**2+dy**2)**.5
    line=shapes.Line(x1,y1,x2,y2,width=3,color=(200,100,100))
    # delta = 5
    #delta = max(5/length,(dx**2+dy**2)**.5/(15*length))
    delta = 15/length
    triangle = shapes.Triangle(
         x2-dx/100,y2-dy/100,x2-delta*dx-delta*dy,y2-delta*dy+delta*dx,x2-delta*dx+delta*dy,
         y2-delta*dy-delta*dx,color=(200,100,100))
    # triangle = shapes.Triangle(
    #     x2+dx/25,y2+dy/25,x2-delta*dx-delta*dy,y2-delta*dy+delta*dx,x2-delta*dx+delta*dy,
    #     y2-delta*dy-delta*dx,color=(100,100,200))
    line.draw()
    triangle.draw()
    return [line,triangle]

def path_subtree_list(head,arrow_list):
    for edge in head.edgeList:
        arrow_list.extend(drawArrow(*head.cds(),*proj(edge.v1.cds(),edge.v2.cds(),head.cds())))
        print("The projected point is", proj(edge.v1.cds(),edge.v2.cds(),head.cds()))
    for child in head.getChildren():
        arrow_list.extend(drawArrow(*head.cds(),*child.cds()))
        path_subtree_list(child,arrow_list)

#will return a list of lines and triangles to draw
def path_tree_arrows(path_tree):
    #print("We start here with the arrows")
    arrow_list = []
    root = path_tree.get_root()
    path_subtree_list(root,arrow_list)
    return arrow_list

def activate_point(polygon,x,y):
    try:
        return polygon[activate_index(polygon,x,y)]
    except:
        return None

def activate_index(polygon,x,y):
    point_index = min(range(len(polygon)), key=lambda i:dist(polygon[i],(x,y)))
    if dist((x,y),polygon[point_index])<=10:
        return point_index
    else:
        return None
#polygon = [(0,0),(1,1)]
#activate_point(polygon,0.5,0.6)
    
def create_polygon_lines(polygon,stage):
    lines = []
    for i in range(len(polygon)-1):
        lines.append(shapes.Line(*polygon[i],*polygon[i+1],width=2,color=(100,100,100)))
    if stage != 0:
        lines.append(shapes.Line(*polygon[-1],*polygon[0],width=2,color=(100,100,100)))
    return lines

def create_polygon_points(polygon):
    points = []
    for point in polygon:
        points.append(shapes.Circle(*point,radius=5,color = (100,100,100)))
    return points