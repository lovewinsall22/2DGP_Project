from pico2d import load_image, draw_rectangle
from town import Town
from npc import NPC
from hit_objects.dummy import Dummy
from hit_objects.monster_base import Red_Golem, White_Golem

WIDTH, HEIGHT = 1280, 720

class Portal:
    def __init__(self,stage,number,x,y,dungeon):
        self.image = load_image('resource/portal.png')
        self.stage = stage
        self.number = number
        self.x, self.y = x, y
        self.dungeon = dungeon

    def update(self):
        pass

    def draw(self):
        if self.dungeon.cur_dungeon == self.stage:
            self.image.draw(self.x,self.y,64,64)
            draw_rectangle(*self.get_bb())

    def enter_portal(self, world, player, dungeon,monsters):
        if self.number ==1 :
            # 제거 대상 타입
            remove_types = (Town, NPC, Dummy)
            # 모든 레이어에서 해당 타입의 오브젝트 제거
            for layer in world.layers.values():
                layer[:] = [obj for obj in layer if not isinstance(obj, remove_types)]
            dungeon.stage_on = True
            dungeon.cur_dungeon = 0
            player.x, player.y = WIDTH // 2, 100
            fire_golems = [White_Golem(player) for _ in range(20)]
            monsters += fire_golems
            for golem in fire_golems:
                world.add(golem, 'object')
                world.add_collision_pair('player:golem', player, golem)
                world.add_collision_pair('sword:golem', None, golem)

        elif self.number == 3:
            remove_types = White_Golem
            for layer in world.layers.values():
                layer[:] = [obj for obj in layer if not isinstance(obj, remove_types)]
            self.dungeon.stage_on = False
            self.dungeon.cur_dungeon = 99
            player.x, player.y = WIDTH // 2 + 15, HEIGHT - 60
            world.add(Town(), 'background')
            world.add(NPC())
            world.add(Dummy())

    def get_bb(self):
        return self.x - 32, self.y - 32, self.x + 32, self.y + 32

    def handle_collision(self, group, other):
        if group == 'player:portal':
            pass

