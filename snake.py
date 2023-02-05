
class Snake:
    def __init__(self):
        self.length = 3
        self.directon = 'E'
        self.head = None
        self.rectangles_taken = []

    def move_snake(self, board, where):
        # where = 'up' / 'left' / 'right' / 'down'
        i, j = self.head
        if where == 'up':
            i -= 1
        elif where == 'down':
            i += 1
        elif where == 'right':
            j += 1
        elif where == 'left':
            j -= 1
        cond1 = (i <= len(board.rectangles) - 1)
        cond2 = (j <= len(board.rectangles[0]) - 1)
        if i >= 0 and j >= 0:
            if cond1 and cond2:
                taken = self.rectangles_taken
                if board.rectangles[i][j] not in taken:
                    self.started = True
                    self.head = (i, j)
                    self.rectangles_taken.append(
                        board.rectangles[i][j])
        self.check_length()

    def check_length(self):
        while len(self.rectangles_taken) > self.length:
            self.rectangles_taken.pop(0)
