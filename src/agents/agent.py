# agent.py
from utilities import *
from graphics import *
from traits import *

class Agent(object):
    last_agent_id = 0
    agent_type = ""

    sprite = None
    world = None
    alive = True

    position = Vector2D(0, 0)
    last_position = position
    movement = Vector2D(0, 0)
    last_movement = movement

    default_traits = [
        MaxSpeed,
        #SocialEffect,
        Madness
    ]

    @classmethod
    def reset_id(cls):
        cls.last_agent_id = 0

    def __init__(self, agent_type=None):
        if agent_type is None:
            agent_type = self.__name__
        self.agent_type = agent_type
        self.id = self.last_agent_id
        self.__class__.last_agent_id += 1
        self.traits = []
        self.agent_data = self.init_agent_data()
        self.add_traits(self.default_traits)

    def add_traits(self, traits):
        for trait in traits:
            for existing_trait in self.traits:
                if isinstance(existing_trait, trait):
                    break
            else:
                new_trait = trait(self)
                trait_stats = new_trait.init_agent_data()
                trait_stats.update(self.agent_data)
                self.agent_data = trait_stats
                self.traits.append(new_trait)

    def init_agent_data(self):
        return {}

    def do_update(self, dt_hours):
        self.last_movement = self.movement
        self.last_position = self.position
        self.movement = Vector2D()
        for trait in self.traits:
            trait.do_update(dt_hours)

    def do_move(self, dt_hours):
        for trait in self.traits:
            trait.do_move(dt_hours)
        delta_pos = self.movement * dt_hours
        self.position += delta_pos

    def do_draw(self, dt_hours):
        pos = self.position
        if self.sprite is None:
            self.init_sprite()
            self.sprite.draw(self.world.window)
            self.set_highlight()
        if hasattr(self.sprite, "getCenter"):
            delta_pos = pos - self.sprite.getCenter()
        else:
            delta_pos = pos - self.sprite.getAnchor()
        self.sprite.move(delta_pos.x, delta_pos.y)

    def init_sprite(self):
        self.sprite = Rectangle(Point(self.position.x-5, self.position.y-5),
                                Point(self.position.x+5, self.position.y+5))
        self.sprite.setFill(color_rgb(0, 255, 0))

    def set_world(self, world):
        self.world = world

    def set_highlight(self, intensity=0):
        self.sprite.setOutline(color_rgb(intensity, intensity, 0))

    def on_death(self):
        if self.alive:
            print("{} {} died!".format(self.agent_type, self.id))
            if self.sprite is not None:
                self.sprite.undraw()
            self.alive = False
