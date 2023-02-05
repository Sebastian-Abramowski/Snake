from pygame import sprite


class Apple(sprite.Sprite):
    def __init__(self, image, colour, center_p):
        super().__init__()
        self.image = image
        self.colour = colour
        self.rect = self.image.get_rect(
            center=center_p)
