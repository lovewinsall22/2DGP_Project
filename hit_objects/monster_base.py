from random import randint
from pico2d import load_image, draw_rectangle
from math import sqrt
import game_framework
WIDTH, HEIGHT = 1280, 720

FRAMES_PER_ACTION = 5 # 5개 애니메이션
TIME_PER_ACTION = 0.5 # #액션 한번당 0.5초
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION # 초당 2회 액션

class Monster:
    def __init__(self, x, y, hp = 1000, damage = 1 ,player = None):
        self.x, self.y = x, y
        self.hp = hp
        self.damage = damage
        self.alive = True
        self.player = player

        self.trace_on = False # 한번 피격당할시 추적모드
        self.stop_time = 120 # 120프레임 멈춤
        self.is_hit = False
        self.flash_timer = 0


    def draw(self):
        pass

    def update(self):
        pass

    def handle_collision(self, group, other):
        pass



class Golem(Monster):
    image = None
    def __init__(self, player = None):
        super().__init__(randint(0, WIDTH), randint(0,HEIGHT), 10000, 2,player)
        if Golem.image == None:
            Golem.image = load_image('resource/l_golem.png')
        self.frame = randint(0,6)
        self.speed = 0.3
        self.on_right = True # 캐릭터기준 오른쪽인지 ,,
        self.attack_range = 50


    def draw(self):
        if not self.alive:
            return

        if self.is_hit and (self.flash_timer // 5) % 2 == 0:
            return  # 5프레임마다 안 그려짐

        if self.on_right:
            Golem.image.clip_composite_draw(int(self.frame) * 35, 0, 35, 35, 0, 'h', self.x, self.y, 35, 35)
        else:
            Golem.image.clip_composite_draw(int(self.frame) * 35, 0, 35, 35, 0, '', self.x, self.y, 35, 35)
        draw_rectangle(*self.get_bb())

    def update(self):
        if not self.alive:
            return
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7

        if self.is_hit:
            self.stop_time -= 1
            self.flash_timer += 1
            if self.stop_time <= 0:
                self.is_hit = False
                self.stop_time = 120
                self.flash_timer = 0
            return

        if self.trace_on:
            dx = self.player.x - self.x
            dy = self.player.y - self.y
            distance = sqrt(dx * dx + dy * dy)
            if dx >= 0:
                self.on_right = True
            else:
                self.on_right = False
            if distance > self.attack_range:
                self.x += self.speed * (dx / distance)
                self.y += self.speed * (dy / distance)

    def get_bb(self):
        return self.x - 16, self.y - 16, self.x + 16, self.y + 16

    def handle_collision(self, group, other):
        if group == 'sword:golem':
            if other.sword_active:
                self.hp -= other.damage
                self.is_hit = True
                self.flash_timer = 0
                self.trace_on = True
        elif group == 'player:golem':
            pass


