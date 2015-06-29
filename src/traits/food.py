from .trait import Trait
from agents import *
from utilities import *
import random

class Food(Trait):

    # Food value of agent
    value = 0
    cooldown = 0
    max_cooldown = 0

    def init_agent_data(self):
        return {
            "calories": 0,
            "max_bite": 30,
            "min_bite": 10,
            "hunger_rate": 10,
            "hunger": 0,
            "flee_predator": True,
            "sight": 100
        }

    def do_update(self, dt_hours):
        total_effect = Vector2D()

        for target_agent in self.agent.world.agents_in_range(self.agent.position, self.agent.agent_data["sight"]):
            if target_agent is self.agent:
                continue
            if isinstance(target_agent, type(self.agent)):
                continue

            if target_agent.agent_data["calories"] < self.agent.agent_data["hunger"] and\
                self.agent.agent_data["min_bite"] <=\
                target_agent.agent_data["calories"] <= \
                self.agent.agent_data["max_bite"]:

                # If the target agent is valid food for this agent, move towards it and eat it when close enough.
                delta = target_agent.position - self.agent.position
                if delta.r != 0:
                    total_effect += Vector2D(r=75*target_agent.agent_data["calories"]/delta.r, theta=delta.theta)
                if (self.agent.position - target_agent.position).r < 10:
                    self.agent.agent_data["hunger"] -= target_agent.agent_data["calories"]
                    target_agent.on_death()

            if self.agent.agent_data["flee_predator"]:

                if self.agent.agent_data["calories"] < target_agent.agent_data["hunger"] and\
                    target_agent.agent_data["min_bite"] <=\
                    self.agent.agent_data["calories"] <= \
                    target_agent.agent_data["max_bite"]:

                    # If the agent is valid food for the target agent, flee it!
                    delta = target_agent.position - self.agent.position
                    if delta.r != 0:
                        total_effect += Vector2D(r=100*self.agent.agent_data["calories"]/delta.r, theta=delta.theta+180)
        self.agent.movement += total_effect

        # Handle hunger depletion and starvation
        self.agent.agent_data["hunger"] += self.agent.agent_data["hunger_rate"] * dt_hours/24
        if self.agent.agent_data["hunger"] >= self.agent.agent_data["calories"]:
            self.agent.on_death()
