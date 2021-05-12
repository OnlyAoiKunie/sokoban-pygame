from element.obj import Object
import parameter
from pygame import image, rect

# 初始化所有圖片
img = image.load("imgs/portal.webp").convert_alpha()
imgs = [_ for _ in range(16)]
for i, _ in enumerate(imgs):
    offset = parameter.PORTAL_SIZE * i
    rect_ = rect.Rect(offset, 0, parameter.PORTAL_SIZE, parameter.PORTAL_SIZE)
    imgs[i] = img.subsurface(rect_)


class Portal(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.__img_index = 0
        self.__frame = 0
        super().set_img(imgs[self.__img_index])

    def update(self):
        self.__frame += 1
        if self.__frame % parameter.PORTAL_DELAY == 0:
            self.__img_index += 1
            if self.__img_index >= len(imgs):
                self.__img_index = 0
            super().set_img(imgs[self.__img_index])

if __name__ == "__main__":
    pass
