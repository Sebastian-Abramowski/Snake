from pygame import sprite
from random import choice


class Apple(sprite.Sprite):
    def __init__(self, image, colour, center=(0, 0)):
        super().__init__()
        self.exists = True
        self.image = image
        self.colour = colour
        self.board = None
        self.snake = None
        self.center = center
        self.rect = self.image.get_rect(
            center=center)

    def configuration(self, board, snake):
        self.board = board
        self.snake = snake
        if self.center == (0, 0):
            self.rect.center = self.pick_random_center_of_rect()

    def pick_random_center_of_rect(self):
        picked = False
        while picked is False:
            center = choice(choice(self.board.rectangles)).center
            for rectangle in self.snake.rectangles_taken:
                if rectangle.center == center:
                    continue

            if center not in self.board.centers_with_apples:
                self.board.centers_with_apples.append(center)
                picked = True
            else:
                continue
        return center

    def update_random_center_of_rect(self):
        self.board.centers_with_apples.remove(self.rect.center)
        center = self.pick_random_center_of_rect()
        self.rect.center = center
        self.exists = True

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)
