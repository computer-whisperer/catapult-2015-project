from utilities import *
from world import World
from controller import Controller
import time

STARTING_POPULATION = 50
CYCLES_PER_SECOND = 60
WORLD_DIMENSIONS = Vector2D(500, 500)

def main():

    world = World(WORLD_DIMENSIONS)
    world.set_population_gen({"count": STARTING_POPULATION})
    controller = Controller(world)
    controller.start()
    last_time = time.time()
    while True:
        time.sleep(1/CYCLES_PER_SECOND)
        current_time = time.time()
        world.tick(current_time - last_time)
        last_time = current_time
    controller.join()

if __name__ == "__main__":
    main()
