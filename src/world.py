import random
from graphics import *

from utilities import *
from agents import *
from traits import *
import math

GRID_SIZE = 100
LAZY_UPDATE_TIMER_RESET = 1

class World(object):

    run = False
    do_reset = True
    selected_agent = None
    sim_age = 0

    def __init__(self, dimensions, scale=1, rate=1, max_update=1):
        """
        :param dimensions: A Vector2D with the internal x and y dimensions of the world
        :param scale: The render scale of the world. Larger numbers decrease the rendered size.
        :param rate: The ratio of real-life seconds to in-sim hours
        :param max_update: The maximum time, in in-sim hours, to simulate in a single tick
        """
        self.agents = []

        self.agent_grid = {}
        self.lazy_update_timer = 0

        self.stats = {}

        self.window = GraphWin(title="My World", width=dimensions.x/scale, height=dimensions.y/scale, autoflush=False)
        self.window.setCoords(-dimensions.x/2, dimensions.y/2, dimensions.x/2, -dimensions.y/2)
        self.window.setBackground(color_rgb(255, 255, 255))

        self.rate = rate
        self.dimensions = dimensions
        self.scale = scale
        self.max_update = max_update

        self.population_gen_params = {
            "Plankton": {
                "class": Plankton,
                "count": 30,
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
                "count": 10,
                "spawn_area_top_left": Vector2D(-dimensions.x/2, -dimensions.y/2),
                "spawn_area_bottom_right": Vector2D(dimensions.x/2, dimensions.y/2),
                "extra_traits": []
            },
            "Pelican": {
                "class": Pelican,
                "count": 1,
                "spawn_area_top_left": Vector2D(-dimensions.x/2, -dimensions.y/2),
                "spawn_area_bottom_right": Vector2D(dimensions.x/2, dimensions.y/2),
                "extra_traits": []
            }
        }

    def select_agent(self, agent):
        self.selected_agent = agent

    def reset(self):
        self.sim_age = 0
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
            cell_radius = int(math.ceil(radius/GRID_SIZE))
            cell_x, cell_y = int(point.x//GRID_SIZE), int(point.y//GRID_SIZE)
            for column in range(cell_x-cell_radius, cell_x+cell_radius):
                for row in range(cell_y-cell_radius, cell_y+cell_radius):
                    for agent in self.agent_grid.get(column, {}).get(row, []):
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

            # Process lazy world updates
            if self.lazy_update_timer < 0:
                self.agent_grid = {}
                self.stats = {
                    "real_fps": 1/real_dt,
                    "sim_fph": 1/sim_dt,
                    "sim_age (days)": self.sim_age
                }
                for agent in self.agents:
                    # Process grid
                    cell_x, cell_y = int(agent.position.x//GRID_SIZE), int(agent.position.y//GRID_SIZE)
                    if cell_x not in self.agent_grid:
                        self.agent_grid[cell_x] = {}
                    if cell_y not in self.agent_grid[cell_x]:
                        self.agent_grid[cell_x][cell_y] = []
                    self.agent_grid[cell_x][cell_y].append(agent)

                    # Process census
                    if agent.agent_type not in self.stats:
                        self.stats[agent.agent_type] = 0
                    self.stats[agent.agent_type] += 1

                self.grid_dirty = False
                self.lazy_update_timer = LAZY_UPDATE_TIMER_RESET

            # Process agent updates
            torem = []
            for agent in self.agents:
                agent.do_update(sim_dt)
                if not agent.alive:
                    torem.append(agent)

            # Process agent removals
            for agent in torem:
                self.agents.remove(agent)

            # Process timer updates
            self.lazy_update_timer -= sim_dt
            self.sim_age += sim_dt/24

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
