from razormane import RazorMane


class HellHound(RazorMane):

    def __init__(self, *args):
        super(HellHound, self).__init__(*args)
        self.speed = 180
        self.stats.maxhp = 200
        self.stats.hp = 200
        self.stats.att = 32
        self.stats.exp = 80
        self.name='hellhound'