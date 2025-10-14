from pico2d import load_font


class DmgText:
    def __init__(self,x,y,damage):
        self.font = load_font('DNFBitBitTTF.ttf', 20)
        self.x, self.y = x,y
        self.damage = damage
        self.timer = 30

    def update(self):
        self.y += 5
        self.timer -= 1
        return self.timer > 0

    def draw(self):
        self.font.draw(self.x, self.y, f'{self.damage}', (255, 0, 0))
