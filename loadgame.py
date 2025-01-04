import pygame
import os
import paths
import constants
import pygame_gui
class LoadGame:
    def __init__(self, display):
        self.display = display
        self.state = "load_game"
        self.game_reference = None

        # задник загрузки
        self.background = pygame_gui.Image(paths.imagePath + "background-load.png", 0, 0)

        # guiшка
        self.back_button = pygame_gui.Button(paths.uiPath + "backwhite.png",paths.uiPath + "backwhite-hover.png",5, 5)
        self.title = pygame_gui.Text("Выберете уровень",constants.FONTS["sizes"]["large"], constants.FONTS["colour"], constants.FONTS["main"],275, 55)

        self.file_selector = FileSelector(self, [275, 100])
        self.page_back_button = pygame_gui.Button(paths.uiPath + "pageback.png", paths.uiPath + "pageback-hover.png",670, 53)
        self.page_forward_button = pygame_gui.Button(paths.uiPath + "pageforward.png",paths.uiPath + "pageforward-hover.png",710, 53)
        self.run()

    def run(self):
        while self.state == "load_game":
            self.handle_events()
            self.draw()

    def get_state(self):
        return self.state

    def get_game(self):
        return self.game_reference

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.file_selector.check_clicked():
                    if self.back_button.check_clicked():
                        self.state = "menu"

                    elif self.page_back_button.check_clicked():
                        self.file_selector.page_back()

                    elif self.page_forward_button.check_clicked():
                        self.file_selector.page_forward()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "quit"

    def select_game(self, game_name):
        self.game_reference = game_name
        self.state = "game"

    def draw(self):
        self.display.fill((0, 0, 0))
        self.background.draw(self.display)

        self.title.draw(self.display)
        self.back_button.draw(self.display)

        self.file_selector.draw(self.display)
        self.page_back_button.draw(self.display)
        self.page_forward_button.draw(self.display)

        pygame.display.update()

class FileSelector:
    def __init__(self, control, origin):
        self.control = control
        self.origin = origin
        self.max_count = 3

        # имена карт
        self.games = sorted([file for file in os.listdir(paths.gamePath)])

        self.split_games = [self.games[i:i + self.max_count] for i in range(0, len(self.games), self.max_count)]

        # guiшка
        self.current_page = 0
        self.game_pages = []
        padding = 70
        for page in self.split_games:
            self.game_pages.append([])
            counter = 0
            for game_name in page:
                self.game_pages[len(self.game_pages)-1].append(GameSlot(self.control, game_name, [self.origin[0], self.origin[1] + padding*counter]))
                counter += 1

    def refresh_list(self):
        self.__init__(self.control, self.origin)

    def check_clicked(self):
        for slot in self.game_pages[self.current_page]:
            slot.handle_click()
    def page_forward(self):
        if self.current_page < len(self.game_pages)-1:
            self.current_page += 1
        else:
            self.current_page = 0

    def page_back(self):
        if self.current_page > 0:
            self.current_page -= 1
        else:
            self.current_page = len(self.game_pages)-1

    def draw(self, display):
        for game_slot in self.game_pages[self.current_page]:
            game_slot.draw(display)


class GameSlot:
    def __init__(self, control, game_name, position):
        self.control = control
        self.game_name = game_name
        self.position = position

        #guiшка
        self.back_panel = pygame_gui.Panel([self.position[0], self.position[1], 450, 50],255, constants.COLOURS["panel"])
        self.back_panel_hover = pygame_gui.Panel([self.position[0], self.position[1], 450, 50],255, constants.COLOURS["panel-hover"])

        self.text = pygame_gui.Text(game_name,constants.FONTS["sizes"]["medium"], constants.FONTS["colour"], constants.FONTS["main"],self.position[0] + 50, self.position[1] + 15)

    def handle_click(self):
        if self.mouse_over():
            self.control.select_game(self.game_name)

    def mouse_over(self):
        return self.back_panel.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, display):
        if self.mouse_over():
            self.back_panel_hover.draw(display)
        else:
            self.back_panel.draw(display)
            self.text.draw(display)

