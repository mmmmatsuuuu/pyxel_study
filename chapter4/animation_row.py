import pyxel

def draw_rabbit(x, y, color):
  pyxel.line(x + 2, y, x + 2, y + 2, color)
  pyxel.line(x + 4, y, x + 4, y + 4, color)
  pyxel.rect(x + 2, y + 3, 4, 3, color)
  pyxel.rect(x + 1, y + 6, 4, 3, color)
  pyxel.line(x, y + 9, x + 2, y + 9, color)
  pyxel.line(x + 4, y + 9, x + 5, y + 9, color)
  pyxel.pset(x + 3, y + 4, 8)
  pyxel.pset(x + 5, y + 4, 8)

pyxel.init(80, 60, title="Pyxel Animation")

rabbit_x = 0

while True:
  pyxel.cls(1)
  draw_rabbit(rabbit_x, 25, 15)
  pyxel.flip()
  rabbit_x += 1

  if rabbit_x >= pyxel.width:
    rabbit_x = -6

