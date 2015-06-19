# agent.py
from utilities import *
from graphics import *
import random

last_agent_id = 0

class Agent(object):

    rect = None
    world = None

    @staticmethod
    def reset_id():
        global last_agent_id
        last_agent_id = 0

    def __init__(self):
        global last_agent_id
        self.id = last_agent_id
        last_agent_id += 1
        self.state = {
            "position": Vector2D(0, 0),
            "velocity": Vector2D(0, 0)
        }
        self.traits = {
            "sociality": 0,
            "max_speed": 10,
            "mass": 1,
            "sight": 200
        }

    def randomize_traits(self):
        # Sociality is a measure, from -1 to 1, of how much the
        # agent likes to be near other agents.
        self.traits["sociality"] = random.uniform(-1, 1)

        # Max_speed is a measure, from 5 to 10, of how fast the
        # agent can to move around.
        self.traits["max_speed"] = random.uniform(5, 10)

    def set_traits(self, traits):
        self.traits.update(traits)

    def set_state(self, state):
        self.state.update(state)

    def do_update(self, dt):
        velocity = Vector2D()
        for agent in self.world.agents_in_range(self.state["position"], self.traits["sight"]):
            if agent is self:
                continue
            delta = agent.state["position"] - self.state["position"]
            if delta.r != 0:
                velocity += Vector2D(r=(250*self.traits["sociality"])/delta.r, theta=delta.theta)

        # Constrain velocity magnitude to "max_speed"
        velocity = Vector2D(r=min(velocity.r, self.traits["max_speed"]), theta=velocity.theta)
        self.state["velocity"] = velocity

    def do_move(self, dt):
        delta_pos = self.state["velocity"] * dt
        self.state["position"] += delta_pos

    def do_draw(self, dt):
        delta_pos = self.state["position"] - self.rect.getCenter()
        self.rect.move(delta_pos.x, delta_pos.y)

    def set_world(self, world):
        if self.world is not None:
            self.rect.undraw()
        self.world = world
        if self.world is not None:
            pos = self.state["position"]
            self.rect = Rectangle(Point(pos.x-5, pos.y-5), Point(pos.x+5, pos.y+5))
            green = (self.traits["sociality"]-1) * -127
            red = self.traits["max_speed"] * 255/10
            self.rect.setFill(color_rgb(red, green, 0))
            self.set_highlight()
            self.rect.draw(world.window)

    def set_highlight(self, intensity=0):
        self.rect.setOutline(color_rgb(intensity, intensity, 0))