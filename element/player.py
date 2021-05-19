import pygame.image
import pygame.transform
import pygame.sprite

from element.obj import Object, ObjectID
from element import direction
import parameter

import time

# 初始化圖片
up_imgs = []
down_imgs = []
left_imgs = []
right_imgs = []

for i in range(3):
    img = pygame.image.load(f"imgs/player/up_{i}.webp").convert_alpha()
    up_imgs.append(img)
    img = pygame.image.load(f"imgs/player/down_{i}.webp").convert_alpha()
    down_imgs.append(img)
    img = pygame.image.load(f"imgs/player/right_{i}.webp").convert_alpha()
    right_imgs.append(img)
    img = pygame.transform.flip(img, True, False)
    left_imgs.append(img)

imgs = [up_imgs, down_imgs, left_imgs, right_imgs]


class Player(Object):
    def __init__(self, x, y, skin: int):
        super().__init__()
        self.__ammo = parameter.INIT_BULLET_NUM
        self.__isdead = False
        self.__skin = skin
        self.__cooldown = time.time()
        self.set_dir(direction.DOWN)

        self.set_img(self.__img())
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def set_dir(self, direction):
        self.__dir = direction
        self.set_img(self.__img())

    def direction(self):
        return self.__dir

    def isdead(self):
        return self.__isdead

    def Set_Dead(self):
        self.__isdead = True   

    def is_won(self, all_objects: dict) -> bool:
        for goal in all_objects[ObjectID.GOAL]:
            if not pygame.sprite.spritecollide(goal, all_objects[ObjectID.BOX], dokill=False):
                return False
        return True

    # 增加子彈
    def add_ammo(self, delta):
        self.__ammo += delta

    # 攻擊，回傳是否成功（有沒有子彈）
    def shoot(self) -> bool:
        if self.__ammo <= 0:
            return False
        now = time.time()
        if now - self.__cooldown > parameter.BULLET_COOLDOWN:
            self.__cooldown = now
            self.__ammo -= 1
            return True
        return False

    # 當前擁有子彈數
    def ammos(self) -> int:
        return self.__ammo

    def draw(self, screen):
        screen.blit(self.img(), self.rect)

    def move(self, delta_x: int, delta_y: int, all_objects: dict) -> bool:
        super().move(delta_x, delta_y)
        if self.__is_collide(delta_x, delta_y, all_objects):
            super().move(-delta_x, -delta_y)
            return False
        return True

    def __is_collide(self, delta_x: int, delta_y: int, all_objects: dict) -> bool:
        collided_boxes = pygame.sprite.spritecollide(self, all_objects[ObjectID.BOX], dokill=False)
        for box in collided_boxes:
            box_moved = box.move(delta_x, delta_y, all_objects)
            if not box_moved:
                return True
        collided = pygame.sprite.spritecollide(self, all_objects[ObjectID.WALL], dokill=False)
        if collided:
            return True
        collided = pygame.sprite.spritecollide(self, all_objects[ObjectID.BORDER], dokill=False)
        if collided:
            return True
        collided = pygame.sprite.spritecollide(self, all_objects[ObjectID.GUARD], dokill=False)
        if collided:
            self.Set_Dead()
            return True
        return False

    def __img(self):
        return imgs[self.__dir][self.__skin]


if __name__ == "__main__":
    p = Player(1, 1, 2)
    print(p.img())
    # print(p.__ammo)
