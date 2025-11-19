from pico2d import load_image, draw_rectangle
from town import Town
from npc import NPC
from hit_objects.dummy import Dummy
from hit_objects.monster_base import Red_Golem, White_Golem, Boss
from sdl2 import SDL_KEYDOWN, SDLK_y, SDLK_n
from world import game_world

WIDTH, HEIGHT = 1280, 720

class Portal:
    image = None
    boss_dungeon_portal = None
    def __init__(self,stage,number,x,y,dungeon, player = None):
        if Portal.image == None:
            Portal.image = load_image('resource/portal.png')
        if Portal.boss_dungeon_portal == None:
            Portal.boss_dungeon_portal = load_image('resource/boss_portal.png')
        self.stage = stage
        self.number = number
        self.x, self.y = x, y
        self.dungeon = dungeon
        self.player = player

        self.ask_you = False # 최종 보스 던전 입구에서 물어보는 창 띄울지 여부
        self.player_answer_yes = -1 # 1: yes , 0: no , -1 : 아직 선택 안함

    def update(self):
        if not self.ask_you:
            return

        if self.player_answer_yes == 1: # yes 선택
            if self.player_answer_yes == 1:
                removes_types = White_Golem
                for layer in list(game_world.layers.values()):
                    for obj in list(layer):
                        if isinstance(obj, removes_types):
                            game_world.remove(obj)

                self.dungeon.cur_dungeon = 2
                self.player.x, self.player.y = WIDTH // 2, 100
                self.ask_you = False
        elif self.player_answer_yes == 0: # no 선택
            self.player_answer_yes = -1
            self.ask_you = False

    def draw(self):
        if self.ask_you:
            draw_rectangle(WIDTH // 2 - 200, HEIGHT // 2 - 150, WIDTH // 2 + 200, HEIGHT // 2 + 150)
        if self.dungeon.cur_dungeon == self.stage:
            if self.number == 6:
                self.boss_dungeon_portal.draw(self.x,self.y,64,64)
            else:
                self.image.draw(self.x,self.y,64,64)
            draw_rectangle(*self.get_bb())

    def enter_portal(self, world, player, dungeon,monsters):
        if self.number == 1 and dungeon.cur_dungeon == 99 :
            # 제거 대상 타입
            remove_types = (Town, NPC, Dummy)
            for layer in list(world.layers.values()):
                for obj in list(layer):  # 복사본으로 순회 (삭제 중 오류 방지)
                    if isinstance(obj, remove_types):
                        world.remove(obj)  # ← 여기서 remove() 함수 호출!
            dungeon.stage_on = True
            dungeon.cur_dungeon = 0
            player.x, player.y = WIDTH // 2, 100
            white_golems = [White_Golem(player) for _ in range(20)]
            monsters += white_golems
            for golem in white_golems:
                world.add(golem, 'object')
                world.add_collision_pair('player:golem', player, golem)
                world.add_collision_pair('sword:golem', None, golem)
        elif self.number == 2 and dungeon.cur_dungeon == 99:
            remove_types = (Town, NPC, Dummy)
            for layer in list(world.layers.values()):
                for obj in list(layer):  # 복사본으로 순회 (삭제 중 오류 방지)
                    if isinstance(obj, remove_types):
                        world.remove(obj)  # ← 여기서 remove() 함수 호출!
            dungeon.stage_on = True
            dungeon.cur_dungeon = 1
            player.x, player.y = WIDTH // 2, HEIGHT // 2
            fire_golems = [Red_Golem(player) for _ in range(20)]
            monsters += fire_golems
            for golem in fire_golems:
                world.add(golem, 'object')
                world.add_collision_pair('player:golem', player, golem)
                world.add_collision_pair('sword:golem', None, golem)
        elif self.number == 3 and dungeon.cur_dungeon == 0:
            remove_types = White_Golem
            for layer in list(world.layers.values()):
                for obj in list(layer):  # 복사본으로 순회 (삭제 중 오류 방지)
                    if isinstance(obj, remove_types):
                        world.remove(obj)  # ← 여기서 remove() 함수 호출!
            self.dungeon.stage_on = False
            self.dungeon.cur_dungeon = 99
            player.x, player.y = WIDTH // 2 + 15, HEIGHT - 60
            world.add(Town(), 'background')
            world.add(NPC())
            world.add(Dummy())
            print(f'[DEBUG] Portal {self.number} triggered, cur_dungeon={dungeon.cur_dungeon}')
        elif self.number == 4 and dungeon.cur_dungeon == 1:
            remove_types = Red_Golem
            for layer in list(world.layers.values()):
                for obj in list(layer):  # 복사본으로 순회 (삭제 중 오류 방지)
                    if isinstance(obj, remove_types):
                        world.remove(obj)  # ← 여기서 remove() 함수 호출!
            self.dungeon.stage_on = False
            self.dungeon.cur_dungeon = 99
            player.x, player.y = WIDTH - 80, HEIGHT - 60
            world.add(Town(), 'background')
            world.add(NPC())
            world.add(Dummy())
            print(f'[DEBUG] Portal {self.number} triggered, cur_dungeon={dungeon.cur_dungeon}')
        elif self.number == 5 and dungeon.cur_dungeon == 0:
            self.ask_you = True
            self.player_answer_yes = -1
            # 입력 기다리기 ...
            return

        elif self.number == 6 and dungeon.cur_dungeon == 2:
            self.dungeon.cur_dungeon = 3
            player.x, player.y = WIDTH // 2, 100

            world.add(Boss(player), 'object')


    def get_bb(self):
        return self.x - 32, self.y - 32, self.x + 32, self.y + 32

    def handle_collision(self, group, other):
        if group == 'player:portal':
            pass

    def handle_event(self,event):
        if not self.ask_you:
            return
        if event.type == SDL_KEYDOWN and event.key == SDLK_y:
            self.player_answer_yes = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_n:
            self.player_answer_yes = 0

