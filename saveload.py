"""Save/loadgame semantic poop.
   Binary would be a pain in the ass.  Fuckit.  Cheat all you want,
   see if I care.
"""

import savedata
import system
from statset import StatSet
import base64

quicksave=None

from automap import map

class SaveGame(object):
    def __init__(self, fileName = None):
        self.stats = StatSet()
        self.flags = {}
        self.mapName = ''
        self.time = ''
        self.seconds=0
        self.minutes=0
        self.hours=0
        self.fname = fileName
        self.visible = [0]*(map.mapwidth*map.mapheight)
        self.visited = [0]*(map.mapwidth*map.mapheight)

        self.pos = (0, 0, 0)
        if fileName:
            self.load(fileName)

    def getStats(self):
        self.stats = system.engine.player.stats.clone()
        self.visible = map.visiblerooms[:]
        self.visited = map.visitedrooms[:]
		
    def setStats(self):
        system.engine.player.stats = self.stats.clone()
        map.visiblerooms = self.visible[:]
        map.visitedrooms = self.visited[:]
        
    def getFlags(self):
        self.flags = {}
        for k, v in savedata.__dict__.iteritems():
            if isinstance(v, (int, str, list, tuple)):
                self.flags[k] = v

    def setFlags(self):
        self.clearSaveFlags()
        for k, v in self.flags.iteritems():
            savedata.__dict__[k] = v

    def clearSaveFlags():
        destroy = []
        for var, val in savedata.__dict__.iteritems():
            if not var.startswith('_') and isinstance(val, (str, int, list, tuple)):
                destroy.append(var)
        for d in destroy:
            del savedata.__dict__[d]

    clearSaveFlags = staticmethod(clearSaveFlags)

    def currentGame():
        s = SaveGame()
        s.getStats()
        s.getFlags()
        s.mapName = system.engine.mapName
        s.time = system.engine.time
        s.seconds = system.engine.seconds
        s.minutes = system.engine.minutes
        s.hours = system.engine.hours
        s.visible = map.visiblerooms        	
        s.visited = map.visitedrooms 
        
        p = system.engine.player
        s.pos = (p.x, p.y, p.layer)
        return s

    currentGame = staticmethod(currentGame)

    def setCurrent(self):
        self.setStats()
        self.setFlags()

    def save(self, fileName):
        file(fileName, 'wt').write(str(self))

    def load(self, fileName):
        self.read(file(fileName, 'rt'))

    def __str__(self):
        s = ''
        for k in StatSet.STAT_NAMES:
            s += '%s=%i\n' % (k, self.stats[k])
        s += 'FLAGS\n'
        s += 'MAPNAME=\'%s\'\n' % self.mapName        
        s += 'POS=\'%s\'\n' % ','.join([str(x) for x in self.pos])
        s += 'TIME=\'%s\'\n' % self.time
        s += 'SECONDS=\'%s\'\n' % str(self.seconds)
        s += 'MINUTES=\'%s\'\n' % str(self.minutes)
        s += 'HOURS=\'%s\'\n' % str(self.hours)
        s += 'MAPDATA=\'%s\'\n' % ','.join([str(x) for x in map.visiblerooms])        
        s += 'MAPDATA2=\'%s\'\n' % ','.join([str(x) for x in map.visitedrooms])        
        for var, val in savedata.__dict__.iteritems():
            if not var.startswith('_'):
                if isinstance(val, (int, str)):
                    s += '%s=%r\n' % (var, val)

                elif isinstance(val, (list, tuple)):
                    s += '%s=LIST\n' % var
                    for el in val:
                        s += '  %s\n' % `el`
                    s += 'END\n'

        
        return s

    def read(self, f):
        lines = [x.strip() for x in f.readlines()]

        def parse(v):
            v = v.strip()
            if v == 'LIST':
                l = []
                while True:
                    v = lines.pop(0)
                    if v == 'END':      break
                    else:               l.append(parse(v))
                return l

            elif v.startswith("'"):
                return v[1:-1]
            else:
                return int(v)

        # Read stats
        while True:
            s = lines.pop(0)
            if s == 'FLAGS':    break
            
            p = s.find('=')
            k, v = s[:p], s[p + 1:]
            setattr(self.stats, k, parse(v))

        # read flags
        while lines:
            s = lines.pop(0)

            p = s.find('=')
            k, v = s[:p], parse(s[p + 1:])
            if k == 'MAPNAME':  self.mapName = v
            elif k == 'TIME': self.time=v
            elif k == 'SECONDS': self.seconds=int(v)
            elif k == 'MINUTES': self.minutes=int(v)
            elif k == 'HOURS': self.hours=int(v)
            elif k == 'POS':
                self.pos = tuple([int(x) for x in v.split(',')])
            elif k == 'MAPDATA':                             
				self.visible = [int(x) for x in v.split(',')]      
            elif k == 'MAPDATA2':                                 
				self.visited = [int(x) for x in v.split(',')]                      
            else:               
                self.flags[k] = v

        #read map data
        #s = lines.pop(0)
        #map.visible = [int(x) for x in s.split(', ')]
        

#test()
