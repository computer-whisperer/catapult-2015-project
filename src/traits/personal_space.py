from .trait import Trait
from utilities import *
import random

class PersonalSpace(Trait):

    value = 0

    def init_agent_data(self):
        return {
            "personal_space": 10,
            "personal_space_tolerance": 15
        }

    def do_update(self, dt_hours):

        total_effect = Vector2D()
        crowd_score = 0
        for target_agent in self.agent.get_visible_agents():
            if target_agent is self.agent or type(target_agent) != type(self.agent):
                continue
            delta = target_agent.position - self.agent.position
            if delta.r != 0:
                score = self.agent.agent_data["personal_space"]/delta.r
                total_effect += Vector2D(r=score, theta=delta.theta+180)
                crowd_score += score
        if crowd_score > self.agent.agent_data["personal_space_tolerance"]:
            self.agent.on_death()
        self.agent.movement += total_effect
