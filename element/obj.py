# 物件原形
class Object:
    def __init__(self, x, y):
        self.__x, self.__y = x, y
        
    def move(self, delta_x, delta_y):
        self.__x += delta_x
        self.__y += delta_y

    def set_pos(self, x , y):
        self.__x, self.__y = x, y

    def pos(self):
        return self.__x, self.__y

    def name(self):
        return self.__class__

    def img(self):
        return self.__img

    def set_img(self, img):
        self.__img = img


if __name__ == "__main__":
    o = Object(1, 1)
    print(o.name())
