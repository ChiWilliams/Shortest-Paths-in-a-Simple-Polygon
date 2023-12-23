#The purpose of this document is to have some basic list operations which will be useful
#when we start moving things around

import statistics

#This method finds the centroid given the x coordinates and y coordinates of every point
#input:
#  xlist: list of x coordinates
#  ylist: list of y coordinates
#output:
#  list of two points: which are the centroid
#side effects: none
def centroid(xlist,ylist):
    xcoord=statistics.fmean(xlist)
    ycoord=statistics.fmean(ylist)
    return [xcoord, ycoord]

#This method concatenates a list of x and y coordinates into one list
#input:
#  xlist,ylist are lists of x and y coordinates (must be same length)
#output:
#  list of lists of length two
def pointlist(xlist,ylist):
    list_of_points = []
    for i in range(min(len(xlist),len(ylist))):
        list_of_points.append((xlist[i],ylist[i]))
    return list_of_points

#Here, we create a dictionary which takes a vertex of a polygon, and returns its vertex #
def vertex_dict(polygon):
    dict = {}
    for i in range(len(polygon)):
        dict.update({polygon[i]:i})
    return dict

def find_index(list,element):
    for i in range(len(list)):
        if list[i]==element:
            return i
    return None