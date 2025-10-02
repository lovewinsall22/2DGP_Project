from pico2d import *

def init_world():
    pass

def update_world():
    pass

def render_world():
    pass

def handle_events():
    global running
    events = get_events() # 이벤트 받아오기
    for event in events:
        if event.type == SDL_QUIT: # 창 닫기 버튼
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE: # ESC
            running = False


open_canvas()
init_world() # 게임 초기화 후 시작

while running:
    handle_events() # 입력처리
    update_world() # 게임 로직 업데이트
    render_world() # 렌더링
    delay(0.05)



close_canvas()

