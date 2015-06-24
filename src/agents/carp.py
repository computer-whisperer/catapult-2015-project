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
            "max_bite": 30,
            "min_bite": 5,
            "max_hunger": 500,
            "hunger": 0,
            "repro_max_cooldown": 20,
            "repro_cooldown": 6,
            "age_days": 0,
            "sight": 120
        }

    def do_update(self, dt_hours):
        self.agent_data["age_days"] += dt_hours/24
        if self.agent_data["age_days"] < 3:
            # Carp is in an egg, set stuff appropriately
            self.cycle_state = 0
            self.agent_data.update({
                "calories": 50,
                "hunger_rate": 0,
                "max_speed": 0
            })
        elif self.agent_data["age_days"] < 6:
            # Carp is a young fish, set stuff appropriately
            self.cycle_state = 1
            self.agent_data.update({
                "calories": 75,
                "hunger_rate": 75,
                "max_speed": 5,
            })
        elif self.agent_data["age_days"] < 365:
            # Carp is an adult, set stuff appropriately
            self.cycle_state = 2
            self.agent_data.update({
                "calories": 100,
                "hunger_rate": 100,
                "max_speed": 7,
                "repro_max_cooldown": 1
            })
        else:
            # Carp is elderly, set stuff appropriately
            self.cycle_state = 3
            self.agent_data.update({
                "calories": 80,
                "hunger_rate": 150,
                "max_speed": 5,
                "repro_max_cooldown": 2
            })

        super().do_update(dt_hours)

    def init_sprite(self):
        #self.sprite = Rectangle(Point(self.position.x-5, self.position.y-5),
        #    Point(self.position.x+5, self.position.y+5))
        #self.sprite.setFill(color_rgb(255, 0, 0))

        self.sprite = Image(Point(self.position.x, self.position.y), "../fish-small.png")

    def set_highlight(self, intensity=0):
        pass
