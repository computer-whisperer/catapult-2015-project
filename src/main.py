from utilities import *
from world import World
from controller import Controller
import time

# Simulation Timing:
UPDATES_PER_SECOND = 30  # Count of logic updates to process per second

MOVES_PER_SECOND = 30  # Count of movement updates to process per second
# (Should be at least equal to UPDATES_PER_SECOND, but no greater than MOVES_PER_SECOND)

FRAMES_PER_SECOND = 30  # Count of graphic updates to process per second

SIMULATION_RATE = 8  # Ratio of in-sim hours to real-life seconds

WORLD_DIMENSIONS = Vector2D(500, 500)
USE_CONTROLLER = True
AUTOSTART = True

def main():

    world = World(WORLD_DIMENSIONS, SIMULATION_RATE)
    world.run = AUTOSTART

    if USE_CONTROLLER:
        controller = Controller(world)
        controller.start()

    current_time = time.time()

    last_update = current_time
    update_period = 1/UPDATES_PER_SECOND

    last_move = current_time
    move_period = 1/MOVES_PER_SECOND

    last_draw = current_time
    draw_period = 1/FRAMES_PER_SECOND

    while True:
        current_time = time.time()
        update_delta = current_time - last_update
        move_delta = current_time - last_move
        draw_delta = current_time - last_draw

        if update_delta > update_period:
            world.do_update(update_delta)
            last_update = current_time

        if move_delta > move_period:
            world.do_move(move_delta)
            last_move = current_time

        if draw_delta > draw_period:
            world.do_draw(draw_delta)
            last_draw = current_time

        time.sleep(.01)

    if USE_CONTROLLER:
        controller.join()

if __name__ == "__main__":
    main()
