import os
import pygame
import constants
import paths
from project import game
import pygame_gui

class Controller:
    def __init__(self, map_name):
        # инициализация игры
        self.map_name = map_name
        self.level = game.Level(self.map_name)
        self.state = "game"

        # настройка окна
        self.display = pygame.display.set_mode(self.level.DISPLAY_SIZE)
        pygame.display.set_caption(constants.DISPLAY_NAME + " - " + os.path.basename(map_name))
        self.clock = pygame.time.Clock()
        self.back_button = pygame_gui.Button(paths.uiPath + "backwhite.png", paths.uiPath + "backwhite-hover.png", 5, 5)

        # создание игрока
        spawn = game.get_pixel_position(self.level, self.level.get_spawn())
        spawn = [position + self.level.PLAYER_PADDING/2 for position in spawn]
        self.player = game.UserPLayer(spawn, [0, 0], self.level)

        # создание врагов
        self.enemies = []
        for enemy in self.level.enemies:
            if enemy["type"] == "er":
                self.enemies.append(game.RandomPatrol(self.level, enemy["spawn"]))

            elif enemy["type"] == "es":
                self.enemies.append(game.EnemySeeker(self.level, self.player, enemy["spawn"]))

            elif enemy["type"] == "ep":
                self.enemies.append(game.EnemyPatrol(self.level, enemy["patrol"]))


    def play(self): # логика игры
        while self.state not in ["menu", "quit"]:
            if self.state in ["won", "lost"]:
                self.state = game.GameOverMenu(self.display, self.state).get_option()
                if self.state == "game":
                    self.__init__(self.map_name)

            else:
                self.handle_events()
                self.player.update()
                self.level.update()

                for enemy in self.enemies:
                    enemy.update()
                    if self.player.rect.colliderect(enemy.rect):
                        self.state = "lost"

                for key in self.level.keys: # пересекается ли ключ с прямоугольником игрока
                    if self.player.rect.colliderect(key.rect):
                        self.level.keys.remove(key)

                if self.level.exit.is_open():
                    if self.level.exit.rect.contains(self.player.rect):
                        self.state = "won"

                self.draw()

        return self.state

    def handle_events(self): # перебор событий произощедщих
        for event in pygame.event.get(): # выход из игры
            if event.type == pygame.QUIT:
                self.state = "quit"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "quit"
                self.handle_key_down(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN: # чтобы работало нажатие кнопкой мыши
                self.handle_click(pygame.mouse.get_pos())

        self.handle_pressed_keys()

    def handle_key_down(self, key):
        if key == pygame.K_v:
            pygame.image.save(self.display, "background-%s.png" % time.time())  # делает скриншот, просто прикольно

    def handle_pressed_keys(self): # клавиши
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.move_up()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.move_down()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()

    def handle_click(self, position):
        if self.back_button.check_clicked():
            self.state = "menu"

    def draw(self):
        self.display.fill(constants.COLOURS["dark-gray"])
        self.level.draw_paths(self.display)
        self.level.draw_grid(self.display)
        self.player.draw(self.display)
        self.level.draw_walls(self.display)
        for enemy in self.enemies:
            enemy.draw(self.display)
        self.back_button.draw(self.display)
        pygame.display.update()
        self.clock.tick(constants.FPS)

