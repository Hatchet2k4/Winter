
import ika
from thing import Thing
import system

def sgn(i):
    if i > 0: return 1
    elif i < 0: return -1
    else: return 0

class Gauge(Thing):
    def __init__(self, imageName, x, y, justify = 'left', colour = ika.RGB(255, 255, 255)):
        '''
        imageName - name of the image series to use.
         ie 'gfx/ui/barhp%i.png'
        x,y are position
        justify is either 'left' or 'right'
        '''

        (self.span, self.left, self.middle, self.right) =\
            [ika.Image(imageName % i) for i in range(4)]
        self.oldVal = self.oldMax = 0
        self.x, self.y = x,y
        self.justify = justify.lower()
        self.opacity = 0
        self.colour = ika.GetRGB(colour)[:-1]
        self.width = None
        self.fadeIn = False
        self.type = ''

    def update(self):
        v = sgn(self.curVal - self.oldVal)
        m = sgn(self.curMax - self.oldMax)

        if self.fadeIn:
            self.opacity = min(512, self.opacity + 20)
            if self.opacity == 512:
                self.fadeIn = False

        if not v and not m:
            self.opacity = max(0, self.opacity - 1)
        else:
            self.fadeIn = True
            self.oldVal += v
            self.oldMax += m

    def draw(self, op=0):
        if self.opacity == 0 and op == 0:
            return

        o = min(255, self.opacity)
        o = max(op, o)

        # the width of the repeated span image thingo.
        # each end of the gauge occupies two pixels, so we subtract four.
        # (bad hack, I know)
        width = (self.width or self.oldMax) - 3

        if self.justify == 'left':
            x = self.x + 2
        else:
            x = ika.Video.xres - width - self.left.width - self.right.width - self.x - 2

        ika.Video.TintBlit(self.left, x, self.y, ika.RGB(255, 255, 255, o))
        ika.Video.TintBlit(self.right, x + width + self.left.width, self.y, ika.RGB(255, 255, 255, o))

        x += self.left.width

        ika.Video.ClipScreen(x, 0, x + width + 1, ika.Video.yres)
        for X in range(0, width, self.span.width):
            ika.Video.TintBlit(self.span, x + X, self.y, ika.RGB(255, 255, 255, o))
        ika.Video.ClipScreen()

        x -= 2

        if self.width:
            v = self.oldVal * self.width / self.oldMax
        else:
            v = self.oldVal

        if self.oldVal:
            if self.justify == 'left':
                self.drawRect(x, self.y + 5, x + v, self.y + 6, o)
            else:
                self.drawRect(x + (self.width or self.oldMax) - v, self.y + 5, x + (self.width or self.oldMax), self.y + 6, o)

    def drawRect(self, x, y, w, h, opacity):
        'Used to draw in the filled part of the gauge.'
        ika.Video.DrawRect(x, y, w, h, ika.RGB(*(self.colour + (opacity,))), True)

    curVal = property() # ditto
    curMax = property() # override.  Needs to be readable.

class HPBar(Gauge):
    def __init__(self):
        Gauge.__init__(self, 'gfx/ui/barhp%i.png', 0, 0, justify='right')
        self.y = ika.Video.yres - self.left.height - 1
        self.colour = (255, 0, 0)
        self.type = 'HP'
        
        self.beeptime = 0
        self.beepw = self.beeph = 0
        self.beepx = self.beepy = 0
        self.beepo = 0
        
    def update(self):
        Gauge.update(self)
        
        if float(self.curVal) / float(self.curMax) < 0.95 and not self.beeptime: #less than 20% health, beep beep!
            self.beeptime = 100
            
            #width = (self.width or self.oldMax) - 3
            
            if self.justify == 'left':
                self.beepx = self.x + 2
            else:
                self.beepx = ika.Video.xres - self.left.width - self.right.width - self.x - 2
            
            #self.beepx = self.x + 2
            self.beepy = self.y
            
            self.beepw = self.curVal
            self.beeph=5
            self.beepo=210
            
        elif self.beeptime > 0:
            self.beepo = max(self.beepo-2, 0)
            
            #self.beepx-=1
            #self.beepy-=1
            #self.beepw+=2
            #self.beeph+=2
                        
            self.beeptime-=1
            
    def draw(self):
        Gauge.draw(self)
        #if self.beeptime > 0: 
        #    ika.Video.DrawRect(self.beepx, self.beepy, self.beepw, self.beeph, ika.RGB(*(self.colour + (self.beepo,))), False)
        


    curVal = property(lambda self: system.engine.player.stats.hp)
    curMax = property(lambda self: system.engine.player.stats.maxhp)

class MPBar(Gauge):
    def __init__(self):
        Gauge.__init__(self, 'gfx/ui/barhp%i.png', 0, 0, justify='right')
        self.y = ika.Video.yres - self.left.height * 2 - 1
        self.colour = (0, 0, 255)
        self.oldMax = self.curMax
        self.oldVal = self.curVal
        self.type = 'MP'

    curVal = property(lambda self: system.engine.player.stats.mp)
    curMax = property(lambda self: system.engine.player.stats.maxmp)

class EXPBar(Gauge):
    def __init__(self):
        Gauge.__init__(self, 'gfx/ui/barmp%i.png', 0, 0, justify='right')
        #self.y = ika.Video.yres - self.left.height * 2 - 1
        self.width = 100
        self.colour = (0, 128, 128)
        self.oldMax = self.curMax
        self.oldVal = self.curVal
        self.type = 'EXP'

    def drawRect(self, x, y, w, h, opacity):
        super(EXPBar, self).drawRect(x, y, w, h - 1, opacity)

    curVal = property(lambda self: system.engine.player.stats.exp * self.width / system.engine.player.stats.next)
    curMax = property(lambda self: self.width)