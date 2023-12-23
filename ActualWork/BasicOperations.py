import numpy as np
from scipy.optimize import fsolve

def ccw(A, B, C):
    """Tests whether the turn formed by A, B, and C is ccw"""
    return (B[0] - A[0]) * (C[1] - A[1]) > (B[1] - A[1]) * (C[0] - A[0])

#print(ccw((0,0),(1,0),(1,1)))

def intersect(a1, b1, a2, b2):
    """Returns True if line segments a1b1 and a2b2 intersect."""
    return ccw(a1, b1, a2) != ccw(a1, b1, b2) and ccw(a2, b2, a1) != ccw(a2, b2, b1)

def valid_add(polygon,x,y):
    for i in range(len(polygon)-2):
        if intersect(polygon[i],polygon[i+1],polygon[-1],(x,y)):
            if not ((x,y) == polygon[i] or (x,y) == polygon[i+1]):
                return False
    for i in range(1,len(polygon)):
        if (x,y)== polygon[i]:
            return False
    return True

#this method takes a list of points and determines whether it is counterclockwise or not
def isCounterClockwise(polygon):
    min_x_vertex_index=0
    min_x_vertex_value=polygon[0][0]
    for i in range(len(polygon)):
        if polygon[i][0]<min_x_vertex_value:
            min_x_vertex_value=polygon[i][0]
            min_x_vertex_index=i
        elif polygon[i][0]==min_x_vertex_value and polygon[i][1]>polygon[min_x_vertex_index][1]:
            min_x_vertex_index=i
    # now we calculate whether these three are a left turn or a right turn
    if min_x_vertex_index==0:
        return ccw(polygon[-1],polygon[0],polygon[1])
    elif min_x_vertex_index==len(polygon)-1:
        return ccw(polygon[min_x_vertex_index-1],polygon[min_x_vertex_index],polygon[0])
    else:
        return ccw(polygon[min_x_vertex_index-1],polygon[min_x_vertex_index],polygon[min_x_vertex_index+1])

def makeCCW(polygon):
    if not isCounterClockwise(polygon):
        polygon.reverse()
    return polygon

# poly = [(0,0),(0,1),(1,1),(1,0)]
# print("The polygon is counterclockwise:", isCounterClockwise(poly))
# print("reversing the list:", poly.reverse())
# print("using the function:", makeCCW(poly))

#This is a cute little helper function which checks if the chord between two vertices is contained
#in the polygon
#input: polygon (a list of paired floats with the first corresponding to x and the second to y)
#   point1: a paired float
#   point2: a paired float
#Returns a boolean true false
def is_chord(polygon,point1,point2):
    for i in range(-1,len(polygon)-1):
        if polygon[i]!=point1 and polygon[i]!=point2 and polygon[i+1]!=point1 and polygon[i+1]!=point2:
            if intersect(point1,point2,polygon[i],polygon[i+1]):
                return False
    return True

def proj(linepoint1,linepoint2,point3):
    linevec = np.array([linepoint2[0]-linepoint1[0],linepoint2[1]-linepoint1[1]])
    othervec= np.array([point3[0]-linepoint1[0],point3[1]-linepoint1[1]])
    norm = np.sqrt(sum(linevec**2))
    projection = (np.dot(linevec, othervec)/norm**2)*linevec 
    point = (projection[0]+linepoint1[0],projection[1]+linepoint1[1])
    return point

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       print(line1,line2)
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return (x, y)

def tuple_minus(tuple1,tuple2):
    return (tuple1[0]-tuple2[0],tuple1[1]-tuple2[1])

def perp_tuple(pt1,pt2):
    return (pt1[1]-pt2[1],pt2[0]-pt1[0])

def findIntersection(fun1,fun2,x0):
    return fsolve(lambda x : fun1(x) - fun2(x),x0)

#THIS MUST BE FIXED
def funcIntersector(fun1,fun2,x0):
    return fsolve(lambda x: fun1.eval(x)-fun2.eval(x),x0)

