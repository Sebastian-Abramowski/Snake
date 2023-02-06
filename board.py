from constants import PADDING
from constants import SQUARE_SIZE
from pygame import Rect


class Board:
    def __init__(self, window):
        # window - object pygame.display
        self.window = window
        self.square_size = SQUARE_SIZE
        self.centers_of_squares = self.calc_centers_of_squares()
        self.rectangles = self.make_array_of_rectangles()
        self.centers_with_apples = []

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
        w, h = self._possible_size_of_win()

        centers_of_squares = []
        half_of_square = self.square_size//2
        num_of_squares_hori, num_of_squares_verti = self.calc_num_of_squares()

        x_start_point = (w - (num_of_squares_hori * self.square_size)) // 2
        y_start_point = (h - (num_of_squares_verti * self.square_size)) // 2
        y_point = PADDING + y_start_point + half_of_square

        for _ in range(num_of_squares_verti):
            x_point = PADDING + x_start_point + half_of_square
            row = []
            for _ in range(num_of_squares_hori):
                row.append((x_point, y_point))
                x_point += self.square_size
            centers_of_squares.append(row)
            y_point += self.square_size

        return centers_of_squares

    def make_array_of_rectangles(self):
        rects = []
        for row in self.centers_of_squares:
            row_of_rects = []
            for center in row:
                half_of_square = self.square_size//2
                top_left = (center[0]-half_of_square, center[1]-half_of_square)
                rect = Rect(
                    top_left[0], top_left[1],
                    self.square_size, self.square_size)
                row_of_rects.append(rect)
            rects.append(row_of_rects)

        return rects

    def update_size(self):
        self.centers_of_squares = self.calc_centers_of_squares()
        self.rectangles = self.make_array_of_rectangles()
