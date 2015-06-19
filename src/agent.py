# agent.py
from utilities import *
from random import *
from graphics import *

last_agent_id = 0

class Agent(object):

    rect = None

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
            "speed": Vector2D(0, 0)
        }
        self.traits = {
            "sociality": 0,
            "max_speed": 10,
            "mass": 1
        }
        self.total_force = Vector2D(0, 0)

    def randomize_traits(self):
        # Sociality is a measure, from -1 to 1, of how much the
        # agent likes to be near other agents.
        self.traits["sociality"] = (random()*2)-1

        # Max_speed is a measure, from 0 to 10, of how fast the
        # agent can to move around.
        self.traits["max_speed"] = random() * 10

    def set_traits(self, traits):
        self.traits.update(traits)

    def set_state(self, state):
        self.state.update(state)

    def reset_force(self):
        self.total_force = Vector2D(0, 0)

    def add_force(self, force):
        self.total_force += force

    def apply_forces(self, dt):
        accel = self.total_force * self.traits["mass"]
        desired_speed = (accel*dt) + self.state["speed"]
        self.state["speed"] = Vector2D(r=min(desired_speed.r, self.traits["max_speed"]), theta=desired_speed.theta)
        delta_pos = self.state["speed"] * dt
        self.state["position"] += delta_pos
        self.rect.move(delta_pos.x, delta_pos.y)

    def draw(self, window):
        pos = self.state["position"]
        self.rect = Rectangle(Point(pos.x-5, pos.y-5), Point(pos.x+5, pos.y+5))
        green = (self.traits["sociality"]-1) * -127
        red = self.traits["max_speed"] * 255/10
        self.rect.setFill(color_rgb(red, green, 0))
        self.set_highlight()
        self.rect.draw(window)

    def undraw(self):
        self.rect.undraw()

    def set_highlight(self, intensity=0):
        self.rect.setOutline(color_rgb(intensity, intensity, 0))