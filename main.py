from pico2d import *
import logo_mode

WIDTH, HEIGHT = 1280, 720
character_size = 64

open_canvas(WIDTH, HEIGHT)
logo_mode.init()
while logo_mode.running:
    logo_mode.handle_events()
    logo_mode.update()
    logo_mode.draw()
    delay(0.01)
logo_mode.finish()
close_canvas()