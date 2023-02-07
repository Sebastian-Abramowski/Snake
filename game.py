from constants import BLACK1, BLACK2, FONT
from constants import WHITE, SQUARE_SIZE
from pygame import draw, event
from other import take_best_score
from apples import Apple
from constants import NORMAL_SPEED_EVENT, END_OF_THE_GAME_EVENT
from constants import EXTRA_SPEED_EVENT


class Game:
    def __init__(self, window, board, snake):
        self.end = False
        self.game_logic = GameLogic(board, snake)
        self.printer = GamePrinter(window, board, self.game_logic, self)
        self.board = board
        self.window = window
        self.snake = snake
        self.green_apple = None
        self.black_apple = None
        self.yellow_apple = None
        self.colour_apple = None

    def configurate_apples(self, green_img, black_img,
                           yellow_img, colour_img):
        self.green_apple = Apple(green_img, 'green')
        self.green_apple.configuration(self.board, self.snake)
        self.black_apple = Apple(black_img, 'black')
        self.black_apple.configuration(self.board, self.snake)
        self.yellow_apple = Apple(yellow_img, 'yellow')
        self.yellow_apple.configuration(self.board, self.snake)
        self.colour_apple = Apple(colour_img, 'colour')
        self.colour_apple.configuration(self.board, self.snake)

    def check_for_collision_with_apple(self):
        bool_coll_with_green = self.snake.check_for_coll_with_apple(
            self.green_apple)
        bool_coll_with_yellow = self.snake.check_for_coll_with_apple(
            self.yellow_apple)
        if bool_coll_with_green or bool_coll_with_yellow:
            event.post(event.Event(NORMAL_SPEED_EVENT))
        if self.snake.check_for_coll_with_apple(self.black_apple):
            event.post(event.Event(END_OF_THE_GAME_EVENT))
        if self.snake.check_for_coll_with_apple(self.colour_apple):
            event.post(event.Event(EXTRA_SPEED_EVENT))

    def update_apples(self):
        self._check_for_update_apples(self.green_apple)
        self._check_for_update_apples(self.yellow_apple)
        self._check_for_update_apples(self.colour_apple)

    def _check_for_update_apples(self, apple):
        if apple.exists is False:
            apple.update_random_center_of_rect()


class GamePrinter:
    def __init__(self, window, board, logic, game):
        self.window = window
        self.board = board
        self.game_logic = logic
        self.game = game

    def draw_rectangles(self):
        for num_of_row, row in enumerate(self.board.rectangles):
            for num_of_col, rectangle in enumerate(row):
                if num_of_row % 2 == 0 and num_of_col % 2 != 0:
                    colour = BLACK1
                elif num_of_row % 2 != 0 and num_of_col % 2 == 0:
                    colour = BLACK1
                else:
                    colour = BLACK2
                draw.rect(self.window, colour, rectangle)

    def _draw_text(self, text, percent: float):
        # percent 0.5 means center 0.25 means left quarter etc
        img_font = FONT.render(text, True, WHITE)
        font_width, _ = FONT.size(text)
        font_width = font_width * percent
        width = self.window.get_width() * percent
        x = width - font_width
        self.window.blit(img_font, (x, 15))

    def _draw_text_by_border(self, text, right_border):
        # right border in pixels
        img_font = FONT.render(text, True, WHITE)
        self.window.blit(img_font, (right_border, 15))

    def draw_score(self, snake):
        text = f"Score: {snake.length}"
        self._draw_text(text, 0.25)

    def draw_time(self, num_of_seconds):
        min = num_of_seconds // 60
        sec = num_of_seconds - (60 * min)
        text = f"Time {min:02}:{sec:02}"
        self._draw_text(text, 0.75)

    def draw_best_score(self, file_path):
        best_score = self.game_logic.check_best_score(file_path)
        text = str(best_score)
        self._draw_text_by_border(text, 125)

    def draw_eyes_on_snakes(self):
        radius = int(SQUARE_SIZE*0.1)
        for poss_x, poss_y in self.game_logic.possition_of_eyes():
            draw.circle(self.window, BLACK1, (poss_x, poss_y), radius)

    def draw(self, snake, seconds, file_path):
        self.draw_score(snake)
        self.draw_rectangles()
        self.draw_time(seconds)
        self.draw_best_score(file_path)
        self.game_logic.snake.draw(self.window)
        self.draw_eyes_on_snakes()
        self.draw_apples()

    def draw_apples(self):
        self.game.green_apple.draw(self.window)
        if self.game.black_apple.exists:
            self.game.black_apple.draw(self.window)
        self.game.yellow_apple.draw(self.window)
        self.game.colour_apple.draw(self.window)


class GameLogic:
    def __init__(self, board, snake):
        self.board = board
        self.snake = snake
        snake.rectangles_taken = [self.starting_rectangle()]

    def starting_rectangle(self):
        index_i = len(self.board.rectangles) // 2
        index_j = 2

        # some restriction needed
        self.snake.head = (index_i, index_j)
        return self.board.rectangles[index_i][index_j]

    def update_starting_point_before_start(self):
        self.snake.rectangles_taken = [self.starting_rectangle()]

    def possition_of_eyes(self):
        direction = self.snake.direction
        currect_rect = self.snake.rectangles_taken[-1]

        to_return = []
        x, y = currect_rect.center
        if direction in ['N', 'W']:
            x -= int(0.25 * SQUARE_SIZE)
            y -= int(0.25 * SQUARE_SIZE)
        else:
            x += int(0.25 * SQUARE_SIZE)
            y += int(0.25 * SQUARE_SIZE)
        to_return.append((x, y))
        x, y = currect_rect.center
        if direction in ['S', 'W']:
            x -= int(0.25 * SQUARE_SIZE)
            y += int(0.25 * SQUARE_SIZE)
        else:
            x += int(0.25 * SQUARE_SIZE)
            y -= int(0.25 * SQUARE_SIZE)
        to_return.append((x, y))
        return to_return

    def check_best_score(self, file_path):
        best_score_acc_to_file = take_best_score(file_path)
        best_score_maybe = self.snake.length
        if best_score_maybe > best_score_acc_to_file:
            return best_score_maybe
        return best_score_acc_to_file
