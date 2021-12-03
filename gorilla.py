from yeti import Yeti


class Gorilla(Yeti):

    def __init__(self, *args):
        super(Gorilla, self).__init__(*args)
        self.speed = 90
        self.stats.maxhp = 250
        self.stats.hp = 250
        self.stats.att = 30
        self.stats.exp = 200
        self.name='gorilla'
