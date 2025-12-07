from pico2d import *
import logo_mode as start_mode
import game_framework

WIDTH, HEIGHT = 1280, 720

open_canvas(WIDTH, HEIGHT)
game_framework.run(start_mode)
close_canvas()