from pygame import *
from os import path

# класс полки
class Shelf(sprite.Sprite):
    SIZE = 25
    COLOR = "#775533"
    SPEED = 1

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        # изображение
        self.move = True
        self.image = Surface((self.SIZE, self.SIZE / 2))
        self.image.fill(Color(self.COLOR))
        self.rect = Rect(x + 1, y, self.SIZE, self.SIZE / 2)

    # обновление
    def update(self, shelfs = None, cat = None):
        if cat.moving:
            self.SPEED = 1
            self.rect.y += self.SPEED
        else:
            self.SPEED = 0