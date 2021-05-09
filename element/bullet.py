from element.obj import Object
from element.player import Player
from element.police import Police
from element.goal import Goal
from element import consts, direction
from pygame import image

img = image.load("imgs/bullet.png")

class Bullet(Object):
    def __init__(self, x, y, bullet_dir):
        super().__init__(x, y)
        super().set_img(img)
        self.__velocity = consts.BULLET_VELOCITY
        self.__direction = bullet_dir

        if self.__direction == direction.DOWN:
            self.__movement = (0, self.__velocity)
        elif self.__direction == direction.UP:
            self.__movement = (0, -self.__velocity)
        elif self.__direction == direction.LEFT:
            self.__movement = (-self.__velocity, 0)
        elif self.__direction == direction.RIGHT:
            self.__movement = (self.__velocity, 0)

    def update(self, world: list):
        delta_x, delta_y = self.__movement
        super().move(delta_x, delta_y)
        self.__check_collide(world)

    def __check_collide(self, world: list):
        bullet_x, bullet_y = self.pos()
        for item in world:
            # 不跟自己比較
            if item is self or isinstance(item, Player) or isinstance(item, Goal):
                continue
            item_x, item_y = item.pos()
            if abs(item_x - bullet_x) < consts.GAP and abs(item_y - bullet_y) < consts.GAP:
                world.remove(self)
                if isinstance(item, Police):
                    world.remove(item)
                return

if __name__ == "__main__":
    pass
