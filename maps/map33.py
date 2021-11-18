import ika
import savedata
import system
import dir
from serpent import Serpent
from thing import Thing
import sound
from caption import Caption
import xi
import ending

savedata = savedata.__dict__ # fuckit



def AutoExec():
    system.engine.background = ika.Image('gfx/mountains2.png')
    
    engine = system.engine
    p = engine.player
    p.direction=dir.UP            
    p._state = p.cutsceneState() 
    engine.draw()
    ika.Video.ShowPage()
    
    for y in range(21 * 16):        
        ika.ProcessEntities()
        engine.tick()
        engine.camera.update()
        engine.draw()
        ika.Video.ShowPage()
        ika.Delay(1)        
         
    p.state = p.standState()
    engine.tick()
    
    for y in range(300):
        engine.draw()
        ika.Video.ShowPage()
        ika.Delay(1)    
    
    engine.synchTime()
    xi.effects.fadeOut(200, draw=system.engine.draw)
    ending.credits()
    
