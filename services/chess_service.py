import pygame

from domain.entities.board import Board
from services.evaluation_service import EvaluationService
from services.move_generation_service import MoveGenerationService
from services.move_service import MoveService


class Game:
    def __init__(self, white_player, black_player, depth, board_type="Normal"):
        self.__board = Board(board_type)
        self._move_generation_service = MoveGenerationService(self)
        self._evaluation_service = EvaluationService(self._move_generation_service)
        self._move_service = MoveService(self, self._move_generation_service, self._evaluation_service)
        self.__game_status = "ACTIVE"
        self.__white_player = white_player
        self.__black_player = black_player
        self.__depth = depth
        self.__current_player = self.__white_player

    @property
    def current_player(self):
        return self.__current_player

    @current_player.setter
    def current_player(self, value):
        self.__current_player = value

    @property
    def white_player(self):
        return self.__white_player

    @white_player.setter
    def white_player(self, value):
        self.__white_player = value

    @property
    def black_player(self):
        return self.__black_player

    @black_player.setter
    def black_player(self, value):
        self.__black_player = value

    @property
    def board(self):
        return self.__board

    @property
    def game_status(self):
        return self.__game_status

    @game_status.setter
    def game_status(self, value):
        self.__game_status = value

    @property
    def depth(self):
        return self.__depth

    @depth.setter
    def depth(self, value):
        self.__depth = value

    def get_next_player_turn(self):
        """
        Method to set the current player variable of the game to the next player.
        If the previous player was the player playing the black pieces, the next one is the one with the white pieces.
        If the previous player was the player playing the white pieces, the next one is the one with the black pieces.
        :return:
        """
        if self.current_player == self.__white_player:
            self.current_player = self.__black_player
        else:
            self.current_player = self.__white_player

    def get_computer_move(self):
        """
        Method to get the computer's move.
        This method is a connector between the UI/GUI and the chess move service.
        """
        return self._move_service.get_computer_move_applied()

    def get_human_move(self, player, source_rank, source_file, destination_rank, destination_file):
        """
        Method to get the player's move applied.
        The source and destination parameters represent the square's coordinates on the chessboard. The source square
        is the square from which a piece is raised and the destination square is the square to which the raised piece is
        placed.
        The method returns whether or not the move has been applied successfully (True/False).
        :param player: Player, holds the Player object value of the player performing the move.
        :param source_rank: integer, between 1 and 8, holds the value of the initial square's rank value.
        :param source_file: integer, between 1 and 8, holds the value of the initial square's file value.
        :param destination_rank: integer, between 1 and 8, holds the value of the target square's rank value.
        :param destination_file: integer, between 1 and 8, holds the value of the target square's file value.
        :return: True/False, according to whether or not the move has been applied successfully.
        """
        return self._move_service.get_human_move_applied(player, source_rank, source_file, destination_rank,
                                                         destination_file)

    def get_undo_performed(self):
        """
        Method to get the previous move undone.
        This method is a connector between the UI/GUI and the chess undo move service.
        """
        self._move_service.undo_move()

    def get_double_undo_performed(self):
        """
        Method to undo the last two moves that altered the chessboard.
        """
        self._move_service.get_double_undo_performed()

    def get_game_status(self):
        """
        Method to return whether the status of the game is active or not.
        For the "CHECKMATE" and "STALEMATE" statuses, the method returns False.
        For the "ACTIVE" status, the method returns True.
        The method checks all the possible moves of the current player in the reached position of the board.
        If at least a valid move is found, the game is not over, so the game status is "ACTIVE".
        If no valid move is found, the method checks if in the reached position the current player's king is attacked.
        If the king is attacked, the position is a "CHECKMATE" position.
        Otherwise, the position is a "STALEMATE" position. In both of the above cases, the method returns False.
        :return: True/False, according to the game status.
        """
        current_player = self.current_player
        for move in self._move_generation_service.get_all_moves(self.board):
            if move.moved_piece.is_white == current_player.is_white:
                available_move_exists = self._move_service.get_move_applied(move.moved_piece, move, current_player)
                if available_move_exists:
                    self._move_service.undo_move()
                    self.__game_status = "ACTIVE"
                    return True
        self.get_next_player_turn()
        if self._move_service.is_in_check():
            self.__game_status = "CHECKMATE"

            self.get_next_player_turn()
            return False
        self.__game_status = "STALEMATE"

        self.get_next_player_turn()
        return False

    def is_move_not_king_suicide(self, move):
        """
        Method to check whether or not the move will leave the player's king defenseless next turn, leading to its
        capture (invalid move).
        :param move: Move, object recording details about the move to be checked.
        :return: True/False, according to the validity of the move
        """
        if self._move_service.get_move_applied(move.moved_piece, move, self.__current_player):
            self.get_undo_performed()
            return True
        return False

    def get_game_status_updated_as_active(self):
        """
        Method to set the game status as active.
        Used when the game ended (checkmate or stalemate) and the human player performs an undo operation,
        thus getting out of the game-ending position and the game becoming once again active.
        """
        if self.game_status != "ACTIVE":
            self.game_status = "ACTIVE"
            self.get_next_player_turn()

    def get_all_valid_moves_of_square(self, square):
        """
        Method to yield all the valid moves of the piece found on the chessboard at the given square.
        Method is used in the interface to highlight the piece's possible moves.
        :param square: Square, object of the chessboard from which the piece's moves are checked.
        :return: Move, object recording a valid move of the given square's piece.
        """
        yield from self._move_generation_service.get_all_valid_moves_of_square(square)

    def get_last_move(self):
        """
        Method to return the last applied move of the chessboard.
        This method is a connector between the UI/GUI and the chess move service.
        :return: Move, object recording the last performed move of the chess game.
        """
        return self._move_service.get_last_move()
