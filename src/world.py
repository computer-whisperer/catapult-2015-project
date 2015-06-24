import random
import math
from graphics import *

from utilities import *
from agents import *
from traits import *

GRID_SIZE = 150

class World(object):

    run = False
    do_reset = True

    def __init__(self, dimensions, rate):
        self.agents = []
        self.rate = rate
        self.selected_agent = None
        self.window = GraphWin(title="My World", width=dimensions.x, height=dimensions.y, autoflush=False)
        self.window.setCoords(-dimensions.x/2, dimensions.y/2, dimensions.x/2, -dimensions.y/2)
        try:
            self.background_img = Image(Point(0, 0), "resources/backdrop.png")
        except:
            self.background_img = Image(Point(0, 0), "resources/backdrop.gif")
        self.background_img.draw(self.window)
        self.window.setBackground(color_rgb(255, 255, 255))
        self.dimensions = dimensions

        self.population_gen_params = {
            "Agent": {
                "class": Agent,
                "count": 0,
                "spawn_center": Vector2D(),
                "max_spread": 250,
                "min_spread": 50,
                "extra_traits": []
            },
            "Plankton": {
                "class": Plankton,
                "count": 30,
                "spawn_center": Vector2D(0, 100),
                "max_spread": 100,
                "min_spread": 0,
                "extra_traits": [Madness]
            },
            "Carp": {
                "class": Carp,
                "count": 20,
                "spawn_center": Vector2D(0, -150),
                "max_spread": 100,
                "min_spread": 0,
                "extra_traits": []
            },
            "Fish": {
                "class": Fish,
                "count": 0,
                "spawn_center": Vector2D(),
                "max_spread": 250,
                "min_spread": 100,
                "extra_traits": []
            },
            "Pelican": {
                "class": Pelican,
                "count": 1,
                "spawn_center": Vector2D(),
                "max_spread": 250,
                "min_spread": 0,
                "extra_traits": []
            }
        }


    def select_agent(self, agent):
        self.selected_agent.set_highlight()
        agent.set_highlight(255)
        self.selected_agent = agent

    def reset(self):
        for agent in self.agents:
            agent.on_death()
        self.agents = []
        for agent_type in self.population_gen_params:
            gen_params = self.population_gen_params[agent_type]
            gen_params["class"].reset_id()
            for _ in range(gen_params["count"]):
                spread_vector = Vector2D(r=random.uniform(gen_params["min_spread"], gen_params["max_spread"]),
                                         theta=random.random() * 360)
                self.spawn_agent(agent_type, gen_params["spawn_center"] + spread_vector)

    def spawn_agent(self, type, pos=Vector2D()):
        gen_params = self.population_gen_params[type]
        agent = gen_params["class"](type)
        agent.add_traits(gen_params["extra_traits"])
        agent.position = pos
        agent.set_world(self)
        self.selected_agent = agent
        self.agents.append(agent)

        print("{} {} spawned!".format(type, agent.id))

    def agents_in_range(self, point, radius=-1):
        if radius < 0:
            for agent in self.agents:
                yield agent
        else:
            for agent in self.agents:
                if (agent.position - point).r <= radius:
                    yield agent

    def do_update(self, real_dt):
        if self.do_reset:
            self.reset()
            self.do_reset = False

        click_pos = self.window.checkMouse()

        if click_pos is not None:
            for agent in self.agents:
                if (agent.position - click_pos).r <= 10:
                    self.select_agent(agent)

        if self.run:
            # Convert real_dt second count to sim_dt hour count
            sim_dt = real_dt * self.rate
            torem = []
            for agent in self.agents:
                agent.do_update(sim_dt)
                if not agent.alive:
                    torem.append(agent)
            for agent in torem:
                self.agents.remove(agent)

    def do_move(self, real_dt):

        if self.run:
            # Convert real_dt second count to sim_dt hour count
            sim_dt = real_dt * self.rate
            for agent in self.agents:
                agent.do_move(sim_dt)

                # Handle world boundaries
                if -self.dimensions.x/2 > agent.position.x:
                    agent.position.x = -self.dimensions.x/2
                if self.dimensions.x/2 < agent.position.x:
                    agent.position.x = self.dimensions.x/2
                if -self.dimensions.y/2 > agent.position.y:
                    agent.position.y = -self.dimensions.y/2
                if self.dimensions.y/2 < agent.position.y:
                    agent.position.y = self.dimensions.y/2

    def do_draw(self, real_dt):

        for agent in self.agents:
            agent.do_draw(real_dt)

        self.window.update()
