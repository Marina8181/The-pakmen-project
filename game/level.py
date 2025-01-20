import pygame
import random
import paths
import constants
from project import game
import project.data as data

"""
ПОЯСНЕНИЕ:
Все уровни определены следующим образом
level = {
 tile_size: int
map_size= [int, int]

 map_format: двумерный массив, состоящий из базовой разметки стен/путей. Также включает в себя: player_spawn и площадь выхода.
 параметры для каждой плитки:
 "1" = стена
 "0" = путь
 "s" = безопасная точка (стена для врагов, они не могут пройти через нее)
 "p" = точка появления
 выходы:
 "t" = выход (через верхнюю часть стены)
 "b" = выход (через нижнюю часть стены)
 "l" = выход (через левую часть стены)
 "r" = выход (через правую часть стены)

 ключи: список позиций, т.е. [x, y] на карте, где расположены ключи.

 враги: список, содержащий всех врагов, населяющих уровень.
 враг:
 тип:
параметры типа противника:
 "ep": патруль (враг, для которого по умолчанию установлен режим патрулирования)
 "скорая помощь": случайный (враг, который случайным образом исследует)
Проверка уровня:
При разборе уровня при создании игры выполняется ряд проверок на достоверность, чтобы убедиться, что уровень воспроизводим.

map_format:
- проверьте, нет ли недопустимых параметров плитки.
- проверьте наличие полной внешней стены, чтобы игрок не мог покинуть карту. (выходы могут быть на краю, когда они закрыты, они считаются полными стенами)
- проверьте наличие только одной точки появления
- проверьте наличие только одного выхода

- проверьте, соединены ли точка появления и выход. (выполняет поиск пути между точками)

ключи:
- проверьте, все ли позиции указаны на карте и является ли плитка действительной

- проверьте, все ли ключи доступны для коллекционирования. (выполняет поиск пути между каждым ключом и точкой появления)

враги:
- проверьте всех врагов допустимого типа.
- проверьте, что у всех врагов типа "p" (патруль) есть патруль.
- проверьте, все ли враги имеют уникальные спавны, которые также не являются игроками и находятся на допустимых плитках.
ДЛЯ КАЖДОГО ВРАЖЕСКОГО ПАТРУЛЯ:
 - проверьте, все ли точки патрулирования находятся на допустимых плитках
 - проверьте, можно ли найти путь между всеми точками
"""

class Tile: # создаётся плитка на основании её позиции (строка и столбец)
    def __init__(self, level, row, col, filename):
        self.position = [row, col]
        self.image = pygame.image.load(paths.imagePath + filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, [level.TILE_SIZE, level.TILE_SIZE])
        self.rect = self.image.get_rect().move(game.get_pixel_position(level, [row, col]))

    def draw(self, display):
        display.blit(self.image, [self.rect.x, self.rect.y])

class IrregularWall:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
class Exit(Tile):
    def __init__(self, level, row, col, direction):
        self.direction = direction
        super().__init__(level, row, col, "exit-closed-%s.png" % self.direction)
        self.open = False

    def unlock(self):
        self.open = True
        size = self.image.get_size()
        self.image = pygame.image.load(paths.imagePath + "exit-open-%s.png" % self.direction).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)

    def is_closed(self):
        return not self.open

    def is_open(self):
        return self.open

    def get_open_walls(self):  # 4 прямоугольника - стены
        top_rect = IrregularWall([self.rect.x, self.rect.y, self.rect.width, 1])
        bottom_rect = IrregularWall([self.rect.x, self.rect.y + self.rect.height - 1, self.rect.width, 1])
        right_rect = IrregularWall([self.rect.x + self.rect.width - 1, self.rect.y, 1, self.rect.height])
        left_rect = IrregularWall([self.rect.x, self.rect.y, 1, self.rect.height])

        if self.direction == "top":
            return [right_rect, bottom_rect, left_rect]
        elif self.direction == "right":
            return [top_rect, bottom_rect, left_rect]
        elif self.direction == "bottom":
            return [top_rect, right_rect, left_rect]
        elif self.direction == "left":
            return [top_rect, right_rect, bottom_rect]


class Key(Tile): # наследует от tile
    def __init__(self, level,  row, col):
        super().__init__(level, row, col, "key.png")

class Level:
    def __init__(self, filename):
        self.data = data.load(filename)

        self.format = self.data["map-format"]
        self.enemies = self.data["enemies"]

        self.TILE_SIZE = self.data["tile-size"]
        self.MAP_SIZE = self.data["map-size"]

        self.DISPLAY_SIZE = [self.TILE_SIZE * self.MAP_SIZE[0], self.TILE_SIZE * self.MAP_SIZE[1]]

        self.PLAYER_SIZE = round(0.7 * self.TILE_SIZE)
        self.PLAYER_PADDING = self.TILE_SIZE - self.PLAYER_SIZE

        self.ENEMY_SIZE = round(0.5 * self.TILE_SIZE)
        self.ENEMY_PADDING = self.TILE_SIZE - self.ENEMY_SIZE

        # Map Setup
        self.walls = []
        self.path = []
        self.spawn = None
        self.exit = None

        spawn_number = 0
        exit_number = 0

        for row in range(len(self.format)):
            for col in range(len(self.format[0])):
                if self.format[row][col] == "1":
                    self.walls.append(Tile(self, row, col, "wall.png"))

                elif self.format[row][col] == "0":
                    self.path.append(Tile(self, row, col,  "path.png"))

                elif self.format[row][col] == "p":
                    self.path.append(Tile(self, row, col, "spawn-point.png"))
                    self.spawn = [row, col]
                    spawn_number += 1

                elif self.format[row][col] == "s":
                    self.path.append(Tile(self, row, col, "safe-point.png"))

                elif self.format[row][col] == "t":
                    self.exit = Exit(self, row, col, "top")
                    exit_number += 1

                elif self.format[row][col] == "l":
                    self.exit = Exit(self, row, col, "left")
                    exit_number += 1

                elif self.format[row][col] == "b":
                    self.exit = Exit(self, row, col, "bottom")
                    exit_number += 1

                elif self.format[row][col] == "r":
                    self.exit = Exit(self, row, col, "right")
                    exit_number += 1

        self.keys = []
        for key in self.data["keys"]:
            self.keys.append(Key(self, key[0], key[1]))

    def update(self):
        if len(self.keys) == 0:
            self.exit.unlock()

    def get_walls(self):
        if self.exit.is_closed():
            return self.walls + [self.exit]
        else:
            return self.walls + self.exit.get_open_walls()

    def get_spawn(self):
        return self.spawn

    def get_random_point(self):
        row, col = [0, 0]  # 0 0 ВСЕГДА стена
        while self.format[row][col] != "0":
            row, col = [random.randint(0, len(self.format) - 1), random.randint(0, len(self.format[0]) - 1)]
        return [row, col]  # 1 проход

    def draw_paths(self, display):
        for tile in self.path:
            tile.draw(display)

        for key in self.keys:
            key.draw(display)

    def draw_walls(self, display):
        for tile in self.walls:
            tile.draw(display)

        self.exit.draw(display)

    def draw_grid(self, display):
        for row in range(len(self.format)):
            for col in range(len(self.format[1])):
                pygame.draw.line(display, constants.COLOURS["dark-gray"],[0, col * self.TILE_SIZE],[row * self.TILE_SIZE, col * self.TILE_SIZE], 1)

                pygame.draw.line(display, constants.COLOURS["dark-gray"],[row*self.TILE_SIZE, 0],[row*self.TILE_SIZE, constants.DISPLAY_SIZE[1]], 1)

