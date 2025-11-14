from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_a, SDLK_d, SDLK_w, SDLK_s, SDLK_SPACE, SDLK_1, SDLK_2, SDLK_3, SDLK_l
from input_helper import get_keys

WIDTH, HEIGHT = 1280, 720
from player_ui import PlayerUI
from sword import Sword
import game_framework
from world import game_world

PIXEL_PER_METER = (1 / 0.04) # 1픽셀당 4cm => 플레이어 대략 120cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

FRAMES_PER_ACTION = 5 # 5개 애니메이션
TIME_PER_ACTION = 0.5 # #액션 한번당 0.5초
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION # 초당 2회 액션


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
        self.money = load_image('resource/money.png')
        #self.attack_r = load_image('resource/attack_r.png')
        #self.attack_l = load_image('resource/attack_l.png')

        self.x, self.y = WIDTH / 2, HEIGHT / 2 # 플레이어 초기 좌표
        self.dirX,self.dirY = 0, 0 # 이동 방향 1 <--> -1
        self.ifRight = 1 # 1: 오른쪽, 0: 왼쪽

        #self.ani_count = 0 # 기본 애니메이션 프레임 조절을 위해 ,, 카운트
        self.frame = 0 # 기본 애니메이션 프레임
        self.is_hitted = False
        self.flash_timer = 0 # 지속시간은 120 프레임


        self.max_hp = 100 # 최대 체력
        self.hp = 100 # 현재 체력
        self.level = 1 # 현재 레벨
        self.speed = RUN_SPEED_PPS # 이동 속도
        self.damage = 1000 # 공격력
        self.gold = 1000 # 골드
        self.hp_potion_count = 0 # 체력포션 개수
        self.get_money_animation = False
        self.money_animation_count = 0

        self.playerUI = PlayerUI(self)
        self.sword = Sword(self)
        game_world.add_collision_pair('sword:dummy', self.sword, None)
        game_world.add_collision_pair('sword:golem', self.sword, None)



    def draw(self):
        if self.is_hitted and (self.flash_timer // 5) % 2 == 0:
            return  # 5프레임마다 안 그려짐
        if self.ifRight == 1 : self.rightMove[int(self.frame)].draw(self.x, self.y, 40, 62)
        elif self.ifRight == 0 : self.leftMove[int(self.frame)].draw(self.x, self.y, 40, 62)
        draw_rectangle(*self.get_bb())
        self.playerUI.draw()
        self.sword.draw()
        self.playerUI.draw()
        if self.get_money_animation:
            self.money.draw(self.x, self.y + self.money_animation_count // 3, 22, 21)

    def update(self):
        self.sword.update()
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.x += self.dirX * self.speed * game_framework.frame_time
        self.y += self.dirY * self.speed * game_framework.frame_time
        if self.is_hitted:
            self.flash_timer += 1
            if self.flash_timer >= 120:
                self.is_hitted = False
                self.flash_timer = 0
        self.playerUI.update()
        if self.get_money_animation:
            self.money_animation_count += 1
            if self.money_animation_count >= 120:
                self.get_money_animation = False
                self.money_animation_count = 0
        self.boundary_check()


    def handle_event(self, event):
        if event.type == SDL_KEYUP:
            if event.key == SDLK_d:
                keys = get_keys()
                if not keys[SDLK_a]:
                    self.dirX = 0
                else:
                    self.dirX = -1
            if event.key == SDLK_a:
                keys = get_keys()
                if not keys[SDLK_d]:
                    self.dirX = 0
                else:
                    self.dirX = 1
            if event.key == SDLK_w:
                keys = get_keys()
                if not keys[SDLK_s]:
                    self.dirY = 0
                else:
                    self.dirY = -1
            if event.key == SDLK_s:
                keys = get_keys()
                if not keys[SDLK_w]:
                    self.dirY = 0
                else:
                    self.dirY = 1
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_d:
                self.dirX = 1
                if not self.sword.sword_active: self.ifRight = 1  # 공격중엔 방향전환 X
            if event.key == SDLK_a:
                self.dirX = -1
                if not self.sword.sword_active: self.ifRight = 0  # 공격중엔 방향전환 X
            if event.key == SDLK_w:
                self.dirY = 1
            if event.key == SDLK_s:
                self.dirY = -1
            if event.key == SDLK_SPACE and self.sword.sword_active == False:
                self.sword.sword_active = True
                self.sword.already_hit.clear()  # 충돌 기록 초기
                self.sword.sword_frame = 0
                if self.ifRight == 0:
                    self.sword.sword_angle = 90
                else:
                    self.sword.sword_angle = 45  # ??

    def get_bb(self):
        return self.x - 20, self.y - 31, self.x + 20, self.y + 31

    def handle_collision(self, group, other):
        if group == 'player:townNpc':
            pass
        elif group == 'player:portal':
            pass
        elif group == 'player:golem':
            if not self.is_hitted:
                if not other.spawn_effect:
                    self.hp -= other.damage
                    self.flash_timer = 0
                    self.is_hitted = True

    def boundary_check(self):
        if self.x < 20:
            self.x = 20
        elif self.x > WIDTH - 20:
            self.x = WIDTH - 20
        if self.y < 31:
            self.y = 31
        elif self.y > HEIGHT - 31:
            self.y = HEIGHT - 31

