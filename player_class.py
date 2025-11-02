from pico2d import load_image, draw_rectangle

WIDTH, HEIGHT = 1280, 720
from player_ui import PlayerUI
from sword import Sword


class Player:
    def __init__(self):
        self.right1 = load_image('resource/white_r_1.png')
        self.right2 = load_image('resource/white_r_2.png')
        self.right3 = load_image('resource/white_r_3.png')
        self.right4 = load_image('resource/white_r_4.png')
        self.right5 = load_image('resource/white_r_5.png')
        self.left1 = load_image('resource/white_l_1.png')
        self.left2 = load_image('resource/white_l_2.png')
        self.left3 = load_image('resource/white_l_3.png')
        self.left4 = load_image('resource/white_l_4.png')
        self.left5 = load_image('resource/white_l_5.png')
        self.rightMove = [self.right1, self.right2, self.right3, self.right4, self.right5]
        self.leftMove = [self.left1, self.left2, self.left3, self.left4, self.left5]

        #self.attack_r = load_image('resource/attack_r.png')
        #self.attack_l = load_image('resource/attack_l.png')

        self.x, self.y = WIDTH / 2, HEIGHT / 2 # 플레이어 초기 좌표
        self.dirX,self.dirY = 0, 0 # 이동 방향
        self.ifRight = 1 # 1: 오른쪽, 0: 왼쪽

        self.ani_count = 0 # 기본 애니메이션 프레임 조절을 위해 ,, 카운트
        self.frame = 0 # 기본 애니메이션 프레임

        self.max_hp = 100 # 최대 체력
        self.hp = 100 # 현재 체력
        self.level = 1 # 현재 레벨
        self.speed = 5 # 이동 속도
        self.damage = 1000 # 공격력
        self.gold = 1000 # 골드
        self.hp_potion_count = 0 # 체력포션 개수

        self.playerUI = PlayerUI(self)
        self.sword = Sword(self)

    def draw(self):

        if self.ifRight == 1 : self.rightMove[self.frame].draw(self.x, self.y, 40, 62)
        elif self.ifRight == 0 : self.leftMove[self.frame].draw(self.x, self.y, 40, 62)
        draw_rectangle(self.x - 20, self.y - 31, self.x + 20, self.y + 31)
        self.playerUI.draw()
        self.sword.draw()

    def update(self):
        self.ani_count += 1
        if self.ani_count % 12 == 0:
            self.sword.update()
            self.frame = (self.frame + 1) % 5
            self.ani_count = 0
        self.x += self.dirX * self.speed
        self.y += self.dirY * self.speed
        self.playerUI.update()
