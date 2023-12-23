#Import
import pyglet

#define our window
window = pyglet.window.Window()

#response to a key being pressed
#we first import a package for this:
from pyglet.window import key
@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.A:
        print('The "A" key was pressed.')
    elif symbol == key.LEFT:
        print('The left arrow key was pressed.')
    elif symbol == key.ENTER:
        print('The enter key was pressed.')

#we can do something similar with mouse strokes!
#first import the package
from pyglet.window import mouse
@window.event
def on_mouse_press(x,y,button,modifiers):
    if button == mouse.LEFT:
        print('The left mouse button was pressed.')


@window.event
def on_draw():
    window.clear()



pyglet.app.run()