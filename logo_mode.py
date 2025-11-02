from pico2d import *
import game_framework

WIDTH, HEIGHT = 1280, 720

image = None
logo_start_time = 0

def init():
    # 로고 이미지 로드
    global image, running, logo_start_time

    image = load_image('resource/tuk_credit.png')
    logo_start_time = get_time() # 시작 시간 설정

def update():
    # 시간 체크
    if get_time() - logo_start_time > 2: game_framework.quit()

def draw():
    # 로고 이미지 그리기
    clear_canvas()
    image.draw(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)
    update_canvas()


def finish():
    global image
    del image # 소멸자

def handle_events():
    event_list = get_events()
