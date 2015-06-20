from agents import Agent
from graphics import *
import traits

class Carp(Agent):

    default_traits = [
        traits.MaxSpeed,
        traits.SocialEffect,
        traits.Madness
    ]

    def do_draw(self, dt):
        if self.sprite is None:
            self.sprite = Circle(self.position, 5)
            self.sprite.setFill(color_rgb(255, 0, 0))
            self.sprite.draw(self.world.window)
            self.set_highlight()
        delta_pos = self.position - self.sprite.getCenter()
        self.sprite.move(delta_pos.x, delta_pos.y)
