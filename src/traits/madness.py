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
        if length < 0:
            length = 0
        if random() * 10 > 2**self.value / 100 and length == 0:
            self.heading += self.speed * dt
            self.agent.movement += Vector2D(r=self.value, theta=self.heading)
            last_x =
            last_y = 
        elif length > 0:
            length += -1 * dt
        else:
            self.update_spasm()

    def get_movement(self):
        if last_x is not None:
            dx = self.getX() - last_x
            dy = self.getY() - last_y
        else:
            dx = self.getX()
            dy = self.getY()
        return atan(dy/dx)

    def update_spasm(self):
        self.agent.movement += Vector2D(r = 10 * random(), theta = getMovement()) #Determine current or planned direction
        length = random() * self.value
