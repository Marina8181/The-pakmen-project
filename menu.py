import pygame
import paths
import constants
import pygame_gui
class Menu:
    def __init__(self, display):
        self.display = display
        self.state = "menu"

        # задник
        self.background = pygame_gui.Image(paths.imagePath + "background-menu.png", 0, 0)

        # название
        self.title = pygame_gui.Text(constants.DISPLAY_NAME,45, constants.FONTS["colour"], constants.FONTS["main"],290, 220)
        self.menux = 420
        self.menuy = 350

        #guiшка
        self.continue_button = pygame_gui.TextButton([self.menux, self.menuy + 40, 150, 40],constants.COLOURS["panel"], constants.COLOURS["panel-hover"],"Уровни",constants.FONTS["sizes"]["large"], constants.FONTS["colour"], constants.FONTS["main"])
        self.version = pygame_gui.Text(constants.version,constants.FONTS["sizes"]["medium"], constants.FONTS["colour"], constants.FONTS["main"],3, constants.DISPLAY_SIZE[1] - 20)
        self.run()

    def run(self):
        while self.state == "menu":
            self.handle_events()
            self.draw()

    def get_state(self):
        return self.state

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.continue_button.check_clicked():
                    self.state = "load_game"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "quit"

    def draw(self):
        self.display.fill((0, 0, 0))
        self.background.draw(self.display)
        self.title.draw(self.display)
        self.continue_button.draw(self.display)
        self.version.draw(self.display)
        pygame.display.update()