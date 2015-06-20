from .trait import Trait
from utilities import *
import random

class Madness(Trait):

    value = 0
    speed = 0
    heading = 0

    def randomize(self):
        self.value = random.uniform(0, 10)
        self.speed = self.value * 10
        self.heading = random.uniform(0, 360)

    def do_update(self, dt):
        self.heading += self.speed * dt
        self.agent.movement += Vector2D(r=self.value, theta=self.heading)
