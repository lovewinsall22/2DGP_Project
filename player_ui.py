from pico2d import load_font, draw_rectangle, load_image
WIDTH, HEIGHT = 1280, 720
import game_framework

class PlayerUI:
    def __init__(self,player):
        self.player = player
        self.font = load_font('DNFBitBitTTF.ttf', 20)
        self.hp_potion = load_image('resource/heart.png')
        self.defeat_image = load_image('resource/defeat.png')
        self.clear_image = load_image('resource/clear.png')
        self.clear_timer = 0

    def draw(self):
        x1, y1 = WIDTH - 500, 20
        bar_width = 480
        bar_height = 30

        hp_ratio = self.player.hp / self.player.max_hp
        draw_rectangle(x1, y1, x1 + bar_width, y1 + bar_height)  # 테두리

        fill_w = int(bar_width * hp_ratio)
        for i in range(0, fill_w, 5):  # 5픽셀 단위로 채움
            draw_rectangle(x1 + i, y1, x1 + i + 5, y1 + bar_height,255,0,0 ,0,1)
        if self.player.hp >= 11:
            self.font.draw(WIDTH - 500, y1 + 50, f'HP: {int(self.player.hp)}/{self.player.max_hp}', (255, 255, 255))
        else:
            self.font.draw(WIDTH - 500, y1 + 50, f'HP: {int(self.player.hp)}/{self.player.max_hp}', (255, 0, 0))

        self.font.draw(WIDTH - 500, y1 + 80, f'GOLD: {int(self.player.gold)}G', (255, 215, 0))  # 노란색

        self.hp_potion.draw(WIDTH - 320, y1 + 50, 21, 17)
        self.font.draw(WIDTH - 300, y1 + 50, f'x {self.player.hp_potion_count}', (255, 255, 255))

        self.font.draw(WIDTH - 230, y1 + 80, f'Damage {self.player.damage}', (255, 255, 255))
        self.font.draw(WIDTH - 230, y1 + 50, f'Speed {self.player.speed:.3f}', (255, 255, 255))

        if self.player.hp <= 0:
            self.defeat_image.draw(WIDTH // 2, HEIGHT // 2, 200, 100)

        if self.player.CLEAR and self.clear_timer > 200:
            self.clear_image.draw(WIDTH // 2, HEIGHT // 2, 200, 100)


    def update(self):
        if self.player.CLEAR:
            self.clear_timer += 1
            if self.clear_timer > 500:
                game_framework.quit()
