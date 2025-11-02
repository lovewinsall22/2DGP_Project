from pico2d import *
import play_mode

WIDTH, HEIGHT = 1280, 720
character_size = 64

open_canvas(WIDTH, HEIGHT)
play_mode.init()
while play_mode.running:
    play_mode.handle_events()
    play_mode.update()
    play_mode.draw()
    delay(0.01)
play_mode.finish()
close_canvas()