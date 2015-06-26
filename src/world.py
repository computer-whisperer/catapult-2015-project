import random
from graphics import *

from utilities import *
from agents import *
from traits import *

class World(object):

    run = False
    do_reset = True

    def __init__(self, dimensions, scale=1, rate=1, max_update=1):
        """
        :param dimensions: A Vector2D with the internal x and y dimensions of the world
        :param scale: The render scale of the world. Larger numbers decrease the rendered size.
        :param rate: The ratio of real-life seconds to in-sim hours
        :param max_update: The maximum time, in in-sim hours, to simulate in a single tick
        """
        self.agents = []
        self.rate = rate
        self.selected_agent = None
        self.window = GraphWin(title="My World", width=dimensions.x/scale, height=dimensions.y/scale, autoflush=False)
        self.window.setCoords(-dimensions.x/2, dimensions.y/2, dimensions.x/2, -dimensions.y/2)
        # try:
        #     self.background_img = Image(Point(0, 0), "resources/backdrop.png")
        # except:
        #     self.background_img = Image(Point(0, 0), "resources/backdrop.gif")
        # self.background_img.draw(self.window)
        self.window.setBackground(color_rgb(255, 255, 255))
        self.dimensions = dimensions
        self.scale = scale
        self.max_update = max_update

        self.population_gen_params = {
            "Plankton": {
                "class": Plankton,
                "count": 25,
                "spawn_area_top_left": Vector2D(-dimensions.x/2, -dimensions.y/2),
                "spawn_area_bottom_right": Vector2D(dimensions.x/2, dimensions.y/2),
                "extra_traits": []
            },
            "Carp": {
                "class": Carp,
                "count": 0,
                "spawn_area_top_left": Vector2D(-dimensions.x/2, -dimensions.y/2),
                "spawn_area_bottom_right": Vector2D((3/4)*(-dimensions.x/2), dimensions.y/2),
                "extra_traits": []
            },
            "Fish": {
                "class": Fish,
                "count": 20,
                "spawn_area_top_left": Vector2D(-dimensions.x/2, -dimensions.y/2),
                "spawn_area_bottom_right": Vector2D(dimensions.x/2, dimensions.y/2),
                "extra_traits": []
            },
            "Pelican": {
                "class": Pelican,
                "count": 0,
                "spawn_area_top_left": Vector2D(-dimensions.x/2, -dimensions.y/2),
                "spawn_area_bottom_right": Vector2D(dimensions.x/2, dimensions.y/2),
                "extra_traits": []
            }
        }

        self.population_gen_params = {
            "Plankton": {
                "class": Plankton,
                "count": 3,
                "spawn_area_top_left": Vector2D(-dimensions.x/2, -dimensions.y/2),
                "spawn_area_bottom_right": Vector2D(0, 0),
                "extra_traits": []
            },
            "Carp": {
                "class": Carp,
                "count": 3,
                "spawn_area_top_left": Vector2D(0, -dimensions.y/2),
                "spawn_area_bottom_right": Vector2D(dimensions.x/2, 0),
                "extra_traits": []
            },
            "Fish": {
                "class": Fish,
                "count": 3,
                "spawn_area_top_left": Vector2D(-dimensions.x/2, 0),
                "spawn_area_bottom_right": Vector2D(0, dimensions.y/2),
                "extra_traits": []
            },
            "Pelican": {
                "class": Pelican,
                "count": 3,
                "spawn_area_top_left": Vector2D(0, 0),
                "spawn_area_bottom_right": Vector2D(dimensions.x/2, dimensions.y/2),
                "extra_traits": []
            }
        }

    def select_agent(self, agent):
        self.selected_agent = agent

    def reset(self):
        for agent in self.agents:
            agent.on_death()
        self.agents = []
        for agent_type in self.population_gen_params:
            gen_params = self.population_gen_params[agent_type]
            gen_params["class"].reset_id()
            top_left = gen_params["spawn_area_top_left"]
            bottom_right = gen_params["spawn_area_bottom_right"]
            for _ in range(gen_params["count"]):
                spawn_pos = Vector2D(random.uniform(top_left.x, bottom_right.x),
                                         random.uniform(top_left.y, bottom_right.y))
                self.spawn_agent(agent_type, spawn_pos)

    def spawn_agent(self, type, pos=Vector2D()):
        gen_params = self.population_gen_params[type]
        agent = gen_params["class"](type)
        agent.add_traits(gen_params["extra_traits"])
        agent.position = pos
        agent.set_world(self)
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
                if (agent.position - click_pos).r <= 10*self.scale:
                    self.select_agent(agent)

        if self.run:
            # Convert real_dt second count to sim_dt hour count
            sim_dt = real_dt * self.rate
            # Give it a ceiling of max_update
            sim_dt = min(sim_dt, self.max_update)
            # Run do_move
            self.do_move(sim_dt)
            # Process updates
            torem = []
            for agent in self.agents:
                agent.do_update(sim_dt)
                if not agent.alive:
                    torem.append(agent)
            for agent in torem:
                self.agents.remove(agent)

    def do_move(self, sim_dt):

        if self.run:
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
