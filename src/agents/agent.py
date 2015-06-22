# agent.py
from utilities import *
from graphics import *
from traits import *

class Agent(object):
    last_agent_id = 0
    agent_name = ""

    sprite = None
    world = None

    position = Vector2D(0, 0)
    movement = Vector2D(0, 0)

    default_traits = [
        MaxSpeed,
        SocialEffect
    ]

    @classmethod
    def reset_id(cls, agent_name=None):
        if agent_name is None:
            agent_name = cls.__name__
        cls.agent_name = agent_name
        cls.last_agent_id = 0

    def __init__(self):
        self.id = self.last_agent_id
        self.__class__.last_agent_id += 1
        self.traits = []
        for trait in self.default_traits:
            self.traits.append(trait(self))

    def add_traits(self, traits):
        for trait in traits:
            for existing_trait in self.traits:
                if trait is type(existing_trait):
                    break
            else:
                self.traits.append(trait(self))

    def randomize_traits(self):
        for trait in self.traits:
            trait.randomize()

    def getX(self):
        return position.x

    def getY(self):
        return position.y

    def do_update(self, dt):
        for trait in self.traits:
            trait.do_update(dt)

    def do_move(self, dt):
        for trait in self.traits:
            trait.do_move(dt)
        delta_pos = self.movement * dt
        self.position += delta_pos

    def do_draw(self, dt):
        pos = self.position
        if self.sprite is None:
            self.sprite = Rectangle(Point(pos.x-5, pos.y-5), Point(pos.x+5, pos.y+5))
            self.sprite.setFill(color_rgb(0, 255, 0))
            self.sprite.draw(self.world.window)
            self.set_highlight()
        delta_pos = pos - self.sprite.getCenter()
        self.sprite.move(delta_pos.x, delta_pos.y)

    def set_world(self, world):
        if self.sprite is not None:
            self.sprite.undraw()
            self.sprite = None
        self.world = world

    def set_highlight(self, intensity=0):
        self.sprite.setOutline(color_rgb(intensity, intensity, 0))
