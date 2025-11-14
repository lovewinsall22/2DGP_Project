from pico2d import load_image, draw_rectangle
WIDTH, HEIGHT = 1280, 720

block = [
    (50, 560, 240, 710),  # 첫번째 집
    (290, 470, 460, 680),  # 두번째 집
    (560, 400, 590, 720),  # 일자 벽
    (725, 370, 800, 720),  # 위쪽 4개 연속벽
    (800, 410, 850, 720),  # 위쪽 4개 연속벽
    (850, 450, 900, 720),  # 위쪽 4개 연속벽
    (900, 510, 1100, 720),  # 위쪽 4개 연속벽
    (830, 250, 900, 300),  # 아래쪽 3개 연속벽
    (900, 250, 960, 370),  # 아래쪽 3개 연속벽
    (960, 250, 1280, 420)  # 아래쪽 3개 연속벽
]

class Town:
    def __init__(self):
        self.image = load_image('resource/town.jpg')

    def draw(self):
        self.image.draw(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)
        for l, b, r, t in block:
            draw_rectangle(l, b, r, t)

    def update(self):
        pass
