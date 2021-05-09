from element.obj import Object
from pygame import image, transform
from element import direction
from element import consts

imgs = [_ for _ in range(4)]

img = image.load("imgs/guard/up.png")
imgs[direction.UP] = img
img = image.load("imgs/guard/down.png")
imgs[direction.DOWN] = img
img = image.load("imgs/guard/right.png")
imgs[direction.RIGHT] = img
img = transform.flip(img, True, False)
imgs[direction.LEFT] = img


class Guard(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.__dir = direction.DOWN
        super().set_img(self.__img())
        self.__velocity = consts.GUARD_VELOCITY

    def set_dir(self, direction):
        self.__dir = direction
        super().set_img(self.__img())

    # 移動
    def update(self, world: list):
        current = direction.random_dir()
        self.set_dir(current)
        if self.__dir == direction.DOWN:
            move_x, move_y = 0, self.__velocity
        elif self.__dir == direction.UP:
            move_x, move_y = 0, -self.__velocity
        elif self.__dir == direction.LEFT:
            move_x, move_y = -self.__velocity, 0
        elif self.__dir == direction.RIGHT:
            move_x, move_y = self.__velocity, 0
        else:
            move_x, move_y = 0, 0
        super().move(move_x, move_y)
        if self.__is_collide(world):
            super().move(-move_x, -move_y)

    def __is_collide(self, world: list) -> bool:
        police_x, police_y = super().pos()
        for item in world:
            if item is self:
                continue
            item_x, item_y = item.pos()
            if abs(item_x - police_x) < consts.GAP and abs(item_y - police_y) < consts.GAP:
                return True
        return False

    def __img(self):
        return imgs[self.__dir]


if __name__ == "__main__":
    g = Guard(10, 10)
    print(g.pos())
