import pygame
from constants import GREEN, WHITE, SQUARE_SIZE

SNAKE_COLLISION = pygame.USEREVENT + 4
COLLISION_WITH_WALL_EVENT = pygame.USEREVENT


class Snake:
    def __init__(self):
        self.colour = GREEN
        self.moved = False
        self.length = 1
        self.direction = 'E'
        self.head = None
        self.rectangles_taken = []

    def move_snake(self, board, where):
        i, j = self.head
        if where == 'N':
            i -= 1
        elif where == 'S':
            i += 1
        elif where == 'E':
            j += 1
        elif where == 'W':
            j -= 1
        self.direction = where
        cond1 = (i <= len(board.rectangles) - 1)
        cond2 = (j <= len(board.rectangles[0]) - 1)
        if (i >= 0 and j >= 0) and (cond1 and cond2):
            taken = self.rectangles_taken
            if board.rectangles[i][j] not in taken:
                self.moved = True
                self.head = (i, j)
                self.rectangles_taken.append(
                    board.rectangles[i][j])
            else:
                pygame.event.post(pygame.event.Event(SNAKE_COLLISION))
        else:
            if self.colour == GREEN:
                pygame.event.post(pygame.event.Event(COLLISION_WITH_WALL_EVENT))
            else:
                if i < 0:
                    i = len(board.rectangles) - 1
                elif j < 0:
                    j = len(board.rectangles[0]) - 1
                elif not cond1:
                    i = 0
                elif not cond2:
                    j = 0
                self.moved = True
                self.head = (i, j)
                self.rectangles_taken.append(board.rectangles[i][j])
        self.check_length()

    def move_snake_player(self, board, where):
        # where = 'up' / 'left' / 'right' / 'down'
        if self.skip_unallowed_move(where):
            return None
        self.move_snake(board, where)

    def check_length(self):
        while len(self.rectangles_taken) > self.length:
            self.rectangles_taken.pop(0)

    def skip_unallowed_move(self, direction_p):
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
            elif i == (how_many - 1):
                if self.direction == 'E':
                    recta = pygame.Rect(
                        rectangle.left, rectangle.top, SQUARE_SIZE // 2, SQUARE_SIZE)
                if self.direction == 'W':
                    recta = pygame.Rect(
                        rectangle.left + SQUARE_SIZE // 2, rectangle.top, SQUARE_SIZE // 2, SQUARE_SIZE)
                if self.direction == 'N':
                    recta = pygame.Rect(
                        rectangle.left, rectangle.top + SQUARE_SIZE//2, SQUARE_SIZE, SQUARE_SIZE//2)
                if self.direction == 'S':
                    recta = pygame.Rect(
                        rectangle.left, rectangle.top, SQUARE_SIZE, SQUARE_SIZE//2)
                pygame.draw.rect(window, self.colour, recta)
                pygame.draw.circle(
                    window, self.colour, rectangle.center, SQUARE_SIZE//2)
            elif i == 0:
                direction = self._direction_of_last_square()
                if direction == 'E':
                    recta = pygame.Rect(
                        rectangle.left + SQUARE_SIZE // 2, rectangle.top, SQUARE_SIZE // 2, SQUARE_SIZE)
                if direction == 'W':
                    recta = pygame.Rect(
                        rectangle.left, rectangle.top, SQUARE_SIZE // 2, SQUARE_SIZE)
                if direction == 'N':
                    recta = pygame.Rect(
                        rectangle.left, rectangle.top, SQUARE_SIZE, SQUARE_SIZE//2)
                if direction == 'S':
                    recta = pygame.Rect(
                        rectangle.left, rectangle.top + SQUARE_SIZE//2, SQUARE_SIZE, SQUARE_SIZE//2)
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
