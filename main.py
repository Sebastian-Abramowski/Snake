import pygame
from constants import FPS, MIN_WIDTH, MIN_HEIGHT
from constants import BLACK3, SOUND_EFFECTS
from board import Board
from game import Game
from snake import Snake
from time import time
from other import no_music_icon

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption("Snake")
window = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Sounds
point_sound = pygame.mixer.Sound(
    'Sound/point_sound.wav')
collis_with_wall_sound = pygame.mixer.Sound(
    'Sound/collision_with_wall_sound.wav')
pygame.mixer.music.load('Sound/old_snake_theme.wav')
if SOUND_EFFECTS == 1:
    music = True
    pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

play = True

board = Board(window)
snake = Snake()
snake_game = Game(window, board, snake)

last_time = time()
seconds = 0
while play:
    clock.tick(FPS)
    window.fill(BLACK3)

    if time() - last_time >= 1:
        seconds += 1
        last_time = time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                music = False
                pygame.mixer.music.fadeout(2000)
            if event.key == pygame.K_g:
                music = True
                pygame.mixer.music.play(-1)
        if event.type == pygame.VIDEORESIZE:
            width, height = event.size
            # setting the minimal screen size
            if width < MIN_WIDTH:
                width = MIN_WIDTH
            if height < MIN_HEIGHT:
                height = MIN_HEIGHT
            window = pygame.display.set_mode(
                (width, height), pygame.RESIZABLE)

    snake_game.printer.draw_rectangles()
    snake_game.printer.draw_score(snake)
    snake_game.printer.draw_time(seconds)

    no_music_icon(window, music)
    pygame.display.update()

pygame.quit()
