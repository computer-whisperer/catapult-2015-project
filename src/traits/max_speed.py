__author__ = 'christian'
from .trait import Trait
from utilities import *
import random

class MaxSpeed(Trait):

    value = 10

    def randomize(self):
        self.value = random.uniform(5, 10)

    def do_move(self, dt):
        current_vel = self.agent.movement
        self.agent.movement = Vector2D(r=min(current_vel.r, self.value), theta=current_vel.theta)
