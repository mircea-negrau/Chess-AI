class ComputerMoveService:
    def __init__(self, game, move_generation_service, evaluation_service, move_service):
        self.__game = game
        self._move_generation_service = move_generation_service
        self._move_service = move_service
        self._evaluation_service = evaluation_service

    def get_minimax(self, depth):
        """
        Method to return the best move the computer can make in the reached chessboard position.
        This method applies the Minimax Algorithm.
        If the current player is the one playing the white pieces, the algorithm computes the maximal guaranteed
        evaluation for a depth given by the received parameter 'depth'.
        If the current player is the one playing the black pieces, the algorithm computes the minimal guaranteed
        evaluation for a depth given by the received parameter 'depth'.
        If no possible move is found at the given depth, the depth is decreased until the best move is found.
        If in the end (even at depth 1) no possible move is found, that means the position is a checkmate or stalemate,
        so the method returns the value None.
        :param depth: integer, holding the depth at which the Minimax Algorithm should be applied. The higher it is, the
        more time it will take to return an answer, but the answer will be stronger.
        :return: Move, object recording the best move possible for the computer in the given chessboard position. If no
        move is available, it returns None.
        """
        player = self.__game.current_player
        if player.is_white:
            best_move, evaluation = self.get_max(depth, alpha=-10000000, beta=10000000)
            index = 0
            while best_move is None:
                index += 1
                best_move, evaluation = self.get_max(depth - index, alpha=-10000000, beta=10000000)
        else:
            best_move, evaluation = self.get_min(depth, alpha=-10000000, beta=10000000)
            index = 0
            while best_move is None:
                index += 1
                best_move, evaluation = self.get_max(depth - index, alpha=-10000000, beta=10000000)
        return best_move

    def get_max(self, depth, alpha, beta):
        """
        Method that computes the maximal guaranteed evaluation possible for the given position.
        This method goes through all the available valid moves of the current player in the reached chessboard position
        and applies them one by one.
        If the depth has not been reached (depth is not 0), for each of the possible moves the method advances further
        into the Minimax Algorithm, calling the 'get_min' method and decreasing the remaining depth to be applied. If
        the result of the 'get_min' evaluation is None, it means the position leads to a forced checkmate and is thus
        the best possible move.
        Otherwise, if the depth has been reached (depth is 0), the method returns the evaluation of the current
        reached position.
        The Alpha variable takes the maximal value between the previous Alpha value and the current evaluation.
        After the evaluation took place, the applied move is undone (so that the chessboard becomes one step closer to
        the one received initially).
        If the current evaluation is greater than the maximal one found until now, the current evaluation becomes the
        maximal evaluation and the best move becomes the current move.
        If the Beta variable is less or equal to the Alpha variable, it means looking further into this branch is
        futile, as there is a possible move leading to a worse evaluation than a guaranteed evaluation reached before.
        If no possible move is found, the method returns None and None as values for the evaluation and best move
        variables.
        Otherwise, the method returns the best move and the maximal evaluation found.
        :param depth: integer, holds the value of the remaining depth to be applied before a final answer is expected.
        :param alpha: integer, holds the value of the maximal guaranteed evaluation found throughout the Minimax
        Algorithm.
        :param beta: integer, holds the value of the minimal guaranteed evaluation found throughout the Minimax
        Algorithm.
        :return: Move, recording the best possible move the computer can make in the given chessboard position; Integer,
        holding the value of the maximal guaranteed evaluation.
        """
        best_move, max_evaluation = None, -100000000
        player = self.__game.current_player
        board = self.__game.board
        for current_move in self._move_generation_service.get_all_moves(board):
            piece_belongs_to_player = player.is_white == current_move.moved_piece.is_white
            if piece_belongs_to_player:
                move_applied_successfully = self._move_service.get_move_tested(current_move, player)
                if move_applied_successfully:
                    depth_not_reached = depth - 1
                    if depth_not_reached:
                        _, evaluation = self.get_min(depth - 1, alpha, beta)
                        if evaluation is None:
                            self.__game.get_next_player_turn()
                            if self._move_service.is_in_check():
                                evaluation = 100000000
                            else:
                                evaluation = -100000000
                            self.__game.get_next_player_turn()
                    else:
                        evaluation = self._evaluation_service.evaluate_move(board)
                    alpha = max(alpha, evaluation)
                    self._move_service.undo_move()
                    if max_evaluation < evaluation:
                        max_evaluation = evaluation
                        best_move = current_move
                    if beta <= alpha:
                        break
        no_possible_move_found = best_move is None
        if no_possible_move_found:
            return None, None
        return best_move, max_evaluation

    def get_min(self, depth, alpha, beta):
        """
        Method that computes the minimal guaranteed evaluation possible for the given position.
        This method goes through all the available valid moves of the current player in the reached chessboard position
        and applies them one by one.
        If the depth has not been reached (depth is not 0), for each of the possible moves the method advances further
        into the Minimax Algorithm, calling the 'get_max' method and decreasing the remaining depth to be applied. If
        the result of the 'get_max' evaluation is None, it means the position leads to a forced checkmate and is thus
        the best possible move.
        Otherwise, if the depth has been reached (depth is 0), the method returns the evaluation of the current
        reached position.
        The Beta variable takes the minimal value between the previous Beta value and the current evaluation.
        After the evaluation took place, the applied move is undone (so that the chessboard becomes one step closer to
        the one received initially).
        If the current evaluation is lesser than the minimal one found until now, the current evaluation becomes the
        minimal evaluation and the best move becomes the current move.
        If the Beta variable is less or equal to the Alpha variable, it means looking further into this branch is
        futile, as there is a possible move leading to a worse evaluation than a guaranteed evaluation reached before.
        If no possible move is found, the method returns None and None as values for the evaluation and best move
        variables.
        Otherwise, the method returns the best move and the minimal evaluation found.
        :param depth: integer, holds the value of the remaining depth to be applied before a final answer is expected.
        :param alpha: integer, holds the value of the maximal guaranteed evaluation found throughout the Minimax
        Algorithm.
        :param beta: integer, holds the value of the minimal guaranteed evaluation found throughout the Minimax
        Algorithm.
        :return: Move, recording the best possible move the computer can make in the given chessboard position; Integer,
        holding the value of the minimal guaranteed evaluation.
        """
        best_move, min_evaluation = None, 100000000
        player = self.__game.current_player
        board = self.__game.board
        for current_move in self._move_generation_service.get_all_moves(board):
            piece_belongs_to_player = player.is_white == current_move.moved_piece.is_white
            if piece_belongs_to_player:
                move_applied_successfully = self._move_service.get_move_tested(current_move, player)
                if move_applied_successfully:
                    depth_not_reached = depth - 1
                    if depth_not_reached:
                        _, evaluation = self.get_max(depth - 1, alpha, beta)
                        if evaluation is None:
                            self.__game.get_next_player_turn()
                            if self._move_service.is_in_check():
                                evaluation = -100000000
                            else:
                                evaluation = 100000000
                            self.__game.get_next_player_turn()
                    else:
                        evaluation = self._evaluation_service.evaluate_move(board)
                    beta = min(beta, evaluation)
                    self._move_service.undo_move()
                    if min_evaluation > evaluation:
                        min_evaluation = evaluation
                        best_move = current_move
                    if beta <= alpha:
                        break
        no_possible_move_found = best_move is None
        if no_possible_move_found:
            return None, None
        return best_move, min_evaluation