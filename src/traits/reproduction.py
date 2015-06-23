from .trait import Trait
from utilities import *
import random

class Reproduction(Trait):

    def init_agent_data(self):
        return {
            "repro_value": 10,
            "gender": random.choice([True, False]),
            "repro_max_cooldown": random.uniform(5, 10),
            "repro_cooldown": 0}

    def do_update(self, dt):
        total_effect = Vector2D()
        for target_agent in self.agent.world.agents_in_range(self.agent.position, -1):
            if target_agent is self.agent:
                continue
            if not isinstance(target_agent, type(self.agent)):
                continue
            if target_agent.agent_data["gender"] is self.agent.agent_data["gender"]:
                continue
            if self.agent.agent_data["repro_cooldown"] > 0 or target_agent.agent_data["repro_cooldown"] > 0:
                continue
            delta = target_agent.position - self.agent.position
            if delta.r != 0:
                total_effect += Vector2D(r=250/delta.r, theta=delta.theta)
            if (self.agent.position - target_agent.position).r < 10:
                self.agent.agent_data["repro_cooldown"] = self.agent.agent_data["repro_max_cooldown"]
                target_agent.agent_data["repro_cooldown"] = target_agent.agent_data["repro_max_cooldown"]
                self.agent.world.spawn_agent(self.agent.agent_type, self.agent.position)
        self.agent.movement += Vector2D(r=total_effect.r * self.agent.agent_data["repro_value"], theta=total_effect.theta)

        if self.agent.agent_data["repro_cooldown"] > 0:
            self.agent.agent_data["repro_cooldown"] -= dt

