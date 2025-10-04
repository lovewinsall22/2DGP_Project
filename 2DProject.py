from pico2d import *
import math

class DmgText:
    def __init__(self,x,y,damage):
        self.font = load_font('K_Damage.ttf', 20)
        self.x, self.y = x,y
        self.damage = damage
        self.timer = 60

    def update(self):
        self.y += 5
        self.timer -= 1
        return self.timer > 0

    def draw(self):
        self.font.draw(self.x, self.y, f'{self.damage}', (255, 0, 0))

class Dummy:
    def __init__(self):
        self.image = load_image('resource/snowmanDummy.png')
        self.x, self.y = 264, 123
        self.frame = 0
        self.ani_count = 0
        self.hp = 9999
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


class NPC:
    def __init__(self):
        self.image = load_image('resource/townNPC.png')
        self.x, self.y = 200, 500
        self.frame = 0
        self.ani_count = 0
    def draw(self):
        self.image.clip_draw(self.frame * 32, 0, 32, 32, self.x, self.y, character_size, character_size)
        draw_rectangle(self.x - 32, self.y - 32, self.x + 32, self.y + 32)

    def update(self):
        self.ani_count +=1
        if self.ani_count % 5 == 0:
            self.frame = (self.frame + 1) % 6
            self.ani_count = 0

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

        self.attack_r = load_image('resource/attack_r.png')
        self.attack_l = load_image('resource/attack_l.png')

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
        self.speed = 5
        self.damage = 10

        self.ifAttack = False
        self.attack_frame = 0
        self.sword_active = False
        self.sword_angle = -1
        self.sword_frame = 0


    def draw(self):
        if self.ifRight == 1 and self.ifAttack == False: self.rightMove[self.frame].draw(self.x, self.y, 40, 62)
        elif self.ifRight == 0 and self.ifAttack == False: self.leftMove[self.frame].draw(self.x, self.y, 40, 62)
        if self.ifRight == 1 and self.ifAttack == True: self.attack_r.clip_draw(self.attack_frame * 32, 0, 32, 32, self.x, self.y, character_size, character_size)
        elif self.ifRight == 0 and self.ifAttack == True: self.attack_l.clip_draw(self.attack_frame * 32, 0, 32, 32, self.x, self.y, character_size, character_size)
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
        if self.ani_count % 5 == 0:
            if self.ifAttack == False: self.frame = (self.frame + 1) % 5
            elif self.ifAttack == True:
                self.speed = 2
                self.attack_frame = (self.attack_frame + 1) % 7 # 0-6
                if self.attack_frame % 2 == 0 and self.ifRight == 0:
                    self.sword_angle += 45; self.sword_frame = (self.sword_frame + 1) % 3
                elif self.attack_frame % 2 == 0 and self.ifRight == 1:
                    self.sword_angle -= 45; self.sword_frame = (self.sword_frame + 1) % 3
                if self.attack_frame == 6:
                    self.ifAttack = False
                    self.sword_active = False
                    self.attack_frame = 0
                    self.sword_angle = 90
                    self.speed = 5
            self.ani_count = 0
        self.x += self.dirX * self.speed
        self.y += self.dirY * self.speed

    def get_sword_bb(self):
        if self.sword_active:
            sx = self.x + 40 * math.cos(self.sword_angle)
            sy = self.y + 40 * math.sin(self.sword_angle)

            if self.sword_frame == 1:
                return sx - 20, sy - 5, sx + 20, sy + 5
            else:
                return sx - 16, sy - 16, sx + 16, sy + 16
        return None


def init_world():
    global running; running = True
    global worldObject
    global player; player = Player()
    global town; town = Town()
    global townNpc; townNpc = NPC()
    global dummy; dummy = Dummy()

    global damage_texts; damage_texts = []

    worldObject = []
    worldObject.append(town)
    worldObject.append(townNpc)
    worldObject.append(dummy)
    worldObject.append(player)

def update_world():
    for object in worldObject:
        object.update()
    if check_collision():
        dummy.hitted(player.damage)
        damage_texts.append(DmgText(dummy.x, dummy.y + 30, player.damage))

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
                if not player.ifAttack: player.ifRight = 1 # 공격중엔 방향전환 X
            elif event.key == SDLK_a:
                player.dirX -= 1
                if not player.ifAttack: player.ifRight = 0 # 공격중엔 방향전환 X
            elif event.key == SDLK_w:  player.dirY += 1;
            elif event.key == SDLK_s:  player.dirY -= 1;
            elif event.key == SDLK_SPACE and player.ifAttack == False:
                player.ifAttack = True
                player.sword_active = True
                if player.ifRight == 0: player.sword_angle = 90
                else: player.sword_angle = 45 # ??
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:    player.dirX -= 1
            elif event.key == SDLK_a:  player.dirX += 1
            elif event.key == SDLK_w:  player.dirY -= 1
            elif event.key == SDLK_s:  player.dirY += 1

def check_collision():
    sword_bb = player.get_sword_bb()
    if sword_bb:
        left_a, bottom_a, right_a, top_a = sword_bb
        left_b, bottom_b, right_b, top_b = dummy.get_bb()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        print("Collision with Dummy!")
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
