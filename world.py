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
