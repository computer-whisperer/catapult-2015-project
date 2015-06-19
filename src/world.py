from graphics import *
from utilities import *
from agent import Agent
import random

class World(object):

    run = False
    do_reset = True

    def __init__(self, dimensions):
        self.agents = []
        self.selected_agent = None
        self.window = GraphWin(title="My World", width=dimensions.x, height=dimensions.y)
        self.window.setCoords(-dimensions.x/2, dimensions.y/2, dimensions.x/2, -dimensions.y/2)
        self.window.setBackground(color_rgb(255, 255, 255))
        self.dimensions = dimensions

        self.population_gen_params = {
            "count": 50,
            "spawn_center": Vector2D(),
            "max_spread": 250,
            "min_spread": 50,
            "agent_class": Agent
        }

    def set_population_gen(self, params):
        self.population_gen_params.update(params)

    def add_agent(self, agent):
        agent.draw(self.window)
        self.agents.append(agent)
        self.selected_agent = agent

    def select_agent(self, agent):
        self.selected_agent.set_highlight()
        agent.set_highlight(255)
        self.selected_agent = agent

    def reset(self):
        params = self.population_gen_params

        for agent in self.agents:
            agent.undraw()
        self.agents = []
        params["agent_class"].reset_id()
        for _ in range(params["count"]):
            agent = params["agent_class"]()
            agent.randomize_traits()
            spread_vector = Vector2D(r=random.uniform(params["min_spread"], params["max_spread"]),
                                     theta=random.random() * 360)
            agent.set_state({"position": params["spawn_center"] + spread_vector})
            self.add_agent(agent)

    def tick(self, dt):

        if self.do_reset:
            self.reset()
            self.do_reset = False

        click_pos = self.window.checkMouse()

        if click_pos is not None:
            for agent in self.agents:
                if (agent.state["position"] - click_pos).r <= 10:
                    self.select_agent(agent)

        if not self.run:
            return

        for agent in self.agents:
            agent.reset_force()

            # Calculate sociality forces

            for agent_b in self.agents:
                if agent_b is agent:
                    continue
                agent_b_pos = agent_b.state["position"]
                if -self.dimensions.x/2 < agent_b_pos.x < self.dimensions.x/2 and\
                   -self.dimensions.y/2 < agent_b_pos.y < self.dimensions.y/2:
                    delta = agent.state["position"] - agent_b_pos
                    agent.add_force(Vector2D(r=250/delta.r, theta=delta.theta) * agent.traits["sociality"])

        for agent in self.agents:
            agent.apply_forces(dt)
