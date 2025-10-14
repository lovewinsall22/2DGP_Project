from pico2d import *
import math

from dmg_font import DmgText
from npc import NPC
from store import Store


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


class Dummy(Monster):
    def __init__(self):
        super().__init__(264,123,99999999,0)
        self.image = load_image('resource/snowmanDummy.png')
        self.frame = 0
        self.ani_count = 0

    def draw(self):
        self.image.clip_draw(self.frame * 32, 0, 32, 32, self.x, self.y, character_size, character_size)
        draw_rectangle(self.x - 32, self.y - 32, self.x + 32, self.y + 32)

    def update(self):
        self.ani_count +=1
        if self.ani_count % 5 == 0:
            self.frame = (self.frame + 1) % 5
            self.ani_count = 0

    def get_bb(self):
        return self.x - 32, self.y - 32, self.x + 32, self.y + 32

    def hitted(self, damage):
        self.hp -= damage
        print(f"Dummy Hp : {self.hp}")


class Town:
    def __init__(self):
        self.image = load_image('resource/town.jpg')

    def draw(self):
        self.image.draw(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)

    def update(self):
        pass

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

        self.L_sword1 = load_image('resource/L_1.png')
        self.L_sword2 = load_image('resource/L_2.png')
        self.L_sword3 = load_image('resource/L_3.png')
        self.R_sword1 = load_image('resource/R_1.png')
        self.R_sword2 = load_image('resource/R_2.png')
        self.R_sword3 = load_image('resource/R_3.png')
        self.L_swordAni = [self.L_sword1, self.L_sword2, self.L_sword3]
        self.R_swordAni = [self.R_sword1, self.R_sword2, self.R_sword3]

        self.x, self.y = WIDTH / 2, HEIGHT / 2
        self.dirX,self.dirY = 0, 0
        self.ifRight = 1

        self.ani_count = 0
        self.frame = 0

        self.max_hp = 100
        self.hp = 100
        self.max_exp = 100
        self.exp = 0
        self.level = 1
        self.speed = 5
        self.damage = 1000
        self.already_hit = set()

        self.attack_hit = False # 충돌처리 한번
        self.sword_active = False
        self.sword_angle = 90
        self.sword_frame = 0

        self.playerUI = PlayerUI(self)


    def draw(self):
        self.playerUI.draw()
        if self.ifRight == 1 : self.rightMove[self.frame].draw(self.x, self.y, 40, 62)
        elif self.ifRight == 0 : self.leftMove[self.frame].draw(self.x, self.y, 40, 62)
        draw_rectangle(self.x - 20, self.y - 31, self.x + 20, self.y + 31)

        if self.sword_active == True:
            sx = self.x + 40 * math.cos(self.sword_angle)
            sy = self.y + 40 * math.sin(self.sword_angle)
            if self.sword_frame == 1:
                if self.ifRight == 0: self.L_swordAni[self.sword_frame].draw(sx, sy, 40, 10)
                else: self.R_swordAni[self.sword_frame].draw(sx, sy, 40, 10)
                draw_rectangle(sx-20, sy-5, sx+20, sy+5)
            else:
                if self.ifRight == 0: self.L_swordAni[self.sword_frame].draw(sx, sy, 32, 32)
                else: self.R_swordAni[self.sword_frame].draw(sx, sy, 32, 32)
                draw_rectangle(sx-16, sy-16, sx+16, sy+16)

    def update(self):
        self.ani_count += 1
        if self.ani_count % 10 == 0:
            self.frame = (self.frame + 1) % 5
            if self.sword_active == True:
                self.speed = 2
                if self.ifRight == 0:
                    self.sword_angle += 45
                    self.sword_frame = (self.sword_frame + 1) % 3
                elif self.ifRight == 1:
                    self.sword_angle -= 45
                    self.sword_frame = (self.sword_frame + 1) % 3

                if self.sword_frame == 0:
                    self.sword_active = False
                    self.sword_angle = 90
                    self.speed = 5
            self.ani_count = 0
        self.x += self.dirX * self.speed
        self.y += self.dirY * self.speed

    def get_sword_bb(self): # 검 히트박스 얻기
        if self.sword_active:
            sx = self.x + 40 * math.cos(self.sword_angle)
            sy = self.y + 40 * math.sin(self.sword_angle)

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
                    m.hitted(self.damage)
                    self.already_hit.add(m)
                    damage_texts.append(DmgText(m.x, m.y + 30, self.damage))

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

    def update(self):
        pass

def init_world():
    global running; running = True
    global worldObject
    global player; player = Player()
    global town; town = Town()
    global townNpc; townNpc = NPC()
    global dummy; dummy = Dummy()
    global store; store = Store()

    global monsters; monsters = []
    monsters.append(dummy)
    global damage_texts; damage_texts = []


    worldObject = []
    worldObject.append(town)
    worldObject.append(townNpc)
    worldObject.append(player)
    for m in monsters:
        worldObject.append(m)
    worldObject.append(store)

def update_world():
    for object in worldObject:
        object.update()
    player.attack_check(monsters, damage_texts)

    # 데미지 텍스트 갱신
    for t in damage_texts[:]:
        if not t.update():
            damage_texts.remove(t)

def render_world():
    clear_canvas()
    for object in worldObject:
        object.draw()

    for t in damage_texts:
        t.draw()
    update_canvas()

def handle_events():
    global running
    global player
    events = get_events() # 이벤트 받아오기
    for event in events:
        if event.type == SDL_QUIT: # 창 닫기 버튼
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE: running = False # esc
            elif event.key == SDLK_d:
                player.dirX += 1
                if not player.sword_active: player.ifRight = 1 # 공격중엔 방향전환 X
            elif event.key == SDLK_a:
                player.dirX -= 1
                if not player.sword_active: player.ifRight = 0 # 공격중엔 방향전환 X
            elif event.key == SDLK_w:  player.dirY += 1;
            elif event.key == SDLK_s:  player.dirY -= 1;
            elif event.key == SDLK_SPACE and player.sword_active == False:
                player.sword_active = True
                player.already_hit.clear() # 충돌 기록 초기화
                player.sword_frame = 0
                if player.ifRight == 0: player.sword_angle = 90
                else: player.sword_angle = 45 # ??
            elif event.key == SDLK_l: # 상점 열기
                if check_npc_collision():
                    store.IsOpen = not store.IsOpen
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:    player.dirX -= 1
            elif event.key == SDLK_a:  player.dirX += 1
            elif event.key == SDLK_w:  player.dirY -= 1
            elif event.key == SDLK_s:  player.dirY += 1


def check_collision(bb1, bb2):
    left_a, bottom_a, right_a, top_a = bb1
    left_b, bottom_b, right_b, top_b = bb2
    return not (left_a > right_b or right_a < left_b or top_a < bottom_b or bottom_a > top_b)
def check_npc_collision():
    left_a, bottom_a, right_a, top_a = player.x - 20, player.y - 31, player.x + 20, player.y + 31
    left_b, bottom_b, right_b, top_b = townNpc.x - 32, townNpc.y - 32, townNpc.x + 32, townNpc.y + 32

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

WIDTH, HEIGHT = 1280, 720
character_size = 64
open_canvas(WIDTH,HEIGHT)
init_world() # 게임 초기화 후 시작

while running:
    handle_events() # 입력처리
    update_world() # 게임 로직 업데이트
    render_world() # 렌더링
    delay(0.02)



close_canvas()
