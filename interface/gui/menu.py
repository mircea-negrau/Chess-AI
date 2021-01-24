import pygame
import pygame_menu

from domain.entities.players import Computer, Human
from interface.gui.gui import GUI
from services.chess_service import Game


class GuiMenu:
    def __init__(self, screen_size):
        self.__white_computer = Computer(is_white=True)
        self.__black_computer = Computer(is_white=False)
        self.__white_human = Human(is_white=True)
        self.__black_human = Human(is_white=False)
        self.__white = self.__white_computer
        self.__black = self.__black_human
        self.__engine_depth = 2
        self.__screen_size = screen_size
        self.setup_menu()

    def setup_menu(self):
        pygame.init()
        pygame.display.set_caption('Chess Menu')
        surface = pygame.display.set_mode((500, 500))
        programIcon = pygame.image.load("interface/gui/images/White Queen.png")
        pygame.display.set_icon(programIcon)
        menu = pygame_menu.Menu(500, 500, 'Chess', theme=pygame_menu.themes.THEME_DARK)
        menu.add_button('Play Chess', self.start_game)
        menu.add_selector('White Player:', [('Computer', 1), ('  Human  ', 2)], onchange=self.set_white_player)
        menu.add_selector('Black Player:', [('  Human  ', 1), ('Computer', 2)], onchange=self.set_black_player)
        menu.add_selector('Engine Depth:', [('2', 1), ('4', 2)], onchange=self.set_engine_depth)
        menu.add_button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(surface)

    def start_game(self):
        game = Game(self.__white, self.__black, self.__engine_depth)
        interface = GUI(game, self.__screen_size)
        interface.run()

    def set_white_player(self, *args):
        if self.__white.is_human:
            self.__white = self.__white_computer
        else:
            self.__white = self.__white_human

    def set_black_player(self, *args):
        if self.__black.is_human:
            self.__black = self.__black_computer
        else:
            self.__black = self.__black_human

    def set_engine_depth(self, *args):
        if self.__engine_depth == 4:
            self.__engine_depth = 2
        else:
            self.__engine_depth = 4
