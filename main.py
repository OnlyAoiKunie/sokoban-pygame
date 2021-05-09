import pygame
import time

import element
import maps

# bg_r = pygame.transform.scale(bg_r, (img_width, img_height))


class Game():

    def __init__(self, level):
        pygame.init()  # 初始化pygame
        width, height = 1400, 800  # 設定視窗大小
        self.game_display = pygame.display.set_mode((width, height))
        self.ticker = pygame.time.Clock()
        self.background = (230, 230, 200)  # 背景顏色
        self.level = level
        self.map_ = maps.get_map(level)
        self.build_world()
        self.key_cooldown = time.time()

    def run_game(self):
        in_game = True
        while in_game:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    in_game = False

            self.game_display.fill(self.background)
            self.update_world()
            self.draw_world()
            self.game_display.blit(self.player.img(), self.player.pos())

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
                self.world.append(element.Bullet(
                    player_x, player_y, player_dir))

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
            self.game_display.blit(obj.img(), obj.pos())

    def restart(self):
        self.build_world()


if __name__ == "__main__":
    game = Game(9)
    game.run_game()
