import pyglet
from pyglet import shapes
from pyglet import key


# Create a Pyglet window
window = pyglet.window.Window(width=800, height=600)

# Create a batch for optimized rendering
batch = pyglet.graphics.Batch()

# Define arrow coordinates
x1, y1 = 150, 200
x2, y2 = 100, 300

points = []

def drawArrow(x1,y1,x2,y2):
    dx = x2-x1
    dy = y2-y1
    length = (dx**2+dy**2)**.5
    line=shapes.Line(x1,y1,x2,y2,width=3,color=(100,100,200),batch=batch)
    delta = max(5/length,(dx**2+dy**2)**.5/(25*length))
    triangle = shapes.Triangle(
        x2+dx/25,y2+dy/25,x2-delta*dx-delta*dy,y2-delta*dy+delta*dx,x2-delta*dx+delta*dy,
        y2-delta*dy-delta*dx,color=(100,100,200),batch=batch)
    line.draw()
    triangle.draw()
    return [line,triangle]

previousclick=[]
arrows = []

#line = shapes.Line(x1,y1,x2,y2,width=4,color=(200,150,100),batch=batch)
shaper = drawArrow(x1,y1,x2,y2)
shapes2 = drawArrow(x1+10,y1+10,x2+10,y2+10)
# Create vertex lists for the arrow
# arrow_vertex_list = batch.add(2, pyglet.gl.GL_LINES, None,
#     ('v2i', (x1, y1, x2, y2)),
#     ('c3B', (255, 0, 0, 255, 0, 0))  # Red color
# )

@window.event
def on_mouse_press(x,y,button,modifiers):
    if len(previousclick) != 0:    
        prevcoords = previousclick.pop()
    previousclick.append([x,y])
    if len(previousclick) != 0:
        arrows.append(drawArrow(*prevcoords,x,y))

    #points.append(shapes.Circle(x,y,radius=10,color=(255,255,255),batch=batch))

@window.event
def on_draw():
    window.clear()
    batch.draw()

if __name__ == "__main__":
    pyglet.app.run()