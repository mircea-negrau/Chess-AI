from domain.entities.pieces import Rook, Knight, Bishop, Queen, King, Pawn, NoPiece


class Board:
    def __init__(self, type):
        self.__board = []
        self.__available_en_passant = False
        self.__reset_board(type)

    @property
    def available_en_passant(self):
        return self.__available_en_passant

    @available_en_passant.setter
    def available_en_passant(self, value):
        self.__available_en_passant = value

    def get_square(self, rank, file):
        """
        Method to return the square of the board found at the given parameters. If the coordinates are not valid,
        the method returns a None value.
        :param rank: integer, holds the value of the square's rank on the board;
        :param file: integer, holds the value of the square's file on the board;
        :return: None, if invalid coordinates. Otherwise, Square object from the pointed coordinates.
        """
        if rank < 1 or rank > 8 or file < 1 or file > 8:
            return None
        return self.__board[rank][file]

    def __getitem__(self, rank):
        return self.__board[rank]

    def __reset_board(self, type):
        """
        Method to set the board for the start of the game.
        The white pieces are always on the first two ranks and the black pieces are always on the last two ranks
        of the board.
        """
        if type == "Normal":
            self.__board = {
                8: {1: Square(8, 1, Rook(is_white=False)),
                    2: Square(8, 2, Knight(is_white=False)),
                    3: Square(8, 3, Bishop(is_white=False)),
                    4: Square(8, 4, Queen(is_white=False)),
                    5: Square(8, 5, King(is_white=False)),
                    6: Square(8, 6, Bishop(is_white=False)),
                    7: Square(8, 7, Knight(is_white=False)),
                    8: Square(8, 8, Rook(is_white=False))
                    },
                7: {1: Square(7, 1, Pawn(is_white=False)),
                    2: Square(7, 2, Pawn(is_white=False)),
                    3: Square(7, 3, Pawn(is_white=False)),
                    4: Square(7, 4, Pawn(is_white=False)),
                    5: Square(7, 5, Pawn(is_white=False)),
                    6: Square(7, 6, Pawn(is_white=False)),
                    7: Square(7, 7, Pawn(is_white=False)),
                    8: Square(7, 8, Pawn(is_white=False)),
                    },
                6: {1: Square(6, 1, NoPiece()),
                    2: Square(6, 2, NoPiece()),
                    3: Square(6, 3, NoPiece()),
                    4: Square(6, 4, NoPiece()),
                    5: Square(6, 5, NoPiece()),
                    6: Square(6, 6, NoPiece()),
                    7: Square(6, 7, NoPiece()),
                    8: Square(6, 8, NoPiece()),
                    },
                5: {1: Square(5, 1, NoPiece()),
                    2: Square(5, 2, NoPiece()),
                    3: Square(5, 3, NoPiece()),
                    4: Square(5, 4, NoPiece()),
                    5: Square(5, 5, NoPiece()),
                    6: Square(5, 6, NoPiece()),
                    7: Square(5, 7, NoPiece()),
                    8: Square(5, 8, NoPiece()),
                    },
                4: {1: Square(4, 1, NoPiece()),
                    2: Square(4, 2, NoPiece()),
                    3: Square(4, 3, NoPiece()),
                    4: Square(4, 4, NoPiece()),
                    5: Square(4, 5, NoPiece()),
                    6: Square(4, 6, NoPiece()),
                    7: Square(4, 7, NoPiece()),
                    8: Square(4, 8, NoPiece()),
                    },
                3: {1: Square(3, 1, NoPiece()),
                    2: Square(3, 2, NoPiece()),
                    3: Square(3, 3, NoPiece()),
                    4: Square(3, 4, NoPiece()),
                    5: Square(3, 5, NoPiece()),
                    6: Square(3, 6, NoPiece()),
                    7: Square(3, 7, NoPiece()),
                    8: Square(3, 8, NoPiece()),
                    },
                2: {1: Square(2, 1, Pawn(is_white=True)),
                    2: Square(2, 2, Pawn(is_white=True)),
                    3: Square(2, 3, Pawn(is_white=True)),
                    4: Square(2, 4, Pawn(is_white=True)),
                    5: Square(2, 5, Pawn(is_white=True)),
                    6: Square(2, 6, Pawn(is_white=True)),
                    7: Square(2, 7, Pawn(is_white=True)),
                    8: Square(2, 8, Pawn(is_white=True)),
                    },
                1: {1: Square(1, 1, Rook(is_white=True)),
                    2: Square(1, 2, Knight(is_white=True)),
                    3: Square(1, 3, Bishop(is_white=True)),
                    4: Square(1, 4, Queen(is_white=True)),
                    5: Square(1, 5, King(is_white=True)),
                    6: Square(1, 6, Bishop(is_white=True)),
                    7: Square(1, 7, Knight(is_white=True)),
                    8: Square(1, 8, Rook(is_white=True))
                    }
            }
        elif type == "Checkmate":
            self.get_checkmate_board_placement()
        elif type == "Stalemate":
            self.get_stalemate_board_placement()
        elif type == "Check":
            self.get_check_board_placement()
        elif type == "Castling_Test":
            self.get_castling_test_placement()
        elif type == "Fail_castling_test":
            self.get_failing_castling_test_placement()
        elif type == "One-step-to-check-for-white":
            self.get_one_step_white_check_board_placement()
        elif type == "One-step-to-check-for-black":
            self.get_one_step_black_check_board_placement()
        elif type == "end-game-evaluation":
            self.get_end_game_evaluation_board_placement()

    def get_end_game_evaluation_board_placement(self):
        self.__board = {
            8: {1: Square(8, 1, Rook(is_white=False)),
                2: Square(8, 2, Knight(is_white=False)),
                3: Square(8, 3, Bishop(is_white=False)),
                4: Square(8, 4, NoPiece()),
                5: Square(8, 5, King(is_white=False)),
                6: Square(8, 6, Bishop(is_white=False)),
                7: Square(8, 7, Knight(is_white=False)),
                8: Square(8, 8, Rook(is_white=False))
                },
            7: {1: Square(7, 1, Pawn(is_white=False)),
                2: Square(7, 2, Pawn(is_white=False)),
                3: Square(7, 3, Pawn(is_white=False)),
                4: Square(7, 4, Pawn(is_white=False)),
                5: Square(7, 5, Pawn(is_white=False)),
                6: Square(7, 6, Pawn(is_white=False)),
                7: Square(7, 7, Pawn(is_white=False)),
                8: Square(7, 8, Pawn(is_white=False)),
                },
            6: {1: Square(6, 1, NoPiece()),
                2: Square(6, 2, NoPiece()),
                3: Square(6, 3, NoPiece()),
                4: Square(6, 4, NoPiece()),
                5: Square(6, 5, NoPiece()),
                6: Square(6, 6, NoPiece()),
                7: Square(6, 7, NoPiece()),
                8: Square(6, 8, NoPiece()),
                },
            5: {1: Square(5, 1, NoPiece()),
                2: Square(5, 2, NoPiece()),
                3: Square(5, 3, NoPiece()),
                4: Square(5, 4, NoPiece()),
                5: Square(5, 5, NoPiece()),
                6: Square(5, 6, NoPiece()),
                7: Square(5, 7, NoPiece()),
                8: Square(5, 8, NoPiece()),
                },
            4: {1: Square(4, 1, NoPiece()),
                2: Square(4, 2, NoPiece()),
                3: Square(4, 3, NoPiece()),
                4: Square(4, 4, NoPiece()),
                5: Square(4, 5, NoPiece()),
                6: Square(4, 6, NoPiece()),
                7: Square(4, 7, NoPiece()),
                8: Square(4, 8, NoPiece()),
                },
            3: {1: Square(3, 1, NoPiece()),
                2: Square(3, 2, NoPiece()),
                3: Square(3, 3, NoPiece()),
                4: Square(3, 4, NoPiece()),
                5: Square(3, 5, NoPiece()),
                6: Square(3, 6, NoPiece()),
                7: Square(3, 7, NoPiece()),
                8: Square(3, 8, NoPiece()),
                },
            2: {1: Square(2, 1, Pawn(is_white=True)),
                2: Square(2, 2, Pawn(is_white=True)),
                3: Square(2, 3, Pawn(is_white=True)),
                4: Square(2, 4, Pawn(is_white=True)),
                5: Square(2, 5, Pawn(is_white=True)),
                6: Square(2, 6, Pawn(is_white=True)),
                7: Square(2, 7, Pawn(is_white=True)),
                8: Square(2, 8, Pawn(is_white=True)),
                },
            1: {1: Square(1, 1, Rook(is_white=True)),
                2: Square(1, 2, Knight(is_white=True)),
                3: Square(1, 3, Bishop(is_white=True)),
                4: Square(1, 4, NoPiece()),
                5: Square(1, 5, King(is_white=True)),
                6: Square(1, 6, Bishop(is_white=True)),
                7: Square(1, 7, Knight(is_white=True)),
                8: Square(1, 8, Rook(is_white=True))
                }
        }

    def get_one_step_white_check_board_placement(self):
        self.__board = {
            8: {1: Square(8, 1, King(is_white=False)),
                2: Square(8, 2, NoPiece()),
                3: Square(8, 3, NoPiece()),
                4: Square(8, 4, NoPiece()),
                5: Square(8, 5, NoPiece()),
                6: Square(8, 6, NoPiece()),
                7: Square(8, 7, NoPiece()),
                8: Square(8, 8, NoPiece())
                },
            7: {1: Square(7, 1, NoPiece()),
                2: Square(7, 2, NoPiece()),
                3: Square(7, 3, NoPiece()),
                4: Square(7, 4, NoPiece()),
                5: Square(7, 5, NoPiece()),
                6: Square(7, 6, NoPiece()),
                7: Square(7, 7, NoPiece()),
                8: Square(7, 8, NoPiece()),
                },
            6: {1: Square(6, 1, NoPiece()),
                2: Square(6, 2, NoPiece()),
                3: Square(6, 3, NoPiece()),
                4: Square(6, 4, NoPiece()),
                5: Square(6, 5, NoPiece()),
                6: Square(6, 6, NoPiece()),
                7: Square(6, 7, NoPiece()),
                8: Square(6, 8, NoPiece()),
                },
            5: {1: Square(5, 1, NoPiece()),
                2: Square(5, 2, NoPiece()),
                3: Square(5, 3, NoPiece()),
                4: Square(5, 4, NoPiece()),
                5: Square(5, 5, NoPiece()),
                6: Square(5, 6, NoPiece()),
                7: Square(5, 7, NoPiece()),
                8: Square(5, 8, NoPiece()),
                },
            4: {1: Square(4, 1, NoPiece()),
                2: Square(4, 2, NoPiece()),
                3: Square(4, 3, NoPiece()),
                4: Square(4, 4, NoPiece()),
                5: Square(4, 5, NoPiece()),
                6: Square(4, 6, NoPiece()),
                7: Square(4, 7, NoPiece()),
                8: Square(4, 8, NoPiece()),
                },
            3: {1: Square(3, 1, NoPiece()),
                2: Square(3, 2, NoPiece()),
                3: Square(3, 3, NoPiece()),
                4: Square(3, 4, NoPiece()),
                5: Square(3, 5, NoPiece()),
                6: Square(3, 6, NoPiece()),
                7: Square(3, 7, NoPiece()),
                8: Square(3, 8, King(is_white=True)),
                },
            2: {1: Square(2, 1, NoPiece()),
                2: Square(2, 2, NoPiece()),
                3: Square(2, 3, Rook(is_white=True)),
                4: Square(2, 4, NoPiece()),
                5: Square(2, 5, NoPiece()),
                6: Square(2, 6, NoPiece()),
                7: Square(2, 7, NoPiece()),
                8: Square(2, 8, NoPiece()),
                },
            1: {1: Square(1, 1, NoPiece()),
                2: Square(1, 2, Rook(is_white=True)),
                3: Square(1, 3, NoPiece()),
                4: Square(1, 4, NoPiece()),
                5: Square(1, 5, NoPiece()),
                6: Square(1, 6, NoPiece()),
                7: Square(1, 7, NoPiece()),
                8: Square(1, 8, NoPiece())
                }
        }

    def get_one_step_black_check_board_placement(self):
        self.__board = {
            8: {1: Square(8, 1, King(is_white=True)),
                2: Square(8, 2, NoPiece()),
                3: Square(8, 3, NoPiece()),
                4: Square(8, 4, NoPiece()),
                5: Square(8, 5, NoPiece()),
                6: Square(8, 6, NoPiece()),
                7: Square(8, 7, NoPiece()),
                8: Square(8, 8, NoPiece())
                },
            7: {1: Square(7, 1, NoPiece()),
                2: Square(7, 2, NoPiece()),
                3: Square(7, 3, NoPiece()),
                4: Square(7, 4, NoPiece()),
                5: Square(7, 5, NoPiece()),
                6: Square(7, 6, NoPiece()),
                7: Square(7, 7, NoPiece()),
                8: Square(7, 8, NoPiece()),
                },
            6: {1: Square(6, 1, NoPiece()),
                2: Square(6, 2, NoPiece()),
                3: Square(6, 3, NoPiece()),
                4: Square(6, 4, NoPiece()),
                5: Square(6, 5, NoPiece()),
                6: Square(6, 6, NoPiece()),
                7: Square(6, 7, NoPiece()),
                8: Square(6, 8, NoPiece()),
                },
            5: {1: Square(5, 1, NoPiece()),
                2: Square(5, 2, NoPiece()),
                3: Square(5, 3, NoPiece()),
                4: Square(5, 4, NoPiece()),
                5: Square(5, 5, NoPiece()),
                6: Square(5, 6, NoPiece()),
                7: Square(5, 7, NoPiece()),
                8: Square(5, 8, NoPiece()),
                },
            4: {1: Square(4, 1, NoPiece()),
                2: Square(4, 2, NoPiece()),
                3: Square(4, 3, NoPiece()),
                4: Square(4, 4, NoPiece()),
                5: Square(4, 5, NoPiece()),
                6: Square(4, 6, NoPiece()),
                7: Square(4, 7, NoPiece()),
                8: Square(4, 8, NoPiece()),
                },
            3: {1: Square(3, 1, NoPiece()),
                2: Square(3, 2, NoPiece()),
                3: Square(3, 3, NoPiece()),
                4: Square(3, 4, NoPiece()),
                5: Square(3, 5, NoPiece()),
                6: Square(3, 6, NoPiece()),
                7: Square(3, 7, NoPiece()),
                8: Square(3, 8, King(is_white=False)),
                },
            2: {1: Square(2, 1, NoPiece()),
                2: Square(2, 2, NoPiece()),
                3: Square(2, 3, Rook(is_white=False)),
                4: Square(2, 4, NoPiece()),
                5: Square(2, 5, NoPiece()),
                6: Square(2, 6, NoPiece()),
                7: Square(2, 7, NoPiece()),
                8: Square(2, 8, NoPiece()),
                },
            1: {1: Square(1, 1, NoPiece()),
                2: Square(1, 2, Rook(is_white=False)),
                3: Square(1, 3, NoPiece()),
                4: Square(1, 4, NoPiece()),
                5: Square(1, 5, NoPiece()),
                6: Square(1, 6, NoPiece()),
                7: Square(1, 7, NoPiece()),
                8: Square(1, 8, NoPiece())
                }
        }

    def get_failing_castling_test_placement(self):
        self.__board = {
            8: {1: Square(8, 1, Queen(is_white=False)),
                2: Square(8, 2, NoPiece()),
                3: Square(8, 3, NoPiece()),
                4: Square(8, 4, NoPiece()),
                5: Square(8, 5, NoPiece()),
                6: Square(8, 6, NoPiece()),
                7: Square(8, 7, NoPiece()),
                8: Square(8, 8, NoPiece())
                },
            7: {1: Square(7, 1, NoPiece()),
                2: Square(7, 2, NoPiece()),
                3: Square(7, 3, NoPiece()),
                4: Square(7, 4, NoPiece()),
                5: Square(7, 5, NoPiece()),
                6: Square(7, 6, NoPiece()),
                7: Square(7, 7, Pawn(is_white=True)),
                8: Square(7, 8, NoPiece()),
                },
            6: {1: Square(6, 1, NoPiece()),
                2: Square(6, 2, NoPiece()),
                3: Square(6, 3, NoPiece()),
                4: Square(6, 4, NoPiece()),
                5: Square(6, 5, NoPiece()),
                6: Square(6, 6, NoPiece()),
                7: Square(6, 7, Pawn(is_white=True)),
                8: Square(6, 8, King(is_white=False)),
                },
            5: {1: Square(5, 1, NoPiece()),
                2: Square(5, 2, NoPiece()),
                3: Square(5, 3, NoPiece()),
                4: Square(5, 4, NoPiece()),
                5: Square(5, 5, NoPiece()),
                6: Square(5, 6, NoPiece()),
                7: Square(5, 7, NoPiece()),
                8: Square(5, 8, NoPiece()),
                },
            4: {1: Square(4, 1, NoPiece()),
                2: Square(4, 2, NoPiece()),
                3: Square(4, 3, NoPiece()),
                4: Square(4, 4, NoPiece()),
                5: Square(4, 5, NoPiece()),
                6: Square(4, 6, NoPiece()),
                7: Square(4, 7, NoPiece()),
                8: Square(4, 8, NoPiece()),
                },
            3: {1: Square(3, 1, NoPiece()),
                2: Square(3, 2, NoPiece()),
                3: Square(3, 3, NoPiece()),
                4: Square(3, 4, NoPiece()),
                5: Square(3, 5, NoPiece()),
                6: Square(3, 6, NoPiece()),
                7: Square(3, 7, NoPiece()),
                8: Square(3, 8, NoPiece()),
                },
            2: {1: Square(2, 1, NoPiece()),
                2: Square(2, 2, NoPiece()),
                3: Square(2, 3, NoPiece()),
                4: Square(2, 4, NoPiece()),
                5: Square(2, 5, NoPiece()),
                6: Square(2, 6, NoPiece()),
                7: Square(2, 7, NoPiece()),
                8: Square(2, 8, NoPiece()),
                },
            1: {1: Square(1, 1, Rook(is_white=True)),
                2: Square(1, 2, NoPiece()),
                3: Square(1, 3, NoPiece()),
                4: Square(1, 4, NoPiece()),
                5: Square(1, 5, King(is_white=True)),
                6: Square(1, 6, NoPiece()),
                7: Square(1, 7, NoPiece()),
                8: Square(1, 8, NoPiece())
                }
        }

    def get_castling_test_placement(self):
        self.__board = {
            8: {1: Square(8, 1, NoPiece()),
                2: Square(8, 2, NoPiece()),
                3: Square(8, 3, NoPiece()),
                4: Square(8, 4, NoPiece()),
                5: Square(8, 5, NoPiece()),
                6: Square(8, 6, NoPiece()),
                7: Square(8, 7, NoPiece()),
                8: Square(8, 8, Queen(is_white=False))
                },
            7: {1: Square(7, 1, NoPiece()),
                2: Square(7, 2, NoPiece()),
                3: Square(7, 3, Pawn(is_white=False)),
                4: Square(7, 4, NoPiece()),
                5: Square(7, 5, NoPiece()),
                6: Square(7, 6, NoPiece()),
                7: Square(7, 7, NoPiece()),
                8: Square(7, 8, NoPiece()),
                },
            6: {1: Square(6, 1, NoPiece()),
                2: Square(6, 2, NoPiece()),
                3: Square(6, 3, NoPiece()),
                4: Square(6, 4, NoPiece()),
                5: Square(6, 5, NoPiece()),
                6: Square(6, 6, NoPiece()),
                7: Square(6, 7, NoPiece()),
                8: Square(6, 8, King(is_white=False)),
                },
            5: {1: Square(5, 1, NoPiece()),
                2: Square(5, 2, NoPiece()),
                3: Square(5, 3, NoPiece()),
                4: Square(5, 4, Pawn(is_white=True)),
                5: Square(5, 5, NoPiece()),
                6: Square(5, 6, NoPiece()),
                7: Square(5, 7, NoPiece()),
                8: Square(5, 8, NoPiece()),
                },
            4: {1: Square(4, 1, NoPiece()),
                2: Square(4, 2, NoPiece()),
                3: Square(4, 3, Pawn(is_white=False)),
                4: Square(4, 4, NoPiece()),
                5: Square(4, 5, NoPiece()),
                6: Square(4, 6, NoPiece()),
                7: Square(4, 7, NoPiece()),
                8: Square(4, 8, NoPiece()),
                },
            3: {1: Square(3, 1, NoPiece()),
                2: Square(3, 2, NoPiece()),
                3: Square(3, 3, NoPiece()),
                4: Square(3, 4, NoPiece()),
                5: Square(3, 5, NoPiece()),
                6: Square(3, 6, NoPiece()),
                7: Square(3, 7, NoPiece()),
                8: Square(3, 8, NoPiece()),
                },
            2: {1: Square(2, 1, Pawn(is_white=True)),
                2: Square(2, 2, Pawn(is_white=True)),
                3: Square(2, 3, NoPiece()),
                4: Square(2, 4, NoPiece()),
                5: Square(2, 5, NoPiece()),
                6: Square(2, 6, NoPiece()),
                7: Square(2, 7, NoPiece()),
                8: Square(2, 8, NoPiece()),
                },
            1: {1: Square(1, 1, Rook(is_white=True)),
                2: Square(1, 2, NoPiece()),
                3: Square(1, 3, NoPiece()),
                4: Square(1, 4, NoPiece()),
                5: Square(1, 5, King(is_white=True)),
                6: Square(1, 6, NoPiece()),
                7: Square(1, 7, NoPiece()),
                8: Square(1, 8, Rook(is_white=True))
                }
        }

    def get_checkmate_board_placement(self):
        self.__board = {
            8: {1: Square(8, 1, NoPiece()),
                2: Square(8, 2, NoPiece()),
                3: Square(8, 3, NoPiece()),
                4: Square(8, 4, NoPiece()),
                5: Square(8, 5, NoPiece()),
                6: Square(8, 6, NoPiece()),
                7: Square(8, 7, NoPiece()),
                8: Square(8, 8, NoPiece())
                },
            7: {1: Square(7, 1, NoPiece()),
                2: Square(7, 2, NoPiece()),
                3: Square(7, 3, NoPiece()),
                4: Square(7, 4, NoPiece()),
                5: Square(7, 5, NoPiece()),
                6: Square(7, 6, NoPiece()),
                7: Square(7, 7, NoPiece()),
                8: Square(7, 8, NoPiece()),
                },
            6: {1: Square(6, 1, NoPiece()),
                2: Square(6, 2, NoPiece()),
                3: Square(6, 3, NoPiece()),
                4: Square(6, 4, NoPiece()),
                5: Square(6, 5, NoPiece()),
                6: Square(6, 6, NoPiece()),
                7: Square(6, 7, NoPiece()),
                8: Square(6, 8, King(is_white=False)),
                },
            5: {1: Square(5, 1, NoPiece()),
                2: Square(5, 2, NoPiece()),
                3: Square(5, 3, NoPiece()),
                4: Square(5, 4, NoPiece()),
                5: Square(5, 5, NoPiece()),
                6: Square(5, 6, NoPiece()),
                7: Square(5, 7, NoPiece()),
                8: Square(5, 8, NoPiece()),
                },
            4: {1: Square(4, 1, NoPiece()),
                2: Square(4, 2, NoPiece()),
                3: Square(4, 3, NoPiece()),
                4: Square(4, 4, NoPiece()),
                5: Square(4, 5, NoPiece()),
                6: Square(4, 6, NoPiece()),
                7: Square(4, 7, NoPiece()),
                8: Square(4, 8, NoPiece()),
                },
            3: {1: Square(3, 1, NoPiece()),
                2: Square(3, 2, NoPiece()),
                3: Square(3, 3, NoPiece()),
                4: Square(3, 4, NoPiece()),
                5: Square(3, 5, NoPiece()),
                6: Square(3, 6, NoPiece()),
                7: Square(3, 7, NoPiece()),
                8: Square(3, 8, NoPiece()),
                },
            2: {1: Square(2, 1, Queen(is_white=False)),
                2: Square(2, 2, NoPiece()),
                3: Square(2, 3, NoPiece()),
                4: Square(2, 4, NoPiece()),
                5: Square(2, 5, NoPiece()),
                6: Square(2, 6, NoPiece()),
                7: Square(2, 7, NoPiece()),
                8: Square(2, 8, NoPiece()),
                },
            1: {1: Square(1, 1, King(is_white=True)),
                2: Square(1, 2, Queen(is_white=False)),
                3: Square(1, 3, NoPiece()),
                4: Square(1, 4, Queen(is_white=False)),
                5: Square(1, 5, NoPiece()),
                6: Square(1, 6, NoPiece()),
                7: Square(1, 7, NoPiece()),
                8: Square(1, 8, NoPiece())
                }
        }

    def get_stalemate_board_placement(self):
        self.__board = {
            8: {1: Square(8, 1, NoPiece()),
                2: Square(8, 2, NoPiece()),
                3: Square(8, 3, NoPiece()),
                4: Square(8, 4, NoPiece()),
                5: Square(8, 5, NoPiece()),
                6: Square(8, 6, NoPiece()),
                7: Square(8, 7, NoPiece()),
                8: Square(8, 8, NoPiece())
                },
            7: {1: Square(7, 1, NoPiece()),
                2: Square(7, 2, NoPiece()),
                3: Square(7, 3, NoPiece()),
                4: Square(7, 4, NoPiece()),
                5: Square(7, 5, NoPiece()),
                6: Square(7, 6, NoPiece()),
                7: Square(7, 7, NoPiece()),
                8: Square(7, 8, NoPiece()),
                },
            6: {1: Square(6, 1, NoPiece()),
                2: Square(6, 2, NoPiece()),
                3: Square(6, 3, NoPiece()),
                4: Square(6, 4, NoPiece()),
                5: Square(6, 5, NoPiece()),
                6: Square(6, 6, NoPiece()),
                7: Square(6, 7, NoPiece()),
                8: Square(6, 8, King(is_white=False)),
                },
            5: {1: Square(5, 1, NoPiece()),
                2: Square(5, 2, NoPiece()),
                3: Square(5, 3, NoPiece()),
                4: Square(5, 4, NoPiece()),
                5: Square(5, 5, NoPiece()),
                6: Square(5, 6, NoPiece()),
                7: Square(5, 7, NoPiece()),
                8: Square(5, 8, NoPiece()),
                },
            4: {1: Square(4, 1, NoPiece()),
                2: Square(4, 2, NoPiece()),
                3: Square(4, 3, NoPiece()),
                4: Square(4, 4, NoPiece()),
                5: Square(4, 5, NoPiece()),
                6: Square(4, 6, NoPiece()),
                7: Square(4, 7, NoPiece()),
                8: Square(4, 8, NoPiece()),
                },
            3: {1: Square(3, 1, NoPiece()),
                2: Square(3, 2, Queen(is_white=False)),
                3: Square(3, 3, NoPiece()),
                4: Square(3, 4, NoPiece()),
                5: Square(3, 5, NoPiece()),
                6: Square(3, 6, NoPiece()),
                7: Square(3, 7, NoPiece()),
                8: Square(3, 8, NoPiece()),
                },
            2: {1: Square(2, 1, NoPiece()),
                2: Square(2, 2, NoPiece()),
                3: Square(2, 3, Queen(is_white=False)),
                4: Square(2, 4, NoPiece()),
                5: Square(2, 5, NoPiece()),
                6: Square(2, 6, NoPiece()),
                7: Square(2, 7, NoPiece()),
                8: Square(2, 8, NoPiece()),
                },
            1: {1: Square(1, 1, King(is_white=True)),
                2: Square(1, 2, NoPiece()),
                3: Square(1, 3, NoPiece()),
                4: Square(1, 4, NoPiece()),
                5: Square(1, 5, NoPiece()),
                6: Square(1, 6, NoPiece()),
                7: Square(1, 7, NoPiece()),
                8: Square(1, 8, NoPiece())
                }
        }

    def get_check_board_placement(self):
        self.__board = {
            8: {1: Square(8, 1, NoPiece()),
                2: Square(8, 2, NoPiece()),
                3: Square(8, 3, NoPiece()),
                4: Square(8, 4, NoPiece()),
                5: Square(8, 5, NoPiece()),
                6: Square(8, 6, NoPiece()),
                7: Square(8, 7, NoPiece()),
                8: Square(8, 8, NoPiece())
                },
            7: {1: Square(7, 1, NoPiece()),
                2: Square(7, 2, NoPiece()),
                3: Square(7, 3, NoPiece()),
                4: Square(7, 4, NoPiece()),
                5: Square(7, 5, NoPiece()),
                6: Square(7, 6, NoPiece()),
                7: Square(7, 7, NoPiece()),
                8: Square(7, 8, NoPiece()),
                },
            6: {1: Square(6, 1, NoPiece()),
                2: Square(6, 2, NoPiece()),
                3: Square(6, 3, NoPiece()),
                4: Square(6, 4, NoPiece()),
                5: Square(6, 5, NoPiece()),
                6: Square(6, 6, NoPiece()),
                7: Square(6, 7, NoPiece()),
                8: Square(6, 8, King(is_white=False)),
                },
            5: {1: Square(5, 1, NoPiece()),
                2: Square(5, 2, NoPiece()),
                3: Square(5, 3, NoPiece()),
                4: Square(5, 4, NoPiece()),
                5: Square(5, 5, NoPiece()),
                6: Square(5, 6, NoPiece()),
                7: Square(5, 7, NoPiece()),
                8: Square(5, 8, NoPiece()),
                },
            4: {1: Square(4, 1, NoPiece()),
                2: Square(4, 2, NoPiece()),
                3: Square(4, 3, NoPiece()),
                4: Square(4, 4, NoPiece()),
                5: Square(4, 5, NoPiece()),
                6: Square(4, 6, NoPiece()),
                7: Square(4, 7, NoPiece()),
                8: Square(4, 8, NoPiece()),
                },
            3: {1: Square(3, 1, NoPiece()),
                2: Square(3, 2, NoPiece()),
                3: Square(3, 3, NoPiece()),
                4: Square(3, 4, NoPiece()),
                5: Square(3, 5, NoPiece()),
                6: Square(3, 6, NoPiece()),
                7: Square(3, 7, NoPiece()),
                8: Square(3, 8, NoPiece()),
                },
            2: {1: Square(2, 1, NoPiece()),
                2: Square(2, 2, NoPiece()),
                3: Square(2, 3, NoPiece()),
                4: Square(2, 4, NoPiece()),
                5: Square(2, 5, NoPiece()),
                6: Square(2, 6, NoPiece()),
                7: Square(2, 7, NoPiece()),
                8: Square(2, 8, Queen(is_white=False)),
                },
            1: {1: Square(1, 1, King(is_white=True)),
                2: Square(1, 2, NoPiece()),
                3: Square(1, 3, NoPiece()),
                4: Square(1, 4, NoPiece()),
                5: Square(1, 5, NoPiece()),
                6: Square(1, 6, NoPiece()),
                7: Square(1, 7, NoPiece()),
                8: Square(1, 8, NoPiece())
                }
        }


class Square(object):
    def __init__(self, rank, file, piece):
        self.__piece = piece
        self.__rank = rank
        self.__file = file

    @property
    def piece(self):
        return self.__piece

    @piece.setter
    def piece(self, value):
        self.__piece = value

    @property
    def rank(self):
        return self.__rank

    @rank.setter
    def rank(self, value):
        self.__rank = value

    @property
    def file(self):
        return self.__file

    @file.setter
    def file(self, value):
        self.__file = value

    def __str__(self):
        return "File-" + str(self.__file) + ": Rank-" + str(self.__rank)

    def __eq__(self, other_square):
        if other_square is None:
            return False
        if self.__file == other_square.file:
            if self.__rank == other_square.rank:
                return True
        return False


class Move(object):
    def __init__(self, player, move_from, move_to):
        self.__player = player
        self.__move_from = move_from
        self.__move_to = move_to
        self.__moved_piece = move_from.piece
        self.__killed_piece = None
        self.__castling_move = False
        self.__changed_initial_position = False
        self.__enables_en_passant = False
        self.__en_passant_move = False

    @property
    def castling_move(self):
        return self.__castling_move

    @castling_move.setter
    def castling_move(self, value):
        self.__castling_move = value

    @property
    def changed_initial_position(self):
        return self.__changed_initial_position

    @changed_initial_position.setter
    def changed_initial_position(self, value):
        self.__changed_initial_position = value

    @property
    def enables_en_passant(self):
        return self.__enables_en_passant

    @enables_en_passant.setter
    def enables_en_passant(self, value):
        self.__enables_en_passant = value

    @property
    def en_passant_move(self):
        return self.__en_passant_move

    @en_passant_move.setter
    def en_passant_move(self, value):
        self.__en_passant_move = value

    @property
    def moved_piece(self):
        return self.__moved_piece

    @property
    def move_from(self):
        return self.__move_from

    @property
    def move_to(self):
        return self.__move_to

    @property
    def killed_piece(self):
        return self.__killed_piece

    @killed_piece.setter
    def killed_piece(self, value):
        self.__killed_piece = value
