# python
from sdl2 import SDL_GetKeyboardState
from sdl2 import SDL_SCANCODE_A, SDL_SCANCODE_D, SDL_SCANCODE_W, SDL_SCANCODE_S
from sdl2 import SDLK_a, SDLK_d, SDLK_w, SDLK_s

def get_keys():
    """
    SDL_GetKeyboardState 으로 현재 키 상태를 읽어
    기존 코드에서 사용하던 SDLK_* 키값으로 접근 가능한 dict 반환
    """
    state = SDL_GetKeyboardState(None)
    return {
        SDLK_a: bool(state[SDL_SCANCODE_A]),
        SDLK_d: bool(state[SDL_SCANCODE_D]),
        SDLK_w: bool(state[SDL_SCANCODE_W]),
        SDLK_s: bool(state[SDL_SCANCODE_S]),
    }