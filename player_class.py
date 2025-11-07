from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_a, SDLK_d, SDLK_w, SDLK_s, SDLK_SPACE, SDLK_1, SDLK_2, SDLK_3, SDLK_l

WIDTH, HEIGHT = 1280, 720
from player_ui import PlayerUI
from sword import Sword
import game_framework

PIXEL_PER_METER = (1 / 0.04) # 1픽셀당 4cm => 플레이어 대략 120cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class Player:
    def __init__(self):
        self.right1 = load_image('resource/white_r_1.png')
        self.right2 = load_image('resource/white_r_2.png')
        self.right3 = load_image('resource/white_r_3.png')
        self.right4 = load_image('resource/white_r_4.png')
        self.right5 = load_image('resource/white_r_5.png')
        self.left1 = load_image('resource/white_l_1.png')
        self.left2 = load_image('resource/white_l_2.png')
        self.left3 = load_image('resource/white_l_3.png')
        self.left4 = load_image('resource/white_l_4.png')
        self.left5 = load_image('resource/white_l_5.png')
        self.rightMove = [self.right1, self.right2, self.right3, self.right4, self.right5]
        self.leftMove = [self.left1, self.left2, self.left3, self.left4, self.left5]

        #self.attack_r = load_image('resource/attack_r.png')
        #self.attack_l = load_image('resource/attack_l.png')

        self.x, self.y = WIDTH / 2, HEIGHT / 2 # 플레이어 초기 좌표
        self.dirX,self.dirY = 0, 0 # 이동 방향
        self.ifRight = 1 # 1: 오른쪽, -1: 왼쪽

        self.ani_count = 0 # 기본 애니메이션 프레임 조절을 위해 ,, 카운트
        self.frame = 0 # 기본 애니메이션 프레임

        self.max_hp = 100 # 최대 체력
        self.hp = 100 # 현재 체력
        self.level = 1 # 현재 레벨
        #self.speed = 5 # 이동 속도
        self.damage = 1000 # 공격력
        self.gold = 1000 # 골드
        self.hp_potion_count = 0 # 체력포션 개수

        self.playerUI = PlayerUI(self)
        self.sword = Sword(self)

        self.pressed = set()

    def draw(self):
        if self.ifRight == 1 : self.rightMove[self.frame].draw(self.x, self.y, 40, 62)
        elif self.ifRight == 0 : self.leftMove[self.frame].draw(self.x, self.y, 40, 62)
        draw_rectangle(self.x - 20, self.y - 31, self.x + 20, self.y + 31)
        self.playerUI.draw()
        self.sword.draw()
        self.playerUI.draw()

    def update(self):
        self.ani_count += 1
        if self.ani_count % 12 == 0:
            self.sword.update()
            self.frame = (self.frame + 1) % 5
            self.ani_count = 0
        self.x += self.dirX * RUN_SPEED_PPS * game_framework.frame_time
        self.y += self.dirY * RUN_SPEED_PPS * game_framework.frame_time
        self.playerUI.update()


    def handle_event(self, event):
        if event.type == SDL_KEYUP:
            if event.key == SDLK_d:  self.dirX = 0
            if event.key == SDLK_a:  self.dirX = 0
            if event.key == SDLK_w:  self.dirY = 0
            if event.key == SDLK_s:  self.dirY = 0
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_d:
                self.dirX = 1
                if not self.sword.sword_active: self.ifRight = 1  # 공격중엔 방향전환 X
            elif event.key == SDLK_a:
                self.dirX = -1
                if not self.sword.sword_active: self.ifRight = 0  # 공격중엔 방향전환 X
            elif event.key == SDLK_w:
                self.dirY = 1
            elif event.key == SDLK_s:
                self.dirY = -1
            elif event.key == SDLK_SPACE and self.sword.sword_active == False:
                self.sword.sword_active = True
                self.sword.already_hit.clear()  # 충돌 기록 초기
                self.sword.sword_frame = 0
                if self.ifRight == 0:
                    self.sword.sword_angle = 90
                else:
                    self.sword.sword_angle = 45  # ??
