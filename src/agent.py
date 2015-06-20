# agent.py
from utilities import *
from graphics import *

last_agent_id = 0

class Agent(object):

    rect = None
    world = None

    position = Vector2D(0, 0)
    movement = Vector2D(0, 0)

    @staticmethod
    def reset_id():
        global last_agent_id
        last_agent_id = 0

    def __init__(self, traits=[]):
        global last_agent_id
        self.id = last_agent_id
        last_agent_id += 1
        self.traits = traits[:]

    def add_traits(self, traits):
        self.traits.extend(traits)

    def randomize_traits(self):
        for trait in self.traits:
            trait.randomize()

    def do_update(self, dt):
        for trait in self.traits:
            trait.do_update(dt)

    def do_move(self, dt):
        for trait in self.traits:
            trait.do_move(dt)
        delta_pos = self.movement * dt
        self.position += delta_pos

    def do_draw(self, dt):
        delta_pos = self.position - self.rect.getCenter()
        self.rect.move(delta_pos.x, delta_pos.y)

    def set_world(self, world):
        if self.world is not None:
            self.rect.undraw()
        self.world = world
        if self.world is not None:
            pos = self.position
            self.rect = Rectangle(Point(pos.x-5, pos.y-5), Point(pos.x+5, pos.y+5))
            self.rect.setFill(color_rgb(0, 255, 0))
            self.set_highlight()
            self.rect.draw(world.window)

    def set_highlight(self, intensity=0):
        self.rect.setOutline(color_rgb(intensity, intensity, 0))