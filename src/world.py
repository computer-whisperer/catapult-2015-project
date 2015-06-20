import random

from graphics import *

from utilities import *
from agents import *
from traits import *


class World(object):

    run = False
    do_reset = True

    def __init__(self, dimensions):
        self.agents = []
        self.selected_agent = None
        self.window = GraphWin(title="My World", width=dimensions.x, height=dimensions.y, autoflush=False)
        self.window.setCoords(-dimensions.x/2, dimensions.y/2, dimensions.x/2, -dimensions.y/2)
        self.window.setBackground(color_rgb(255, 255, 255))
        self.dimensions = dimensions

        self.population_gen_params = {
            "Carp": {
                "class": Carp,
                "count": 25,
                "spawn_center": Vector2D(),
                "max_spread": 250,
                "min_spread": 50,
                "extra_traits": [MaxSpeed, SocialEffect]
            },
            "Algae": {
                "class": Agent,
                "count": 25,
                "spawn_center": Vector2D(),
                "max_spread": 250,
                "min_spread": 50,
                "extra_traits": [MaxSpeed, SocialEffect]
            }
        }

    def add_agent(self, agent):
        agent.set_world(self)
        self.agents.append(agent)
        self.selected_agent = agent

    def select_agent(self, agent):
        self.selected_agent.set_highlight()
        agent.set_highlight(255)
        self.selected_agent = agent

    def reset(self):
        for agent in self.agents:
            agent.set_world(None)
        self.agents = []
        for agent_type in self.population_gen_params:
            gen_params = self.population_gen_params[agent_type]
            gen_params["class"].reset_id(agent_type)
            for _ in range(gen_params["count"]):
                agent = gen_params["class"]()
                agent.add_traits(gen_params["extra_traits"])
                agent.randomize_traits()
                spread_vector = Vector2D(r=random.uniform(gen_params["min_spread"], gen_params["max_spread"]),
                                         theta=random.random() * 360)
                agent.position = gen_params["spawn_center"] + spread_vector
                self.add_agent(agent)

    def agents_in_range(self, point, radius=-1):
        if radius < 0:
            for agent in self.agents:
                yield agent
        else:
            for agent in self.agents:
                if (agent.state["position"] - point).r <= radius:
                    yield agent

    def do_update(self, dt):

        if self.do_reset:
            self.reset()
            self.do_reset = False

        click_pos = self.window.checkMouse()

        if click_pos is not None:
            for agent in self.agents:
                if (agent.position - click_pos).r <= 10:
                    self.select_agent(agent)

        if self.run:
            for agent in self.agents:
                agent.do_update(dt)

    def do_move(self, dt):
        if self.run:
            for agent in self.agents:
                agent.do_move(dt)

                # Handle world boundaries
                if -self.dimensions.x/2 > agent.position.x:
                    agent.position.x = -self.dimensions.x/2
                if self.dimensions.x/2 < agent.position.x:
                    agent.position.x = self.dimensions.x/2
                if -self.dimensions.y/2 > agent.position.y:
                    agent.position.y = -self.dimensions.y/2
                if self.dimensions.y/2 < agent.position.y:
                    agent.position.y = self.dimensions.y/2

    def do_draw(self, dt):
        for agent in self.agents:
            agent.do_draw(dt)

        self.window.update()
