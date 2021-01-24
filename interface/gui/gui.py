import pygame

from domain.entities.pieces import NoPiece


class GUI:
    def __init__(self, game, screen_size):
        self.game = game
        self.move_sound = None
        self.dimension = 8
        self.width = self.height = screen_size
        self.square_size = self.height // self.dimension
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.frames_per_second = 15
        self.images = {}
        self.Clock = pygame.time.Clock()
        self.selected_square = ()
        self.clicked_squares = []

    def run(self):
        self.get_game_initialized()
        while True:
            pygame.time.delay(100)

            human_to_move = self.game.current_player.is_human
            if human_to_move:
                events = pygame.event.get()

                for event in events:
                    exit_game = event.type == pygame.QUIT
                    game_is_active = self.game.game_status == "ACTIVE"
                    is_key_press = event.type == pygame.KEYDOWN

                    if exit_game:
                        exit()
                    elif game_is_active:
                        game_was_active = self.game.game_status == "ACTIVE"
                        clicked = self.get_click_event(event)
                        game_is_active = self.game.game_status == "ACTIVE"
                        if game_is_active and clicked:
                            self.get_game_drawn(self.selected_square)
                            self.get_screen_refreshed()
                        if game_was_active and not game_is_active:
                            self.game.get_next_player_turn()
                    if is_key_press:
                        key_Z_pressed = event.key == pygame.K_z
                        if key_Z_pressed:
                            if self.game.game_status != "ACTIVE":
                                self.get_undo()
                                self.game.get_next_player_turn()
                            else:
                                self.get_undo()
                        game_is_active = self.game.game_status == "ACTIVE"
                        if game_is_active:
                            self.get_game_drawn(self.selected_square)
                            self.get_screen_refreshed()
            else:
                if self.game.game_status != "ACTIVE":
                    break
                self.get_text_drawn("Computer loading...")
                self.game.get_computer_move()
                self.get_move_sound_triggered()
                self.get_game_drawn(self.selected_square)
                self.get_screen_refreshed()
                self.get_game_ending_manner_displayed()
        input()

    def get_game_initialized(self):
        pygame.init()
        pygame.display.set_caption('Chess')
        programIcon = pygame.image.load("interface\\gui\\images\\White Queen.png")
        pygame.display.set_icon(programIcon)
        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound("interface\\gui\\sounds\\move.ogg")
        self.get_images_loaded()
        self.screen.fill(pygame.Color("white"))
        self.get_game_drawn(self.selected_square)
        self.Clock.tick(self.frames_per_second)
        pygame.display.update()

    def get_move_sound_triggered(self):
        pygame.mixer.Sound.play(self.move_sound)

    def get_undo(self):
        self.game.get_double_undo_performed()
        self.get_screen_refreshed()
        self.get_click_history_reset()

    def get_screen_refreshed(self):
        self.Clock.tick(self.frames_per_second)
        pygame.display.update()
        self.get_pieces_drawn()
        self.game.get_game_status()

    def get_click_event(self, event):
        is_mouse_click = event.type == pygame.MOUSEBUTTONDOWN
        if is_mouse_click:
            file, rank = self.get_chessboard_position(self.square_size, self.dimension)
            square_already_selected = self.selected_square == (file, rank)
            source_file, source_rank = None, None

            if square_already_selected:
                self.selected_square = ()
                self.clicked_squares = []
            else:
                self.selected_square = (file, rank)
                self.clicked_squares.append(self.selected_square)
                source_file, source_rank = self.get_source_move_coordinates(self.clicked_squares)

                source_square = self.game.board.get_square(source_rank, source_file)
                is_empty_square = type(source_square.piece) == NoPiece
                is_own_piece = source_square.piece.is_white == self.game.current_player.is_white
                square_owned = not is_empty_square and is_own_piece
                if not square_owned:
                    self.selected_square = ()
                    self.clicked_squares = []

            move_is_ready = len(self.clicked_squares) == 2
            if move_is_ready:
                self.get_move_performed(source_file, source_rank)
                self.get_game_ending_manner_displayed()
            return True
        return False

    def get_move_performed(self, source_file, source_rank):
        destination_file, destination_rank = self.get_destination_move_coordinates(self.clicked_squares)
        player = self.game.current_player
        move_performed_successfully = self.game.get_human_move(player, source_rank, source_file,
                                                               destination_rank,
                                                               destination_file)
        if move_performed_successfully:
            move = self.game.get_last_move()
            self.get_move_animation(move)
            self.get_move_sound_triggered()
        self.get_screen_refreshed()
        self.get_click_history_reset()

    def get_game_ending_manner_displayed(self):
        if self.game.game_status == "CHECKMATE":
            if not self.game.current_player.is_white:
                self.get_text_drawn("White wins by checkmate!")
            else:
                self.get_text_drawn("Black wins by checkmate!")
        elif self.game.game_status == "STALEMATE":
            self.get_text_drawn("Stalemate!")

    def get_text_drawn(self, text):
        font = pygame.font.SysFont("Tahoma", 50, True, False)
        text_object = font.render(text, 0, pygame.Color('Black'))
        text_location = pygame.Rect(0, 0, self.width, self.height).move(self.width / 2 - text_object.get_width() / 2,
                                                                        self.height / 2 - text_object.get_height() / 2)
        self.screen.blit(text_object, text_location)
        self.Clock.tick(self.frames_per_second)
        pygame.display.flip()

    def get_click_history_reset(self):
        self.clicked_squares = []
        self.selected_square = ()

    def is_selected_square_available(self, selected_square):
        if selected_square != ():
            file, rank = selected_square
            square = self.game.board.get_square(rank, file)
            piece = self.game.board[rank][file].piece
            if not isinstance(piece, NoPiece):
                if self.game.current_player.is_white == piece.is_white:
                    self.get_selected_square_available_moves_highlighted(square.file, square.rank)

    def get_selected_square_available_moves_highlighted(self, file, rank):
        square = self.game.board.get_square(rank, file)
        surface = pygame.Surface((self.square_size, self.square_size))
        surface.set_alpha(100)
        surface.fill(pygame.Color('yellow'))
        self.screen.blit(surface, ((file - 1) * self.square_size, (self.dimension - rank) * self.square_size))
        surface.fill(pygame.Color('gray'))
        for move in self.game.get_all_valid_moves_of_square(square):
            self.screen.blit(surface, (
                (move.move_to.file - 1) * self.square_size, (self.dimension - move.move_to.rank) * self.square_size))

    def get_chessboard_position_from_square(self, file, rank):
        file_position = (file - 1) * self.square_size
        rank_position = (self.dimension - rank) * self.square_size
        return file_position, rank_position

    def get_images_loaded(self):
        pieces = [
            "White Pawn", "Black Pawn",
            "White Knight", "Black Knight",
            "White Bishop", "Black Bishop",
            "White Rook", "Black Rook",
            "White Queen", "Black Queen",
            "White King", "Black King"
        ]
        for piece in pieces:
            self.images[piece] = pygame.transform.scale(pygame.image.load("interface/gui/images/" + piece + ".png"),
                                                        (self.square_size, self.square_size))

    def get_game_drawn(self, selected_square):
        self.get_board_drawn()
        self.is_selected_square_available(selected_square)
        self.get_pieces_drawn()

    def get_board_drawn(self):
        colors = [pygame.Color("#b58863"), pygame.Color("#f0d9b5")]
        chessboard = range(self.dimension)
        for rank in chessboard:
            for file in chessboard:
                color = colors[((rank + file + 1) % 2)]
                pygame.draw.rect(self.screen, color,
                                 pygame.Rect(file * self.square_size, rank * self.square_size, self.square_size,
                                             self.square_size))

    def get_pieces_drawn(self):
        chessboard = range(self.dimension)
        for rank in chessboard:
            for file in chessboard:
                board = self.game.board
                rank_position = self.dimension - rank
                file_position = self.dimension - file
                square = board[rank_position][file_position]
                piece = square.piece
                piece_name = piece.__str__()
                square_is_not_empty = piece_name != "None"
                if square_is_not_empty:
                    self.screen.blit(self.images[piece_name],
                                     pygame.Rect((self.dimension - file - 1) * self.square_size,
                                                 rank * self.square_size,
                                                 self.square_size, self.square_size))

    def get_move_animation(self, move):
        colors = [pygame.Color("#b58863"), pygame.Color("#f0d9b5")]
        destination_rank = move.move_to.rank - move.move_from.rank
        destination_file = move.move_to.file - move.move_from.file
        frame_count = (abs(destination_rank) + abs(destination_file)) * self.frames_per_second
        for frame in range(frame_count + 1):
            rank = self.dimension - move.move_from.rank + -destination_rank * frame / frame_count
            file = (move.move_from.file - 1 + destination_file * frame / frame_count)
            self.get_board_drawn()
            self.get_pieces_drawn()
            color = colors[((int(move.move_to.rank) + int(move.move_to.file)) % 2)]
            end_square = pygame.Rect((move.move_to.file - 1) * self.square_size,
                                     (self.dimension - move.move_to.rank) * self.square_size, self.square_size,
                                     self.square_size)
            pygame.draw.rect(self.screen, color, end_square)
            piece_was_captured = str(move.killed_piece) != "None"
            if piece_was_captured:
                piece_to_add = str(move.killed_piece)
                self.screen.blit(self.images[piece_to_add], end_square)
            piece = move.moved_piece
            piece_name = piece.__str__()
            self.screen.blit(self.images[piece_name],
                             pygame.Rect(file * self.square_size,
                                         rank * self.square_size,
                                         self.square_size, self.square_size))
            pygame.display.flip()
            self.Clock.tick(600)

    @staticmethod
    def get_source_move_coordinates(clicked_squares):
        source_click = clicked_squares[0]
        source_rank = source_click[1]
        source_file = source_click[0]
        return source_file, source_rank

    @staticmethod
    def get_destination_move_coordinates(clicked_squares):
        destination_click = clicked_squares[1]
        destination_rank = destination_click[1]
        destination_file = destination_click[0]
        return destination_file, destination_rank

    @staticmethod
    def get_chessboard_position(square_size, dimension):
        location = pygame.mouse.get_pos()
        horizontal_location = location[0]
        vertical_location = location[1]
        file = horizontal_location // square_size + 1
        rank = dimension - (vertical_location // square_size)
        return file, rank
