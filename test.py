import unittest

from domain.entities.board import Move, Square
from domain.entities.pieces import Pawn, NoPiece
from domain.entities.players import Human, Computer
from services.chess_service import Game


class ChessServiceTest(unittest.TestCase):
    def setUp(self):
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=1)

    def test_get_computer_move(self):
        self.game.get_computer_move()
        assert (self.game.current_player.is_white is False)

    def test_get_human_move(self):
        assert (self.game.get_human_move(self.game.current_player, 2, 2, 4, 2) is True)
        assert self.game.get_last_move().moved_piece.is_white is True
        self.game.get_undo_performed()
        assert str(self.game.board[2][2]) is not None

    def test_get_undo(self):
        assert (self.game.get_human_move(self.game.current_player, 2, 2, 4, 2) is True)
        assert (self.game.get_human_move(self.game.current_player, 7, 2, 5, 2) is True)
        self.game.get_double_undo_performed()
        assert self.game.current_player.is_white is False

        del self.game
        self.game = Game(white_player=Computer(is_white=True), black_player=Human(is_white=False), depth=1)
        self.game.get_computer_move()
        assert (self.game.get_human_move(self.game.current_player, 7, 2, 5, 2) is True)
        self.game.get_double_undo_performed()
        assert self.game.current_player.is_white is True

    def test_get_game_status(self):
        assert (self.game.get_game_status() is True)
        del self.game
        self.game = Game(white_player=Computer(is_white=True), black_player=Human(is_white=False), depth=1,
                         board_type="Checkmate")
        assert (self.game.get_game_status() is False)
        del self.game
        self.game = Game(white_player=Computer(is_white=True), black_player=Human(is_white=False), depth=1,
                         board_type="Stalemate")
        assert (self.game.get_game_status() is False)

    def test_get_all_valid_moves_of_square(self):
        square = self.game.board.get_square(2, 1)
        index = 0
        for _ in self.game.get_all_valid_moves_of_square(square):
            index += 1
        assert index == 2

    def test_is_move_not_king_suicide(self):
        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=1,
                         board_type="Checkmate")
        initial_square = self.game.board.get_square(1, 1)
        target_square = self.game.board.get_square(1, 2)
        move = Move(self.game.current_player, initial_square, target_square)
        assert self.game.is_move_not_king_suicide(move) is False
        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=1,
                         board_type="Check")
        target_square = self.game.board.get_square(1, 2)
        move = Move(self.game.current_player, initial_square, target_square)
        assert self.game.is_move_not_king_suicide(move) is True

    def test_get_game_status_updated_as_active(self):
        self.game.game_status = "INACTIVE"
        self.game.get_game_status_updated_as_active()
        assert self.game.game_status == "ACTIVE"

    def test_game_variables_change(self):
        self.game.black_player = None
        self.game.white_player = None
        self.game.depth = 1
        assert self.game.black_player is None
        assert self.game.white_player is None
        assert self.game.depth == 1

    def tearDown(self):
        del self.game


class MoveServiceTest(unittest.TestCase):
    def setUp(self):
        self.game = Game(white_player=Human(is_white=True), black_player=Computer(is_white=False), depth=2)

    def test_get_move_tested(self):
        player = self.game.current_player
        initial_square = self.game.board.get_square(1, 1)
        target_square = self.game.board.get_square(1, 2)
        move = Move(player, initial_square, target_square)
        self.game.get_next_player_turn()
        assert self.game._move_service.get_move_tested(move, player) is False

        self.game.get_next_player_turn()
        initial_square = self.game.board.get_square(3, 3)
        target_square = self.game.board.get_square(1, 1)
        move = Move(player, initial_square, target_square)
        assert self.game._move_service.get_move_tested(move, player) is False

        initial_square = self.game.board.get_square(7, 2)
        target_square = self.game.board.get_square(7, 4)
        move = Move(player, initial_square, target_square)
        assert self.game._move_service.get_move_tested(move, player) is False

        initial_square = self.game.board.get_square(1, 2)
        target_square = self.game.board.get_square(3, 2)
        move = Move(player, initial_square, target_square)
        assert self.game._move_service.get_move_tested(move, player) is False

        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=1,
                         board_type="Castling_Test")
        self.game.get_human_move(self.game.current_player, 1, 1, 1, 2)
        self.game.get_undo_performed()

    def test_get_wrong_move_tested(self):
        assert self.game.get_human_move(self.game.current_player, 1, 3, 3, 1) is False
        self.game.get_next_player_turn()
        assert self.game.get_human_move(self.game.current_player, 8, 3, 5, 1) is False
        assert self.game.get_human_move(self.game.current_player, 8, 8, 1, 8) is False
        assert self.game.get_human_move(self.game.current_player, 8, 8, 8, 8) is False
        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=1,
                         board_type="Castling_Test")
        assert self.game.get_human_move(self.game.current_player, 1, 1, 2, 3) is False
        assert self.game.get_human_move(self.game.current_player, 1, 5, 8, 8) is False
        assert self.game.get_human_move(self.game.current_player, 2, 5, 1, 8) is False
        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=1,
                         board_type="Fail_castling_test")
        assert self.game.get_human_move(self.game.current_player, 1, 5, 1, 8) is False
        assert self.game.get_human_move(self.game.current_player, 6, 7, 8, 7) is False

    def test_get_castling_move_tested(self):
        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=1,
                         board_type="Castling_Test")
        self.game.get_human_move(self.game.current_player, 1, 1, 1, 2)
        self.game.get_human_move(self.game.current_player, 8, 8, 5, 5)
        initial_square = self.game.board.get_square(1, 5)
        target_square = self.game.board.get_square(1, 7)
        move = Move(self.game.current_player, initial_square, target_square)
        assert self.game._move_service.get_move_tested(move, self.game.current_player) is False

    def test_get_long_castling_tested(self):
        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=1,
                         board_type="Castling_Test")
        assert self.game.get_human_move(self.game.current_player, 1, 5, 1, 3) is True
        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=1,
                         board_type="Fail_castling_test")
        self.game.get_next_player_turn()
        assert self.game.get_human_move(self.game.current_player, 8, 1, 8, 4) is True
        assert self.game.get_human_move(self.game.current_player, 1, 5, 1, 3) is False
        self.game.get_undo_performed()
        self.game.get_undo_performed()
        assert self.game.get_human_move(self.game.current_player, 8, 1, 3, 1) is True
        assert self.game.get_human_move(self.game.current_player, 1, 5, 1, 3) is False

    def test_get_short_castling_tested(self):
        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=1,
                         board_type="Castling_Test")
        assert self.game.get_human_move(self.game.current_player, 1, 5, 1, 7) is True
        self.game.get_undo_performed()
        assert self.game.get_human_move(self.game.current_player, 2, 2, 4, 2) is True
        assert self.game.get_human_move(self.game.current_player, 8, 8, 6, 6) is True
        assert self.game.get_human_move(self.game.current_player, 1, 5, 1, 7) is False

    def test_get_captured_piece_for_pawn_captures(self):
        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=1,
                         board_type="Castling_Test")
        self.game.get_next_player_turn()
        assert self.game.get_human_move(self.game.current_player, 7, 3, 6, 3) is True
        assert self.game.get_human_move(self.game.current_player, 5, 4, 6, 3) is True
        assert self.game.get_human_move(self.game.current_player, 6, 8, 6, 7) is True
        self.game.get_undo_performed()

    def test_get_pawn_promotion_move_tested(self):
        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=1,
                         board_type="Castling_Test")
        self.game.get_next_player_turn()
        assert self.game.get_human_move(self.game.current_player, 7, 3, 5, 3) is True
        assert self.game.get_human_move(self.game.current_player, 5, 4, 6, 3) is True
        self.game.get_undo_performed()
        self.game.get_undo_performed()
        assert self.game.get_human_move(self.game.current_player, 7, 3, 5, 3) is True
        assert self.game.get_human_move(self.game.current_player, 5, 4, 6, 3) is True
        self.game.get_human_move(self.game.current_player, 8, 8, 7, 7)
        assert self.game.get_human_move(self.game.current_player, 2, 1, 4, 1) is True
        self.game.get_human_move(self.game.current_player, 7, 7, 8, 8)
        assert self.game.get_human_move(self.game.current_player, 4, 1, 5, 1) is True
        self.game.get_human_move(self.game.current_player, 8, 8, 7, 7)
        assert self.game.get_human_move(self.game.current_player, 5, 1, 6, 1) is True
        self.game.get_human_move(self.game.current_player, 7, 7, 8, 8)
        assert self.game.get_human_move(self.game.current_player, 6, 1, 7, 1) is True
        self.game.get_human_move(self.game.current_player, 8, 8, 7, 7)
        assert self.game.get_human_move(self.game.current_player, 7, 1, 8, 1) is True

    def test_get_en_passant_move(self):
        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=1,
                         board_type="Castling_Test")
        assert self.game.get_human_move(self.game.current_player, 2, 2, 4, 2) is True
        assert self.game.get_human_move(self.game.current_player, 4, 3, 3, 2) is True
        self.game.get_undo_performed()

    def test_get_moves_played(self):
        assert len(self.game._move_service.get_moves_played()) == 0
        assert self.game.get_human_move(self.game.current_player, 2, 2, 4, 2) is True
        assert len(self.game._move_service.get_moves_played()) == 1

    def test_attributes(self):
        assert self.game._move_service.white_king == (1, 5)
        assert self.game._move_service.black_king == (8, 5)
        self.game._move_service.black_king = (5, 5)
        assert self.game._move_service.black_king == (5, 5)

    def tearDown(self):
        del self.game


class ComputerMoveServiceTest(unittest.TestCase):
    def setUp(self):
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=2)

    def test_get_minimax(self):
        self.game._move_service.get_computer_move_applied()
        self.game._move_service.get_computer_move_applied()
        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=2,
                         board_type="Check")
        self.game._move_service.get_computer_move_applied()
        self.game._move_service.get_computer_move_applied()
        self.game._move_service.get_computer_move_applied()
        self.game._move_service.get_computer_move_applied()
        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=3,
                         board_type="One-step-to-check-for-white")
        self.game._move_service.get_computer_move_applied()
        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=3,
                         board_type="One-step-to-check-for-white")
        self.game.get_next_player_turn()
        self.game._move_service.get_computer_move_applied()
        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=3,
                         board_type="One-step-to-check-for-black")
        self.game._move_service.get_computer_move_applied()
        del self.game
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=3,
                         board_type="One-step-to-check-for-black")
        self.game.get_next_player_turn()
        self.game._move_service.get_computer_move_applied()

    def tearDown(self):
        del self.game


class MoveGenerationServiceTest(unittest.TestCase):
    def setUp(self):
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=2)

    def test_move_generation(self):
        square = self.game.board.get_square(1, 4)
        piece = square.piece
        self.game._move_generation_service.get_all_queen_moves(piece, square)

    def tearDown(self):
        del self.game


class EvaluationServiceTest(unittest.TestCase):
    def setUp(self):
        self.game = Game(white_player=Human(is_white=True), black_player=Human(is_white=False), depth=2,
                         board_type="end-game-evaluation")

    def test_end_game_evaluation(self):
        self.game._evaluation_service.evaluate_move(self.game.board)

    def tearDown(self):
        del self.game


class EntityTest(unittest.TestCase):
    def test_square(self):
        square1 = Square(1, 1, Pawn(is_white=True))
        square2 = NoPiece()
        square3 = None
        square1.rank = 2
        square1.file = 2
        assert square1.rank == 2
        assert square1.file == 2
        assert square1 != square3
        assert str(square2) == "None"
        square1.piece.is_white = False
        assert square1.piece.is_white is False
        square1.piece.is_dead = False
        assert square1.piece.is_dead is False
