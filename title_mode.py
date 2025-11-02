from pico2d import *
WIDTH, HEIGHT = 1280, 720
import game_framework, play_mode

image = None

def init():
    # 타이틀 이미지 로드
    global image
    image = load_image('resource/title.png')


def update():
    pass



def draw():
    # 로고 이미지 그리기
    clear_canvas()
    image.draw(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)
    update_canvas()


def finish():
    global image
    del image # 소멸자 역할 ( 끝날시 이미지 메모리에서 삭제 )


def handle_events():
    event_list = get_events() # 현재까지 들어온 이벤트들을 받아온다
    # 스페이스 키 이벤트 처리하여 게임 모드로 전환
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RETURN:
                game_framework.change_mode(play_mode)
