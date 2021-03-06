from razormane import RazorMane


class DragonPup(RazorMane):

    def __init__(self, *args):
        super(DragonPup, self).__init__(*args)
        self.speed = 160
        self.stats.maxhp = 160
        self.stats.hp = 160
        self.stats.att = 28
        self.stats.exp = 40

class DragonGuard(RazorMane):

    def __init__(self, *args):
        super(DragonGuard, self).__init__(*args)
        self.speed = 160
        self.stats.maxhp = 200
        self.stats.hp = 200
        self.stats.att = 33
        self.stats.exp = 60
