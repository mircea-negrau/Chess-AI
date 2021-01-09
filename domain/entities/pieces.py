class Piece(object):
    def __init__(self, is_white):
        self.__is_dead = False
        self.__is_white = is_white

    @property
    def is_dead(self):
        return self.__is_dead

    @is_dead.setter
    def is_dead(self, value):
        self.__is_dead = value

    @property
    def is_white(self):
        return self.__is_white

    @is_white.setter
    def is_white(self, value):
        self.__is_white = value


class King(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.__is_castling_available = True

    @property
    def can_castle(self):
        return self.__is_castling_available

    @can_castle.setter
    def can_castle(self, value):
        self.__is_castling_available = value

    def __str__(self):
        color = "White"
        if not self.is_white:
            color = "Black"
        return color + " King"


class Queen(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)

    def __str__(self):
        color = "White"
        if not self.is_white:
            color = "Black"
        return color + " Queen"


class Rook(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.__can_castle = True

    @property
    def can_castle(self):
        return self.__can_castle

    @can_castle.setter
    def can_castle(self, value):
        self.__can_castle = value

    def __str__(self):
        color = "White"
        if not self.is_white:
            color = "Black"
        return color + " Rook"


class Bishop(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)

    def __str__(self):
        color = "White"
        if not self.is_white:
            color = "Black"
        return color + " Bishop"


class Knight(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)

    def __str__(self):
        color = "White"
        if not self.is_white:
            color = "Black"
        return color + " Knight"


class Pawn(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.__initial_square = True

    @property
    def initial_square(self):
        return self.__initial_square

    @initial_square.setter
    def initial_square(self, value):
        self.__initial_square = value

    def __str__(self):
        color = "White"
        if not self.is_white:
            color = "Black"
        return color + " Pawn"


class NoPiece(Piece):
    def __init__(self):
        super().__init__(is_white=False)

    def __str__(self):
        return "None"
