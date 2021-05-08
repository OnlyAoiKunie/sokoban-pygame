from element.obj import Object
from pygame import image

img = image.load("imgs/arrow.png")

class Arrow(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        super().set_img(img)

if __name__ == "__main__":
    pass
