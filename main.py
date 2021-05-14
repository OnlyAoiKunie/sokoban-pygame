import pygame
import time

pygame.init()  # 初始化pygame
pygame.font.init()

import parameter

# 設定視窗大小
screen = pygame.display.set_mode((parameter.WIN_WIDTH, parameter.WIN_HEIGHT))

import element
from element.obj import ObjectID
import maps
import frame


class Game():
    """
    level 表示第幾關
    mask 是用來增加遊戲難度的物件，mask_enabled決定mask是否啟用，
    debug時不啟用mask
    """
    def __init__(self, level, mask_enabled=True):
        self.screen = screen
        self.ticker = pygame.time.Clock()
        self.background = (230, 230, 200)  # 背景顏色
        self.level = level
        self.map_ = maps.get_map(level)
        self.build_world()
        self.key_cooldown = time.time()
        self.game_pause = frame.pause.Pause() # pause frame
        self.STW = False # stop the world (pause)

        self.display_font = pygame.font.SysFont("default", 32)

        self.mask_enabled = mask_enabled
        if self.mask_enabled:
            player_x, player_y = self.player.pos()
            self.mask = element.Mask(player_x, player_y)

    def run_game(self):
        in_game = True
        while in_game:
            # 基礎事件
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    in_game = False
            
            if self.STW:
                # 背景色
                self.screen.fill(self.background)
                selection = self.game_pause.update(self.screen)
                if selection == frame.pause.RESUME:
                    self.STW = False
                elif selection == frame.pause.RESTART:
                    self.restart()
                    self.STW = False
                elif selection == frame.pause.EXIT:
                    in_game = False
            else:
                self.update_world()
                self.key_handle()
                self.draw_world()

            # debug用資訊
            text = " fps: {:.1f}".format(self.ticker.get_fps())
            text = self.display_font.render(text, False, (0, 0, 0))
            self.screen.blit(text, (1440, 740))

            # debug用資訊
            objects = 0
            for _, v in self.all_objects.items():
                try:
                    objects += len(v)
                except Exception:
                    pass
            text = " objects: {}".format(objects)
            text = self.display_font.render(text, False, (0, 0, 0))
            self.screen.blit(text, (1440, 770))

            pygame.display.update()
            self.ticker.tick(60)  # 60 fps

        pygame.quit()

    def gameover(self):
        print("game over")
        
    # 按鍵輸入處理
    def key_handle(self):
        keys = pygame.key.get_pressed()

        # player movement
        if keys[pygame.K_UP]:
            self.player.move(0, -parameter.PLAYER_VELOCITY, self.all_objects)
            self.player.set_dir(element.direction.UP)
        elif keys[pygame.K_DOWN]:
            self.player.move(0, parameter.PLAYER_VELOCITY, self.all_objects)
            self.player.set_dir(element.direction.DOWN)
        elif keys[pygame.K_LEFT]:
            self.player.move(-parameter.PLAYER_VELOCITY, 0, self.all_objects)
            self.player.set_dir(element.direction.LEFT)
        elif keys[pygame.K_RIGHT]:
            self.player.move(parameter.PLAYER_VELOCITY, 0, self.all_objects)
            self.player.set_dir(element.direction.RIGHT)

        # player attack
        if keys[pygame.K_SPACE]:
            if self.player.shoot():
                player_x, player_y = self.player.pos()
                player_dir = self.player.direction()
                self.bullets.add(element.Bullet(player_x, player_y, player_dir))

        # game pause
        if keys[pygame.K_ESCAPE]:
            self.STW = True

    # 建構地圖
    def build_world(self):
        self.borders = pygame.sprite.Group()
        self.boxes = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.guards = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        x, y = 0, 0
        for i, v in enumerate(self.map_):
            if v == "\n": # 換行
                y += 40
                x = 0
            elif v == "H": # 邊界
                self.borders.add(element.Border(x, y))
            elif v == "#": # 牆
                self.walls.add(element.Wall(x, y))
            elif v == ".": # 終點
                self.goals.add(element.Goal(x, y))
            elif v == "$": # 箱子
                self.boxes.add(element.Box(x, y))
            elif v == "%": # 終點上有箱子
                self.goals.add(element.Goal(x, y))
                self.boxes.add(element.Box(x, y))
            elif v == "!": # 警衛
                self.guards.add(element.Guard(x, y))
            elif v == "P":
                self.portals.add(element.Portal(x, y))
            elif v == "@": # 玩家（初始）位置
                self.player = element.Player(x, y, 0)
            elif v == " ":
                pass
            else:
                raise maps.UnknowIdentifierError(f"unknow idetifier {v} in map {self.level}")
            x += 40

        # dict
        self.all_objects = {
            element.ObjectID.BORDER: self.borders,
            element.ObjectID.BOX: self.boxes,
            element.ObjectID.BULLET: self.bullets,
            element.ObjectID.GOAL: self.goals,
            element.ObjectID.GUARD: self.guards,
            element.ObjectID.PORTAL: self.portals,
            element.ObjectID.WALL: self.walls,
            element.ObjectID.PLAYER: self.player,
        }

    # 遊戲邏輯處理，更新遊戲狀態
    def update_world(self):
        self.bullets.update(self.all_objects)
        self.guards.update(self.all_objects)
        self.portals.update()

        if self.mask_enabled:
            self.mask.update(self.player)

        #玩家死亡
        if self.player.isdead() == True:
            self.gameover()


    # 畫在螢幕上
    def draw_world(self):
        # 背景色
        self.screen.fill(self.background)
        
        self.borders.draw(self.screen)
        self.walls.draw(self.screen)
        self.goals.draw(self.screen)
        self.guards.draw(self.screen)
        self.portals.draw(self.screen)
        self.boxes.draw(self.screen)
        self.bullets.draw(self.screen)
        self.player.draw(self.screen)
        
        # 如果mask啟用，畫在player身邊
        if self.mask_enabled:
            self.mask.draw(self.screen)

    def restart(self):
        self.build_world()


if __name__ == "__main__":
    # debugging now, mask_enabled should be True
    game = Game(level=9, mask_enabled=False)
    game.run_game()
