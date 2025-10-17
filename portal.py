from pico2d import load_image, draw_rectangle
from town import Town
from npc import NPC
from hit_objects.dummy import Dummy
from dungeon import Dungeon

WIDTH, HEIGHT = 1280, 720

class Portal:
    def __init__(self,number,x,y):
        self.image = load_image('resource/portal.png')
        self.number = number
        self.x , self.y = x, y

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x,self.y,64,64)
        draw_rectangle(self.x - 32, self.y - 32, self.x + 32, self.y + 32)

    def goto_dungeon1(self,world_object, player, dungeon):
        # 원본 world_object 에 삭제될 클래스만 빼고 복사
        world_object[:] = [
            obj for obj in world_object
            if not isinstance(obj, (Town, NPC, Dummy, Portal))
        ]
        dungeon.stage_on = True
        dungeon.cur_dungeon = 0
        player.x, player.y = WIDTH // 2, 100
