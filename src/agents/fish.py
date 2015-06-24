from agents import Agent
from graphics import *
import traits

class Fish(Agent):

    default_traits = [
        traits.MaxSpeed,
        traits.PersonalSpace,
        traits.Madness,
        traits.Reproduction,
        traits.Food
    ]

    def init_agent_data(self):
        return {
            "calories": 100,
            "max_bite": 30,
            "min_bite": 5,
            "max_hunger": 500,
            "hunger_rate": 75,
            "hunger": 0,
            "repro_max_cooldown": 100,
            "repro_cooldown": 6,
            "age_days": 0,
            "max_speed": 7,
            "sight": 200
        }

    def init_sprite(self):
        #self.sprite = Rectangle(Point(self.position.x-5, self.position.y-5),
        #    Point(self.position.x+5, self.position.y+5))
        #self.sprite.setFill(color_rgb(0, 0, 255))

        try:
            self.sprite = Image(Point(self.position.x, self.position.y), "resources/fish.png")
        except:
            self.sprite = Image(Point(self.position.x, self.position.y), "resources/fish.gif")

    def set_highlight(self, intensity=0):
        pass