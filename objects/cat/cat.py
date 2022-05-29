from pygame import *
from pyganim import *
from typing import List
import time as TIME
from os import path

# класс кота
class Cat(sprite.Sprite):
    GRAVITY = 0.3
    SPEED = 3
    JUMP = 7
    COLOR = "#333333"
    DIR = path.dirname(__file__)

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        # скорость
        self.move_x = 0
        self.move_y = 0
        # движение
        self.move_up = False
        self.move_left = False
        self.move_right = False

        # движение платформ
        self.moving = False

        self.on_shelf = False

        self.fish = 0
        self.start_time = 0
        self.elapsed_time = 0

        size = 32
        # изображение
        self.rect = Rect(x + 4, y, size - 8, size)
        self.image = Surface((size, size))
        self.image.fill(self.COLOR)
        self.image.set_colorkey(self.COLOR)

        # анимация бездействия
        delay = 150
        animation = [
            (f"{self.DIR}\\anim\\stay\\tile000.png", delay),
            (f"{self.DIR}\\anim\\stay\\tile001.png", delay),
            (f"{self.DIR}\\anim\\stay\\tile002.png", delay),
            (f"{self.DIR}\\anim\\stay\\tile003.png", delay),
        ]
        self.animation= PygAnimation(animation)
        self.animation.play()
        self.animation.blit(self.image, (0, 0))

        # анимация бега
        delay = 100
        animation = [
            (f"{self.DIR}\\anim\\run\\tile000.png", delay),
            (f"{self.DIR}\\anim\\run\\tile001.png", delay),
            (f"{self.DIR}\\anim\\run\\tile002.png", delay),
            (f"{self.DIR}\\anim\\run\\tile003.png", delay),
            (f"{self.DIR}\\anim\\run\\tile004.png", delay),
            (f"{self.DIR}\\anim\\run\\tile005.png", delay),
            (f"{self.DIR}\\anim\\run\\tile006.png", delay),
            (f"{self.DIR}\\anim\\run\\tile007.png", delay),
        ]
        self.animationRunRight= PygAnimation(animation)
        self.animationRunRight.play()

        self.animationRunLeft= PygAnimation(animation)
        self.animationRunLeft.flip(True, False)
        self.animationRunLeft.play()

        # анимация прыжка
        delay = 100
        animation = [
            (f"{self.DIR}\\anim\\jump\\tile000.png", delay),
            (f"{self.DIR}\\anim\\jump\\tile001.png", delay),
            (f"{self.DIR}\\anim\\jump\\tile002.png", delay),
            (f"{self.DIR}\\anim\\jump\\tile003.png", delay),
            (f"{self.DIR}\\anim\\jump\\tile004.png", delay),
            (f"{self.DIR}\\anim\\jump\\tile005.png", delay),
        ]
        self.animationJumpRight= PygAnimation(animation)
        self.animationJumpRight.play()

        self.animationJumpLeft= PygAnimation(animation)
        self.animationJumpLeft.flip(True, False)
        self.animationJumpLeft.play()

    # обновление
    def update(self, shelfs, cat = None):
        self.rect.y += shelfs[0].SPEED

        # если платформы двигаются
        if self.moving:
            # считаем время
            self.elapsed_time = TIME.time() - self.start_time
        
        # если стрелка вверх
        if self.move_up: 
            if not self.moving:
                self.moving = True
                self.start_time = TIME.time()
            # если игрок на земле
            if self.on_shelf:
                # прыгнуть
                self.move_y = -self.JUMP
            # обновить анимацию
            self.image.fill(self.COLOR) 
            if self.move_x >= 0:
                self.animationJumpRight.blit(self.image, (0, 0))
            else:
                self.animationJumpLeft.blit(self.image, (0, 0))

        # если нажата влево
        if self.move_left:
            # переместить влево
            self.move_x = -self.SPEED 
            # если не вверх
            if not self.move_up: 
                # обновить анимацию 
                self.image.fill(self.COLOR)
                self.animationRunLeft.blit(self.image, (0, 0))
        
        # если нажата стрелка вправо
        if self.move_right:
            # переместить вправо
            self.move_x = self.SPEED 
            # если не вверх
            if not self.move_up: 
                # обновить анимацию 
                self.image.fill(self.COLOR)
                self.animationRunRight.blit(self.image, (0, 0))

        # если стрелки не нажаты 
        if not (self.move_left or self.move_right):
            # не двигаться
            self.move_x = 0
            # если не стрелка вверх и не двигаемся
            if not self.move_up and self.move_y == 0: 
                # обновить анимацию 
                self.image.fill(self.COLOR)
                self.animation.blit(self.image, (0, 0))
        
        # если не на земле
        if not self.on_shelf:
            # увеличить гравитацию
            self.move_y += self.GRAVITY 

        # переместить игрока
        self.on_shelf = False
        self.rect.y += self.move_y
        self.collide(0, self.move_y, shelfs)
        self.rect.x += self.move_x
        self.collide(self.move_x, 0, shelfs)

    # функция проверки на столкновение с платформами
    def collide(self, move_x, move_y, shelfs):
        # цикл по платформам
        for s in shelfs:
            # если столкнулись
            if sprite.collide_rect(self, s) and s.alive():
                # обновление перемещения игрока
                if move_x > 0:
                    self.rect.right = s.rect.left
                if move_x < 0:
                    self.rect.left = s.rect.right
                if move_y > 0:
                    self.on_shelf = True
                    self.rect.bottom = s.rect.top
                    self.move_y = 0
                if move_y < 0:
                    self.rect.top = s.rect.bottom
                    self.move_y = 0