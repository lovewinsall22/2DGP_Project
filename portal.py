from pico2d import load_image, draw_rectangle
from town import Town
from npc import NPC
from hit_objects.dummy import Dummy

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
            draw_rectangle(self.x - 32, self.y - 32, self.x + 32, self.y + 32)

    def goto_dungeon1(self, world, player, dungeon):
        # 제거 대상 타입
        remove_types = (Town, NPC, Dummy)
        # 모든 레이어에서 해당 타입의 오브젝트 제거
        for layer in world.layers.values():
            layer[:] = [obj for obj in layer if not isinstance(obj, remove_types)]
        dungeon.stage_on = True
        dungeon.cur_dungeon = 0
        player.x, player.y = WIDTH // 2, 100
