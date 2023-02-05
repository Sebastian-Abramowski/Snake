
class Snake:
    def __init__(self):
        self.moved = False
        self.length = 3
        self.direction = 'E'
        self.head = None
        self.rectangles_taken = []

    def move_snake(self, board, where):
        # where = 'up' / 'left' / 'right' / 'down'
        if self.skip_unallowed_move(where):
            return None

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
        if i >= 0 and j >= 0:
            if cond1 and cond2:
                taken = self.rectangles_taken
                if board.rectangles[i][j] not in taken:
                    self.moved = True
                    self.head = (i, j)
                    self.rectangles_taken.append(
                        board.rectangles[i][j])
        self.check_length()

    def check_length(self):
        while len(self.rectangles_taken) > self.length:
            self.rectangles_taken.pop(0)

    def skip_unallowed_move(self, direction_p):
        cond1 = self.direction == 'N' and direction_p == 'S'
        cond2 = self.direction == 'S' and direction_p == 'N'
        cond3 = self.direction == 'E' and direction_p == 'W'
        cond4 = self.direction == 'W' and direction_p == 'E'
        if cond1 or cond2 or cond3 or cond4:
            return True
        return False
