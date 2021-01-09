from domain.entities.pieces import NoPiece, Rook, Pawn, King


class UndoMoveService:
    def __init__(self, game, moves_played, move_service):
        self.__game = game
        self.__moves_played = moves_played
        self.__move_service = move_service

    def get_double_undo_applied(self):
        """
        Method to undo the last two performed moves on the chessboard if any of the players are human.
        Otherwise, the method applies once the undo.
        """
        first_player, second_player = self.__game.white_player, self.__game.black_player
        if not first_player.is_human or not second_player.is_human:
            self.undo_move()
            self.undo_move()
        else:
            self.undo_move()

    def undo_move(self):
        """
        Method to restore the chessboard position reached before the last move was applied.
        If any special cases were applied previously, they are properly restored to their initial stance.
        The target square's piece is replaced with its previous value.
        The initial square's piece is replaced with its previous value.
        The captured piece is liberated.
        The 'en passant' special case is restored to its proper value.
        If the game ended on last move, the game is set as "ACTIVE" once again.
        """
        moves_to_undo = len(self.__moves_played) != 0
        if moves_to_undo:
            move = self.__moves_played.pop()
            piece = move.moved_piece
            move.move_to.piece = NoPiece()
            self.undo_capture_if_possible(move)
            move.move_from.piece = piece
            self.__game.get_next_player_turn()
            self.undo_special_move_ability_if_possible(move, piece)
            self.get_board_en_passant_availability_updated()
            self.__game.get_game_status_updated_as_active()

    def get_board_en_passant_availability_updated(self):
        """
        Method to update the 'en passant' ability on the chessboard to the value it has before the previously applied
        move that altered the chessboard.
        """
        previous_move_exists = len(self.__moves_played)
        if previous_move_exists:
            previous_move = self.__moves_played[-1]
            previous_en_passant = previous_move.enables_en_passant
            self.__game.board.available_en_passant = previous_en_passant

    def undo_special_move_ability_if_possible(self, move, piece):
        """
        Method to restore any special moves that were applied in the last move that altered the chessboard.
        If the rook or king were able to castle initially, they are allowed once again.
        If the pawn was able to advance two steps initially, it can once again.
        If the previous move was a castling move, the king and rook's positions are restored alongside their attributes.
        :param move: Move, object recording details about the move to be undone.
        :param piece: Piece, object recording details about the piece to be restored.
        """
        moved_piece_is_rook = piece is not None and isinstance(piece, Rook)
        moved_piece_is_pawn = piece is not None and isinstance(piece, Pawn)
        moved_piece_is_king = piece is not None and isinstance(piece, King)
        if moved_piece_is_rook:
            if move.changed_initial_position:
                piece.can_castle = True

        elif moved_piece_is_pawn:
            if move.changed_initial_position:
                piece.initial_square = True

        elif moved_piece_is_king:
            if piece.is_white:
                self.__move_service.white_king = (move.move_from.rank, move.move_from.file)
            else:
                self.__move_service.black_king = (move.move_from.rank, move.move_from.file)
            if move.changed_initial_position:
                piece.can_castle = True
        if move.castling_move:
            piece.can_castle = True
            new_move = self.__moves_played.pop()
            new_move.move_to.piece = NoPiece()
            new_move.move_from.piece = new_move.moved_piece
            new_move.move_from.piece.can_castle = True

    def undo_capture_if_possible(self, move):
        """
        Method to liberate previously captured piece.
        :param move: Move, object recording details about the move to be undone.
        """
        move_killed = move.killed_piece is not None
        if move_killed:
            if move.en_passant_move:
                self.undo_en_passant_move(move)
            else:
                move.move_to.piece = move.killed_piece

    def undo_en_passant_move(self, move):
        """
        Method to liberate previously en-passant captured piece.
        :param move: Move, object recording details about the move to be undone.
        """
        board = self.__game.board
        if move.moved_piece.is_white:
            affected_square = board.get_square(move.move_to.rank - 1, move.move_to.file)
            affected_square.piece = move.killed_piece
        else:
            affected_square = board.get_square(move.move_to.rank + 1, move.move_to.file)
            affected_square.piece = move.killed_piece