from domain.entities.players import Computer, Human
from interface.gui.gui import GUI
from interface.ui.console import Console
from services.chess_service import Game


class Program:
    def __init__(self):
        self.__interface = None
        self.__white = None
        self.__black = None
        self.__engine_depth = None
        self.__screen_size = None
        self.__game = None
        self.settings()

    def settings(self):
        try:
            self.get_settings()
            self.configure_players()
            self.configure_gui_screen()
            self.configure_interface()
        except ValueError as error:
            print(error)

    def run(self):
        # try:
            self.__interface.run()
        # except AttributeError:
        #     print("Invalid settings configuration!")

    def get_settings(self):
        with open("settings/settings.properties", "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip(' ').split()
                if line != "":
                    setting = line[0]
                    value = line[2].lower()
                    if setting.lower() == "interface":
                        self.__interface = value
                    elif setting.lower() == "white":
                        self.__white = value
                    elif setting.lower() == "black":
                        self.__black = value
                    elif setting.lower() == "engine_depth":
                        try:
                            self.__engine_depth = int(value)
                        except ValueError:
                            raise ValueError("Invalid engine depth settings!")
                    elif setting.lower() == "screen_size":
                        self.__screen_size = value

    def configure_gui_screen(self):
        try:
            self.__screen_size = int(self.__screen_size)
        except ValueError:
            raise ValueError("Invalid screen size settings!")

    def configure_players(self):
        if self.__white == "computer":
            self.__white = Computer(is_white=True)
        elif self.__white == "human":
            self.__white = Human(is_white=True)
        if self.__black == "computer":
            self.__black = Computer(is_white=False)
        elif self.__black == "human":
            self.__black = Human(is_white=False)
        self.__game = Game(self.__white, self.__black, self.__engine_depth)

    def configure_interface(self):
        if self.__interface == "ui":
            self.__interface = Console(self.__game)
        elif self.__interface == "gui":
            self.__interface = GUI(self.__game, self.__screen_size)