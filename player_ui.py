from pico2d import load_font, draw_rectangle
WIDTH, HEIGHT = 1280, 720

class PlayerUI:
    def __init__(self,player):
        self.player = player
        self.font = load_font('DNFBitBitTTF.ttf', 20)

    def draw(self):
        x1, y1 = WIDTH - 500, 20
        bar_width = 480
        bar_height = 30

        hp_ratio = self.player.hp / self.player.max_hp
        draw_rectangle(x1, y1, x1 + bar_width, y1 + bar_height)  # 테두리

        fill_w = int(bar_width * hp_ratio)
        for i in range(0, fill_w, 5):  # 5픽셀 단위로 채움
            draw_rectangle(x1 + i, y1, x1 + i + 5, y1 + bar_height)

        self.font.draw(WIDTH - 500, y1 + 50, f'HP: {int(self.player.hp)}/{self.player.max_hp}', (255, 255, 255))

        self.font.draw(WIDTH - 500, y1 + 80,
                       f'GOLD: {int(self.player.gold)}G',
                       (255, 215, 0))  # 노란색

    def update(self):
        pass
