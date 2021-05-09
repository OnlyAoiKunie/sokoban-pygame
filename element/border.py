from element.obj import Object
from pygame import image

img = image.load("imgs/border.png")


class Border(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        super().set_img(img)


if __name__ == "__main__":
    b = Border(10, 10)
    print(b.pos())
