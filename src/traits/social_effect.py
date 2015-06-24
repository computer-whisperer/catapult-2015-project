from .trait import Trait
from utilities import *
import random

class SocialEffect(Trait):

    value = 0

    def init_agent_data(self):
        return {
            "social_effect": random.uniform(-10, 10),
            "personal_space": 10
        }

    def do_update(self, dt_hours):
        total_effect = Vector2D()
        for target_agent in self.agent.world.agents_in_range(self.agent.position, -1):
            if target_agent is self.agent or type(target_agent) != type(self.agent):
                continue
            delta = target_agent.position - self.agent.position
            if delta.r != 0:
                total_effect += Vector2D(r=250/delta.r, theta=delta.theta)
        self.agent.movement += Vector2D(r=self.agent.agent_data["social_effect"], theta=total_effect.theta)
