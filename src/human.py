# human.py

from math import *
from graphics import *
from random import *
import time

#############################################
#   Traits  |   All values are from 0 to 1  #
#-------------------------------------------#
#   Individualism   vs      Collectivism    # 
#   Sociability     vs      Survivalist     # 
#   Wealthy         vs      Needy           #
#   Strong          vs      Weak            #   # 
#   Smart           vs      Dumbass         # 
#   Leader          vs      Follower        # 
#   Aggression      vs      Pacifism        # 
#   Anarchist       vs      Communist       # 
#############################################

class Human(object):
    
    social = 1 - (random() * random())

    def social(self):
        return self.social

    def update(self):
        return 0
