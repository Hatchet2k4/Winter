from yeti import Yeti


class Gorilla(Yeti):

    def __init__(self, *args):
        super(Gorilla, self).__init__(*args)
        self.speed = 90
        self.stats.maxhp = 200
        self.stats.hp = 200
        self.stats.att = 24
        self.stats.exp = 200
