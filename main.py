import pygame
import time

pygame.init()  # 初始化pygame
pygame.font.init()
width, height = 1600, 800  # 設定視窗大小
screen = pygame.display.set_mode((width, height))

import element
import maps

# bg_r = pygame.transform.scale(bg_r, (img_width, img_height))


class Game():

    def __init__(self, level, mask_enabled=True):
        self.screen = screen
        self.ticker = pygame.time.Clock()
        self.background = (230, 230, 200)  # 背景顏色
        self.level = level
        self.map_ = maps.get_map(level)
        self.build_world()
        self.key_cooldown = time.time()

        self.display_font = pygame.font.SysFont("default", 32)

        self.mask_enabled = mask_enabled
        if self.mask_enabled:
            player_x, player_y = self.player.pos()
            self.mask = element.Mask(player_x, player_y)

    def run_game(self):
        in_game = True
        while in_game:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    in_game = False

            self.screen.fill(self.background)
            self.update_world()
            self.draw_world()
            self.screen.blit(self.player.img(), self.player.pos())

            text = " fps: {:.03f}".format(self.ticker.get_fps())
            text = self.display_font.render(text, False, (0, 0, 0))
            self.screen.blit(text, (1440, 740))

            text = " objects: {}".format(len(self.world))
            text = self.display_font.render(text, False, (0, 0, 0))
            self.screen.blit(text, (1440, 770))

            pygame.display.update()
            self.ticker.tick(60)  # 60 fps

            self.key_handle()

        pygame.quit()

    # 按鍵輸入處理
    def key_handle(self):
        keys = pygame.key.get_pressed()

        # player movement
        if keys[pygame.K_UP]:
            self.player.move(0, -element.consts.PLAYER_VELOCITY, self.world)
            self.player.set_dir(element.direction.UP)
        elif keys[pygame.K_DOWN]:
            self.player.move(0, element.consts.PLAYER_VELOCITY, self.world)
            self.player.set_dir(element.direction.DOWN)
        elif keys[pygame.K_LEFT]:
            self.player.move(-element.consts.PLAYER_VELOCITY, 0, self.world)
            self.player.set_dir(element.direction.LEFT)
        elif keys[pygame.K_RIGHT]:
            self.player.move(element.consts.PLAYER_VELOCITY, 0, self.world)
            self.player.set_dir(element.direction.RIGHT)

        # game restart
        if keys[pygame.K_r]:
            now = time.time()
            if now - self.key_cooldown > element.consts.KEY_COOLDOWN:
                self.restart()
                self.key_cooldown = now

        # game pause
        # todo
        if keys[pygame.K_ESCAPE]:
            pass

        # player attack
        if keys[pygame.K_SPACE]:
            if self.player.shoot():
                player_x, player_y = self.player.pos()
                player_dir = self.player.direction()
                self.world.append(element.Bullet(player_x, player_y, player_dir))

    # 建構地圖
    def build_world(self):
        self.world = []

        x, y = 0, 0
        for i, v in enumerate(self.map_):
            if v == "\n":
                y += 40
                x = 0
            elif v == "H":
                self.world.append(element.Border(x, y))
            elif v == "#":
                self.world.append(element.Wall(x, y))
            elif v == ".":
                self.world.append(element.Goal(x, y))
            elif v == "$":
                self.world.append(element.Box(x, y))
            elif v == "%":
                self.world.append(element.Goal(x, y))
                self.world.append(element.Box(x, y))
            elif v == "!":
                self.world.append(element.Guard(x, y))
            elif v == "@":
                self.player = element.Player(x, y, 0)
                self.world.append(self.player)
            x += 40

    # 遊戲邏輯處理，更新遊戲狀態
    def update_world(self):
        for item in self.world:
            # 子彈位置更新
            if isinstance(item, element.Bullet):
                item.update(self.world)
            elif isinstance(item, element.Guard):
                item.update(self.world)

    # 畫在螢幕上
    def draw_world(self):
        for obj in self.world:
            self.screen.blit(obj.img(), obj.pos())
        
        if self.mask_enabled:
            player_x, player_y = self.player.pos()
            self.screen.blit(self.mask.img(), (player_x-self.mask.offset_x, player_y-self.mask.offset_y))

    def restart(self):
        self.build_world()


if __name__ == "__main__":
    # debugging now, mask_enabled should be True
    game = Game(level=9, mask_enabled=False)
    game.run_game()
