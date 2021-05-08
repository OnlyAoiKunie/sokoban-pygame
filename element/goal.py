from element.obj import Object
from pygame import image

img = image.load("imgs/goal.png")

class Goal(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        super().set_img(img)

if __name__ == "__main__":
    g = Goal(10, 10)
    print(g.pos())
