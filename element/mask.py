from pygame import image
from element import consts

img = image.load("imgs/mask.webp").convert_alpha()


class Mask:
    def __init__(self, x, y):
        self.__x, self.__y = x, y
        self.__img = img
        self.img_size = (3840, 2160)
        self.offset_x = (3840-consts.IMG_SIZE) // 2
        self.offset_y = (2160-consts.IMG_SIZE) // 2

    def set_pos(self, x, y):
        self.__x, self.__y = x, y

    def pos(self):
        return self.__x, self.__y

    def img(self):
        return self.__img

if __name__ == "__main__":
    pass