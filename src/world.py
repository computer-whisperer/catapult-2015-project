from graphics import *
from utilities import *
from agent import Agent
from traits import *
import random

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
            "count": 50,
            "spawn_center": Vector2D(),
            "max_spread": 250,
            "min_spread": 50,
            "agent_class": Agent,
            "traits": [
                MaxSpeed,
                SocialEffect,
                Madness]
        }



    def set_population_gen(self, params):
        self.population_gen_params.update(params)

    def add_agent(self, agent):
        agent.set_world(self)
        self.agents.append(agent)
        self.selected_agent = agent

    def select_agent(self, agent):
        self.selected_agent.set_highlight()
        agent.set_highlight(255)
        self.selected_agent = agent

    def reset(self):
        params = self.population_gen_params

        for agent in self.agents:
            agent.set_world(None)
        self.agents = []
        params["agent_class"].reset_id()
        for _ in range(params["count"]):
            agent = params["agent_class"]()
            agent.add_traits([trait(agent) for trait in params["traits"]])
            agent.randomize_traits()
            spread_vector = Vector2D(r=random.uniform(params["min_spread"], params["max_spread"]),
                                     theta=random.random() * 360)
            agent.position = params["spawn_center"] + spread_vector
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

    def do_draw(self, dt):
        for agent in self.agents:
            agent.do_draw(dt)

        self.window.update()
