import math

from pico2d import load_image, draw_rectangle

from dmg_font import DmgText

def check_collision(bb1, bb2):
    left_a, bottom_a, right_a, top_a = bb1
    left_b, bottom_b, right_b, top_b = bb2
    return not (left_a > right_b or right_a < left_b or top_a < bottom_b or bottom_a > top_b)

class Sword:
    def __init__(self, player):
        self.L_sword1 = load_image('resource/L_1.png')
        self.L_sword2 = load_image('resource/L_2.png')
        self.L_sword3 = load_image('resource/L_3.png')
        self.R_sword1 = load_image('resource/R_1.png')
        self.R_sword2 = load_image('resource/R_2.png')
        self.R_sword3 = load_image('resource/R_3.png')
        self.L_swordAni = [self.L_sword1, self.L_sword2, self.L_sword3]
        self.R_swordAni = [self.R_sword1, self.R_sword2, self.R_sword3]

        self.player = player
        self.already_hit = set() # 충돌처리된 몬스터 기록
        self.attack_hit = False  # 충돌처리 한번
        self.sword_active = False # 공격중 처리 => 공격중일시 다시 입력 불가
        self.sword_angle = 90
        self.sword_frame = 0 # 검 애니메이션 프레임

    def draw(self):
        if self.sword_active:
            sx = self.player.x + 40 * math.cos(self.sword_angle)
            sy = self.player.y + 40 * math.sin(self.sword_angle)
            if self.sword_frame == 1:
                if self.player.ifRight == 0: self.L_swordAni[self.sword_frame].draw(sx, sy, 40, 10)
                else: self.R_swordAni[self.sword_frame].draw(sx, sy, 40, 10)
                draw_rectangle(sx-20, sy-5, sx+20, sy+5)
            else:
                if self.player.ifRight == 0: self.L_swordAni[self.sword_frame].draw(sx, sy, 32, 32)
                else: self.R_swordAni[self.sword_frame].draw(sx, sy, 32, 32)
                draw_rectangle(sx-16, sy-16, sx+16, sy+16)

    def update(self):
        if self.sword_active == True:
            self.player.speed = 2
            if self.player.ifRight == 0:
                self.sword_angle += 45
                self.sword_frame = (self.sword_frame + 1) % 3
            elif self.player.ifRight == 1:
                self.sword_angle -= 45
                self.sword_frame = (self.sword_frame + 1) % 3

            if self.sword_frame == 0:
                self.sword_active = False
                self.sword_angle = 90
                self.player.speed = 5

    def get_sword_bb(self): # 검 히트박스 얻기
        if self.sword_active:
            sx = self.player.x + 40 * math.cos(self.sword_angle)
            sy = self.player.y + 40 * math.sin(self.sword_angle)

            if self.sword_frame == 1:
                return sx - 20, sy - 5, sx + 20, sy + 5
            else:
                return sx - 16, sy - 16, sx + 16, sy + 16
        return None

    def attack_check(self,monsters,dmg_text):
        if not self.sword_active:
            return
        sword_bb = self.get_sword_bb()
        if sword_bb:
            for m in monsters:
                if m not in self.already_hit and check_collision(sword_bb, m.get_bb()):
                    m.hitted(self.player.damage)
                    self.already_hit.add(m)
                    dmg_text.append(DmgText(m.x, m.y + 30, self.player.damage))
