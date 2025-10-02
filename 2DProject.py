from pico2d import *

class NPC:
    def __init__(self):
        self.image = load_image('resource/townNPC.png')
        self.x, self.y = 200, 500
        self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame * 32, 0, 32, 32, self.x, self.y)

    def update(self):
        self.frame = (self.frame + 1) % 6


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

        self.x, self.y = WIDTH / 2, HEIGHT / 2
        self.dirX,self.dirY = 0, 0
        self.ifRight = 1
        self.ifAttack = False
        self.attack_frame = 0
        self.frame = 0

    def draw(self):
        if self.ifRight == 1 and self.ifAttack == False: self.rightMove[self.frame].draw(self.x, self.y)
        elif self.ifRight == 0 and self.ifAttack == False: self.leftMove[self.frame].draw(self.x, self.y)
        if self.ifRight == 1 and self.ifAttack == True: self.attack_r.clip_draw(self.attack_frame * 32, 0, 32, 32, self.x, self.y)
        elif self.ifRight == 0 and self.ifAttack == True: self.attack_l.clip_draw(self.attack_frame * 32, 0, 32, 32, self.x, self.y)
    def update(self):
        if self.ifAttack == False: self.frame = (self.frame + 1) % 5
        elif self.ifAttack == True:
            self.attack_frame = (self.attack_frame + 1) % 7
            delay(0.1)
            if self.attack_frame == 6:
                self.ifAttack = False
                self.attack_frame = 0
        self.x += self.dirX * 5
        self.y += self.dirY * 5



def init_world():
    global running; running = True
    global worldObject
    global player; player = Player()
    global town; town = Town()
    global townNpc; townNpc = NPC()

    worldObject = []
    worldObject.append(town)
    worldObject.append(player)
    worldObject.append(townNpc)

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
            elif event.key == SDLK_d: player.dirX += 1; player.ifRight = 1
            elif event.key == SDLK_a:  player.dirX -= 1; player.ifRight = 0
            elif event.key == SDLK_w:    player.dirY += 1;
            elif event.key == SDLK_s:  player.dirY -= 1;
            elif event.key == SDLK_SPACE: player.ifAttack = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:   player.dirX -= 1
            elif event.key == SDLK_a:  player.dirX += 1
            elif event.key == SDLK_w:    player.dirY -= 1
            elif event.key == SDLK_s:  player.dirY += 1

WIDTH, HEIGHT = 1280, 720
open_canvas(WIDTH,HEIGHT)
init_world() # 게임 초기화 후 시작

while running:
    handle_events() # 입력처리
    update_world() # 게임 로직 업데이트
    render_world() # 렌더링
    delay(0.025)



close_canvas()

