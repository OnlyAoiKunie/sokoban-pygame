import pygame
import element

# bg_r = pygame.transform.scale(bg_r, (img_width, img_height))

def main(map_):
    pygame.init()  # 初始化pygame
    width, height = 1400, 800  # 設定視窗大小

    game_display = pygame.display.set_mode((width,height))
    ticker = pygame.time.Clock()
    background = (230, 230, 200) # 背景顏色

    world, player = build_map(map_)

    in_game = True
    while in_game:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                in_game = False

        game_display.fill(background)
        draw_world(world, game_display)
        game_display.blit(player.img(), player.pos())

        pygame.display.update()
        ticker.tick(60) # 60 fps

        # 按鍵輸入處理
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move(0, -element.consts.PLAYER_VELOCITY, world)
            player.set_dir(element.direction.UP)
        elif keys[pygame.K_DOWN]:
            player.move(0, element.consts.PLAYER_VELOCITY, world)
            player.set_dir(element.direction.DOWN)
        elif keys[pygame.K_LEFT]:
            player.move(-element.consts.PLAYER_VELOCITY, 0, world)
            player.set_dir(element.direction.LEFT)
        elif keys[pygame.K_RIGHT]:
            player.move(element.consts.PLAYER_VELOCITY, 0, world)
            player.set_dir(element.direction.RIGHT)

    pygame.quit()

# 建構地圖
def build_map(map_: str):
    world = []

    x, y = 0, 0
    for i, v in enumerate(map_):
        if v == "\n":
            y += 40
            x = 0
        elif v == "H":
            world.append(element.Border(x, y))
        elif v == "#":
            world.append(element.Wall(x, y))
        elif v == ".":
            world.append(element.Goal(x, y))
        elif v == "$":
            world.append(element.Box(x, y))
        elif v == "%":
            world.append(element.Goal(x, y))
            world.append(element.Box(x, y))
        elif v == "!":
            world.append(element.Police(x, y))
        elif v == "@":
            temp = element.Player(x, y, 0)
            world.append(temp)
        x += 40

    return world, temp

# 畫在螢幕
def draw_world(world, game_display):
    for obj in world:
        game_display.blit(obj.img(), obj.pos())

if __name__ == "__main__":
    import maps
    main(maps.get_map(2))