class Player:
    def __init__(self, is_white, is_human):
        self.is_white = is_white
        self.is_human = is_human


class Human(Player):
    def __init__(self, is_white, is_human=True):
        super().__init__(is_white, is_human)


class Computer(Player):
    def __init__(self, is_white):
        super().__init__(is_white, is_human=False)