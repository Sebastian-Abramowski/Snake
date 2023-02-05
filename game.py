from snake import Snake
from constants import BLACK1, BLACK2, FONT
from constants import WHITE
from pygame import draw
from other import take_best_score


class Game:
    def __init__(self, window, board, snake):
        self.printer = GamePrinter(window, board)
        self.window = window
        self.snake = snake


class GamePrinter:
    def __init__(self, window, board):
        self.window = window
        self.board = board

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
        text = str(take_best_score(file_path))
        self._draw_text_by_border(text, 125)
