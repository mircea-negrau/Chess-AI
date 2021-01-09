from domain.entities.pieces import Queen, NoPiece, Bishop, Rook, Knight, Pawn, King


class MoveValidationService:
    def __init__(self, game):
        self.__game = game

    def is_valid_move(self, current_piece, current_square, target_square, is_first_step=True):
        """
        Method to check whether or not the given initial square, the given piece and the target square can make together
        a valid move.
        The method checks what type of piece the received piece is and calls the adequate method to indicate whether
        or not the move is a valid move. (True / False)
        :param current_piece: Piece, object recording details about the piece that is moved.
        :param current_square: Square, object recording details about the initial square.
        :param target_square: Square, object recording details about the target square.
        :param is_first_step: bool, indicating whether or not the move is the first check of the recursion.
        :return: True / False, according to the validity of the move.
        """
        moved_piece_is_queen = isinstance(current_piece, Queen)
        moved_piece_is_rook = isinstance(current_piece, Rook)
        moved_piece_is_bishop = isinstance(current_piece, Bishop)
        moved_piece_is_knight = isinstance(current_piece, Knight)
        moved_piece_is_pawn = isinstance(current_piece, Pawn)
        moved_piece_is_king = isinstance(current_piece, King)

        if moved_piece_is_queen:
            return self.is_valid_queen_move(current_piece, current_square, is_first_step, target_square)
        elif moved_piece_is_rook:
            return self.is_valid_rook_move(current_piece, current_square, is_first_step, target_square)
        elif moved_piece_is_bishop:
            return self.is_valid_bishop_move(current_piece, current_square, is_first_step, target_square)
        elif moved_piece_is_knight:
            return self.is_valid_knight_move(current_piece, current_square, target_square)
        elif moved_piece_is_pawn:
            return self.is_valid_pawn_move(current_piece, current_square, target_square)
        elif moved_piece_is_king:
            return self.is_valid_king_move(current_piece, current_square, target_square)

    def is_valid_king_move(self, current_piece, current_square, target_square):
        """
        Method to check whether or not the move is a valid king move.
        If the target square has a piece that cannot be killed, the move is an invalid one and the method returns False.
        Otherwise, if the king takes one step in any direction and the target square is empty or has a piece that can
        be killed, the move is a valid one and the method returns True.
        Otherwise, if the king performs a castling move, the method calls the castling validation method.
        :param current_piece: King, object recording details about the king that is moved.
        :param current_square: Square, object recording details about the initial square.
        :param target_square: Square, object recording details about the target square.
        :return: True / False, according to the validity of the move.
        """
        target_square_has_piece = not isinstance(target_square.piece, NoPiece)
        piece_cannot_be_killed = target_square.piece.is_white == current_piece.is_white
        if target_square_has_piece and piece_cannot_be_killed:
            return False

        vertical_coordinate = current_square.rank - target_square.rank
        horizontal_coordinate = current_square.file - target_square.file
        moves_horizontally_or_vertically = abs(vertical_coordinate) + abs(horizontal_coordinate) == 1
        moves_diagonally = abs(vertical_coordinate) + abs(
            horizontal_coordinate) == 2 and vertical_coordinate != 0 and horizontal_coordinate != 0
        castles = vertical_coordinate == 0

        if moves_horizontally_or_vertically:
            return True
        elif moves_diagonally:
            return True
        elif castles:
            return self.get_castling_move_validated(current_piece, current_square, horizontal_coordinate)
        return False

    def get_castling_move_validated(self, current_piece, current_square, horizontal_coordinate):
        """
        Method to check whether or not the move is a valid king castling move.
        If the castling is a short castling, the method calls the short castling method.
        If the castling is a long castling, the method calls the long castling method.
        Otherwise, the method returns False
        :param current_piece: King, object recording details about the king that is moved.
        :param current_square: Square, object recording details about the initial square.
        :param horizontal_coordinate: integer, holding the value by which the king's file changes.
        :return: True / False, according to the validity of the move.
        """
        short_castle = horizontal_coordinate == -2
        long_castle = horizontal_coordinate == 2
        if short_castle:
            return self.get_short_castling_validated(current_piece, current_square)
        elif long_castle:
            if current_piece.can_castle:
                return self.get_long_castling_validated(current_piece, current_square)
        return False

    def get_short_castling_validated(self, current_piece, current_square):
        """
        Method to check whether or not the short castling of the king is a valid move.
        If the king can castle, each of the squares walked by the king during the castling gets put through validation.
        If any of them results in an invalid move, the short castling is invalid and the method returns False.
        Otherwise, the method returns True, and the move is a valid short castling move.
        :param current_piece: King, object recording details about the king that is moved.
        :param current_square: Square, object recording details about the initial square.
        :return: True / False, according to the validity of the move.
        """
        board = self.__game.board
        if current_piece.can_castle:
            first_square = board.get_square(current_square.rank, current_square.file + 1).piece
            second_square = board.get_square(current_square.rank, current_square.file + 2).piece
            third_square = board.get_square(current_square.rank, current_square.file + 3).piece
            if isinstance(first_square, NoPiece) and isinstance(second_square, NoPiece):
                if isinstance(third_square, Rook) and third_square.is_white == current_piece.is_white:
                    if third_square.can_castle:
                        return True
        return False

    def get_long_castling_validated(self, current_piece, current_square):
        """
        Method to check whether or not the long castling of the king is a valid move.
        If the king can castle, each of the squares walked by the king during the castling gets put through validation.
        If any of them results in an invalid move, the long castling is invalid and the method returns False.
        Otherwise, the method returns True, and the move is a valid long castling move.
        :param current_piece: King, object recording details about the king that is moved.
        :param current_square: Square, object recording details about the initial square.
        :return: True / False, according to the validity of the move.
        """
        board = self.__game.board
        first_square = board.get_square(current_square.rank, current_square.file - 1).piece
        second_square = board.get_square(current_square.rank, current_square.file - 2).piece
        third_square = board.get_square(current_square.rank, current_square.file - 3).piece
        fourth_square = board.get_square(current_square.rank, current_square.file - 4).piece
        if isinstance(first_square, NoPiece) and isinstance(second_square, NoPiece) and isinstance(
                third_square, NoPiece):
            if isinstance(fourth_square, Rook) and fourth_square.is_white == current_piece.is_white:
                if fourth_square.can_castle:
                    return True
        return False

    def is_valid_pawn_move(self, current_piece, current_square, target_square):
        """
        Method to check whether or not the move is a valid pawn move.
        If the target square has a piece that cannot be killed, the move is an invalid one and the method returns False.
        If the pawn moves two steps forward, the method calls the two-step-forward validation method.
        If the pawn moves one step diagonally in its direction, the method calls the diagonal pawn move validation.
        If the pawn moves one step forward in its direction, if the target square is free, the method returns True.
        Otherwise, the pawn move is an invalid move and the method returns False.
        :param current_piece: Pawn, object recording details about the pawn that is moved.
        :param current_square: Square, object recording details about the initial square.
        :param target_square: Square, object recording details about the target square.
        :return: True / False, according to the validity of the move.
        """
        piece_cannot_be_killed = target_square.piece.is_white == current_piece.is_white
        target_square_has_piece = not isinstance(target_square.piece, NoPiece)
        if target_square_has_piece and piece_cannot_be_killed:
            return False

        file_change = abs(current_square.file - target_square.file)
        rank_change = current_square.rank - target_square.rank
        if current_piece.is_white:
            rank_change = -rank_change
        valid_rank_change = 0 < rank_change <= 2
        if valid_rank_change:
            two_steps = rank_change == 2
            diagonal_move = rank_change == 1 and abs(file_change) == 1
            one_step = rank_change == 1 and not file_change
            if two_steps:
                return self.get_pawn_two_step_move_validated(current_piece, current_square, file_change,
                                                             target_square_has_piece)
            elif diagonal_move:
                return self.get_pawn_diagonal_move_validated(current_piece, target_square, target_square_has_piece)
            elif one_step:
                step_square_is_free = isinstance(target_square.piece, NoPiece)
                if step_square_is_free:
                    return True
        return False

    def get_pawn_diagonal_move_validated(self, current_piece, target_square, target_square_has_piece):
        """
        Method to check whether or not the diagonal move of the pawn is a valid move.
        If there exists an available en passant move on the chessboard and the pawn captures that en passant square's
        coordinates, the pawn diagonal move is a valid one and it is an en passant move.
        Else, if the target square holds a piece of the opponent, the move is a valid one and the method returns
        True.
        Otherwise, the method returns False and the move is an invalid move.
        :param current_piece: Pawn, object recording details about the pawn that is moved.
        :param target_square: Square, object recording details about the target square.
        :param target_square_has_piece: bool, indicating whether or not the target square has a piece or not
        :return: True / False, according to the validity of the move.
        """
        board = self.__game.board
        target_square_is_empty = isinstance(target_square.piece, NoPiece)
        if board.available_en_passant is not False:
            target_square_is_available_for_en_passant = target_square.rank == board.available_en_passant[0] \
                                                        and target_square.file == board.available_en_passant[1]
        else:
            target_square_is_available_for_en_passant = False
        exists_square_for_en_passant = board.available_en_passant

        if target_square_has_piece and target_square.piece.is_white != current_piece.is_white:
            return True
        elif exists_square_for_en_passant and target_square_is_empty and target_square_is_available_for_en_passant:
            return True
        return False

    def get_pawn_two_step_move_validated(self, current_piece, current_square, file_change, target_square_has_piece):
        """
        Method to check whether or not the two step forward movement of the pawn is a valid move.
        If the pawn moves only forward and there is no piece on its way, the move is a valid one and the method returns
        True. Otherwise, the method returns False.
        :param current_piece: King, object recording details about the pawn that is moved.
        :param current_square: Square, object recording details about the initial square.
        :param file_change: integer, holds the value by which the piece gets moved on its file.
        :param target_square_has_piece: bool, indicating whether or not the target square has a piece or not
        :return: True / False, according to the validity of the move.
        """
        board = self.__game.board
        no_file_change = file_change == 0
        if no_file_change:
            if current_piece.initial_square:
                if not target_square_has_piece:
                    if current_piece.is_white:
                        intermediate_square = board.get_square(current_square.rank + 1, current_square.file)
                        intermediate_square_is_free = isinstance(intermediate_square.piece, NoPiece)
                        if intermediate_square_is_free:
                            return True
                    else:
                        intermediate_square = board.get_square(current_square.rank - 1, current_square.file)
                        intermediate_square_is_free = isinstance(intermediate_square.piece, NoPiece)
                        if intermediate_square_is_free:
                            return True
        return False

    @staticmethod
    def is_valid_knight_move(current_piece, current_square, target_square):
        """
        Method to check whether or not the move is a valid knight move.
        If the target square has a piece and the piece can be captured, the move is valid.
        If the move is an L shaped move, the move is a valid move.
        Otherwise, the move is an invalid move.
        :param current_piece: Knight, object recording details about the knight that is moved.
        :param current_square: Square, object recording details about the initial square.
        :param target_square: Square, object recording details about the target square.
        :return: True / False, according to the validity of the move.
        """
        target_square_has_piece = not isinstance(target_square.piece, NoPiece)
        piece_cannot_be_killed = target_square.piece.is_white == current_piece.is_white
        if target_square_has_piece and piece_cannot_be_killed:
            return False
        vertical_coordinate = abs(current_square.rank - target_square.rank)
        horizontal_coordinate = abs(current_square.file - target_square.file)
        return vertical_coordinate * horizontal_coordinate == 2

    def is_valid_bishop_move(self, current_piece, current_square, is_first_step, target_square):
        """
        Recursive to check whether or not the move is a valid bishop move.
        For each step of the bishop's advancement, the method checks whether or not the square is empty. If all the
        squares are empty, or the final square is not empty and it contains a piece that is valid for capturing, the
        move is a valid move. Otherwise, the move is an invalid move.
        :param current_piece: Bishop, object recording details about the bishop that is moved.
        :param current_square: Square, object recording details about the initial square.
        :param is_first_step: bool, indicates whether or not this is the first step of the recursion.
        :param target_square: Square, object recording details about the target square.
        :return: True / False, according to the validity of the move.
        """
        board = self.__game.board
        if current_square == target_square:
            return self.is_step_final_step_or_error(is_first_step)
        target_square_has_piece = not isinstance(target_square.piece, NoPiece)
        piece_cannot_be_killed = target_square.piece.is_white == current_piece.is_white
        if target_square_has_piece:
            if piece_cannot_be_killed:
                return False
            if not is_first_step:
                return False
        vertical_coordinate = current_square.rank - target_square.rank
        horizontal_coordinate = current_square.file - target_square.file
        if vertical_coordinate < 0:
            next_square_rank = target_square.rank - 1
        else:
            next_square_rank = target_square.rank + 1
        if horizontal_coordinate < 0:
            next_square_file = target_square.file - 1
        else:
            next_square_file = target_square.file + 1
        next_square = board.get_square(next_square_rank, next_square_file)
        valid_diagonal_move = abs(vertical_coordinate) == abs(horizontal_coordinate)
        return valid_diagonal_move and self.is_valid_move(current_piece, current_square, next_square,
                                                          is_first_step=False)

    def is_valid_rook_move(self, current_piece, current_square, is_first_step, target_square):
        """
        Recursive to check whether or not the move is a valid rook move.
        For each step of the rook's advancement, the method checks whether or not the square is empty. If all the
        squares are empty, or the final square is not empty and it contains a piece that is valid for capturing, the
        move is a valid move. Otherwise, the move is an invalid move.
        :param current_piece: Rook, object recording details about the rook that is moved.
        :param current_square: Square, object recording details about the initial square.
        :param is_first_step: bool, indicates whether or not this is the first step of the recursion.
        :param target_square: Square, object recording details about the target square.
        :return: True / False, according to the validity of the move.
        """
        board = self.__game.board
        if current_square == target_square:
            return self.is_step_final_step_or_error(is_first_step)
        target_square_has_piece = not isinstance(target_square.piece, NoPiece)
        piece_cannot_be_killed = target_square.piece.is_white == current_piece.is_white
        if target_square_has_piece:
            if piece_cannot_be_killed:
                return False
            if not is_first_step:
                return False
        vertical_coordinate = current_square.rank - target_square.rank
        horizontal_coordinate = current_square.file - target_square.file
        next_square_file, next_square_rank = self.get_next_rook_recursion_coordinates(current_square,
                                                                                      horizontal_coordinate,
                                                                                      target_square,
                                                                                      vertical_coordinate)
        next_square = board.get_square(next_square_rank, next_square_file)
        vertical_move = abs(vertical_coordinate) and not abs(horizontal_coordinate)
        horizontal_move = abs(horizontal_coordinate) and not abs(vertical_coordinate)
        valid_move = vertical_move or horizontal_move
        return valid_move and self.is_valid_move(current_piece, current_square, next_square, is_first_step=False)

    def is_valid_queen_move(self, current_piece, current_square, is_first_step, target_square):
        """
        Recursive to check whether or not the move is a valid queen move.
        For each step of the queen's advancement, the method checks whether or not the square is empty. If all the
        squares are empty, or the final square is not empty and it contains a piece that is valid for capturing, the
        move is a valid move. Otherwise, the move is an invalid move.
        :param current_piece: Queen, object recording details about the queen that is moved.
        :param current_square: Square, object recording details about the initial square.
        :param is_first_step: bool, indicates whether or not this is the first step of the recursion.
        :param target_square: Square, object recording details about the target square.
        :return: True / False, according to the validity of the move.
        """
        board = self.__game.board
        if current_square == target_square:
            return self.is_step_final_step_or_error(is_first_step)
        if not isinstance(target_square.piece, NoPiece):
            if target_square.piece.is_white == current_piece.is_white:
                return False
            if not is_first_step:
                return False
        vertical_coordinate = current_square.rank - target_square.rank
        horizontal_coordinate = current_square.file - target_square.file
        next_square_file, next_square_rank = self.get_next_queen_recursion_coordinates(current_square,
                                                                                       horizontal_coordinate,
                                                                                       target_square,
                                                                                       vertical_coordinate)
        next_square = board.get_square(next_square_rank, next_square_file)
        vertical_move = (vertical_coordinate and not horizontal_coordinate)
        horizontal_move = horizontal_coordinate and not vertical_coordinate
        diagonal_move = abs(vertical_coordinate) == abs(horizontal_coordinate)
        valid_move = vertical_move or horizontal_move or diagonal_move
        return valid_move and self.is_valid_move(current_piece, current_square, next_square, is_first_step=False)

    @staticmethod
    def get_next_queen_recursion_coordinates(current_square, horizontal_coordinate, target_square,
                                             vertical_coordinate):
        """
        Method to obtain the coordinates of the next move in the queen's move validity recursion.
        If the move is a diagonal one, horizontal one or vertical one, the method returns the adequate next step to be
        validated.
        :param current_square: Square, object recording details about the initial square.
        :param horizontal_coordinate: integer, holding the value by which the queen's file changes.
        :param target_square: Square, object recording details about the target square.
        :param vertical_coordinate: integer, holding the value by which the queen's rank changes.
        :return: integer, holding the next file; integer, holding the next square rank.
        """
        next_square_rank = current_square.rank
        next_square_file = current_square.file
        if vertical_coordinate == horizontal_coordinate:
            if vertical_coordinate > 0:
                next_square_rank = target_square.rank + 1
                next_square_file = target_square.file + 1
            elif vertical_coordinate < 0:
                next_square_rank = target_square.rank - 1
                next_square_file = target_square.file - 1
        elif vertical_coordinate == -horizontal_coordinate:
            if vertical_coordinate > 0:
                next_square_rank = target_square.rank + 1
                next_square_file = target_square.file - 1
            elif vertical_coordinate < 0:
                next_square_rank = target_square.rank - 1
                next_square_file = target_square.file + 1
        elif horizontal_coordinate == 0:
            if vertical_coordinate > 0:
                next_square_rank = target_square.rank + 1
            elif vertical_coordinate < 0:
                next_square_rank = target_square.rank - 1
        elif vertical_coordinate == 0:
            if horizontal_coordinate > 0:
                next_square_file = target_square.file + 1
            elif horizontal_coordinate < 0:
                next_square_file = target_square.file - 1
        return next_square_file, next_square_rank

    @staticmethod
    def get_next_rook_recursion_coordinates(current_square, horizontal_coordinate, target_square,
                                            vertical_coordinate):
        """
        Method to obtain the coordinates of the next move in the rook's move validity recursion.
        If the move is a horizontal one or vertical one, the method returns the adequate next step to be validated.
        :param current_square: Square, object recording details about the initial square.
        :param horizontal_coordinate: integer, holding the value by which the rook's file changes.
        :param target_square: Square, object recording details about the target square.
        :param vertical_coordinate: integer, holding the value by which the rook's rank changes.
        :return: integer, holding the next file; integer, holding the next square rank.
        """
        next_square_rank = current_square.rank
        next_square_file = current_square.file
        if vertical_coordinate > 0:
            next_square_rank = target_square.rank + 1
        elif vertical_coordinate < 0:
            next_square_rank = target_square.rank - 1
        elif horizontal_coordinate > 0:
            next_square_file = target_square.file + 1
        elif horizontal_coordinate < 0:
            next_square_file = target_square.file - 1
        return next_square_file, next_square_rank

    @staticmethod
    def is_step_final_step_or_error(first_check):
        if first_check:
            return False
        return True
