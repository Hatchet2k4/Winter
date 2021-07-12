import ika
from thing import Thing
import system
# Some neat-O special effects


class Nova(Thing):
    def __init__(self, x, y, radius=1.0, duration=200, speed=2, color=ika.RGB(128,128,128), filled=False):
        self.x=x
        self.y=y
        self.rad=radius
        self.duration=0
        self.maxduration=duration
        self.opacity=255
        self.speed=speed
        self.filled=filled
        
        self.r, self.g, self.b, self.a = ika.GetRGB(color)
        self.font = system.engine.font                
        self.update = self._update().next 
        
    def _update(self): 
        while self.duration <= self.maxduration:
            self.duration += 1
            percent = (self.duration * 255 / self.maxduration) #proportion of how much the nova has passed. 
            self.opacity = int(255 - percent) #TODO: a delay before starting to fade perhaps
            
            if self.opacity <= 0: yield True

            self.rad+=self.speed

            yield None

        yield True # seppuku

    def draw(self):           
        color = ika.RGB(self.r, self.g, self.b, self.opacity)
        ika.Video.DrawEllipse(self.x  - ika.Map.xwin, self.y - ika.Map.ywin, int(self.rad), int(self.rad), color, self.filled)

class Point(Thing):
    def __init__(self, x, y):
        self.x=x
        self.y=y    

class Bolt(Thing):
    def __init__(self, x, y, endx, endy, color):
        self.x=x
        self.y=y
        self.endx=endx
        self.endy=endy
        self.duration=0
        self.maxduration=50
        self.opacity=200
                
        self.r, self.g, self.b, self.a = ika.GetRGB(color)        
        self.color=color        
        self.points=self.generatePoints(ika.Random(4, 8))
        
                
        self.update = self._update().next 
        
    def generatePoints(self, numpoints=5):
        points = []
        
        #for i in range(numpoints):
                
        return points
        
    def _update(self): 
        while self.duration <= self.maxduration:
            self.duration += 1
            

            yield None

        yield True # seppuku

    def draw(self):                   
        #ika.Video.DrawEllipse(self.x  - ika.Map.xwin, self.y - ika.Map.ywin, int(self.rad), int(self.rad), color, self.filled)
        x1 = self.x - ika.Map.xwin
        y1 = self.y - ika.Map.ywin
        x2 = self.endx - ika.Map.xwin
        y2 = self.endy - ika.Map.ywin
        ika.Video.DrawLine(x1, y1, x2, y2, self.color)

def blurScreen(factor):
    '''Grabs the screen, blurs it up a bit, then returns the image.
    Returns tinier images.  Use scaleblit to bring them back.

    Grossly inefficient.
    '''

    w = int(ika.Video.xres * factor)
    h = int(ika.Video.yres * factor)

    bleh = ika.Video.GrabImage(0, 0, ika.Video.xres, ika.Video.yres)
    ika.Video.ScaleBlit(bleh, 0, 0, w, h, ika.Opaque)
    return ika.Video.GrabImage(0, 0, w, h)

def createBlurImages():
    BLEH = 1
    images = []
    i = 1.0
    while i < 2:
        img = blurScreen(1.0 / i)
        images.append(img)
        ika.Video.ScaleBlit(img, 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)

        ika.Video.ScaleBlit(img, -BLEH, -BLEH, ika.Video.xres + BLEH * 2, ika.Video.yres + BLEH * 2)

        i += 0.1

    return images

def blurOut():
    wasteOfMemory = []

    i = 1.0
    while i < 2:
        img = blurScreen(1.0 / i)
        wasteOfMemory.append(img)
        ika.Video.ScaleBlit(img, 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
        ika.Video.ShowPage()
        ika.Input.Update()
        ika.Delay(3)

        BLEH = 1
        ika.Video.ScaleBlit(img, -BLEH, -BLEH, ika.Video.xres + BLEH * 2, ika.Video.yres + BLEH * 2)
        ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, 2), True)

        i += 0.1

    return wasteOfMemory

def blurIn(wasteOfMemory):

    for img in wasteOfMemory[::-1]:
        ika.Video.ScaleBlit(img, 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
        ika.Video.ShowPage()
        ika.Input.Update()
        ika.Delay(3)

def crossFade(time, startImage = None, endImage = None):
    '''Crossfades!  Set either startImage or endImage, or both.'''

    assert startImage or endImage, "Don't be a retard."

    if not startImage:
        startImage = ika.Video.GrabImage(0, 0, ika.Video.xres, ika.Video.yres)
    if not endImage:
        endImage = ika.Video.GrabImage(0, 0, ika.Video.xres, ika.Video.yres)

    endTime = ika.GetTime() + time
    now = ika.GetTime()
    while now < endTime:
        opacity = (endTime - now) * 255 / time
        ika.Video.ClearScreen()
        ika.Video.Blit(endImage, 0, 0)
        ika.Video.TintBlit(startImage, 0, 0, ika.RGB(255, 255, 255, opacity))
        ika.Video.ShowPage()
        ika.Input.Update()

        now = ika.GetTime()

def blurFade(time, startImages, endImages):
    startTime = ika.GetTime()
    endTime = ika.GetTime() + time
    now = startTime
    while now < endTime:
        imageIndex = (now - startTime) * len(startImages) / time
        opacity = (now - startTime) * 255 / time
        startfade = ika.RGB(255, 255, 255, 255 - opacity)
        endfade = ika.RGB(255, 255, 255, opacity)

        ika.Video.TintDistortBlit(
            startImages[imageIndex],
            (0, 0, startfade), (ika.Video.xres, 0, startfade),
            (ika.Video.xres, ika.Video.yres, startfade),
            (0, ika.Video.yres, startfade))
        ika.Video.TintDistortBlit(
            endImages[-(imageIndex+1)],
            (0, 0, endfade), (ika.Video.xres, 0, endfade),
            (ika.Video.xres, ika.Video.yres, endfade),
            (0, ika.Video.yres, endfade))

        ika.Video.ShowPage()
        ika.Input.Update()
        now = ika.GetTime()
