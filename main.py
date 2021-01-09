from domain.entities.players import Human
from services.chess_service import Game
from services.evaluation_service import EvaluationService
from services.move_generation_service import MoveGenerationService
from settings.settings import Program

program = Program()
program.run()

# game = Game(Human(is_white=True), Human(is_white=False), 4)
# generation = MoveGenerationService(game)
# evaluation = EvaluationService(generation)
# print(evaluation.evaluate_move(game.board))