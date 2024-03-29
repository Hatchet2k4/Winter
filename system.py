import ika
from engine import Engine
from intro import intro, menu
import sound
import saveload
import controls


ika.SetCaption('Winter')
ika.Video.DrawRect(0,0,320,240,0)

controls.init()

import subscreen
subscreen.init()


try:
    c = controls.readConfig('controls.cfg')
except IOError: #file not found, write defaults to a config file and reload it
    c = controls.defaultControls
    controls.writeConfig('controls.cfg', c)
try: 
    controls.setConfig(c)
except: 
    controls.writeConfig('controls_bak.cfg', c)
    controls.setConfig(controls.defaultControls) #any fails (missing gamepad usually), default to original controls


introMusic = ika.Sound('music/Existing.s3m')
#while not controls.attack():
#        ika.Video.DrawRect(0,0,320,240,0)
#        ika.Video.ShowPage()
#        ika.Input.Update()
sound.fader.kill()
#ika.Delay(5)
introMusic.Play()
#ika.Delay(5)
intro()

    
while True:        
        killmusic=True
        if saveload.quicksave:
            result = 3
        else: 
            result = menu()
        engine = Engine()
        
        if result == 0: #New Game
            introMusic.Pause()
            sound.fader.kill()
            engine.beginNewGame()
            if killmusic:
                sound.fader.kill()
                introMusic.Play()
                            
        elif result == 1: #Load
            introMusic.Pause()
            sound.fader.kill()
            engine.loadGame()            
            if killmusic:
                sound.fader.kill()
                introMusic.Play()   
        elif result == 2: #Exit
            break
        elif result == 3: #quicksave
            introMusic.Pause()
            sound.fader.kill()
            s=saveload.quicksave
            saveload.quicksave=None #reset it to None so that if player dies or exits, doesn't autoload the quicksave                
            engine.loadGame(s)       
            if killmusic:
                sound.fader.kill()
                introMusic.Play()          
        else:
            assert False, 'Wacky intro menu result %i! :o' % result

ika.Exit()