from pico2d import load_image, draw_rectangle
import game_framework
character_size = 64

FRAMES_PER_ACTION = 5 # 5개 애니메이션
TIME_PER_ACTION = 0.5 # #액션 한번당 0.5초
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION # 초당 2회 액션

class NPC:
    def __init__(self):
        self.image = load_image('resource/townNPC.png')
        self.x, self.y = 200, 500
        self.frame = 0
    def draw(self):
        self.image.clip_draw(int(self.frame) * 32, 0, 32, 32, self.x, self.y, character_size, character_size)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

    def get_bb(self):
        return self.x - 32, self.y - 32, self.x + 32, self.y + 32
