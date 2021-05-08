from element.obj import Object
from element.box import Box
from element.goal import Goal
from pygame import image, transform
from element import consts
from element import direction

up_imgs = []
down_imgs = []
left_imgs = []
right_imgs = []

for i in range(3):
    img = image.load("imgs/player/up_" + str(i) + ".png")
    up_imgs.append(img)
    img = image.load("imgs/player/down_" + str(i) + ".png")
    down_imgs.append(img)
    img = image.load("imgs/player/right_" + str(i) + ".png")
    right_imgs.append(img)
    img = transform.flip(img, True, False)
    left_imgs.append(img)

imgs = [up_imgs, down_imgs, left_imgs, right_imgs]

class Player(Object):
    def __init__(self, x, y, skin: int):
        super().__init__(x, y)
        self.__ammo = 3
        self.__skin = skin
        self.__dir = direction.DOWN
        super().set_img(self.__img())

    def set_dir(self, direction):
        self.__dir = direction
        super().set_img(self.__img())

    def add_ammo(self, delta):
        self.__ammo += delta

    def ammos(self):
        return self.__ammo

    def move(self, delta_x, delta_y, world):
        super().move(delta_x, delta_y)
        if self.is_collide(world, delta_x, delta_y):
            super().move(-delta_x, -delta_y)

    def is_collide(self, world, delta_x, delta_y):
        player_x, player_y = super().pos()
        for item in world:
            item_x, item_y = item.pos()
            if isinstance(item, Player) or isinstance(item, Goal):
                continue
            if abs(item_x - player_x) < consts.GAP and abs(item_y - player_y) < consts.GAP:
                # 碰撞到的是箱子的情況
                if isinstance(item, Box):
                    prev_pos = item.pos()
                    item.move(delta_x, delta_y, world)
                    return prev_pos == item.pos() # 如果箱子位置沒變，則箱子已經碰撞其他object
                return True
        return False

    def __img(self):
        return imgs[self.__dir][self.__skin]

if __name__ == "__main__":
    p = Player(1, 1, 2)
    print(p.img())
    # print(p.__ammo)
