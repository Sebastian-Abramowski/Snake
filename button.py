from pygame import mouse


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, window):
        # get mouse possition
        poss = mouse.get_pos()
        action = False

        # check if mouse if over the button
        if self.rect.collidepoint(poss):
            if mouse.get_pressed()[0] == 1:
                action = True

        window.blit(self.image, (
            self.rect.x, self.rect.y))

        return action
