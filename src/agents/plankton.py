from agents import Agent
from graphics import *
import traits

class Plankton(Agent):

    default_traits = [
        traits.MaxSpeed,
        traits.Food,
        traits.Reproduction
    ]

    def init_agent_data(self):
        return {
            "calories": 10,
            "max_bite": 0,
            "max_hunger": 100,
            "hunger": 0,
            "hunger_rate": 0,
            "max_speed": 5,
            "repro_max_cooldown": 30
        }


    def init_sprite(self):
        self.sprite = Circle(self.position, 5)
        self.sprite.setFill(color_rgb(0, 255, 0))
