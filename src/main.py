from math import *
from random import *
from graphics import *
import time

#init
people = []
population = 20
size = 50

#create our population
for i in range(population):
    people.append(Human(size * random(), size * random()))

#update accordingly
for i in range(population):
    people[i].update()
