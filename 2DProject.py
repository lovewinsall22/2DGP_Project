from pico2d import *
import math

class Dummy:
    def __init__(self):
        self.image = load_image('resource/snowmanDummy.png')
        self.x, self.y = 264, 123
        self.frame = 0
        self.ani_count = 0
    def draw(self):
        self.image.clip_draw(self.frame * 32, 0, 32, 32, self.x, self.y, character_size + 10, character_size + 10)

    def update(self):
        self.ani_count +=1
        if self.ani_count % 5 == 0:
            self.frame = (self.frame + 1) % 5
            self.ani_count = 0

class NPC:
    def __init__(self):
        self.image = load_image('resource/townNPC.png')
        self.x, self.y = 200, 500
        self.frame = 0
        self.ani_count = 0
    def draw(self):
        self.image.clip_draw(self.frame * 32, 0, 32, 32, self.x, self.y, character_size, character_size)

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

        self.sword1 = load_image('resource/1.png')
        self.sword2 = load_image('resource/2.png')
        self.sword3 = load_image('resource/3.png')
        self.swordAni = [self.sword1, self.sword2, self.sword3]

        self.x, self.y = WIDTH / 2, HEIGHT / 2
        self.dirX,self.dirY = 0, 0
        self.ifRight = 1
        self.ifAttack = False
        self.ani_count = 0
        self.attack_frame = 0
        self.sword_active = False
        self.sword_angle = 90
        self.sword_frame = 0
        self.frame = 0
        self.speed = 5

    def draw(self):
        if self.ifRight == 1 and self.ifAttack == False: self.rightMove[self.frame].draw(self.x, self.y, 40, 62)
        elif self.ifRight == 0 and self.ifAttack == False: self.leftMove[self.frame].draw(self.x, self.y, 40, 62)
        if self.ifRight == 1 and self.ifAttack == True: self.attack_r.clip_draw(self.attack_frame * 32, 0, 32, 32, self.x, self.y, character_size, character_size)
        elif self.ifRight == 0 and self.ifAttack == True: self.attack_l.clip_draw(self.attack_frame * 32, 0, 32, 32, self.x, self.y, character_size, character_size)
        if self.sword_active == True:
            sx = self.x + 40 * math.cos(self.sword_angle)
            sy = self.y + 40 * math.sin(self.sword_angle)
            if self.sword_frame == 1: self.swordAni[self.sword_frame].draw(sx, sy, 40, 10)
            else: self.swordAni[self.sword_frame].draw(sx, sy, 32, 32)
    def update(self):
        self.ani_count += 1
        if self.ani_count % 5 == 0:
            if self.ifAttack == False: self.frame = (self.frame + 1) % 5
            elif self.ifAttack == True:
                self.speed = 2
                self.attack_frame = (self.attack_frame + 1) % 7 # 0-6
                if self.attack_frame % 2 == 0: self.sword_angle += 45; self.sword_frame = (self.sword_frame + 1) % 3
                if self.attack_frame == 6:
                    self.ifAttack = False
                    self.sword_active = False
                    self.attack_frame = 0
                    self.sword_angle = 90
                    self.speed = 5
            self.ani_count = 0
        self.x += self.dirX * self.speed
        self.y += self.dirY * self.speed

def init_world():
    global running; running = True
    global worldObject
    global player; player = Player()
    global town; town = Town()
    global townNpc; townNpc = NPC()
    global dummy; dummy = Dummy()

    worldObject = []
    worldObject.append(town)
    worldObject.append(player)
    worldObject.append(townNpc)
    worldObject.append(dummy)

def update_world():
    for object in worldObject:
        object.update()

def render_world():
    clear_canvas()
    for object in worldObject:
        object.draw()
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
            elif event.key == SDLK_d:  player.dirX += 1; player.ifRight = 1
            elif event.key == SDLK_a:  player.dirX -= 1; player.ifRight = 0
            elif event.key == SDLK_w:  player.dirY += 1;
            elif event.key == SDLK_s:  player.dirY -= 1;
            elif event.key == SDLK_SPACE: player.ifAttack = True; player.sword_active = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:    player.dirX -= 1
            elif event.key == SDLK_a:  player.dirX += 1
            elif event.key == SDLK_w:  player.dirY -= 1
            elif event.key == SDLK_s:  player.dirY += 1

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
