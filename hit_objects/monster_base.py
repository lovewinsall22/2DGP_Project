from random import randint
from pico2d import load_image
WIDTH, HEIGHT = 1280, 720

class Monster:
    def __init__(self, x, y, hp, damage):
        self.x, self.y = x, y
        self.hp = hp
        self.damage = damage
        self.alive = True

    def draw(self):
        pass

    def update(self):
        pass


class Golem(Monster):
    image = None
    def __init__(self):
        super().__init__(randint(0, WIDTH), randint(0,HEIGHT), 100, 20)
        if Golem.image == None:
            Golem.image = load_image('resource/l_golem.png')
        self.frame = randint(0,6)
        self.speed = 2
        self.anicount = 0


    def draw(self):
        if self.alive == True:
            Golem.image.clip_draw(self.frame * 35, 0, 35, 35, self.x, self.y)

    def update(self):
        self.anicount += 1
        if self.alive == True and self.anicount % 10 == 0:
            self.frame = (self.frame + 1) % 7
            self.anicount = 0
