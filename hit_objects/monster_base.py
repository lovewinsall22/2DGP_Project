from random import randint
from pico2d import load_image
from math import sqrt
WIDTH, HEIGHT = 1280, 720

class Monster:
    def __init__(self, x, y, hp, damage,player = None):
        self.x, self.y = x, y
        self.hp = hp
        self.damage = damage
        self.alive = True
        self.player = player

    def draw(self):
        pass

    def update(self):
        pass

    def hitted(self, damage):
        self.hp -= damage


class Golem(Monster):
    image = None
    def __init__(self, player = None):
        super().__init__(randint(0, WIDTH), randint(0,HEIGHT), 100, 2,player)
        if Golem.image == None:
            Golem.image = load_image('resource/l_golem.png')
        self.frame = randint(0,6)
        self.speed = 2
        self.anicount = 0

        self.attack_range = 50


    def draw(self):
        if self.alive == True:
            Golem.image.clip_draw(self.frame * 35, 0, 35, 35, self.x, self.y)

    def update(self):
        self.anicount += 1
        if self.alive == True and self.anicount % 10 == 0:
            self.frame = (self.frame + 1) % 7
            self.anicount = 0

        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = sqrt(dx * dx + dy * dy)
        if distance > self.attack_range:
            self.x += self.speed * (dx / distance)
            self.y += self.speed * (dy / distance)

    def get_bb(self):
        return self.x - 32, self.y - 32, self.x + 32, self.y + 32

