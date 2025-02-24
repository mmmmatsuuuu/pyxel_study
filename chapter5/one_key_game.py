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

  # 宇宙船から一定距離離れた位置をランダムに算出する関数
  def generate_distanced_pos(self, dist):
    while True:
      x = pyxel.rndi(0, pyxel.width - 8)
      y = pyxel.rndi(0, pyxel.height - 8)
      diff_x = x - self.ship_x
      diff_y = y - self.ship_y
      if diff_x ** 2 + diff_y ** 2 > dist ** 2:
        return (x, y)

  # 宇宙飛行士を追加する
  def add_survivor(self):
    survivor_pos = self.generate_distanced_pos(30)
    self.survivors.append(survivor_pos)

  # 隕石を追加する
  def add_meteor(self):
    meteor_pos = self.generate_distanced_pos(60)
    self.meteors.append(meteor_pos)

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

  # オブジェクト（宇宙飛行士・隕石を追加する）
  def add_objects(self):
    if self.timer == 0:
      self.add_survivor()
      self.add_meteor()
      self.timer = OBJECT_SPAWN_INTERVAL
    else:
      self.timer -= 1

  # 宇宙船とオブジェクトの衝突判定
  def check_ship_collision(self, x, y):
    return abs(self.ship_x - x) <= 5 and abs(self.ship_y - y) <= 5

  # 宇宙船と宇宙飛行士の衝突処理
  def handle_survivor_collisions(self):
    new_survivors = []
    for survivor_x, survivor_y in self.survivors:
      if self.check_ship_collision(survivor_x, survivor_y):
        self.score += 1
        pyxel.play(1, 2)
      else:
        new_survivors.append((survivor_x, survivor_y))
      self.survivors = new_survivors
  
  # 宇宙船と隕石の衝突処理
  def handle_meteor_collisions(self):
    for meteor_x, meteor_y in self.meteors:
      if self.check_ship_collision(meteor_x, meteor_y):
        self.is_exploding =True
        self.is_title = True
        pyxel.play(1, 3)

  

  def update(self):
    if self.is_title:
      if pyxel.btnp(pyxel.KEY_RETURN):
        self.is_title = False
        self.reset_game()
      return
    self.update_ship()
    self.add_objects()
    self.handle_survivor_collisions()
    self.handle_meteor_collisions()


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

    pyxel.blt(self.ship_x - self.ship_dir * 3 + offset_x, self.ship_y, 0, 0, 0, 8, 8, 0)

    # 下方向のジェットを描画する
    pyxel.blt(self.ship_x, self.ship_y + 3 + offset_y, 0, 8, 8, 8, 8, 0)

    # 宇宙船を描画する
    pyxel.blt(self.ship_x, self.ship_y, 0, 8, 0, 8, 8, 0)

    # 爆発を描画する
    if self.is_exploding:
      blast_x = self.ship_x + pyxel.rndi(1, 6)
      blast_y = self.ship_y + pyxel.rndi(1, 6)
      blast_radius = pyxel.rndi(2, 4)
      blast_color = pyxel.rndi(7, 10)
      pyxel.circ(blast_x,blast_y, blast_radius, blast_color)

  def draw_survivors(self):
    for survivor_x, survivor_y in self.survivors:
      pyxel.blt(survivor_x, survivor_y, 0, 16, 0, 8, 8, 0)

  def draw_meteors(self):
    for meteor_x, meteor_y in self.meteors:
      pyxel.blt(meteor_x, meteor_y, 0, 24, 0, 8, 8, 0)

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
    self.draw_survivors()
    self.draw_meteors()
    self.draw_score()

    if self.is_title:
      self.draw_title()


OneKeyGame()
