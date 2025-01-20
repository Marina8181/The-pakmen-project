import pygame
import constants
import paths
import project.menus as menus
import project.game.controller as game

class ApplicationController:
    def __init__(self):
        pygame.init()

        # Icon
        icon = pygame.image.load(paths.imagePath + "icon.png")
        icon.set_colorkey((0, 0, 0))
        pygame.display.set_icon(icon)

        # Display Setup
        self.display = pygame.display.set_mode(constants.DISPLAY_SIZE)
        pygame.display.set_caption(constants.DISPLAY_NAME)

        # General Setup
        self.state = "menu"
        self.game_reference = None

    def run(self):
        while self.state != "quit":
            if self.state == "menu":
                self.run_menu()

            elif self.state == "load_game":
                self.run_loadgame()

            elif self.state == "game":
                self.run_game()

        self.quit()

    def run_menu(self):
        menu = menus.Menu(self.display)
        self.state = menu.get_state()

    def run_loadgame(self):
        load_game = menus.LoadGame(self.display)
        self.state = load_game.get_state()
        self.game_reference = load_game.get_game()

    def run_game(self):
        running_game = game.Controller(paths.gamePath + self.game_reference)
        self.state = running_game.play()
        self.game_reference = None
        self.display = pygame.display.set_mode(constants.DISPLAY_SIZE)
        pygame.display.set_caption(constants.DISPLAY_NAME)

    def quit(self):
        pygame.quit()
        quit()