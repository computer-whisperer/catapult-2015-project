from agents import Agent
from graphics import *
import traits

class Carp(Agent):

    HATCH_TIME = 7*24

    default_traits = [
        traits.MaxSpeed,
        traits.SocialEffect,
        traits.Madness,
        traits.Reproduction,
        traits.Food
    ]

    def init_agent_data(self):
        return {
            "calories": 30,
            "max_bite": 15,
            "min_bite": 5,
            "max_hunger": 100,
            "hunger_rate": 1,
            "hunger": 0,
            "repro_max_cooldown": 100,
            "age": 0,
        }

    def do_update(self, dt):
        super().do_update(dt)

    def init_sprite(self):
        self.sprite = Circle(self.position, 5)
        self.sprite.setFill(color_rgb(255, 0, 0))
