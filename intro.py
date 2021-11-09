import ika
from snow import Snow

import controls

class _DoneException(Exception):
    pass

def delay(draw, count, snow):
    while count > 0:
        draw()
        snow.update()
        snow.draw()
        ika.Delay(1)
        count -= 1
        ika.Video.ShowPage()

        ika.Input.Update()
        if controls.attack() or controls.ui_accept() or controls.cancel() or controls.ui_cancel() or controls.joy_cancel() or controls.joy_attack():
            raise _DoneException()

def intro():
    snow = Snow(velocity=(0,0.5))
    
    i = ika.Random(0, 7)
    gba = ika.Image('gfx/gba'+str(i)+'.png')
    ikalogo = ika.Image('gfx/ika.png')
    hatchlogo = ika.Image('gfx/HatchetLogo2.png')


    v = ika.Video
    d = 50

    def showGba():
        v.ClearScreen()
        v.Blit(gba, (v.xres - gba.width) / 2, (v.yres - gba.height) / 2)

    try:                
        delay(lambda: v.Blit(ikalogo, 0, 0, ika.Opaque), 200, snow)
        delay(lambda: v.ClearScreen(), d, snow)        
        delay(lambda: v.Blit(hatchlogo, 0, 0, ika.Opaque), 200, snow)
        delay(lambda: v.ClearScreen(), d, snow)
        delay(showGba, 200, snow)
        delay(lambda: v.ClearScreen(), d, snow)
        
    except _DoneException:
        return

def menu():
    bg = ika.Image('gfx/title.png')
    cursor = ika.Image('gfx/ui/pointer.png')
    snow = Snow(velocity=(0, 0.5))
    snow.update()
    result = None
    cursorPos = 0
    FADE_TIME = 60

    font = ika.Font('system.fnt')

    def draw():
        ika.Video.Blit(bg, 0, 0, ika.Opaque)
        ika.Video.Blit(cursor, 68, 128 + cursorPos * 26)
        txt = '(c) 2003, 2021'
        length = font.StringWidth(txt)
        font.Print(ika.Video.xres - length - 10, ika.Video.yres-10, txt)
        if controls.useGamePad:
            font.Print(10, ika.Video.yres-10, 'Gamepad controls enabled.')

    for i in range(FADE_TIME - 1, -1, -1):
        draw()
        ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, i * 255 / FADE_TIME), True)
        snow.update()
        snow.draw()
        ika.Video.ShowPage()
        ika.Input.Update()
        ika.Delay(1)

    u = 0 # gay unpress hack

    while result == None:
        draw()
        snow.update()
        snow.draw()
        ika.Video.ShowPage()
        ika.Input.Update()
        ika.Delay(1)

        if (controls.up() or controls.ui_up() or controls.joy_up()) and cursorPos > 0:
            if not u:
                cursorPos -= 1
                u = 1
        elif (controls.down() or controls.ui_down() or controls.joy_down()) and cursorPos < 2:
            if not u:
                cursorPos += 1
                u = 1
        elif controls.attack() or controls.ui_accept() or controls.joy_attack():
            result = cursorPos
        else:
            u = 0

    # one last draw.  Later on, there's a blurfade that can take advantage of this:
    draw()
    snow.draw()
    return result

    for i in range(FADE_TIME):
        draw()
        ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, i * 255 / FADE_TIME), True)
        snow.update()
        snow.draw()
        ika.Video.ShowPage()
        ika.Input.Update()
        ika.Delay(1)
