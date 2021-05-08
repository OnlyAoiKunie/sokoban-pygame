from element.obj import Object
from element.goal import Goal
from element import consts
from pygame import image
import random

imgs = [ _ for _ in range(10) ]

for i in range(10):
    img = image.load(f"imgs/treasures/{i}.png")
    imgs[i] = img

class Box(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.__skin = random.randint(0, 9)
        super().set_img(imgs[self.__skin])

    def move(self, delta_x, delta_y, world):
        super().move(delta_x, delta_y)
        if self.is_collide(world):
            super().move(-delta_x, -delta_y)

    def is_collide(self, world):
        box_x, box_y = super().pos()
        for item in world:
            # 比對到自己則跳過
            if item.pos() == self.pos():
                continue
            if isinstance(item, Goal):
                continue
            item_x, item_y = item.pos()
            if abs(item_x - box_x) < consts.GAP and abs(item_y - box_y) < consts.GAP:
                return True
        return False

if __name__ == "__main__":
    b = Box(10, 10)
    print(b.pos())
    b.move(10, -20)
    print(b.pos())
