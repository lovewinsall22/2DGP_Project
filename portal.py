from pico2d import load_image, draw_rectangle
from town import Town
from npc import NPC
from hit_objects.dummy import Dummy
from hit_objects.monster_base import Red_Golem, White_Golem, Boss

WIDTH, HEIGHT = 1280, 720

class Portal:
    image = None
    boss_dungeon_portal = None
    def __init__(self,stage,number,x,y,dungeon):
        if Portal.image == None:
            Portal.image = load_image('resource/portal.png')
        if Portal.boss_dungeon_portal == None:
            Portal.boss_dungeon_portal = load_image('resource/boss_portal.png')
        self.stage = stage
        self.number = number
        self.x, self.y = x, y
        self.dungeon = dungeon

    def update(self):
        pass

    def draw(self):
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
            removes_types = White_Golem
            for layer in list(world.layers.values()):
                for obj in list(layer):
                    if isinstance(obj, removes_types):
                        world.remove(obj)

            self.dungeon.cur_dungeon = 2
            player.x, player.y = WIDTH // 2, 100

        elif self.number == 6 and dungeon.cur_dungeon == 2:
            self.dungeon.cur_dungeon = 3
            player.x, player.y = WIDTH // 2, 100

            world.add(Boss(player), 'object')


    def get_bb(self):
        return self.x - 32, self.y - 32, self.x + 32, self.y + 32

    def handle_collision(self, group, other):
        if group == 'player:portal':
            pass

