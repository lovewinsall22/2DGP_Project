from random import randint
from pico2d import load_image, draw_rectangle, load_font
from math import sqrt
import game_framework
from world import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import math
WIDTH, HEIGHT = 1280, 720

PIXEL_PER_METER = (1 / 0.04) # 1픽셀당 4cm => 플레이어 대략 120cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 일반 몬스터
FRAMES_PER_ACTION = 7 # 7개 애니메이션
TIME_PER_ACTION = 0.5 # #액션 한번당 0.5초
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION # 초당 2회 액션

# 보스
FRAMES_PER_ACTION_BOSS = 4
TIME_PER_ACTION_BOSS = 1
ACTION_PER_TIME_BOSS = 1.0 / TIME_PER_ACTION_BOSS # 초당 1회 액션

class Monster:
    font = None
    def __init__(self, x, y, hp = 10000, damage = 1 ,player = None):
        self.x, self.y = x, y
        self.hp = hp
        self.damage = damage
        self.alive = False
        self.player = player
        self.respawn_timer = 0

        self.trace_wait = randint(500,5000) # 지날시 추적
        self.trace_on = False # 한번 피격당할시 추적모드
        self.stop_time = 120 # 120프레임 멈춤
        self.is_hit = False
        self.flash_timer = 0
        if Monster.font == None:
            Monster.font = load_font('DNFBitBitTTF.ttf', 10)

        self.scale = 0.1              # 처음 크기
        self.scale_target = 1.0       # 최종 크기
        self.scale_speed = 0.02       # 커지는 속도
        self.spawn_effect = True      # 등장 중인지 여부

    def draw(self):
        pass

    def update(self):
        pass

    def handle_collision(self, group, other):
        pass

class Boss(Monster):
    def __init__(self, player = None):
        super().__init__(WIDTH // 2, HEIGHT - 100, 10000, 10,player)
        self.animation1 = load_image('resource/Golem Iron_1.png')
        self.animation2 = load_image('resource/Golem Iron_2.png')
        self.animation3 = load_image('resource/Golem Iron_3.png')
        self.animation4 = load_image('resource/Golem Iron_4.png')
        self.animation_list = [self.animation1, self.animation2, self.animation3, self.animation4]

        self.alive = True
        self.trace_on = True # 보스는 처음부터 추적모드
        self.frame = 0
        self.speed = 1
        self.attack_range = 70

        self.build_behavior_tree()

    def draw(self):
        if not self.alive:
            return

        if self.is_hit and (self.flash_timer // 5) % 2 == 0:
            return

        self.animation_list[int(self.frame)].draw(self.x, self.y, 108, 102) # 원본 두배 크기로 그리기
        draw_rectangle(*self.get_bb())
        self.font.draw(self.x, self.y + 15, f'(hp: {self.hp})', (255, 0, 0))

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_BOSS * ACTION_PER_TIME_BOSS * game_framework.frame_time) % 4
        #self.bt.run()

    def get_bb(self):
        return self.x - 54, self.y - 51, self.x + 54, self.y + 51

    def is_boss_y_less_than_player_y(self):
        if self.y < self.player.y: # 보스가 더 아래시 true 반환
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def back_dash(self):
        #self.back_dash_animation = True
        self.y += game_framework.frame_time * RUN_SPEED_PPS

        marin = 20
        if self.y + marin > self.player.y:
            return BehaviorTree.SUCCESS
            # self.back_dash_animation = False
        else:
            return BehaviorTree.RUNNING


    def distance_less_than(self, range):
        distance = (self.x - self.player.x) ** 2 + (self.y - self.player.y) ** 2
        return distance < (PIXEL_PER_METER * range) ** 2

    def is_player_in_boss_attack_range(self, range):
        if self.distance_less_than(range):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def attack(self):
        # self.attack_animation = True
        if self.attack_end:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def move_little_to(self, target_x, target_y):
        self.dir = math.atan2(target_y - self.y, target_x - self.x)  # 탄젠트 역함수
        distance = game_framework.frame_time * RUN_SPEED_PPS

        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def trace_player(self):
        self.move_little_to(self.player.x, self.player.y)
        if self.distance_less_than(1):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):

        c1 = Condition('플레이어가 보스보다 더 위에 있는가?', self.is_boss_y_less_than_player_y)
        a1 = Action('보스 백대쉬', self.back_dash)
        back_dash = Sequence('플레이어가 보스보다 위에 위치시 백대쉬', c1, a1)

        c2 = Condition('플레이어가 범위 안에 있는가?', self.is_player_in_boss_attack_range , 5)
        a2 = Action('공격', self.attack)
        attack = Sequence('플레이어가 공격범위 안에 있으면 공격', c2, a2)

        a3 = Action('추적', self.trace_player)
        trace = Sequence('공격범위에 플레이어 없을시 추적', a3)

        root = Selector('백대쉬 or 공격 or 추적', back_dash, attack, trace)
        self.bt = BehaviorTree(root)


class Red_Golem(Monster):
    image = None
    def __init__(self, player = None):
        super().__init__(randint(0, WIDTH), randint(0,HEIGHT), 3000, 2,player)
        if Red_Golem.image == None:
            Red_Golem.image = load_image('resource/red_golem.png')
        self.frame = randint(0,6)
        self.speed = 0.7
        self.on_right = randint(0,1) # 캐릭터기준 오른쪽인지 ,,
        self.attack_range = 50


    def draw(self):
        if not self.alive:
            return

        if self.is_hit and (self.flash_timer // 5) % 2 == 0:
            return  # 5프레임마다 안 그려짐

        if self.spawn_effect:
            if self.scale < self.scale_target:
                self.scale += self.scale_speed
            else:
                self.scale = self.scale_target
                self.spawn_effect = False  # 등장 완료

        size = int(70 * self.scale)

        if self.on_right:
            Red_Golem.image.clip_composite_draw(int(self.frame) * 35, 0, 35, 35, 0, 'h', self.x, self.y, size, size)
        else:
            Red_Golem.image.clip_composite_draw(int(self.frame) * 35, 0, 35, 35, 0, '', self.x, self.y, size, size)
        draw_rectangle(*self.get_bb())
        self.font.draw(self.x, self.y + 15, f'(hp: {self.hp})', (255, 0, 0))

    def update(self):
        if not self.alive:
            self.respawn_timer += 1
            if self.respawn_timer >= 300:
                self.alive = True
                self.respawn_timer = 0
            return

        if self.is_hit:
            self.stop_time -= 1
            self.flash_timer += 1
            if self.stop_time <= 0:
                self.is_hit = False
                self.stop_time = 120
                self.flash_timer = 0
                if self.hp <= 0:
                    self.alive = False
                    game_world.remove(self)
                    self.player.get_money_animation = True
                    self.player.gold += randint(10,50)

                    # 골렘 리스폰
                    respawn_golem = Red_Golem(self.player)
                    game_world.add(respawn_golem, 'object')
                    game_world.add_collision_pair('player:golem', self.player, respawn_golem)
                    game_world.add_collision_pair('sword:golem', self.player.sword, respawn_golem)
                    print(f'[DEBUG] Red Golem Respawned')
            return
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7

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
        else:
            self.trace_wait -= 1
            if self.trace_wait <= 0:
                self.trace_on = True

    def get_bb(self):
        return self.x - 16*2, self.y - 16*2, self.x + 16*2, self.y + 16*2

    def handle_collision(self, group, other):
        if group == 'sword:golem':
            if other.sword_active and not self.is_hit:
                self.hp -= other.damage
                self.is_hit = True
                self.flash_timer = 0
                self.trace_on = True
        elif group == 'player:golem':
            pass


class White_Golem(Monster):
    image = None
    def __init__(self, player = None):
        super().__init__(randint(0, WIDTH), randint(0,HEIGHT), 3000, 2,player)
        if White_Golem.image == None:
            White_Golem.image = load_image('resource/white_golem.png')
        self.frame = randint(0,6)
        self.speed = 0.7
        self.on_right = randint(0,1) # 캐릭터기준 오른쪽인지 ,,
        self.attack_range = 50


    def draw(self):
        if not self.alive:
            return

        if self.is_hit and (self.flash_timer // 5) % 2 == 0:
            return  # 5프레임마다 안 그려짐

        if self.spawn_effect:
            if self.scale < self.scale_target:
                self.scale += self.scale_speed
            else:
                self.scale = self.scale_target
                self.spawn_effect = False  # 등장 완료

        size = int(78 * self.scale)

        if self.on_right:
            White_Golem.image.clip_composite_draw(int(self.frame) * 39, 0, 39, 39, 0, 'h', self.x, self.y, size, size)
        else:
            White_Golem.image.clip_composite_draw(int(self.frame) * 39, 0, 39, 39, 0, '', self.x, self.y, size, size)
        draw_rectangle(*self.get_bb())
        self.font.draw(self.x, self.y + 15, f'(hp: {self.hp})', (255, 0, 0))

    def update(self):
        if not self.alive:
            self.respawn_timer += 1
            if self.respawn_timer >= 300:
                self.alive = True
                self.respawn_timer = 0
            return

        if self.is_hit:
            self.stop_time -= 1
            self.flash_timer += 1
            if self.stop_time <= 0:
                self.is_hit = False
                self.stop_time = 120
                self.flash_timer = 0
                if self.hp <= 0:
                    self.alive = False
                    game_world.remove(self)
                    self.player.get_money_animation = True
                    self.player.gold += randint(10,50)

                    # 골렘 리스폰
                    respawn_golem = White_Golem(self.player)
                    game_world.add(respawn_golem, 'object')
                    game_world.add_collision_pair('player:golem', self.player, respawn_golem)
                    game_world.add_collision_pair('sword:golem', self.player.sword, respawn_golem)
                    print(f'[DEBUG] White Golem Respawned')
            return
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7

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
        else:
            self.trace_wait -= 1
            if self.trace_wait <= 0:
                self.trace_on = True

    def get_bb(self):
        return self.x - 19*2, self.y - 19*2, self.x + 19*2, self.y + 19*2

    def handle_collision(self, group, other):
        if group == 'sword:golem':
            if other.sword_active and not self.is_hit:
                self.hp -= other.damage
                self.is_hit = True
                self.flash_timer = 0
                self.trace_on = True
        elif group == 'player:golem':
            pass


