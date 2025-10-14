class Monster:
    def __init__(self, x, y, hp, damage):
        self.x, self.y = x, y
        self.hp = hp
        self.damage = damage
        self.alive = True
        #self.image = load_image('resource/monster.png')

    def draw(self):
        pass

    def update(self):
        pass
