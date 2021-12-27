from yeti import Yeti


class Gorilla(Yeti):

    def __init__(self, *args):
        super(Gorilla, self).__init__(*args)
        self.speed = 90
        self.stats.maxhp = 300
        self.stats.hp = 300
        self.stats.att = 50
        self.stats.exp = 100
        self.name='gorilla'
        self.stats.givemp=20