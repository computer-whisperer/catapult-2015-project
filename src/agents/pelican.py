from agents import Agent
from graphics import *
import traits

class Carp(Agent):

    cycle_state = 0

    default_traits = [
        traits.MaxSpeed,
        traits.PersonalSpace,
        traits.Madness,
        traits.Reproduction,
        traits.Food
    ]

    def init_agent_data(self):
        return {
            "max_bite": 80,
            "min_bite": 50,
            "max_hunger": 500,
            "hunger_rate": 0,
            "hunger": 0,
            "sight": 200,
            "calories": 50,
            "max_speed": 7
        }

    def init_sprite(self):
        #self.sprite = Rectangle(Point(self.position.x-5, self.position.y-5),
        #    Point(self.position.x+5, self.position.y+5))
        #self.sprite.setFill(color_rgb(255, 0, 0))

        try:
            self.sprite = Image(Point(self.position.x, self.position.y), "resources/pelican.png")
        except:
            self.sprite = Image(Point(self.position.x, self.position.y), "resources/pelican.gif")




    def set_highlight(self, intensity=0):
        pass
