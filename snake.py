import pygame
from constants import GREEN, WHITE, SQUARE_SIZE
from constants import SNAKE_COLLISION, COLLISION_WITH_WALL_EVENT


class Snake:
    def __init__(self):
        self.colour = GREEN
        self.moved = False
        self.length = 1
        self.direction = 'E'
        self.head = None
        self.rectangles_taken = []

    def _change_direction(self, where):
        x, y = self.head
        if where == 'N':
            x -= 1
        elif where == 'S':
            x += 1
        elif where == 'E':
            y += 1
        elif where == 'W':
            y -= 1
        self.direction = where
        return x, y

    def move_snake(self, board, where):
        x_of_new_head, y_of_new_head = self._change_direction(where)
        self._move_or_indicate_collision(board, x_of_new_head, y_of_new_head)
        self._check_length()

    def move_snake_player(self, board, where):
        # where = 'up' / 'left' / 'right' / 'down'
        if self._skip_unallowed_move(where):
            return None
        self.move_snake(board, where)

    def _move_or_indicate_collision(self, board, x_of_new_head, y_of_new_head):
        cond1 = (x_of_new_head <= len(board.rectangles) - 1)
        cond2 = (y_of_new_head <= len(board.rectangles[0]) - 1)
        if (x_of_new_head >= 0 and y_of_new_head >= 0) and (cond1 and cond2):
            taken = self.rectangles_taken
            if board.rectangles[x_of_new_head][y_of_new_head] not in taken:
                self.moved = True
                self.head = (x_of_new_head, y_of_new_head)
                self.rectangles_taken.append(
                    board.rectangles[x_of_new_head][y_of_new_head])
            else:
                pygame.event.post(pygame.event.Event(SNAKE_COLLISION))
        else:
            if self.colour == GREEN:
                pygame.event.post(pygame.event.Event(
                    COLLISION_WITH_WALL_EVENT))
            else:
                if x_of_new_head < 0:
                    x_of_new_head = len(board.rectangles) - 1
                elif y_of_new_head < 0:
                    y_of_new_head = len(board.rectangles[0]) - 1
                elif not cond1:
                    x_of_new_head = 0
                elif not cond2:
                    y_of_new_head = 0
                self.moved = True
                self.head = (x_of_new_head, y_of_new_head)
                self.rectangles_taken.append(
                    board.rectangles[x_of_new_head][y_of_new_head])

    def _check_length(self):
        while len(self.rectangles_taken) > self.length:
            self.rectangles_taken.pop(0)

    def _skip_unallowed_move(self, direction_p):
        verti = ['N', 'S']
        hori = ['E', 'W']
        cond1 = self.direction in verti and direction_p in verti
        cond2 = self.direction in hori and direction_p in hori
        if cond1 or cond2:
            return True
        return False

    def check_for_coll_with_apple(self, apple):
        for rectangle in self.rectangles_taken:
            if apple.rect.center == rectangle.center:
                apple.exists = False
                if apple.colour == 'green':
                    self.length += 1
                    self.colour = GREEN
                if apple.colour == 'yellow':
                    self.length += 2
                    self.colour = WHITE
                return True
        return False

    def draw(self, window):
        how_many = len(self.rectangles_taken)
        for i, rectangle in enumerate(self.rectangles_taken):
            if how_many == 1:
                pygame.draw.circle(
                    window, self.colour, rectangle.center, SQUARE_SIZE//2)
            elif i == (how_many - 1) or i == 0:
                direction_of_head = self.direction
                if i == 0:
                    direction_of_head = None
                    direction_of_tail = self._direction_of_last_square()
                else:
                    direction_of_tail = None

                if direction_of_head == 'E' or direction_of_tail == 'W':
                    recta = pygame.Rect(
                        rectangle.left, rectangle.top,
                        SQUARE_SIZE // 2, SQUARE_SIZE)
                if direction_of_head == 'W' or direction_of_tail == 'E':
                    recta = pygame.Rect(
                        rectangle.left + SQUARE_SIZE // 2, rectangle.top,
                        SQUARE_SIZE // 2, SQUARE_SIZE)
                if direction_of_head == 'N' or direction_of_tail == 'S':
                    recta = pygame.Rect(
                        rectangle.left, rectangle.top + SQUARE_SIZE//2,
                        SQUARE_SIZE, SQUARE_SIZE//2)
                if direction_of_head == 'S' or direction_of_tail == 'N':
                    recta = pygame.Rect(
                        rectangle.left, rectangle.top, SQUARE_SIZE,
                        SQUARE_SIZE//2)
                pygame.draw.rect(window, self.colour, recta)
                pygame.draw.circle(
                    window, self.colour, rectangle.center, SQUARE_SIZE//2)
            else:
                pygame.draw.rect(window, self.colour, rectangle)

    def _direction_of_last_square(self):
        if len(self.rectangles_taken) < 2:
            return None
        center_last = self.rectangles_taken[0].center
        center_after_last = self.rectangles_taken[1].center
        if center_after_last[0] > center_last[0]:
            return 'E'
        elif center_after_last[0] < center_last[0]:
            return 'W'
        elif center_after_last[1] > center_last[1]:
            return 'S'
        else:
            return 'N'
