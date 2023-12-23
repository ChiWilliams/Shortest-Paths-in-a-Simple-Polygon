#We first import

import pyglet

#now we create the window and the image
window = pyglet.window.Window()
image = pyglet.resource.image('kitten.jpg')

@window.event
def on_draw():
    window.clear()
    image.blit(0,0)

pyglet.app.run()