from .fish import Fish
from .agent import Agent
from graphics import *
import traits
import random
class Carp(Fish):

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
            "max_bite": 60,
            "min_bite": 5,
            "repro_max_cooldown": 1,
            "repro_cooldown": 6,
            "repro_radius": 15,
            "personal_space": 10,
            "personal_space_tolerance": 15,
            "age_days": random.random()*4,
            "sight": 500
        }

    def do_update(self, dt_hours):
        self.agent_data["age_days"] += dt_hours/24
        if self.agent_data["age_days"] < 4:
            # Carp is in an egg, set stuff appropriately
            self.cycle_state = 0
            self.agent_data.update({
                "calories": 100,
                "hunger_rate": 0,
                "max_speed": 0
            })
        elif self.agent_data["age_days"] < 7:
            # Carp is a young fish, set stuff appropriately
            self.cycle_state = 1
            self.agent_data.update({
                "calories": 200,
                "hunger_rate": 70,
                "max_speed": 8,
            })
        else:
            # Carp is an adult, set stuff appropriately
            self.cycle_state = 2
            self.agent_data.update({
                "calories": 400,
                "hunger_rate": 140,
                "max_speed": 16,
            })

        Agent.do_update(self, dt_hours)

    def init_sprite(self):


        try:
            self.sprite = Image(Point(self.position.x, self.position.y), "resources/carp.png")
        except:
            self.sprite = Image(Point(self.position.x, self.position.y), "resources/carp.gif")

