"""Save/loadgame semantic poop.
   Binary would be a pain in the ass.  Fuckit.  Cheat all you want,
   see if I care.
"""

import savedata
import system
from statset import StatSet
import ika

quicksave=None

from automap import map


#import sys

def base64encode(s):
  i = 0
  base64 = ending = ''
  base64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
  
  # Add padding if string is not dividable by 3
  pad = 3 - (len(s) % 3)
  if pad != 3:
    s += "A" * pad
    ending += '=' * pad
  
  # Iterate though the whole input string
  while i < len(s):
    b = 0

    # Take 3 characters at a time, convert them to 4 base64 chars
    for j in range(0,3,1):
      
      # get ASCII code of the next character in line
      n = ord(s[i])
      i += 1
  
      # Concatenate the three characters together 
      b += n << 8 * (2-j)
    
    # Convert the 3 chars to four Base64 chars
    base64 += base64chars[ (b >> 18) & 63 ]
    base64 += base64chars[ (b >> 12) & 63 ]
    base64 += base64chars[ (b >> 6) & 63 ]
    base64 += base64chars[ b & 63 ]

  # Add the actual padding to the end
  if pad != 3:
    base64 = base64[:-pad]
    base64 += ending
  
  # Print the Base64 encoded result
  #print (base64)
  return base64
  


def base64decode(s):
  i = 0
  base64 = decoded = ''
  base64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
  
  # Replace padding with "A" characters so the decoder can process the string, and save the padding length for later
  if s[-2:] == '==':
    s = s[0:-2] + "AA"
    padd = 2
  elif s[-1:] == '=':
    s = s[0:-1] + "A"
    padd = 1
  else:
    padd = 0
  
  # Take 4 characters at a time 
  while i < len(s):
    d = 0
    for j in range(0,4,1):
      
      d += base64chars.index( s[i] ) << (18 - j * 6)
      i += 1
    
    # Convert the 4 chars back to ASCII
    decoded += chr( (d >> 16 ) & 255 )
    decoded += chr( (d >> 8 ) & 255 )
    decoded += chr( d & 255 )
  
  # Remove padding
  decoded = decoded[0:len( decoded ) - padd]
  
  # Print the Base64 encoded result
  return decoded
  #print (decoded)


#base64encode(sys.argv[1])

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
        self.collected = [0]*(map.mapwidth*map.mapheight)

        self.pos = (0, 0, 0)
        if fileName:
            self.load(fileName)

    def getStats(self):
        self.stats = system.engine.player.stats.clone()
        self.visible = map.visiblerooms[:]
        self.visited = map.visitedrooms[:]
        self.collected = map.collected[:]
        
    def setStats(self):
        system.engine.player.stats = self.stats.clone()
        map.visiblerooms = self.visible[:]
        map.visitedrooms = self.visited[:]
        map.collected = self.collected[:]
        
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
        s.collected = map.collected
        
        p = system.engine.player
        s.pos = (p.x, p.y, p.layer)
        return s

    currentGame = staticmethod(currentGame)

    def setCurrent(self):
        self.setStats()
        self.setFlags()

    def save(self, fileName):
        encoded = base64encode(str(self))
        file(fileName, 'wt').write(encoded)                
        #file(fileName, 'wt').write(str(self))

    def load(self, fileName):
        self.read(file(fileName, 'rt'))

    def __str__(self):
        s = ''
        for k in StatSet.STAT_NAMES:
            s += '%s=%i|' % (k, self.stats[k])
        s += 'FLAGS|'
        s += 'MAPNAME=\'%s\'|' % self.mapName        
        s += 'POS=\'%s\'|' % ','.join([str(x) for x in self.pos])
        s += 'TIME=\'%s\'|' % self.time
        s += 'SECONDS=\'%s\'|' % str(self.seconds)
        s += 'MINUTES=\'%s\'|' % str(self.minutes)
        s += 'HOURS=\'%s\'|' % str(self.hours)
        s += 'MAPDATA=\'%s\'|' % ','.join([str(x) for x in map.visiblerooms])        
        s += 'MAPDATA2=\'%s\'|' % ','.join([str(x) for x in map.visitedrooms])      
        s += 'MAPDATA3=\'%s\'|' % ','.join([str(x) for x in map.collected])      
        for var, val in savedata.__dict__.iteritems():
            if not var.startswith('_'):
                if isinstance(val, (int, str)):
                    s += '%s=%r|' % (var, val)

                elif isinstance(val, (list, tuple)):
                    s += '%s=LIST|' % var
                    for el in val:
                        s += '  %s|' % `el`
                    s += 'END|'

        
        return s

    def read(self, f):
        encoded = f.read()
        decoded = base64decode(encoded)
        lines = decoded.split('|')
        lines = lines[:-1] #last line is empty, discard

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
            elif k == 'MAPDATA2':                                 
				self.collected = [int(x) for x in v.split(',')]                  
            else:               
                self.flags[k] = v

        #read map data
        #s = lines.pop(0)
        #map.visible = [int(x) for x in s.split(', ')]
        

#test()
