from pygame import image, transform
from constants import ICON_SIZE


def no_music_icon(window, music):
    # window - pygame.dispaly
    if music is True:
        is_on = 'on'
    else:
        is_on = 'off'
    image_p = image.load(f'Images/sound-{is_on}.png')
    image_p = transform.scale(image_p, ICON_SIZE)
    rect = image_p.get_rect()
    rect.top = 5
    rect.left = 5
    window.blit(image_p, rect)
