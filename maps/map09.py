
import system
import cabin
import savedata

def story_fire():
    if 'waterfire' in savedata.__dict__ and 'story_fire' not in savedata.__dict__: 
      cabin.scene('story_fire')      
      system.engine.camera.center()

def to8():
    system.engine.mapSwitch('map08.ika-map', (1 * 16, system.engine.player.y))
    
def to10():
    system.engine.mapSwitch('map10.ika-map', (system.engine.player.x, 28 * 16))