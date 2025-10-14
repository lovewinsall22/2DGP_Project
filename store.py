from pico2d import load_font, draw_rectangle


class Store:
    def __init__(self):
        self.IsOpen = False
        self.font = load_font('DNFBitBitTTF.ttf',20)

    def draw(self):
        if self.IsOpen:
            draw_rectangle(WIDTH // 2 - 200, HEIGHT // 2 - 150, WIDTH // 2 + 200, HEIGHT // 2 + 150)
            self.font.draw(WIDTH // 2 - 20, HEIGHT // 2 + 100, '상점', (255, 255, 0))
            self.font.draw(WIDTH // 2 - 120, HEIGHT // 2 + 50, '1. 체력포션 - 100G', (255, 255, 255))
            self.font.draw(WIDTH // 2 - 120, HEIGHT // 2 + 20, '2. 공격력 강화 - 200G', (255, 255, 255))
            self.font.draw(WIDTH // 2 - 120, HEIGHT // 2 - 10, '3. 이동속도 증가 - 200G', (255, 255, 255))
            self.font.draw(WIDTH // 2 - 40, HEIGHT // 2 - 100, 'L키로 닫기', (255, 255, 0))

    def update(self):
        pass
