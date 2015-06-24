from agents import Agent
from graphics import *
import traits

class Fish(Agent):

    

    default_traits = [
        traits.MaxSpeed,
        traits.SocialEffect,
        traits.Madness,
        traits.Reproduction,
        traits.Food
    ]

    def init_agent_data(self):
        return {
            "calories": 20,
            "max_bite": 10,
            "min_bite": 4,
            "max_hunger": 70,
            "hunger_rate": 1,
            "hunger": 0,
            "repro_max_cooldown": 100,
            "age": 0,
            "max_speed": 20,
            "madness": 2,
        }

    

    def init_sprite(self):
        self.sprite = Circle(self.position, 5)
        self.sprite.setFill(color_rgb(0, 0, 255))
