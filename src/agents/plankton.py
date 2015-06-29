from agents import Agent
from graphics import *
import traits
import random

class Plankton(Agent):

    default_traits = [
        traits.MaxSpeed,
        traits.Food,
        traits.PersonalSpace,
        traits.Reproduction
    ]

    def init_agent_data(self):
        return {
            "calories": 50,
            "max_bite": 0,
            "min_bite": 0,
            "hunger_rate": 0,
            "asexual": True,
            "repro_max_cooldown": random.uniform(1, 5),
            "repro_cooldown": random.random()*3,
            "repro_radius": 15,
            "personal_space": 40,
            "personal_space_tolerance": 10,
            "flee_predator": True,
            "sight": 10,
            "max_speed": 5,
        }

    def init_sprite(self):
        #self.sprite = Rectangle(Point(self.position.x-5, self.position.y-5),
        #    Point(self.position.x+5, self.position.y+5))
        #self.sprite.setFill(color_rgb(0, 255, 0))

        try:
            self.sprite = Image(Point(self.position.x, self.position.y), "resources/plankton.png")
        except:
            self.sprite = Image(Point(self.position.x, self.position.y), "resources/plankton.gif")

    def set_highlight(self, intensity=0):
        pass