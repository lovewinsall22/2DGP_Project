from pico2d import load_image, draw_rectangle


class NPC:
    def __init__(self):
        self.image = load_image('resource/townNPC.png')
        self.x, self.y = 200, 500
        self.frame = 0
        self.ani_count = 0
    def draw(self):
        self.image.clip_draw(self.frame * 32, 0, 32, 32, self.x, self.y, character_size, character_size)
        draw_rectangle(self.x - 32, self.y - 32, self.x + 32, self.y + 32)

    def update(self):
        self.ani_count +=1
        if self.ani_count % 5 == 0:
            self.frame = (self.frame + 1) % 6
            self.ani_count = 0
