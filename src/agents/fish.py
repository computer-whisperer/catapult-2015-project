from agents import Agent
from graphics import *
import traits
import random

class Fish(Agent):

    cycle_state = 0

    default_traits = [
        traits.MaxSpeed,
        traits.PersonalSpace,
        traits.Madness,
        traits.Reproduction,
        traits.Food
    ]

    def init_agent_data(self):
        return {
            "max_bite": 50,
            "min_bite": 5,
            "hunger": 0,
            "repro_max_cooldown": 100,
            "repro_cooldown": 6,
            "age_days": random.random()*4,
            "sight": 500,
        }

    def do_update(self, dt_hours):
        self.agent_data["age_days"] += dt_hours/24
        if self.agent_data["age_days"] < 3:
            # Fish is in an egg, set stuff appropriately
            self.cycle_state = 0

            self.agent_data.update({
                "calories": 75,
                "hunger_rate": 0,
                "max_speed": 0
            })
        elif self.agent_data["age_days"] < 6:
            # Fish is a young fish, set stuff appropriately
            self.cycle_state = 1
            self.agent_data.update({
                "calories": 150,
                "hunger_rate": 60,
                "max_speed": 7,
            })
        else:
            # Fish is an adult, set stuff appropriately
            self.cycle_state = 2
            self.agent_data.update({
                "calories": 300,
                "hunger_rate": 120,
                "max_speed": 12,
                "repro_max_cooldown": 1
            })
        super().do_update(dt_hours)

    def init_sprite(self):

        try:
            self.sprite = Image(Point(self.position.x, self.position.y), "resources/fish.png")
        except:
            self.sprite = Image(Point(self.position.x, self.position.y), "resources/fish.gif")

    def do_draw(self, dt_hours):
        pos = self.position
        if self.cycle_state == 0:
            if self.sprite is None:
                self.sprite = Circle(self.position, 3*self.world.scale)
                self.sprite.setFill(color_rgb(255, 0, 0))
                self.sprite.draw(self.world.window)
        else:
            if isinstance(self.sprite, Circle):
                self.sprite.undraw()
                self.sprite = None
            if self.sprite is None:
                self.init_sprite()
                self.sprite.draw(self.world.window)
        if hasattr(self.sprite, "getCenter"):
            delta_pos = pos - self.sprite.getCenter()
        else:
            delta_pos = pos - self.sprite.getAnchor()
        self.sprite.move(delta_pos.x, delta_pos.y)
