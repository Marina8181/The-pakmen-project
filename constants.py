import paths
version = "by Marina and Diana"

DISPLAY_SIZE = [1000, 700]
DISPLAY_NAME = "Приключения Шрека"
FPS = 66

COLOURS = {
    "black": (0, 0, 0),
    "light-gray": (100, 100, 100),
    "dark-gray": (45, 45, 45),
    "white": (255, 255, 255),
    "yellow": (255, 220, 0),
    "panel": (50, 50, 50),
    "panel-hover": (60, 60, 60),
}

FONTS = {"main": paths.fontPath + "SourceSansPro-Light.ttf",
         "main-bold": paths.fontPath + "SourceSansPro-Semibold.ttf",
         "main-italic": paths.fontPath + "SourceSansPro-LightIt.ttf",
         "main-bold-italic": paths.fontPath + "SourceSansPro-SemiboldIt.ttf",
         "sizes":
             {"large": 20,
              "medium": 15,
              "small": 12},
         "colour": COLOURS["white"]}

WALL_FORMATS = ["1","0","t", "b", "l", "r", "p", "s"]
#  "1" = стена, "0" = путь, t/b/l/r = выходы, p = точка spawn, s = безопасная точка
