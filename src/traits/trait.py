
class Trait(object):

    value = 0

    def __init__(self, agent):
        self.agent = agent

    def randomize(self):
        pass

    def do_update(self, dt):
        pass

    def do_move(self, dt):
        pass

    def get_info(self):
        return "{}: {}".format(self.__class__.__name__, self.value)
