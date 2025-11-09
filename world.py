from pico2d import clear_canvas, update_canvas


class World:
    def __init__(self):
        self.layers = {
            'background' : [],
            'object' : [],
            'player' : [],
            'ui' : []
        }
        self.collision_pairs = {}

    def add(self, obj, layer='object'):
        self.layers[layer].append(obj)

    def remove_collision_object(self,o):
        for pairs in self.collision_pairs.values():
            if o in pairs[0]:
                pairs[0].remove(o)
            if o in pairs[1]:
                pairs[1].remove(o)

    def remove(self, obj):
        for layer in self.layers.values():
            if obj in layer:
                layer.remove(obj)
                # collision_pairs에서도 제거해야함 !!
                self.remove_collision_object(obj)
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

    def collide(self,a, b):
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


    def add_collision_pair(self, group,a,b):
        if group not in self.collision_pairs:
            print('새로운 그룹 등록')
            self.collision_pairs[group] = [[], []]

        if a: self.collision_pairs[group][0].append(a)
        if b: self.collision_pairs[group][1].append(b)

    def handle_collisions(self):
        for group, pairs in self.collision_pairs.items():  # 키 벨류 쌍으로 반환
            for a in pairs[0]:
                for b in pairs[1]:
                    if self.collide(a, b):
                        a.handle_collision(group, b)
                        b.handle_collision(group, a)
                        # group으로 충돌 사유를 알려주는것 !!!!

game_world = World()