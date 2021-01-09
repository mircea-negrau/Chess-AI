import numpy
from domain.entities.pieces import NoPiece, Queen, Rook, Bishop, Knight


class EvaluationService:
    def __init__(self, move_generation_service):
        self._move_generation_service = move_generation_service
        self.piece_values = {'White Pawn': 10.0, 'Black Pawn': -10.0,
                             'White Knight': 32.0, 'Black Knight': -32.0,
                             'White Bishop': 33.0, 'Black Bishop': -33.0,
                             'White Rook': 50.0, 'Black Rook': -50.0,
                             'White Queen': 90.0, 'Black Queen': -90.0,
                             'White King': 2000.0, 'Black King': -2000.0}
        self.mobility = {
            "mid_game": {
                "knight": [-1.5, -0.5, -0.1, 0.2, 0.5, 0.7, 0.9, 1.1, 1.3],
                "bishop": [-2.5, -1.1, -0.6, -0.1, 0.3, 0.6, 0.9, 1.2, 1.4, 1.7, 1.9, 2.1, 2.3, 2.5],
                "rook": [-1.0, -0.4, -0.2, 0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 0.8, 0.9, 1.0, 1.1, 1.2],
                "queen": [-1.0, -0.6, -0.5, -0.4, -0.2, -0.2, -0.1, 0.0, 0.1, 0.2, 0.2, 0.3, 0.3, 0.4, 0.4, 0.5, 0.6,
                          0.6, 0.6, 0.7, 0.7, 0.8, 0.8, 0.9, 0.9, 1.0, 1.0, 1.0]
            },
            "end_game": {
                "knight": [-3.0, -1.0, -0.2, 0.4, 1.0, 1.4, 1.8, 2.2, 2.6],
                "bishop": [-5.0, -2.2, -1.1, -0.2, 0.6, 1.2, 1.8, 2.4, 2.9, 3.4, 3.8, 4.2, 4.6, 5.0],
                "rook": [-5.0, -2.2, -1.1, -0.2, 0.6, 1.2, 1.8, 2.4, 2.9, 3.4, 3.8, 4.2, 4.6, 5.0, 5.4],
                "queen": [-5.0, -3.0, -2.2, -1.6, -1.0, -0.6, -0.2, 0.2, 0.6, 1.0, 1.3, 1.6, 1.9, 2.2, 2.4, 2.7, 3.0,
                          3.2, 3.4, 3.7, 3.9, 4.1, 4.3, 4.5, 4.7, 5.0, 5.1, 5.3]
            }
        }
        self.position_values = {
            'Black Pawn': numpy.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                       [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                                       [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
                                       [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
                                       [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
                                       [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
                                       [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
                                       [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]),

            'Black Knight': numpy.array([[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                                         [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
                                         [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
                                         [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
                                         [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
                                         [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
                                         [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
                                         [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]),

            'Black Bishop': numpy.array([[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                                         [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                                         [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
                                         [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
                                         [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                                         [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
                                         [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
                                         [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]),

            'Black Rook': numpy.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                       [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
                                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                                       [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]]),

            'Black Queen': numpy.array([[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                                        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                                        [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                                        [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                                        [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                                        [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                                        [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
                                        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]),

            'Black King': numpy.array([[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                                       [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                                       [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                                       [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                                       [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                                       [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                                       [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
                                       [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]]),

            'White Pawn': numpy.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                       [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
                                       [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
                                       [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
                                       [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
                                       [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
                                       [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                                       [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]),

            'White Knight': numpy.array([[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                                         [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
                                         [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
                                         [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
                                         [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
                                         [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
                                         [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
                                         [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]),

            'White Bishop': numpy.array([[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                                         [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
                                         [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
                                         [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                                         [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
                                         [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
                                         [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                                         [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]),

            'White Rook': numpy.array([[0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0],
                                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                                       [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
                                       [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]),

            'White Queen': numpy.array([[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                                        [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
                                        [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                                        [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                                        [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                                        [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                                        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                                        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]),

            'White King': numpy.array([[2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0],
                                       [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
                                       [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                                       [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                                       [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                                       [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                                       [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                                       [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0]])
        }

    def evaluate_move(self, board):
        """
        Method to compute the evaluation of the current reached chessboard position.
        This method applies for each found piece on the chessboard the computation of its positional evaluation and
        mobility evaluation, which are added to the piece's value.
        The mobility of pieces is modified according to the reached game moment (endgame/mid-game).
        If the piece is a dark piece, the evaluation is made negative.
        The evaluation is rounded to 3 digits.
        :param board: Board, object recording the chessboard of the current position.
        :return: float, holding the value of the reached position's evaluation.
        """
        evaluation = 0
        chessboard = range(1, 9)
        occupied_squares, number_of_queens = self.get_pieces_and_number_of_queens(board, chessboard)
        for square_details in occupied_squares:
            square, rank, file, piece = square_details
            piece_name = str(square.piece)
            is_end_game = self.get_end_game_status(number_of_queens)
            score_sign = self.get_evaluation_score_sign(piece)
            position_value = score_sign * self.position_values[piece_name][square.rank - 1][8 - square.file]
            evaluation = self.get_mobility_score(evaluation, is_end_game, piece, score_sign, square)
            evaluation += self.piece_values[piece_name] + position_value
            evaluation = round(evaluation, 3)
        return evaluation

    def get_mobility_score(self, evaluation, is_end_game, piece, score_sign, square):
        """
        The method calls the adequate mobility score computation method according to the piece's type.
        (For a piece that is of type 'Rook', it calls the method that computes a rook's mobility score)
        This method returns the evaluation obtained from the called method.
        :param evaluation: float, holds the value of the evaluation obtained until now.
        :param is_end_game: bool, records whether or not the game has reached the endgame or not.
            (The endgame has been reached when there are no queens on the board)
        :param piece: Piece, object recording the details of the piece found placed on the given square.
        :param score_sign: integer, holding the value (1/-1) by which the evaluation will be multiplied.
            (If the current piece is dark, the score_sign is -1, otherwise 1)
        :param square: Square, object recording the details of the square on which the current piece is placed.
        :return: float, holding the value of the reached position's positional value and mobility value.
        """
        if isinstance(piece, Queen):
            evaluation = self.get_queen_mobility_score(evaluation, is_end_game, piece, score_sign, square)
        elif isinstance(piece, Rook):
            evaluation = self.get_rook_mobility_score(evaluation, is_end_game, piece, score_sign, square)
        elif isinstance(piece, Bishop):
            evaluation = self.get_bishop_mobility_score(evaluation, is_end_game, piece, score_sign, square)
        elif isinstance(piece, Knight):
            evaluation = self.get_knight_mobility_score(evaluation, is_end_game, piece, score_sign, square)
        return evaluation

    def get_knight_mobility_score(self, evaluation, is_end_game, piece, score_sign, square):
        """
        The method computes the current knight piece's mobility value according to the reached game moment
        (endgame/mid-game) and returns the value of the reached position's positional value and mobility value
        :param evaluation: float, holds the value of the evaluation obtained until now.
        :param is_end_game: bool, records whether or not the game has reached the endgame or not.
            (The endgame has been reached when there are no queens on the board)
        :param piece: Piece, object recording the details of the piece found placed on the given square.
        :param score_sign: integer, holding the value (1/-1) by which the evaluation will be multiplied.
            (If the current piece is dark, the score_sign is -1, otherwise 1)
        :param square: Square, object recording the details of the square on which the current piece is placed.
        :return: float, holding the value of the reached position's positional value and mobility value.
        """
        mobility = 0
        for _ in self._move_generation_service.get_all_knight_moves(piece, square):
            mobility += 1
        if is_end_game:
            evaluation += score_sign * self.mobility["end_game"]["knight"][mobility]
        else:
            evaluation += score_sign * self.mobility["mid_game"]["knight"][mobility]
        return evaluation

    def get_bishop_mobility_score(self, evaluation, is_end_game, piece, score_sign, square):
        """
        The method computes the current bishop piece's mobility value according to the reached game moment
        (endgame/mid-game) and returns the value of the reached position's positional value and mobility value
        :param evaluation: float, holds the value of the evaluation obtained until now.
        :param is_end_game: bool, records whether or not the game has reached the endgame or not.
            (The endgame has been reached when there are no queens on the board)
        :param piece: Piece, object recording the details of the piece found placed on the given square.
        :param score_sign: integer, holding the value (1/-1) by which the evaluation will be multiplied.
            (If the current piece is dark, the score_sign is -1, otherwise 1)
        :param square: Square, object recording the details of the square on which the current piece is placed.
        :return: float, holding the value of the reached position's positional value and mobility value.
        """
        mobility = 0
        for _ in self._move_generation_service.get_all_bishop_moves(piece, square):
            mobility += 1
        if is_end_game:
            evaluation += score_sign * self.mobility["end_game"]["bishop"][mobility]
        else:
            evaluation += score_sign * self.mobility["mid_game"]["bishop"][mobility]
        return evaluation

    def get_rook_mobility_score(self, evaluation, is_end_game, piece, score_sign, square):
        """
        The method computes the current rook piece's mobility value according to the reached game moment
        (endgame/mid-game) and returns the value of the reached position's positional value and mobility value
        :param evaluation: float, holds the value of the evaluation obtained until now.
        :param is_end_game: bool, records whether or not the game has reached the endgame or not.
            (The endgame has been reached when there are no queens on the board)
        :param piece: Piece, object recording the details of the piece found placed on the given square.
        :param score_sign: integer, holding the value (1/-1) by which the evaluation will be multiplied.
            (If the current piece is dark, the score_sign is -1, otherwise 1)
        :param square: Square, object recording the details of the square on which the current piece is placed.
        :return: float, holding the value of the reached position's positional value and mobility value.
        """
        mobility = 0
        for _ in self._move_generation_service.get_all_rook_moves(piece, square):
            mobility += 1
        if is_end_game:
            evaluation += score_sign * self.mobility["end_game"]["rook"][mobility]
        else:
            evaluation += score_sign * self.mobility["mid_game"]["rook"][mobility]
        return evaluation

    def get_queen_mobility_score(self, evaluation, is_end_game, piece, score_sign, square):
        """
        The method computes the current queen piece's mobility value according to the reached game moment
        (endgame/mid-game) and returns the value of the reached position's positional value and mobility value
        :param evaluation: float, holds the value of the evaluation obtained until now.
        :param is_end_game: bool, records whether or not the game has reached the endgame or not.
            (The endgame has been reached when there are no queens on the board)
        :param piece: Piece, object recording the details of the piece found placed on the given square.
        :param score_sign: integer, holding the value (1/-1) by which the evaluation will be multiplied.
            (If the current piece is dark, the score_sign is -1, otherwise 1)
        :param square: Square, object recording the details of the square on which the current piece is placed.
        :return: float, holding the value of the reached position's positional value and mobility value.
        """
        mobility = 0
        for _ in self._move_generation_service.get_all_queen_moves(piece, square):
            mobility += 1
        evaluation += score_sign * self.mobility["mid_game"]["queen"][mobility]
        return evaluation

    @staticmethod
    def get_evaluation_score_sign(piece):
        """
        Method to get the sign of the evaluation.
        If the current piece is dark, the evaluation score sign will be -1, otherwise it will be 1.
        :param piece: Piece, object recording the details of the piece found placed on the given square.
        :return: integer, holding the value (1/-1) by which the evaluation will be multiplied.
        """
        score_sign = -1
        if piece.is_white:
            score_sign = 1
        return score_sign

    @staticmethod
    def get_end_game_status(number_of_queens):
        """
        Method to compute whether or not the reached chessboard position is in the endgame.
            (The endgame has been reached when there are no queens on the board)
        :param number_of_queens:
        :return: bool, records whether or not the game has reached the endgame or not.
        """
        is_end_game = True
        if number_of_queens > 0:
            is_end_game = False
        return is_end_game

    @staticmethod
    def get_pieces_and_number_of_queens(board, chessboard):
        """
        Method to identify all the pieces on the chessboard and count the number of queens found among the pieces.
        :param board: Board, object recording the chessboard of the current position.
        :param chessboard: range, holding the range of the ranks and files of a chessboard (1->8)
        :return: List, containing the pieces found on the chessboard; integer, containing the number of queens found on
        the chessboard.
        """
        pieces = []
        queens = 0
        for rank in chessboard:
            for file in chessboard:
                square = board.get_square(rank, file)
                if square is not None:
                    piece = square.piece
                    if not isinstance(piece, NoPiece):
                        pieces.append([square, rank, file, piece])
                        if isinstance(piece, Queen):
                            queens += 1
        return pieces, queens
