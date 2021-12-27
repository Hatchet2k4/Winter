from razormane import RazorMane


class HellHound(RazorMane):

    def __init__(self, *args):
        super(HellHound, self).__init__(*args)
        self.speed = 180
        self.stats.maxhp = 240
        self.stats.hp = 240
        self.stats.att = 40
        self.stats.exp = 50
        self.stats.givemp=20
        self.name='hellhound'
        self.stats.givemp=12