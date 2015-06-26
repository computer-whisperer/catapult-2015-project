from utilities import *
from world import World
from controller import Controller
import time

# Simulation Timing:
UPDATES_PER_SECOND = 30  # Count of logic updates to process per second

FRAMES_PER_SECOND = 30  # Count of graphic updates to process per second

SIMULATION_RATE = 8  # Ratio of in-sim hours to real-life seconds
MAX_UPDATE = .75

SCALE = 1
WORLD_DIMENSIONS = Vector2D(1000, 1000)

USE_CONTROLLER = False
AUTOSTART = True

def main():

    world = World(WORLD_DIMENSIONS, SCALE, SIMULATION_RATE, MAX_UPDATE)
    world.run = AUTOSTART

    if USE_CONTROLLER:
        controller = Controller(world)
        controller.start()

    current_time = time.time()

    last_update = current_time
    update_period = 1/UPDATES_PER_SECOND

    last_draw = current_time
    draw_period = 1/FRAMES_PER_SECOND

    while True:
        current_time = time.time()
        update_delta = current_time - last_update
        draw_delta = current_time - last_draw

        if update_delta > update_period:
            world.do_update(update_delta)
            last_update = current_time

        if draw_delta > draw_period:
            world.do_draw(draw_delta)
            last_draw = current_time

        time.sleep(.01)

    if USE_CONTROLLER:
        controller.join()

if __name__ == "__main__":
    main()
