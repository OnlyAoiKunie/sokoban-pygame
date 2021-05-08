from element.obj import Object
from pygame import image, transform
from element import direction

imgs = [ _ for _ in range(4) ]

img = image.load("imgs/police/up.png")
imgs[direction.UP] = img
img = image.load("imgs/police/down.png")
imgs[direction.DOWN] = img
img = image.load("imgs/police/right.png")
imgs[direction.RIGHT] = img
img = transform.flip(img, True, False)
imgs[direction.LEFT] = img

class Police(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.__dir = direction.DOWN
        super().set_img(self.__img())

    def set_dir(self, direction):
        self.__dir = direction
        super().set_img(self.__img())

    def __img(self):
        return imgs[self.__dir]

if __name__ == "__main__":
    p = Police(10, 10)
    print(p.pos())
