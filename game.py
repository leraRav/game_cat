from pygame import *
from os import path
from random import randint
from typing import List

from objects.cat.cat import Cat
from objects.fish.fish import Fish
from objects.shelf.shelf import Shelf
from objects.water.water import Water

# класс рекорда
class Record:
    def __init__(self, time, fish):
        self.time = time
        self.fish = fish

FILE = path.dirname(__file__)
WIN_WIDTH = 384
WIN_HEIGHT = 680
WIN_SIZE = (WIN_WIDTH, WIN_HEIGHT)
WIN_NAME = "Кот-попрыгушка"

FONT_COLOR = "#202020"
FONT_SHADOW_COLOR = "#f8f8f8"

# вывод текста
font_name = font.match_font("Consolas")
def create_text(win: Surface, text, size, x, y, center = False):
    f = font.Font(font_name, size)
    text_shadow = f.render(text, True, FONT_SHADOW_COLOR)
    if center:
        x -= text_shadow.get_rect().width / 2
    text_shadow_rect = text_shadow.get_rect()
    text_shadow_rect.topleft = (x - 1, y - 1)
    text = f.render(text, True, FONT_COLOR)
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    win.blit(text_shadow, text_shadow_rect)
    win.blit(text, text_rect)

def init_game(shelfs: list, water: sprite.Group, objects: sprite.Group):
    for i in range(12):
        shelf = Shelf(i * 32, WIN_HEIGHT - 32 * 3)
        shelfs.append(shelf)
        objects.add(shelf)

    for i in reversed(range(0, 500, 2)):
        for _ in range(randint(4, 7)):
            x = randint(0, 12) * 32
            y = WIN_HEIGHT - 32 * i - 5 * 32
            shelf = Shelf(x, y)
            if randint(1, 4) == 1:
                objects.add(Fish(x, y - 32))
            shelfs.append(shelf)
            objects.add(shelf)

    for i in range(12):
        water.add(Water(32 * i, WIN_HEIGHT - 32))

def main():
    init()
    win = display.set_mode(WIN_SIZE)
    win.fill("white")

    timer = time.Clock()
    objects = sprite.Group()
    water = sprite.Group()
    shelfs = []
    records = []

    cat = Cat(100, WIN_HEIGHT - 32 * 4)
    objects.add(cat)

    init_game(shelfs, water, objects)

    while True:
        timer.tick(60)

        for e in event.get():
            if e.type == QUIT:
                raise exit()
            elif cat.alive():
                if e.type == KEYDOWN and e.key == K_UP:
                    cat.move_up = True
                elif e.type == KEYDOWN and e.key == K_LEFT:
                    cat.move_left = True
                elif e.type == KEYDOWN and e.key == K_RIGHT:
                    cat.move_right = True
                elif e.type == KEYUP and e.key == K_UP:
                    cat.move_up = False
                elif e.type == KEYUP and e.key == K_RIGHT:
                    cat.move_right = False
                elif e.type == KEYUP and e.key == K_LEFT:
                    cat.move_left = False
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                records.clear()
                cat = Cat(100, WIN_HEIGHT - 32 * 4)
                objects.add(cat)
                init_game(shelfs, water, objects)


        win.fill("pink")
        # цикл по игровым объектам
        for o in objects:
            # отрисовка объектов
            win.blit(o.image, o)
            # если кот жив и упал в воду
            if cat.rect.top > win.get_rect().bottom - 32 and cat.alive():
                # убить кота и удалить объекты
                cat.kill()
                cat.moving = False
                objects = sprite.Group()
                water = sprite.Group()
                shelfs = []

                try:
                    # прочитать рекорды из файла
                    with open("records") as f:
                        for r in f:
                            records.append(Record(
                                float(r.split()[0]),
                                int(r.split()[1])
                            ))
                        records.sort(key=lambda r: r.time, reverse=True)
                        records = records[:15]
                    # внести результат в файл рекордов
                    with open("records", "a") as f:
                        f.write(f"{cat.elapsed_time} {cat.fish}\n")
                except:
                    pass
            # обновить объект
            o.update(shelfs, cat)

        # обновить воду
        for w in water:
            win.blit(w.image, w)
            w.update()

        # если кот жив
        if cat.alive():
            # вывести текущие результаты
            create_text(
                win,
                f"Время: {round(cat.elapsed_time, 3)}", 18,
                10, 10
            )
            create_text(win, f"Рыбок: {cat.fish}", 18, 10, 30)
        else:
            # вывести таблицу рекордов
            create_text(
                win,
                f"Ваш результат:", 18,
                WIN_WIDTH / 2, 10, center=True
            )
            create_text(
                win,
                f"время - {round(cat.elapsed_time, 3)}, рыбок - {cat.fish}", 18,
                WIN_WIDTH / 2, 30, center=True
            )
            for i, r in enumerate(records):
                create_text(
                    win,
                    f"Рекорд #{str(i + 1).rjust(2)}: время {str(round(r.time, 3)).rjust(7)}, рыбок {r.fish}", 16,
                    35, 35 * (i + 2)
                )
            create_text(
                win,
                f"Для начала новой игры нажмите ESC", 18,
                WIN_WIDTH / 2, WIN_HEIGHT - 32, center=True
            )

        # обновить экран
        display.update()
        display.set_caption(f"{WIN_NAME} - FPS: {round(timer.get_fps(), 1)}")


if __name__ == "__main__":
    main()