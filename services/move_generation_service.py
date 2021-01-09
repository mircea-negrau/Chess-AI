from domain.entities.board import Move
from domain.entities.pieces import *
from services.move_validation_service import MoveValidationService


class MoveGenerationService:
    def __init__(self, game):
        self.__game = game
        self._validation_service = MoveValidationService(game)

    def get_all_moves(self, board):
        """
        Method to yield all the valid moves of the pieces found on the given chessboard.
        :param board: Board, object recording the chessboard of the current position.
        :return: Move, object recording a valid move of the given chessboard's available pieces.
        """
        chessboard = range(1, 9)
        for rank in chessboard:
            for file in chessboard:
                square = board.get_square(rank, file)
                yield from self.get_all_valid_moves_of_square(square)

    def get_all_valid_moves_of_square(self, square):
        """
        Method to yield all the valid moves of a given square of a chessboard.
        This method chooses the adequate method to yield from, according to the square's piece type.
        :param square: Square, object of the chessboard from which the piece's moves are checked.
        :return: Move, object recording a valid move of the given square's piece.
        """
        piece = square.piece
        if isinstance(piece, Pawn) and piece.is_white == self.__game.current_player.is_white:
            yield from self.get_all_pawn_moves(piece, square)
        elif isinstance(piece, Knight) and piece.is_white == self.__game.current_player.is_white:
            yield from self.get_all_knight_moves(piece, square)
        elif isinstance(piece, Bishop) and piece.is_white == self.__game.current_player.is_white:
            yield from self.get_all_bishop_moves(piece, square)
        elif isinstance(piece, Rook) and piece.is_white == self.__game.current_player.is_white:
            yield from self.get_all_rook_moves(piece, square)
        elif isinstance(piece, Queen) and piece.is_white == self.__game.current_player.is_white:
            yield from self.get_all_queen_moves(piece, square)
        elif isinstance(piece, King) and piece.is_white == self.__game.current_player.is_white:
            yield from self.get_all_king_moves(piece, square)

    def get_all_king_moves(self, piece, square):
        """
        Method to yield all the available moves of a king piece from a given chessboard square.
        :param piece: King, object recording details about the king piece whose moves are to be yielded.
        :param square: Square, object of the chessboard where the king piece is placed.
        :return: Move, object recording a valid move of the given king.
        """
        board = self.__game.board
        player = self.__game.current_player
        moves = [board.get_square(square.rank + 1, square.file),
                 board.get_square(square.rank - 1, square.file),
                 board.get_square(square.rank, square.file + 1),
                 board.get_square(square.rank, square.file - 1),
                 board.get_square(square.rank + 1, square.file + 1),
                 board.get_square(square.rank + 1, square.file - 1),
                 board.get_square(square.rank - 1, square.file + 1),
                 board.get_square(square.rank - 1, square.file - 1),
                 board.get_square(square.rank, square.file - 2),
                 board.get_square(square.rank, square.file + 2)]
        for move in moves:
            target_square = move
            if target_square is not None and self._validation_service.is_valid_move(piece, square, target_square):
                yield Move(player, square, target_square)

    def get_all_queen_moves(self, piece, square):
        """
        Method to yield all the available moves of a queen piece from a given chessboard square.
        :param piece: Queen, object recording details about the queen piece whose moves are to be yielded.
        :param square: Square, object of the chessboard where the queen piece is placed.
        :return: Move, object recording a valid move of the given queen.
        """
        yield from self.get_all_diagonal_moves(piece, square)
        yield from self.get_all_vertical_moves(piece, square)
        yield from self.get_all_horizontal_moves(piece, square)

    def get_all_rook_moves(self, piece, square):
        """
        Method to yield all the available moves of a rook piece from a given chessboard square.
        :param piece: Rook, object recording details about the rook piece whose moves are to be yielded.
        :param square: Square, object of the chessboard where the rook piece is placed.
        :return: Move, object recording a valid move of the given rook.
        """
        yield from self.get_all_vertical_moves(piece, square)
        yield from self.get_all_horizontal_moves(piece, square)

    def get_all_bishop_moves(self, piece, square):
        """
        Method to yield all the available moves of a bishop piece from a given chessboard square.
        :param piece: Bishop, object recording details about the bishop piece whose moves are to be yielded.
        :param square: Square, object of the chessboard where the bishop piece is placed.
        :return: Move, object recording a valid move of the given bishop.
        """
        yield from self.get_all_diagonal_moves(piece, square)

    def get_all_knight_moves(self, piece, square):
        """
        Method to yield all the available moves of a knight piece from a given chessboard square.
        :param piece: Knight, object recording details about the knight piece whose moves are to be yielded.
        :param square: Square, object of the chessboard where the knight piece is placed.
        :return: Move, object recording a valid move of the given knight.
        """
        board = self.__game.board
        player = self.__game.current_player
        moves = [board.get_square(square.rank + 2, square.file + 1),
                 board.get_square(square.rank + 2, square.file - 1),
                 board.get_square(square.rank + 1, square.file - 2),
                 board.get_square(square.rank + 1, square.file + 2),
                 board.get_square(square.rank - 1, square.file - 2),
                 board.get_square(square.rank - 1, square.file + 2),
                 board.get_square(square.rank - 2, square.file - 1),
                 board.get_square(square.rank - 2, square.file + 1)]
        for move in moves:
            target_square = move
            if target_square is not None and self._validation_service.is_valid_move(piece, square, target_square):
                yield Move(player, square, target_square)

    def get_all_pawn_moves(self, piece, square):
        """
        Method to yield all the available moves of a pawn piece from a given chessboard square.
        :param piece: Pawn, object recording details about the pawn piece whose moves are to be yielded.
        :param square: Square, object of the chessboard where the pawn piece is placed.
        :return: Move, object recording a valid move of the given pawn.
        """
        board = self.__game.board
        player = self.__game.current_player
        if self.__game.current_player.is_white:
            moves = [board.get_square(square.rank + 1, square.file),
                     board.get_square(square.rank + 2, square.file),
                     board.get_square(square.rank + 1, square.file + 1),
                     board.get_square(square.rank + 1, square.file - 1)]
        else:
            moves = [board.get_square(square.rank - 1, square.file),
                     board.get_square(square.rank - 2, square.file),
                     board.get_square(square.rank - 1, square.file - 1),
                     board.get_square(square.rank - 1, square.file + 1)]
        for move in moves:
            target_square = move
            if target_square is not None and self._validation_service.is_valid_move(piece, square, target_square):
                yield Move(player, square, target_square)

    def get_all_horizontal_moves(self, piece, square):
        """
        Method to compute all the valid horizontal moves of a given piece of a given square from the chessboard.
        :param piece: Piece, object recording details about the piece whose moves are to be yielded.
        :param square: Square, object of the chessboard where the piece is placed.
        :return: Move, object recording a valid horizontal move of the given piece.
        """
        board = self.__game.board
        player = self.__game.current_player
        index = 0
        running = True
        while running:
            index += 1
            target_square = board.get_square(square.rank, square.file + index)
            if target_square is not None and self._validation_service.is_valid_move(piece, square, target_square):
                yield Move(player, square, target_square)
            else:
                running = False
        index = 0
        running = True
        while running:
            index += 1
            target_square = board.get_square(square.rank, square.file - index)
            if target_square is not None and self._validation_service.is_valid_move(piece, square, target_square):
                yield Move(player, square, target_square)
            else:
                running = False

    def get_all_vertical_moves(self, piece, square):
        """
        Method to compute all the valid vertical moves of a given piece of a given square from the chessboard.
        :param piece: Piece, object recording details about the piece whose moves are to be yielded.
        :param square: Square, object of the chessboard where the piece is placed.
        :return: Move, object recording a valid vertical move of the given piece.
        """
        board = self.__game.board
        player = self.__game.current_player
        index = 0
        running = True
        while running:
            index += 1
            target_square = board.get_square(square.rank + index, square.file)
            if target_square is not None and self._validation_service.is_valid_move(piece, square, target_square):
                yield Move(player, square, target_square)
            else:
                running = False
        index = 0
        running = True
        while running:
            index += 1
            target_square = board.get_square(square.rank - index, square.file)
            if target_square is not None and self._validation_service.is_valid_move(piece, square, target_square):
                yield Move(player, square, target_square)
            else:
                running = False

    def get_all_diagonal_moves(self, piece, square):
        """
        Method to compute all the valid diagonal moves of a given piece of a given square from the chessboard.
        :param piece: Piece, object recording details about the piece whose moves are to be yielded.
        :param square: Square, object of the chessboard where the piece is placed.
        :return: Move, object recording a valid diagonal move of the given piece.
        """
        board = self.__game.board
        player = self.__game.current_player
        index = 0
        running = True
        while running:
            index += 1
            target_square = board.get_square(square.rank + index, square.file + index)
            if target_square is not None and self._validation_service.is_valid_move(piece, square, target_square):
                yield Move(player, square, target_square)
            else:
                running = False
        index = 0
        running = True
        while running:
            index += 1
            target_square = board.get_square(square.rank - index, square.file + index)
            if target_square is not None and self._validation_service.is_valid_move(piece, square, target_square):
                yield Move(player, square, target_square)
            else:
                running = False
        index = 0
        running = True
        while running:
            index += 1
            target_square = board.get_square(square.rank + index, square.file - index)
            if target_square is not None and self._validation_service.is_valid_move(piece, square, target_square):
                yield Move(player, square, target_square)
            else:
                running = False
        index = 0
        running = True
        while running:
            index += 1
            target_square = board.get_square(square.rank - index, square.file - index)
            move_is_okay = target_square is not None and self._validation_service.is_valid_move(piece, square, target_square)
            if move_is_okay:
                yield Move(player, square, target_square)
            else:
                running = False
