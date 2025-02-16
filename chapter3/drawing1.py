import pyxel

WIDTH = 160
HEIGHT = 120

def draw_smileman(x, y, body_color, outline_color, face_color):
  pyxel.circ(x, y, 8, body_color)
  pyxel.circb(x, y, 8, outline_color)
  pyxel.line(x - 4, y - 3, x - 4, y, face_color)
  pyxel.line(x + 2, y - 3, x + 2, y, face_color)
  pyxel.line(x - 4, y + 3, x + 2, y + 3, face_color)
  pyxel.pset(x - 5, y + 2, face_color)
  pyxel.pset(x + 3, y + 2, face_color)

pyxel.init(WIDTH, HEIGHT, title="Pyxel Drawing")

# for i in range(8):
#   x = i * 18 + 17
#   y = i * 10 + 25
#   draw_smileman(x, y, 10, 9, 8)

for i in range(50):
  x = pyxel.rndi(0, WIDTH - 1)
  y = pyxel.rndi(0, HEIGHT - 1)
  body_color = pyxel.rndi(6, 11)
  outline_color = pyxel.rndi(12, 15)
  face_color = pyxel.rndi(0, 5)

  draw_smileman(x, y, body_color, outline_color, face_color)


pyxel.show()