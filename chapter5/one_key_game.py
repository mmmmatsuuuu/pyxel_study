import pyxel

GAME_TITLE = "Space Rescure"
SHIP_ACCEL_X = 0.06
SHIP_ACCEL_UP = 0.04
SHIP_ACCEL_DOWN = 0.02
MAX_SHIP_SPEED = 0.8
OBJECT_SPAWN_INTERVAL = 150


class OneKeyGame():

  def __init__(self):
    pyxel.init(160, 120, title=GAME_TITLE)

    pyxel.load("space_rescue.pyxres")

    self.is_title = True
    self.reset_game()

    pyxel.run(self.update, self.draw)

  def reset_game(self):
    self.score = 0
    self.timer = 0

    # 宇宙船を初期化
    self.ship_x = (pyxel.width - 8) / 2
    self.ship_y = pyxel.height / 4
    self.ship_vx = 0
    self.ship_vy = 1
    self.ship_dir = 1  # 宇宙船の向き
    self.is_jetting = False  # ジェット噴射中かどうか
    self.is_exploding = False  # 爆発中かどうか

    # マップの配置を初期化
    self.survivors = []  # 宇宙飛行士の配置
    self.meteors = []  # 隕石の配置

  def update_ship(self):
    # 宇宙船の速度を更新する
    if pyxel.btn(pyxel.KEY_SPACE):
      self.is_jetting = True
      self.ship_vy = max(self.ship_vy - SHIP_ACCEL_UP, -MAX_SHIP_SPEED)
      self.ship_vx = max(
          min(self.ship_vx + self.ship_dir * SHIP_ACCEL_X, 1),
          -MAX_SHIP_SPEED,
      )
      pyxel.play(0, 0)
    else:
      self.is_jetting = False
      self.ship_vy = min(self.ship_vy + SHIP_ACCEL_DOWN, MAX_SHIP_SPEED)

    # スペースキーが離された時に次に進む方向を逆にする
    if pyxel.btnr(pyxel.KEY_SPACE):
      self.ship_dir = -self.ship_dir

    # 宇宙船の位置を更新する
    self.ship_x += self.ship_vx
    self.ship_y += self.ship_vy

    # 画面端に到達したら跳ね返す
    if self.ship_x < 0:
      self.ship_x = 0
      self.ship_vx = abs(self.ship_vx)
      pyxel.play(0, 1)

    max_ship_x = pyxel.width - 8

    if self.ship_x > max_ship_x:
      self.ship_x = max_ship_x
      self.ship_vx = -abs(self.ship_vx)
      pyxel.play(0, 1)

    if self.ship_y < 0:
      self.ship_y = 0
      self.ship_vy = abs(self.ship_vy)
      pyxel.play(0, 1)

    max_ship_y = pyxel.height - 8

    if self.ship_y > max_ship_y:
      self.ship_y = max_ship_y
      self.ship_vy = -abs(self.ship_vy)
      pyxel.play(0, 1)

  def update(self):
    if self.is_title:
      if pyxel.btnp(pyxel.KEY_RETURN):
        self.is_title = False
        self.reset_game()
      return
    self.update_ship()

  def draw_sky(self):
    num_grads = 4
    grad_height = 6
    grad_start_y = pyxel.height - grad_height * num_grads

    pyxel.cls(0)
    for i in range(num_grads):
      pyxel.dither((i + 1) / num_grads)
      pyxel.rect(
          0,
          grad_start_y + i * grad_height,
          pyxel.width,
          grad_height,
          1,
      )
    pyxel.dither(1)

  def draw_ship(self):
    # ジェット噴射の表示位置をずらす量を計算する
    offset_y = (pyxel.frame_count % 3 + 2) if self.is_jetting else 0
    offset_x = offset_y * -self.ship_dir

    # 左右方向のジェットを描画する
    pyxel.blt(
        self.ship_x - self.ship_dir * 3 + offset_x,
        self.ship_y,
        0,
        0,
        0,
        8,
        8,
        0,
    )

    # 下方向のジェットを描画する
    pyxel.blt(
        self.ship_x,
        self.ship_y + 3 + offset_y,
        0,
        8,
        8,
        8,
        8,
        0,
    )

    # 宇宙船を描画する
    pyxel.blt(self.ship_x, self.ship_y, 0, 8, 0, 8, 8, 0)

  def draw_score(self):
    score = f"SCORE:{self.score:04}"
    for i in range(1, -1, -1):
      color = 7 if i == 0 else 0
      pyxel.text(3 + i, 3, score, color)

  def draw_title(self):
    for i in range(1, -1, -1):
      color = 10 if i == 0 else 8
      pyxel.text(57, 50 + i, GAME_TITLE, color)

  def draw(self):
    self.draw_sky()
    self.draw_ship()
    self.draw_score()

    if self.is_title:
      self.draw_title()


OneKeyGame()
