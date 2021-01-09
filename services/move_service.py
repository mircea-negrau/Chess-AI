from domain.entities.board import Move
from domain.entities.pieces import King, NoPiece, Pawn, Rook, Queen
from services.computer_move_service import ComputerMoveService
from services.move_validation_service import MoveValidationService
from services.undo_move_service import UndoMoveService


class MoveService:
    def __init__(self, game, generation_service, evaluation_service):
        self.__game = game
        self.__moves_played = []
        self.__white_king = (1, 5)
        self.__black_king = (8, 5)
        self._validation_service = MoveValidationService(game)
        self._move_generation_service = generation_service
        self._computer_move_service = ComputerMoveService(game, self._move_generation_service, evaluation_service, self)
        self._undo_move_service = UndoMoveService(game, self.__moves_played, self)

    @property
    def white_king(self):
        return self.__white_king

    @property
    def black_king(self):
        return self.__black_king

    @white_king.setter
    def white_king(self, value):
        self.__white_king = value

    @black_king.setter
    def black_king(self, value):
        self.__black_king = value

    def get_human_move_applied(self, player, current_rank, current_file, target_rank, target_file):
        """
        Method to get the player's move applied.
        The source and destination parameters represent the square's coordinates on the chessboard. The source square
        is the square from which a piece is raised and the destination square is the square to which the raised piece is
        placed.
        The method returns whether or not the move has been applied successfully (True/False).
        :param player: Player, holds the Player object value of the player performing the move.
        :param current_rank: integer, between 1 and 8, holds the value of the initial square's rank value.
        :param current_file: integer, between 1 and 8, holds the value of the initial square's file value.
        :param target_rank: integer, between 1 and 8, holds the value of the target square's rank value.
        :param target_file: integer, between 1 and 8, holds the value of the target square's file value.
        :return: True/False, according to whether or not the move has been applied successfully.
        """
        current_position = self.__game.board[current_rank][current_file]
        target_position = self.__game.board[target_rank][target_file]
        move = Move(player, current_position, target_position)
        return self.get_move_tested(move, player)

    def get_computer_move_applied(self):
        """
        Method to get the computer's move applied.
        The method obtains the best move available for the computer in the given chessboard position and applies it.
        :return: True/False, according to whether or not the move has been applied successfully.
            (The return will always be True, unless the program malfunctions)
        """
        best_move = self._computer_move_service.get_minimax(self.__game.depth)
        return self.get_move_tested(best_move, self.__game.current_player)

    def get_move_tested(self, move, player):
        """
        Method to get the move tested for inconsistencies.
        If any criteria is not met, the move does not pass the test, nothing gets applied to the chessboard and the
        method returns False.
        :param move: Move, object recording details about the move to be tested.
        :param player: Player, holds the Player object value of the player performing the move.
        :return: True/False, according to whether or not the move has been applied successfully.
        """
        piece = move.moved_piece
        player_next_to_move = player is self.__game.current_player
        if not player_next_to_move:
            return False
        square_to_move_from_is_empty = isinstance(piece, NoPiece)
        if square_to_move_from_is_empty:
            return False
        player_owns_piece = piece.is_white == player.is_white
        if not player_owns_piece:
            return False
        move_is_valid = self._validation_service.is_valid_move(piece, move.move_from, move.move_to)
        if not move_is_valid:
            return False
        moved_piece_is_the_king = piece is not None and isinstance(piece, King)
        if moved_piece_is_the_king:
            if not self.get_validity_of_castling_move(move, piece, player):
                return False
        return self.get_move_applied(piece, move, player)

    def get_move_applied(self, piece, move, player):
        """
        Method to apply the move after the initial tests have been passed.
        This method is calling step by step all the possible actions required for the move to be completely applied.
        If in the end, the move does not pass the last test, the method returns False.
        :param piece: Piece, object recording details about the piece that is being moved.
        :param move: Move, object recording details about the move to be performed.
        :param player: Player, holds the Player object value of the player performing the move.
        :return: True/False, whether or not the move was applied.
        """
        self.get_captured_piece(move)
        self.get_castling_move_applied(move, piece, player)
        self.__moves_played.append(move)
        self.get_en_passant_capture(move)
        self.get_normal_move_applied(move, piece)
        self.get_special_moves_applied(move, piece)
        return self.get_if_move_is_safe_from_self_checking()

    def undo_move(self):
        """
        Method to undo the previous move that altered the chessboard.
        """
        self._undo_move_service.undo_move()

    def get_double_undo_performed(self):
        """
        Method to undo the last two moves that altered the chessboard.
        """
        self._undo_move_service.get_double_undo_applied()

    def get_special_moves_applied(self, move, piece):
        """
        Method to apply the special cases of the pawn two step move, the pawn promotion, the rook initial move, the king
        initial move.
        If the moved piece is a pawn, its initial square gets changed so it can no longer take two steps and if it
        reached the promotion zone, the piece becomes a queen. If the move is the two step move, the pawn moves two
        steps forward.
        If the moved piece is a rook, it can no longer partake in castling.
        If the moved piece is a king, it can no longer partake in castling.
        :param move: Move, object recording details about the move to be performed.
        :param piece: Piece, object recording details about the piece that is being moved.
        """
        piece_is_pawn = isinstance(piece, Pawn)
        piece_is_rook = isinstance(piece, Rook)
        piece_is_king = isinstance(piece, King)
        if piece_is_pawn:
            pawn_is_on_initial_square = piece.initial_square
            pawn_reached_promotion = (move.move_to.rank == 8 and piece.is_white) or (
                    move.move_to.rank == 1 and not piece.is_white)

            if pawn_is_on_initial_square:
                self.get_pawn_two_step_move_applied(move, piece)
            elif pawn_reached_promotion:
                move.move_to.piece = Queen(piece.is_white)
        elif piece_is_rook:
            if piece.can_castle:
                piece.can_castle = False
                move.changed_initial_position = True
        elif piece_is_king:
            piece.can_castle = False

    def get_normal_move_applied(self, move, piece):
        """
        Method to apply the normal case of moves: the piece moves from its initial square and gets placed on its
        target square, eventually capturing the opponent's piece if possible. The 'en passant' move is no longer
        available and the 'en passant' coordinates of the board are erased.
        :param move: Move, object recording details about the move to be performed.
        :param piece: Piece, object recording details about the piece that is being moved.
        """
        board = self.__game.board
        move.move_to.piece = piece
        move.move_from.piece = NoPiece()
        move.enables_en_passant = False
        board.available_en_passant = False

    def get_pawn_two_step_move_applied(self, move, piece):
        """
        Method to apply the special case of the pawn's two steps forward move.
        If the pawn only moves forward (does not capture anything), an 'en passant' move becomes available for the
        opponent's next move on the pawn's coordinates, with the rank being increased by 1 in the direction the pawn is
        headed.
        :param move: Move, object recording details about the move to be performed.
        :param piece: Pawn, object recording details about the pawn that is being moved.
        """
        board = self.__game.board
        piece.initial_square = False
        pawn_does_not_move_horizontally = move.move_to.file - move.move_from.file == 0
        if pawn_does_not_move_horizontally:
            pawn_moves_forward_two_steps = abs(move.move_from.rank - move.move_to.rank) == 2
            if pawn_moves_forward_two_steps:
                if piece.is_white:
                    en_passant_move = (move.move_from.rank + 1, move.move_to.file)
                    move.enables_en_passant = en_passant_move
                    board.available_en_passant = en_passant_move
                else:
                    en_passant_move = (move.move_from.rank - 1, move.move_to.file)
                    move.enables_en_passant = en_passant_move
                    board.available_en_passant = en_passant_move
        move.changed_initial_position = True

    def get_en_passant_capture(self, move):
        """
        Method to perform the 'en passant' capture of a pawn.
        The position of the pawn's target square minus a rank in the direction the pawn is headed clears and the pawn
        found there becomes captured.
        :param move: Move, object recording details about the move to be performed.
        """
        board = self.__game.board
        if move.en_passant_move:
            if move.moved_piece.is_white:
                board.get_square(move.move_to.rank - 1, move.move_to.file).piece = NoPiece()
            else:
                board.get_square(move.move_to.rank + 1, move.move_to.file).piece = NoPiece()

    def get_validity_of_castling_move(self, move, piece, player):
        """
        Method to check whether or not the given castling move is a valid one or not.
        If the king moves horizontally, the king can castle and the move is a castling move, the method checks whether
        or not the king is currently in check. If he is, the castling can not take place.
        Otherwise, if the castling take place to the right of the board, it is a short castling move.
        Otherwise, it is a long castling move.
        For each of the castling move's position that the king traverses, the method checks whether or not the king
        would find himself in check. If he would, the move is no a valid move and the method returns False.
        Otherwise, the move is a valid move and the method returns True.
        :param move: Move, object recording details about the move to be validated.
        :param piece: King, object recording details about the king that is being moved.
        :param player: Player, holds the Player object value of the player performing the move.
        :return:
        """
        king_moves_horizontally = move.move_to.rank - move.move_from.rank == 0
        king_castles = abs(move.move_to.file - move.move_from.file) in [2, 3]
        board = self.__game.board
        if piece.can_castle and king_moves_horizontally and king_castles:
            self.__game.get_next_player_turn()
            if self.is_in_check():
                self.__game.get_next_player_turn()
                return False

            self.__game.get_next_player_turn()
            short_castle = move.move_from.file < move.move_to.file
            if short_castle:
                from_square = board.get_square(move.move_from.rank, move.move_from.file)
                to_square = board.get_square(move.move_from.rank, move.move_from.file + 1)
                first_step = Move(player, from_square, to_square)
                if not self.get_move_applied(piece, first_step, player):
                    return False
                self._undo_move_service.undo_move()
            else:
                from_square = board.get_square(move.move_from.rank, move.move_from.file)
                to_square = board.get_square(move.move_from.rank, move.move_from.file - 1)
                first_step = Move(player, from_square, to_square)
                if not self.get_move_applied(piece, first_step, player):
                    return False
                else:
                    from_square = board.get_square(move.move_from.rank, move.move_from.file - 1)
                    to_square = board.get_square(move.move_from.rank, move.move_from.file - 2)
                    second_step = Move(player, from_square, to_square)
                    self.__game.get_next_player_turn()
                    if not self.get_move_applied(piece, second_step, player):
                        self._undo_move_service.undo_move()
                        self.__game.get_next_player_turn()
                        return False
                    self.__game.get_next_player_turn()
                self._undo_move_service.undo_move()
                self._undo_move_service.undo_move()
        return True

    def get_castling_move_applied(self, move, piece, player):
        """
        Method to perform the castling of the king and rook.
        If the moved piece is the king, the king's position becomes updated.
        If the king can castle and the king moves horizontally and the move is a castling move, the method performs the
        castling move.
        :param move: Move, object recording details about the move to be performed.
        :param piece: King, object recording details about the king that is being moved.
        :param player: Player, holds the Player object value of the player performing the move.
        """
        moved_piece_is_the_king = piece is not None and isinstance(piece, King)
        if moved_piece_is_the_king:
            self.get_king_position_updated(move, piece)
            king_moves_horizontally = move.move_to.rank - move.move_from.rank == 0
            king_castles = abs(move.move_to.file - move.move_from.file) in [2, 3]
            if piece.can_castle and king_moves_horizontally and king_castles:
                self.get_rook_castling_move_applied(move, player)
            if piece.can_castle:
                piece.can_castle = False
                move.changed_initial_position = True

    def get_rook_castling_move_applied(self, move, player):
        """
        Method to perform the movement of the rook in the castling move.
        The rook gets placed to the target square and its initial square gets cleared.
        :param move: Move, object recording details about the move to be performed.
        :param player: Player, holds the Player object value of the player performing the castling.
        """
        move.castling_move = True
        move_for_rook_in_castling = self.get_rook_move_for_castling(move, player)
        self.__moves_played.append(move_for_rook_in_castling)
        move_for_rook_in_castling.move_to.piece = move_for_rook_in_castling.moved_piece
        move_for_rook_in_castling.move_from.piece = NoPiece()
        move_for_rook_in_castling.move_to.piece.can_castle = False

    def get_rook_move_for_castling(self, move, player):
        """
        Method to get the rook's Move object so that the castling move is properly applied.
        If the castling is a short castling, the rook slides to the right of the chessboard by two squares.
        Otherwise, the rooks slides to the left of the chessboard by three squares.
        :param move: Move, object recording details about the move to be performed.
        :param player: Player, holds the Player object value of the player performing the castling.
        :return: Move, object recording details about the rook's castling move to be performed.
        """
        board = self.__game.board
        short_castle = move.move_from.file < move.move_to.file
        if short_castle:
            new_move_from = board.get_square(move.move_from.rank, move.move_from.file + 3)
            new_move_to = board.get_square(move.move_from.rank, move.move_from.file + 1)
        else:
            new_move_from = board.get_square(move.move_from.rank, move.move_from.file - 4)
            new_move_to = board.get_square(move.move_from.rank, move.move_from.file - 1)
        new_move = Move(player, new_move_from, new_move_to)
        return new_move

    def get_king_position_updated(self, move, piece):
        """
        Method to update the position of the king after its movement.
        :param move: Move, object recording details about the move that was performed.
        :param piece: King, object recording details about the king that is being moved.
        """
        if piece.is_white:
            self.__white_king = (move.move_to.rank, move.move_to.file)
        else:
            self.__black_king = (move.move_to.rank, move.move_to.file)

    def get_captured_piece(self, move):
        """
        Method to obtain the captured piece from the target square of the move.
        If the destination square of the move has a piece, the method checks whether or not the piece performing the
        capturing is a Pawn or not.
        If the piece is a pawn, a special method is called for it.
        For any other type of piece, the method calls the usual method.
        :param move: Move, object recording details about the move that was performed.
        """
        destination_has_piece = move.move_to.piece is not None
        if destination_has_piece:
            piece_to_move_is_pawn = isinstance(move.move_from.piece, Pawn)
            if not piece_to_move_is_pawn:
                self.get_captured_piece_for_usual_method(move)
            else:
                self.get_captured_piece_for_pawn_captures(move)

    def get_captured_piece_for_pawn_captures(self, move):
        """
        Method to obtain the piece captured by the pawn during the given move.
        If the target square of the pawn is an empty square, it means the capture is an 'en passant' capture, so the
        square found below the target square is being emptied and the piece found there becomes captured.
        Otherwise, the piece found on the target square becomes captured.
        The coordinates of the capture become registered in the move's attributes.
        :param move: Move, object recording details about the move that will be performed.
        """
        board = self.__game.board
        pawn_advances_forward_one_step = abs(move.move_to.file - move.move_from.file) == 1
        pawn_advances_horizontally_one_step = abs(move.move_from.rank - move.move_to.rank) == 1
        pawn_captures = pawn_advances_forward_one_step and pawn_advances_horizontally_one_step
        if pawn_captures:
            captured_square_is_empty = isinstance(move.move_to.piece, NoPiece)
            if captured_square_is_empty:
                move.en_passant_move = True
                moved_piece_is_white = move.moved_piece.is_white
                if moved_piece_is_white:
                    killed_rank = move.move_to.rank - 1
                    killed_file = move.move_to.file
                    killed_square = board.get_square(killed_rank, killed_file)
                    opposite_piece = killed_square.piece
                else:
                    opposite_piece = board.get_square(move.move_to.rank + 1, move.move_to.file).piece
                opposite_piece.is_dead = True
                move.killed_piece = opposite_piece
            else:
                self.get_captured_piece_for_usual_method(move)

    def is_in_check(self):
        """
        Method to check whether or not after performing a move, the previous player is still in check (invalid move).
        For each of the available move of the next player's piece, the method checks if it attacks the player's king.
        If such a move is found, the method returns True, indicating that the previously made move is an invalid one,
        the king being in check.
        Otherwise, the method returns False.
        :return:
        """
        king = self.__white_king
        player = self.__game.current_player
        if player.is_white is True:
            king = self.__black_king
        for move in self._move_generation_service.get_all_moves(self.__game.board):
            if move.moved_piece.is_white == player.is_white:
                if move.move_to.rank == king[0] and move.move_to.file == king[1]:
                    return True
        return False

    def get_if_move_is_safe_from_self_checking(self):
        """
        Method to check whether or not the previously performed move does not lead to the current player being in check.
        If the move is not a safe one (the king is in check), the method returns False, otherwise it returns True.
        :return:
        """
        self.__game.get_next_player_turn()
        if self.is_in_check():
            self._undo_move_service.undo_move()
            return False
        return True

    def get_last_move(self):
        return self.__moves_played[-1]

    def get_moves_played(self):
        return self.__moves_played

    @staticmethod
    def get_captured_piece_for_usual_method(move):
        """
        Method to obtain the captured piece of a move, in the case that the moved piece is not a pawn.
        :param move: Move, object recording details about the move that will be performed.
        """
        opposite_piece = move.move_to.piece
        opposite_piece.is_dead = True
        move.killed_piece = opposite_piece
