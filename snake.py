import pygame
from constants import GREEN, WHITE

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
            pygame.event.post(pygame.event.Event(COLLISION_WITH_WALL_EVENT))
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
        for rectangle in self.rectangles_taken:
            pygame.draw.rect(window, self.colour, rectangle)
