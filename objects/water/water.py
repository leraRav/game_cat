from pygame import *
from pyganim import *
from os import path

# класс воды
class Water(sprite.Sprite):
    SIZE = 32
    COLOR = "#33FF33"
    DIR = path.dirname(__file__)

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        # изображение
        self.move = False
        self.image = Surface((self.SIZE, self.SIZE))
        self.image.fill(self.COLOR)
        self.image.set_colorkey(self.COLOR)
        self.rect = Rect(x, y, self.SIZE, self.SIZE / 2)

        # анимация
        delay = 200
        animation = [
            (f"{self.DIR}\\tile000.png", delay),
            (f"{self.DIR}\\tile001.png", delay),
            (f"{self.DIR}\\tile002.png", delay),
        ]
        self.animation= PygAnimation(animation)
        self.animation.play()
        self.animation.blit(self.image, (0, 0))

    # обновление
    def update(self):
        # перерисовка анимации
        self.image.fill(self.COLOR)
        self.animation.blit(self.image, (0, 0))