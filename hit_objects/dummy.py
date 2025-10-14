from pico2d import load_image, draw_rectangle

from hit_objects.monster_base import Monster

character_size = 64

class Dummy(Monster):
    def __init__(self):
        super().__init__(264,123,99999999,0)
        self.image = load_image('resource/snowmanDummy.png')
        self.frame = 0
        self.ani_count = 0

    def draw(self):
        self.image.clip_draw(self.frame * 32, 0, 32, 32, self.x, self.y, character_size, character_size)
        draw_rectangle(self.x - 32, self.y - 32, self.x + 32, self.y + 32)

    def update(self):
        self.ani_count +=1
        if self.ani_count % 5 == 0:
            self.frame = (self.frame + 1) % 5
            self.ani_count = 0

    def get_bb(self):
        return self.x - 32, self.y - 32, self.x + 32, self.y + 32

    def hitted(self, damage):
        self.hp -= damage
        print(f"Dummy Hp : {self.hp}")
