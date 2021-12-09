
import ika
import sound
from snow import Snow
import system
import xi
from gameover import EndGameException
import automap

_basetext = '''\
*** Winter Remastered Credits ***


* Code, Maps, Scripting *

Francis Brazeau 


* Additional Artwork *

Corey Annis
Daniel Harris (aka Hyptosis)


* Additional Music *

'Boss' by Troupe Gammage


* Playtesting *

Adam Boudreau
Alex Hartshorn
Carlos Petersen


* Additional Sound Effects *
SoundBible.com
Freesound.org


* Special Thanks *
Jeff Brooks
DoctorGamester
Troy Potts (aka Thrasher)


*** Original Credits ***


* Management, Main program *

Andy Friesen


* Artwork *

Corey Annis


* Maps *

Corey Annis
Francis Brazeau
Andy Friesen
Troy Potts (aka Thrasher)


* Music *

'Existing' by Mick Rippon
'Winter' by David Churchill (aka infey)
'Competative' by Disturbed
'Resurrection' (Author unknown)
'xerxes vs solo' (Author unknown)
'Lampoons Haunting' (Author Unknown)


* Script *

Ian Bollinger


Additionally, everybody on the team had a
hand in the concept and layout of the game.


*** Enemy Stats ***



























































Thank you so much for playing! Winter was 
originally made for a game competition all
the way back in the winter of 2003. It was 
great for a game made in a few weeks by a 
small team, but it felt a bit unfinished. 

 
So I resurrected this project to add in 
some quality of life features, missing 
content,and try to give the game some 
proper closure. I hope you enjoyed the 
final product!


Please look forward to my future projects at
hatchet2k4.itch.io. Hopefully you won't have
to wait long for more!




'''

_text = []

def credits():    
    m = sound.music.get('music/Existing.s3m', ika.Sound('music/Existing.s3m'))
    m.loop = True
    sound.fader.kill()
    sound.fader.reset(m)

    bg = ika.Image('gfx/mountains2.png')
    snow = Snow(velocity=(0.5, 0.75))
    y = -ika.Video.yres
    font = ika.Font('system.fnt')
    totalitems=25 #total collectable items - tnt, + all types of runes 
    #currently 5 strength and power, 6 guard runes
    s = system.engine.player.stats
    
    collecteditems = s.totaltnt + s.powerrunes + s.strengthrunes + s.guardrunes + 4 #hack - assume that all 4 main runes are collected :P
    itempercent = str(round(collecteditems * 100/totalitems, 1)) + '%'
    mappercent = str(automap.map.getMapPct()) + '%'
    totaltxt = _basetext + """ *** Final Stats ***
    
    
Total Time Played:     """ + system.engine.time+"""    
Item Collection Rate:  """ + itempercent + """
Map Completion Rate:   """ + mappercent + """


"""


    
    _text=totaltxt.split('\n')
    class CreditEnt(object):
        def __init__(self, e, name, x, y, h):
            self.ent=e
            self.name=name
            self.x=x
            self.y=y
            self.h=int(h/2) #display line at midpoint of image height
            self.displayname=name.capitalize()
            self.num=str(system.engine.player.stats[self.name])
            
        def draw(self, offset):
            self.ent.Draw(self.x, self.y-offset)
            
            font.Print(140, self.y-offset+self.h, self.displayname)            
            font.Print(230, self.y-offset+self.h, self.num)


    def draw():
        ika.Video.Blit(bg, 0, 0, ika.Opaque)
        ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, 128), True)

        firstLine = int(y) / font.height
        adjust = int(y) % font.height
        length = (ika.Video.yres / font.height) + 1

        Y = -adjust
        while Y < ika.Video.yres and firstLine < len(_text):
            if firstLine >= 0:
                font.CenterPrint(160, Y, _text[firstLine])
            Y += font.height
            firstLine += 1
        
        for en in entlist:
            en.draw(int(y))
            
        ika.Video.DrawTriangle(
            (0, 0, ika.RGB(0, 0, 0)),
            (ika.Video.xres, 0, ika.RGB(0, 0, 0, 0)),
            (0, 60, ika.RGB(0, 0, 0, 0)))

        ika.Video.DrawTriangle(
            (ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0)),
            (0, ika.Video.yres, ika.RGB(0, 0, 0, 0)),
            (ika.Video.xres, ika.Video.yres - 60, ika.RGB(0, 0, 0, 0)))
  
        snow.draw()

            
    
    entlist=[]

    startx=80
    starty=0
    for i, txt in enumerate(_text):
        if '*** Enemy Stats ***' in txt:
            starty=i*10+30
            break
    
    #hack because the full sprite dimensions aren't directly accessible 
    heights = [16]*3 + [32]*3 + [72]*3 + [112]
    halfwidths=[8]*3 + [16]*3 + [48]*4
    offseth =[0]*3 + [0]*3 + [16]*3 +[15] #compensate for hotspot
    
    for i, entname in enumerate(['anklebiter', 'carnivore', 'devourer', 'razormane', 'dragonpup','hellhound', 'yeti', 'gorilla','soulreaver','serpent']):
        e=ika.Entity(-100,-100, 2, entname+'.ika-sprite') #put it off screen!               
        entlist.append(CreditEnt(e, entname, startx-halfwidths[i], starty-offseth[i], heights[i]))
        starty+=heights[i]+10
            
    maxy=len(_text)*10

    draw()
    xi.effects.fadeIn(50)

    now = ika.GetTime()
    while True:
        t = ika.GetTime()
        delta = (t - now) / 5.0
        y += delta
        now = t
        snow.update()
        draw()
        ika.Video.ShowPage()
        ika.Input.Update()
        if y > maxy:
            break
    
    system.killmusic=False #keep music playing after returning to menu
    
    raise EndGameException
        
        