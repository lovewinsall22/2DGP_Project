from pico2d import load_image

WIDTH, HEIGHT = 1280, 720

class Dungeon:
    def __init__(self):
        self.stage_on = False
        self.cur_dungeon = 99 # 99 : 타운 , 0 : 흰 골렘 던전 , 1: 불 골렘 던전, 2: 최종보스 던전 입구
        self.image0 = load_image('resource/dungeon1.jpg')
        self.image1 = load_image('resource/dungeon2.jpg')
        self.image2 = load_image('resource/dungeon3.png')
        self.image3 = load_image('resource/dungeon4.jpg') # 최종보스 던전 내부
        self.dungeon_list = [ self.image0, self.image1, self.image2, self.image3 ] # 0 : 흰 골렘 던전 , 1: 불 골렘 던전, 2: 최종보스 던전 입구

    def draw(self):
        if self.stage_on:
            self.dungeon_list[self.cur_dungeon].draw(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)
        pass

    def update(self):
        pass
