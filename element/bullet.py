from element.obj import Object
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

    def update(self):
        delta_x, delta_y = self.__movement
        super().move(delta_x, delta_y)

if __name__ == "__main__":
    pass
