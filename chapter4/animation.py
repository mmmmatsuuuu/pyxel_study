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



class App:
    def __init__(self):
        pyxel.init(80, 60, title="Pyxel Animation")
        self.NUM_RABBITS = 5
        self.RABBIT_HEIGHT = 10
        self.RABBIT_BOUNCY_Y = pyxel.height - self.RABBIT_HEIGHT
        self.rabbit_xs     = [7, 22, 37, 52, 67]
        self.rabbit_ys     = [18, 15, 12, 9, 6]
        self.rabbit_vys    = [0] * self.NUM_RABBITS
        self.rabbit_colors = [6, 5, 4, 3, 2]
        pyxel.run(self.update, self.draw)

    def update(self):
        for i in range(self.NUM_RABBITS):
            self.rabbit_ys[i] += self.rabbit_vys[i]
            self.rabbit_vys[i] += 0.1

            if self.rabbit_ys[i] >= self.RABBIT_BOUNCY_Y:
                self.rabbit_ys[i] = self.RABBIT_BOUNCY_Y
                self.rabbit_vys[i] *= -0.95
        
        

    def draw(self):
        pyxel.cls(1)
        pyxel.text(1, 0, f"{self.rabbit_ys[0]: 3.3f}", 0)
        pyxel.text(0, 0, f"{self.rabbit_ys[0]: 3.3f}", 7)
        pyxel.text(1, 8, f"{self.rabbit_vys[0]: 3.3f}", 0)
        pyxel.text(0, 8, f"{self.rabbit_vys[0]: 3.3f}", 7)
        for i in range(self.NUM_RABBITS):
            draw_rabbit(self.rabbit_xs[i], self.rabbit_ys[i], self.rabbit_colors[i])

App()