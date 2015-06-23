from .trait import Trait
from utilities import *
import random

class MaxSpeed(Trait):

    def init_agent_data(self):
        return {
            "max_speed": random.uniform(0, 10),
        }

    def do_move(self, dt):
        current_vel = self.agent.movement
        self.agent.movement = Vector2D(r=min(current_vel.r, self.agent.agent_data["max_speed"]), theta=current_vel.theta)
