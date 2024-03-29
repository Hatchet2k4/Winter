from entity import Entity
from caption import Caption
import system
import savedata
import automap


class Dynamite(Entity):
    def __init__(self, ent):
        self.flagName = ent.name
        super(Dynamite, self).__init__(ent, None)
        self.invincible = True

        if self.flagName in savedata.__dict__:
            ent.x = ent.y = -100
            system.engine.destroyEntity(self)

    def update(self):
        assert self.flagName not in self.__dict__, 'Already have this.  Why are we updating?'
        if self.touches(system.engine.player):
            setattr(savedata, self.flagName, 'True')
            system.engine.player.stats.tnt+=1
            system.engine.player.stats.totaltnt+=1
            system.engine.destroyEntity(self)
            system.engine.addCaptions(Caption('Got a stick of dynamite!'))
            automap.map.SetCollected('TNT')
