# agent.py

from random import *

class Agent(object):

    def __init__(self):
        self.traits = {}

        # Sociality is a measure, from -1 to 1, of how much the
        # agent likes to be near other agents.
        self.traits["sociality"] = (random()*2)-1




