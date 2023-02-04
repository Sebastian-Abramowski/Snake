from constants import PADDING
from constants import BLACK1, BLACK2
from constants import SQUARE_SIZE
from pygame import draw, Rect


class Board:
    def __init__(self, window):
        # window - object pygame.display
        self.window = window
        self.square_size = SQUARE_SIZE
        self.centers_of_squares = self.calc_centers_of_squares()

    def _possible_size_of_win(self):
        w, h = self.window.get_size()
        poss_width = w - 2*PADDING
        poss_height = h - 2*PADDING
        return poss_width, poss_height

    def calc_num_of_squares(self):
        poss_width, poss_height = self._possible_size_of_win()

        how_many_horiz = poss_width // SQUARE_SIZE
        how_many_vertic = poss_height // SQUARE_SIZE

        return how_many_horiz, how_many_vertic

    def calc_centers_of_squares(self):
        centers_of_squares = []
        half_of_square = self.square_size//2
        y_point = PADDING + half_of_square

        num_of_squares_hori, num_of_squares_verti = self.calc_num_of_squares()

        for _ in range(num_of_squares_verti):
            x_point = PADDING + half_of_square
            row = []
            for _ in range(num_of_squares_hori):
                row.append((x_point, y_point))
                x_point += self.square_size
            centers_of_squares.append(row)
            y_point += self.square_size
        return centers_of_squares

    def draw_small_rectangles(self):
        for num_of_row, row in enumerate(self.centers_of_squares):
            for num_of_col, center in enumerate(row):
                half_of_square = self.square_size//2
                top_left = (center[0]-half_of_square, center[1]-half_of_square)
                rect = Rect(
                    top_left[0], top_left[1],
                    self.square_size, self.square_size)
                if num_of_row % 2 == 0 and num_of_col % 2 != 0:
                    colour = BLACK1
                elif num_of_row % 2 != 0 and num_of_col % 2 == 0:
                    colour = BLACK1
                else:
                    colour = BLACK2
                draw.rect(self.window, colour, rect)


# for later
# def draw_score_and_time(self):
#         img_font = FONT.render(who_won_text, True, colour_won)
#         font_width, _ = FONT.size(who_won_text)
#         width = window.get_width()
#         x = (width // 2)-(font_width//2)
#         window.blit(img_font, (x, 10))