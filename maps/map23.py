
import system
import ika

def AutoExec():
    system.engine.background = ika.Image('gfx/mountains.png')
    
def to21():
    system.engine.mapSwitch('map21.ika-map', (1 * 16, system.engine.player.y))

def to24():
    system.engine.mapSwitch('map24.ika-map', (48 * 16, 34 * 16))
    
def to25():
    system.engine.mapSwitch('map25.ika-map', (54 * 16, 55 * 16))
    
def Tunnel1_1():  system.engine.warp((21 * 16, 21 * 16))
def Tunnel1_2():  system.engine.warp((31 * 16, 36 * 16))
def Tunnel2_1():  system.engine.warp((45 * 16, 28 * 16)) #fall!
def Tunnel2_2():  pass
def Tunnel3_1():  system.engine.warp((6 * 16, 16 * 16))
def Tunnel3_2():  system.engine.warp((22 * 16, 27 * 16))
def Tunnel4_1():  system.engine.warp((5 * 16, 34 * 16))
def Tunnel4_2():  system.engine.warp((30 * 16, 8 * 16))
def Tunnel5_1():  system.engine.warp((18 * 16, 36 * 16))
def Tunnel5_2():  system.engine.warp((45 * 16, 44 * 16))
def Tunnel6_1():  system.engine.warp((45 * 16, 37 * 16))
def Tunnel6_2():  system.engine.warp((6 * 16, 25 * 16))
def Tunnel7_1():  system.engine.warp((24 * 16, 35 * 16)) #fall!
def Tunnel7_2():  pass    


def fall1(): 
    fall(7)

def fall2(): 
    fall(9)

def fall(numtiles):
    engine = system.engine
    p = engine.player
    p.stop()        
    p.ent.specframe = 91
    p._state = lambda: None # keep the player from moving
    engine.draw()
    ika.Video.ShowPage()
    ika.Delay(2)
    
    for y in range(numtiles * 8):
        p.y += 2
        ika.ProcessEntities()
        engine.camera.update()
        engine.draw()
        ika.Video.ShowPage()
        ika.Delay(1)        
        
    p.ent.specframe = 92
    t = ika.GetTime() + 80
    while t > ika.GetTime():
        ika.ProcessEntities()
        engine.camera.update()
        engine.draw()
        ika.Video.ShowPage()
        ika.Input.Update()
        ika.Delay(1)        

    p.state = p.standState()
    engine.synchTime()