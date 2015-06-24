from agents import Agent
from graphics import *
import traits

class Plankton(Agent):

    default_traits = [
        traits.MaxSpeed,
        traits.Food,
        traits.PersonalSpace,
        traits.Reproduction
    ]

    def init_agent_data(self):
        return {
            "calories": 25,
            "max_bite": 0,
            "max_hunger": 100,
            "hunger": 0,
            "hunger_rate": 0,
            "max_speed": .5,
            "repro_max_cooldown": 4,
            "repro_cooldown": 3,
            "asexual": True,
            "personal_space": 10,
            "crowding_resistance": 15,
            "flee_predator": True,
            "sight": 50
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