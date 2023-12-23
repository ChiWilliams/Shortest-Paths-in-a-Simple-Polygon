#We start by importing the package
import pyglet
import tripy
from pyglet import shapes
from pyglet.window import key
from VertexListOperations import *
from BasicOperations import *
from treeclass import *
from ShortestPathTree import *
from GraphicsHelpers import *
import polygenerator
#import glooey
#add the font we want

#Instantiate the window:
window = pyglet.window.Window()

#make our set of circles!
const = [shapes.Circle(x=0,y=0,radius=0)]
circlebatch=pyglet.graphics.Batch()
arrowbatch=pyglet.graphics.Batch()
centroids= []
circles = []
#make our set of lines
lines = []
#line coordinates
polygon = []
vertices = []
arrows=[]
stage = 0
active_point = None


#Create a label for instruction:
label = pyglet.text.Label('Click the screen to draw your simple polygon and ENTER'+\
                            ' to complete the triangle',
                          font_name="Arial",
                          font_size=24,
                          x=window.width//2,y=3*window.height//4,
                          width = window.width,
                          anchor_x='center',anchor_y='center',
                          multiline=True,
                          align='center'
                          )

label2 = pyglet.text.Label('Navigation:\nDrag points to move\nPress "C" to clear the screen\nPress "Backspace" to'+\
                           " Clear Path/Triangulation",
                           font_name="Arial",
                           font_size=14,
                           x = 10, y = 75,
                           width = window.width,
                           multiline=True
                           )


#now we try to add a point when mouse is clicked
@window.event
def on_mouse_press(x,y,button,modifiers):
    global stage, active_point, centroids, arrows
    if stage == 0:
        if valid_add(polygon,x,y):
            circles.append(shapes.Circle(x=x,y=y,radius=5,color=(0,100,200),batch=circlebatch))
            polygon.append((x,y))
        if len(polygon) >= 2:
            lines.append(shapes.Line(*polygon[-2],*polygon[-1],width=2,color=(100,100,100))) 
    if stage == 2 or stage == 6:
        if activate_point(polygon,x,y):
            active_point = activate_index(polygon,x,y)
            path_tree= shortest_path_tree(polygon,polygon[active_point])
            dict = path_tree.makeDictionary()
            if stage == 6:
                addEdges(polygon,path_tree)
                stage = 7
            else:
                stage = 3
            arrows.extend(path_tree_arrows(path_tree))
        #print(active_point)
        #print(stage)
    if stage == 4:
        if activate_point(polygon,x,y):
            if len(active_point)<=1:
                act_ind = activate_index(polygon,x,y)
                active_point.append(act_ind)
                centroids.append(shapes.Circle(*polygon[act_ind],radius = 7, color = (255,0,0)))
                #print(active_point)
            if len(active_point) == 2:
                list = shortest_path(polygon,polygon[active_point[0]],polygon[active_point[1]])
                arrows.extend(vertex_list_arrows(list))
                stage = 5
        
            
                

        
@window.event
def on_mouse_drag(x,y,dx,dy,button,modifiers):
    global stage,active_point,polygon,centroids
    if activate_point(polygon,x,y): #and valid_add(polygon,x+dx,y+dy):
        if stage >=1 and stage!=4:
            hot_index = activate_index(polygon,x,y)
            hot_point = activate_point(polygon,x,y)
            polygon[hot_index] = (hot_point[0]+dx,hot_point[1] + dy)
            if stage == 3 or stage == 7:
                try:
                    path_tree= shortest_path_tree(polygon,polygon[active_point])
                    if stage == 7:
                        addEdges(polygon,path_tree)
                    arrows[:] = []
                    arrows.extend(path_tree_arrows(path_tree)) 
                except:
                    stage = stage                             
            if stage == 5:
                centroids[:] = []
                for i in active_point:
                    centroids.append(shapes.Circle(*polygon[i],radius = 7, color = (255,0,0)))
                list = shortest_path(polygon,polygon[active_point[0]],polygon[active_point[1]])
                
                arrows[:] = []
                arrows.extend(vertex_list_arrows(list))

@window.event
def on_mouse_motion(x,y,dx,dy):
    global polygon, const
    const.pop()
    if (stage == 0 and valid_add(polygon,x,y)) or (stage == 2 and activate_point(polygon,x,y)):
        const.append(shapes.Circle(x=x,y=y,radius=5,color = (0,100,200)))
    else:
        const.append(shapes.Circle(x=x,y=y,radius=5))
    
    
    
#we finish the polygon with the enter key
@window.event
def on_key_press(symbol,modifiers):
    global polygon, vertices, lines, circles, label, stage, arrows, active_point
    if symbol==key.C:
        label.text = "Click the screen to draw your simple polygon and ENTER to complete the triangle"
        lines[:] = []
        polygon[:] = []
        vertices[:] = []
        circles[:] = []
        arrows[:] = []
        stage = 0
    if symbol==key.ENTER:
        if len(polygon) >=3 and valid_add(polygon,*polygon[0]):
            label.text = "Press T to create a shortest path tree on the polygon\n"\
                          +"Press E to create a shortest path tree including edges\n"\
                          +"Press P to find the shortest path between two points"
            lines.append(shapes.Line(*polygon[0],*polygon[-1],width=2,color=(100,100,100)))
            makeCCW(polygon)
            stage = 1
    if stage != 0:
        if symbol ==key.P:
            label.text = "Press on Two Points to Show the shortest path between the two!"
            stage = 4
            active_point = []
        if symbol == key.X:
            polygon = [(point[0]+50,point[1]+50) for point in polygon]
        if symbol == key.T:
            label.text = "Click a vertex to draw the tree"
            stage = 2
            #addEdges(vertices,path_tree)
            #path_tree.print()
            #printEdges(path_tree.root)
            # path_tree.addLengths()
            # print("Root's max dist is",path_tree.root.far_length)
            # print("Root's far edge is",path_tree.root.far_edge)
        if symbol == key.E:
            label.text = "Click a vertex to draw the tree, including edges"
            stage = 6
        if symbol == key.BACKSPACE:
            stage = 1
            label.text = "Press T to create a shortest path tree on the polygon!"
            arrows[:] =[]
            active_point = None
    # if symbol == key.R:
    #     polygon = polygenerator.random_polygon(30)
    #     for i in range(len(polygon)):
    #         polygon[i]=(450*polygon[i][0]+200,450*polygon[i][1]+50)
    #         print("Vertex is",polygon[i])
    #     for i in range(-1,len(polygon)-1):
    #         lines.append(shapes.Line(polygon[i][0],polygon[i][1],polygon[i+1][0],
    #                                  polygon[i+1][1],width=1,color=(200,200,200)))
    #     path_tree= shortest_path_tree(polygon,polygon[0])
    #     path_tree.print()
    #     arrows.extend(path_tree_arrows(path_tree))
            



    

@window.event
def on_draw():
    global lines,complete
    window.clear()
    label.draw()
    label2.draw()
    circles = create_polygon_points(polygon)
    #circlebatch.draw()
    lines = create_polygon_lines(polygon,stage)
    for circle in circles:
        circle.draw()
    for obj in const:
        obj.draw()
    for centr in centroids:
        centr.draw()
    for line in lines:
        line.draw()
    for arrow in arrows:
        arrow.draw()

window.push_handlers(pyglet.window.event.WindowEventLogger())

pyglet.app.run()
