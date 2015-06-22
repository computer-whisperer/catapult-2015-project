#from .trait import Trait
#from utilities import *
#import random
#
#class Madness(Trait):
#
#    value = 0
#    speed = 0
#    heading = 0
#
#    def randomize(self):
#        self.value = random.uniform(0, 10)
#        self.speed = self.value * 10
#        self.heading = random.uniform(0, 360)
#
#    def do_update(self, dt):
#        self.heading += self.speed * dt
#        self.agent.movement += Vector2D(r=self.value, theta=self.heading)
#
from .trait import Trait
from utilities import *
import random
import math

class Madness(Trait):

    value = 0
    speed = 0
    heading = 0
    length = 0.0
    last_pos = Vector2D()
    last_x = None
    last_y = None

    def randomize(self):
        self.value = random.uniform(0, 10)
        self.speed = self.value * 10
        self.heading = random.uniform(0, 360)

    def do_update(self, dt):
        if self.length < 0:
            self.length = 0
        if random.random() * 10 > 2**self.value / 100 and self.length == 0:
            self.heading += self.speed * dt
            self.agent.movement += Vector2D(r=self.value, theta=self.heading)
            self.last_x = self.agent.position.x
            self.last_y = self.agent.position.y
        elif self.length > 0:
            self.length += -1 * dt
        else:
            self.update_spasm()

    def get_movement(self):
        if self.last_x is not None:
            dx = self.agent.position.x - self.last_x
            dy = self.agent.position.y - self.last_y
        else:
            dx = self.agent.position.x
            dy = self.agent.position.y
        return math.atan2(dy, dx)

    def update_spasm(self):
        self.agent.movement += Vector2D(r = 1000 * random.random() * self.value, theta = self.get_movement()) #Determine current or planned direction
        self.length = random.random() * self.value * 10
