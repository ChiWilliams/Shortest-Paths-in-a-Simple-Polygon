#Here we try a hello world kinda vibe

#We import the package (fingers crossed!)
import pyglet
import statistics
from scipy.optimize import fsolve
import numpy as np
import pylab

#Create a window
window = pyglet.window.Window()

#Now, we create the label:
label = pyglet.text.Label('Hello World',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2,y=window.height//2,
                          anchor_x='center',anchor_y='center')

#We now create an event, whatever that means
@window.event
def on_draw():
    window.clear()
    label.draw()

pyglet.app.run()



def findIntersection(fun1,fun2,x0):
 return fsolve(lambda x : fun1(x) - fun2(x),x0)

result = findIntersection(np.sin,np.cos,0.0)
x = np.linspace(-2,2,50)
pylab.plot(x,np.sin(x),x,np.cos(x),result,np.sin(result),'ro')
pylab.show()
        

#AND IT WORKED!!