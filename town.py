from pico2d import load_image
WIDTH, HEIGHT = 1280, 720

class Town:
    def __init__(self):
        self.image = load_image('resource/town.jpg')

    def draw(self):
        self.image.draw(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)

    def update(self):
        pass
