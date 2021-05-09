
# 畫面
WIN_WIDTH, WIN_HEIGHT = 1600, 800

# 圖片
IMG_SIZE = 40  # pixel
GAP = IMG_SIZE - 4  # pixel

# 箱子
BOX_SIZE = 24  # 箱子圖片大小
BOX_GAP = 24  # 箱子碰撞偵測距離
BOX_OFFSET = (IMG_SIZE - BOX_SIZE) // 2  # 箱子顯示的偏移量

# 物體移動速度
BULLET_VELOCITY = 10  # pixel
PLAYER_VELOCITY = 4  # pixel
GUARD_VELOCITY = 4

# 避免按鍵重複觸發的冷卻時間
BULLET_COOLDOWN = 0.2  # sec
KEY_COOLDOWN = 0.5
PAUSE_KEY_COOLDOWN = 0.1
