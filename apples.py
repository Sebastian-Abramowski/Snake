from pygame import sprite
from random import choice


class Apple(sprite.Sprite):
    def __init__(self, image, colour, board=None, snake=None, center=None):
        super().__init__()
        self.exists = True
        self.image = image
        self.colour = colour
        self.board = board
        self.snake = snake
        if board is not None and snake is not None:
            if center is not None:
                self.rect = self.image.get_rect(
                    center=center)
            else:
                self.rect = self.image.get_rect(
                    center=self.pick_random_center_of_rect())

    def pick_random_center_of_rect(self):
        picked = False
        while picked is False:
            center = choice(choice(self.board.rectangles)).center
            for rectangle in self.snake.rectangles_taken:
                if rectangle.center == center:
                    if rectangle.center not in self.board.centers_with_apples:
                        picked = False
                        continue
            self.board.centers_with_apples.append(center)
            picked = True
        return center

    def update_random_center_of_rect(self):
        self.board.centers_with_apples.remove(self.rect.center)
        center = self.pick_random_center_of_rect()
        self.rect.center = center
        self.exists = True

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)
