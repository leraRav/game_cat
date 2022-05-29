from pygame import *
from pyganim import *
from os import path

# класс рыбки
class Fish(sprite.Sprite):
    SIZE = 16
    COLOR = "#00FF00"
    DIR = path.dirname(__file__)

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        # изображение
        self.image = Surface((self.SIZE, self.SIZE))
        self.image.fill(self.COLOR)
        self.image.set_colorkey(self.COLOR)
        self.rect = Rect(x + self.SIZE / 2, y + self.SIZE / 2, self.SIZE, self.SIZE)
        
        # анимация
        delay = 400
        animation = [
            (f"{self.DIR}\\tile000.png", delay),
            (f"{self.DIR}\\tile001.png", delay),
        ]
        self.animation= PygAnimation(animation)
        self.animation.play()
        self.animation.blit(self.image, (0, 0))

    # функция обновления
    def update(self, shelfs = None, cat = None):
        # обновить анимацию
        if cat.moving:
            self.rect.y += 1
        self.image.fill(self.COLOR)
        self.animation.blit(self.image, (0, 0))
        # проверить на столкновение
        self.collide(cat)

    # функция проверки столкновения с игроком
    def collide(self, cat):
        # если столкновение с игроком
        if sprite.collide_rect(self, cat):
            # если рыба существует
            if self.alive():
                # убрать рыбу
                self.kill()
                # добавить рыбу коту
                cat.fish += 1
