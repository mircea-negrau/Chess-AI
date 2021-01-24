class Console:
    def __init__(self, game):
        self.menu_options = {
            1: {"description": "Play", "function": self.__play},
            0: {"description": "Exit", "function": exit},
        }
        self.__game = game
        self.file_letters = "abcdefgh"

    def run(self):
        while True:
            for key in self.menu_options:
                print(key, self.menu_options[key]["description"])
            try:
                user_option = int(input(">"))
                self.menu_options[user_option]["function"]()
            except ValueError:
                print("Invalid value!")
            except KeyError:
                print("Invalid option!")

    def __play(self):
        while self.__game.game_status == "ACTIVE":
            self.print_board(self.__game.board)
            is_game_active = self.__game.get_game_status()
            if is_game_active:
                self.get_next_move_performed()
        print(self.__game.game_status)

    def get_next_move_performed(self):
        if self.__game.current_player.is_human:
            self.get_human_move(self.__game)
        else:
            self.get_computer_move_performed()

    def get_computer_move_performed(self):
        print("Computer move loading...")
        self.__game.get_computer_move()

    def get_human_move(self, game):
        had_errors = False
        print("Insert row letter and column digit (e.g. e3)")
        received_input = input(">").strip().lower()
        if received_input == "back":
            game.undo_move()
        else:
            input_list = []
            for character in received_input:
                input_list.append(character)
            input_does_not_match_command_length = len(input_list) != 4
            if input_does_not_match_command_length:
                print("Invalid move!")
            else:
                self.get_human_move_performed(game, had_errors, input_list)

    def get_human_move_performed(self, game, had_errors, input_list):
        destination_file, destination_rank, source_file, source_rank, had_errors = self.check_input(had_errors,
                                                                                                    input_list)
        if not had_errors:
            player = game.current_player
            source_file, destination_file = self.convert_letter(source_file), self.convert_letter(destination_file)

            move_performed_successfully = game.get_human_move(player, source_rank, source_file,
                                                              destination_rank,
                                                              destination_file)
            if not move_performed_successfully:
                print("Error")

    def check_input(self, had_errors, input_list):
        destination_file, destination_rank, source_file, source_rank = 0, 0, 0, 0
        try:
            source_file, destination_file = input_list[0], input_list[2]
            source_file_not_valid = source_file.lower() not in self.file_letters
            destination_file_not_valid = destination_file.lower() not in self.file_letters
            if source_file_not_valid or destination_file_not_valid:
                raise ValueError("Invalid file!")
            else:
                try:
                    source_rank, destination_rank = int(input_list[1]), int(input_list[3])
                    coordinates_are_wrong = not 0 < source_rank < 9 or not 0 < destination_rank < 9
                    if coordinates_are_wrong:
                        raise ValueError()
                except ValueError:
                    raise ValueError("Invalid rank!")
        except ValueError as error:
            print(error)
            had_errors = True
        return destination_file, destination_rank, source_file, source_rank, had_errors

    def print_board(self, board):
        for rank in range(8, 0, -1):
            for file in range(1, 9):
                full_rank = board[rank]
                piece = full_rank[file].piece.__str__()
                print('%2s' % self.get_piece_character(piece), end="")
            print()

    @staticmethod
    def get_piece_character(piece):
        if piece == "Black Rook":
            return "♖"
        if piece == "Black Knight":
            return "♘"
        if piece == "Black Bishop":
            return "♗"
        if piece == "Black Queen":
            return "♕"
        if piece == "Black King":
            return "♔"
        if piece == "Black Pawn":
            return "♙"
        if piece == "White Rook":
            return "♜"
        if piece == "White Knight":
            return "♞"
        if piece == "White Bishop":
            return "♝"
        if piece == "White Queen":
            return "♛"
        if piece == "White King":
            return "♚"
        if piece == "White Pawn":
            return "♟"
        return "◻"

    @staticmethod
    def convert_letter(letter):
        dictionary = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
            'f': 6,
            'g': 7,
            'h': 8,
        }
        return dictionary[letter.lower()]
