from pico2d import clear_canvas, update_canvas


class World:
    def __init__(self):
        self.layers = {
            'background' : [],
            'object' : [],
            'player' : [],
            'ui' : []
        }

    def add(self, obj, layer='object'):
        self.layers[layer].append(obj)

    def remove(self, obj):
        for layer in self.layers.values():
            if obj in layer:
                layer.remove(obj)
                return True
        return False

    def clear(self):
        for layer in self.layers.values():
            layer.clear()

    def update(self):
        for layer in self.layers.values():
            for obj in layer:
                if hasattr(obj, 'update'):
                    obj.update()

    def draw(self):
        clear_canvas()
        for bg in self.layers['background']:
            bg.draw()
        for e in self.layers['object']:
            e.draw()
        self.layers['player'][0].draw()
        for ui in self.layers['ui']:
            ui.draw()
        update_canvas()

    def collide(a, b):
        # 튜플 반환
        left_a, bottom_a, right_a, top_a = a.get_bb()  # a의 bb
        left_b, bottom_b, right_b, top_b = b.get_bb()  # b의 bb

        # 충돌되지 않는경우 먼저 검사 후 False반환
        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        # 위에서 걸러지지 않으면 충돌 발생 !
        return True
