from snake import Snake
from constants import BLACK1, BLACK2, FONT
from constants import WHITE
from pygame import draw


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

    def draw_score(self, snake):
        text = f"Score: {snake.length}"
        img_font = FONT.render(text, True, WHITE)
        font_width, _ = FONT.size(text)
        width = self.window.get_width()
        # center
        x = (width//2)-(font_width//2)
        # center of the right half
        x = x//2
        self.window.blit(img_font, (x, 15))
