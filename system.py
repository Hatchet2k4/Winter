import ika
from engine import Engine
from intro import intro, menu
import sound
import saveload

import controls
controls.init()

import subscreen
subscreen.init()

#import map2img

try:
    c = controls.readConfig('controls.cfg')
except IOError: #file not found, write defaults to a config file and reload it
    c = controls.defaultControls
    controls.writeConfig('controls.cfg', c)

try: 
    controls.setConfig(c)
except: 
    #c = controls.defaultControls
    #controls.writeConfig('controls_bak.cfg', c)
    controls.setConfig(controls.defaultControls) #any fails (missing gamepad usually), default to original controls


introMusic = ika.Sound('music/Existing.s3m')






intro()


    
while True:
        
    #if saveload.quicksave: # a quicksave exists from a previous attempt to load! Load it instead
    #    s=saveload.quicksave
    #    saveload.quicksave=None #reset it to None so that if player dies or exits, doesn't autoload the quicksave
    #    engine = Engine()
    #    engine.loadGame(s)
    #else:
        sound.fader.kill()
        introMusic.position = 0
        introMusic.Play()
        if saveload.quicksave:
            result = 3
        else: 
            result = menu()
        engine = Engine()
        
        if result == 0: #New Game
            introMusic.Pause()
            engine.beginNewGame()
        elif result == 1: #Load
            introMusic.Pause()
            engine.loadGame()
        elif result == 2: #Exit
            break
        elif result == 3: #quicksave
            introMusic.Pause()
            s=saveload.quicksave
            saveload.quicksave=None #reset it to None so that if player dies or exits, doesn't autoload the quicksave                
            engine.loadGame(s)                  
        else:
            assert False, 'Wacky intro menu result %i! :o' % result






ika.Exit()