import ika
import savedata
import system
import dir
from thing import Thing
import sound
from caption import Caption
import xi
import ending


class RunEnding(Thing):
    def update(self):
        engine = system.engine
        p = engine.player
        p.direction=dir.UP            
        p.state = p.cutsceneWalkState() 
        engine.draw()
        ika.Video.ShowPage()
        
        for i in range(21 * 16 +8):        
            ika.ProcessEntities()
            p.update()
            engine.camera.update()
            engine.draw()
            ika.Video.ShowPage()
            ika.Delay(1)
        p.direction=dir.LEFT
        p.stop()     
        p.state = p.cutsceneStandState()
        p.update()

        y=float(ika.Map.ywin)
        for i in range(500):
            if y>20: 
                y-=0.2
            ika.Map.ywin=int(y)
            ika.ProcessEntities()
            p.update()
            engine.draw()
            ika.Video.ShowPage()
            ika.Delay(1)    
        
        engine.synchTime()
        xi.effects.fadeOut(200, draw=system.engine.draw)
        ending.credits()
    

    def draw(self):
        pass

def AutoExec():
    system.engine.background = ika.Image('gfx/mountains2.png')
    system.engine.mapThings.append(RunEnding()) 
    
    
    

