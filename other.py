from pygame import image, transform
from constants import ICON_SIZE


class FileReadingException(Exception):
    def __init__(self):
        super().__init__('Something went wrong while reading your file')


def music_icon(window, music):
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


def best_score_icon(window):
    image_p = image.load('Images/best_score.jpeg')
    image_p = transform.scale(image_p, ICON_SIZE)
    rect = image_p.get_rect()
    rect.top = 7
    rect.left = 70
    window.blit(image_p, rect)


def take_best_score(txt_file_name):
    try:
        with open(txt_file_name, 'r') as file_handle:
            best_score = file_handle.read()
    except Exception:
        raise FileReadingException()

    try:
        best_score = int(best_score)
    except Exception:
        best_score = 0
        with open(txt_file_name, 'w') as file_handle:
            file_handle.write('0')
    return int(best_score)


def write_best_score(txt_file_name, score):
    with open(txt_file_name, 'w') as file_handle:
        file_handle.write(str(score))
