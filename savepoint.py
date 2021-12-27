
from entity import Entity
import xi.effects

import system
import saveloadmenu
import dir

class SavePoint(Entity):
    def __init__(self, ent):
        Entity.__init__(self, ent, None)
        self.isTouching = False
        self.interruptable = False
        self.invincible = True
        self.touchtimer = 0

    def update(self):
        if self.touchtimer>0: self.touchtimer-=1
        t = self.touches(system.engine.player)
        if t and not self.isTouching and self.touchtimer==0:
            # bump the player backward, so he's not touching us anymore.
            xi.effects.fadeOut(50, draw=system.engine.draw)

            p = system.engine.player
            p.stats.hp = 999
            p.stats.mp = 999

            dx, dy = dir.delta[dir.invert[p.direction]]
            p.x, p.y = p.x + dx*5, p.y + dy*5

            # TODO: neato fadeout, etc.`
            # "Do you wish to save?" "Yes/No"

            self.isTouching = True
            system.engine.draw()
            saveloadmenu.saveMenu()
            xi.effects.fadeIn(50, draw=system.engine.draw)
            system.engine.synchTime()
            self.touchtimer=100

        elif not t:
            self.isTouching = False
