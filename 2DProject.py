from pico2d import *

from hit_objects.dummy import Dummy
from npc import NPC
from player_ui import PlayerUI
from store import Store
from sword import Sword


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

    player.sword.attack_check(monsters, damage_texts)

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
                if not player.sword.sword_active: player.ifRight = 1 # 공격중엔 방향전환 X
            elif event.key == SDLK_a:
                player.dirX -= 1
                if not player.sword.sword_active: player.ifRight = 0 # 공격중엔 방향전환 X
            elif event.key == SDLK_w:  player.dirY += 1;
            elif event.key == SDLK_s:  player.dirY -= 1;
            elif event.key == SDLK_SPACE and player.sword.sword_active == False:
                player.sword.sword_active = True
                player.sword.already_hit.clear() # 충돌 기록 초기화
                player.sword.sword_frame = 0
                if player.ifRight == 0: player.sword.sword_angle = 90
                else: player.sword.sword_angle = 45 # ??
            elif event.key == SDLK_l: # 상점 열기
                if check_npc_collision():
                    store.IsOpen = not store.IsOpen
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:    player.dirX -= 1
            elif event.key == SDLK_a:  player.dirX += 1
            elif event.key == SDLK_w:  player.dirY -= 1
            elif event.key == SDLK_s:  player.dirY += 1


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
