from pico2d import *
import game_framework, title_mode

WIDTH, HEIGHT = 1280, 720
#character_size = 64
from dungeon import Dungeon
from hit_objects.dummy import Dummy
from npc import NPC
from player_class import Player
from portal import Portal
from store import Store
from town import Town
from world import World

#running = True

def init():
    global world, player, town, dungeon, townNpc, dummy, store, portals, monsters, damage_texts
    world = World()

    player = Player()
    town = Town()
    dungeon = Dungeon()
    townNpc = NPC()
    world.add_collision_pair('player:townNpc', player, townNpc)
    dummy = Dummy()
    world.add_collision_pair('player:dummy', player, dummy)
    store = Store()
    portals = []
    portals.append(Portal(99,1, WIDTH // 2 + 15, HEIGHT - 60,dungeon))
    portals.append(Portal(99,2, WIDTH - 80, HEIGHT - 60,dungeon))
    portals.append(Portal(0,3, WIDTH // 2, 100,dungeon))
    for p in portals:
        world.add_collision_pair('player:portal', player,p)

    monsters = []
    monsters.append(dummy)
    damage_texts = []


    world.add(town, 'background')
    world.add(dungeon, 'background')
    world.add(townNpc)
    for m in monsters:
        world.add(m)
    for p in portals:
        world.add(p)
    world.add(store, 'ui')
    world.add(player, 'player')

def finish():
    world.clear()

def update():
    world.update()

    player.sword.attack_check(monsters, damage_texts)

    # 데미지 텍스트 갱신
    for t in damage_texts[:]:
        if not t.update():
            damage_texts.remove(t)

def draw():
    clear_canvas()
    world.draw()

    for t in damage_texts:
        t.draw()
    update_canvas()

def handle_events():
    #global running
    global player
    events = get_events() # 이벤트 받아오기
    for event in events:
        if event.type == SDL_QUIT: # 창 닫기 버튼
            #running = False
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_l:  # 상점 열기
            if check_collision(townNpc):
                store.IsOpen = not store.IsOpen
            else:
                for p in portals:
                    if check_collision(p):
                        p.enter_portal(world, player, dungeon, monsters)
                        return
        elif event.type == SDL_KEYDOWN and SDLK_1 and store.IsOpen:
            if player.gold < 100: store.player_no_money = True; return
            player.gold -= 100
            player.hp_potion_count += 1
        elif event.type == SDL_KEYDOWN and SDLK_2 and store.IsOpen:
            if player.gold < 100: store.player_no_money = True; return
            player.gold -= 100
            player.damage += 100
        elif event.type == SDL_KEYDOWN and SDLK_3 and store.IsOpen:
            if player.gold < 100: store.player_no_money = True; return
            player.gold -= 100
            player.speed += 1
        else:
            player.handle_event(event)

def check_collision(object):
    left_a, bottom_a, right_a, top_a = player.x - 20, player.y - 31, player.x + 20, player.y + 31
    left_b, bottom_b, right_b, top_b = object.x - 32, object.y - 32, object.x + 32, object.y + 32

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


