from pico2d import load_image

WIDTH, HEIGHT = 1280, 720

class Dungeon:
    def __init__(self):
        self.stage_on = False
        self.cur_dungeon = -1
        self.image0 = load_image('resource/dungeon1.jpg')
        self.image1 = load_image('resource/dungeon2.jpg')
        self.dungeon_list = [ self.image0, self.image1 ]

    def draw(self):
        if self.stage_on:
            self.dungeon_list[self.cur_dungeon].draw(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)
        pass

    def update(self):
        pass
