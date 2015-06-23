
class Trait(object):

    value = 0

    def __init__(self, agent):
        self.agent = agent

    def init_agent_data(self):
        return {}

    def do_update(self, dt):
        pass

    def do_move(self, dt):
        pass
