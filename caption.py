import ika
import system
from thing import Thing

class Caption(Thing):
    def __init__(self, text, x = None, y = None, duration=200, delay=0, r=255,g=255,b=255):        
        self.r=r
        self.g=g
        self.b=b          
        self.delay=delay
        font = system.engine.font
        width = font.StringWidth(text)
        height = font.height

        if x is None:   self.x = (ika.Video.xres - width) / 2
        else:           self.x = x

        if y is None:   self.y = ika.Video.yres - height - 40
        else:           self.y = y

        canv = ika.Canvas(width, height)
        canv.DrawText(font, 0, 0, text)

        self.img = ika.Image(canv)
        self.opacity = 0
        self.duration = duration
        self.update = self._update().next

    def _update(self):
        while self.delay>0:
            self.delay-=1
            yield None
        while self.opacity < 256:
            self.opacity += 2
            yield None

        while self.duration > 0:
            self.duration -= 1
            yield None

        while self.opacity > 0:
            self.opacity -= 2
            yield None

        yield True # seppuku

    def draw(self):
        o = min(255, self.opacity)
        ika.Video.TintBlit(self.img, self.x, self.y, ika.RGB(self.r, self.g, self.b, o))

class DamageCaption(Caption):
    def __init__(self, text, x = None, y = None, duration=200, r=255,g=255,b=255):
        Caption.__init__(self, text, x, y, duration)
        self.r=r
        self.g=g
        self.b=b    
        self.opacity = 255
        self.ytimer = 0

    def _update(self):
        while self.duration > 0:
            self.duration -= 1
            self.ytimer += 1
            if self.ytimer > 8: 
                self.ytimer = 0
                self.y+=1
            yield None

        while self.opacity > 0:
            self.opacity -= 8
            if self.opacity <0: yield True
                
            if self.ytimer > 8: 
                self.ytimer = 0
                self.y+=1
            yield None

        yield True # seppuku

    def draw(self):
        o = min(255, self.opacity)
        ika.Video.TintBlit(self.img, self.x  - ika.Map.xwin, self.y - ika.Map.ywin, ika.RGB(self.r, self.g, self.b, o))

class BGRect(Thing):
    def __init__(self, x=0, y=0, w=0, h=0, duration=200, delay=0, r=60, g=60, b=60, a=200):

        self.x=x
        self.y=y
        self.w=w
        self.h=h

        self.delay=delay
        self.r=r
        self.g=g
        self.b=b    
        self.maxa=a #max alpha
        
        self.duration=duration        
        self.opacity = 0
        self.ytimer = 0
        self.update = self._update().next

    def _update(self):
        while self.delay>0:
            self.delay-=1
            yield None
    
        while self.opacity < self.maxa:
            self.opacity += 2
            yield None

        while self.duration > 0:
            self.duration -= 1
            yield None

        while self.opacity > 0:
            self.opacity -= 2
            yield None

        yield True # seppuku

    def draw(self):
        o = min(255, self.opacity)
        #ika.Video.TintBlit(self.img, self.x  - ika.Map.xwin, self.y - ika.Map.ywin, ika.RGB(self.r, self.g, self.b, o))
        ika.Video.DrawRect(self.x, self.y, self.x+self.w, self.y+self.h, ika.RGB(self.r, self.g, self.b, o), 1)
        #ika.Video.DrawRect(int x1, int y1, int x2, int y2, int color[, int filled, int blendMode])

