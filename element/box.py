from element.obj import Object
from element.goal import Goal
from element import consts
from pygame import image, rect
import random

img = image.load("imgs/boxes.webp").convert_alpha()
imgs = [ _ for _ in range(10) ]
for i, _ in enumerate(imgs):
    offset = consts.BOX_SIZE * i
    rect_ = rect.Rect(offset, 0, consts.BOX_SIZE, consts.BOX_SIZE)
    imgs[i] = img.subsurface(rect_)

class Box(Object):
    def __init__(self, x, y):
        super().__init__(x + consts.BOX_OFFSET, y + consts.BOX_OFFSET)
        self.__img = random.choice(imgs)
        super().set_img(self.__img)

    def move(self, delta_x, delta_y, world):
        super().move(delta_x, delta_y)
        if self.__is_collide(world):
            super().move(-delta_x, -delta_y)

    def __is_collide(self, world):
        box_x, box_y = super().pos()
        for item in world:
            # 比對到自己則跳過
            if item is self or isinstance(item, Goal):
                continue
            item_x, item_y = item.pos()
            if abs(item_x - box_x) < consts.BOX_GAP and abs(item_y - box_y) < consts.BOX_GAP:
                return True
        return False


if __name__ == "__main__":
    b = Box(10, 10)
    print(b.pos())
    b.move(10, -20)
    print(b.pos())
