import pygame
from constants import FPS, MIN_WIDTH, MIN_HEIGHT, SQUARE_SIZE
from constants import BLACK3, SOUND_EFFECTS, ICON_SIZE
from board import Board
from game import Game
from snake import Snake
from time import time
from other import music_icon, best_score_icon

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
pygame.mixer.music.set_volume(0.1)

# Images for sprites
COLOUR_APPLE_IMG = pygame.image.load(
        'Images/colourfull_apple.png').convert_alpha()
COLOUR_APPLE_IMG = pygame.transform.scale(
    COLOUR_APPLE_IMG, (SQUARE_SIZE, SQUARE_SIZE))
BLACK_COLOUR_IMG = pygame.image.load(
        'Images/black_apple.png').convert_alpha()
BLACK_COLOUR_IMG = pygame.transform.scale(
    BLACK_COLOUR_IMG, (SQUARE_SIZE, SQUARE_SIZE))
GREEN_COLOUR_IMG = pygame.image.load(
        'Images/green_apple.png').convert_alpha()
GREEN_COLOUR_IMG = pygame.transform.scale(
    GREEN_COLOUR_IMG, (SQUARE_SIZE, SQUARE_SIZE))
YELLOW_COLOUR_IMG = pygame.image.load(
        'Images/yellow_apple.png').convert_alpha()
YELLOW_COLOUR_IMG = pygame.transform.scale(
    YELLOW_COLOUR_IMG, (SQUARE_SIZE, SQUARE_SIZE))


play = True

board = Board(window)
snake = Snake()
snake_game = Game(window, board, snake)

last_time = time()
seconds = 0
while play:
    clock.tick(FPS)

    # turning off resizeability after moving the snake
    w, h = window.get_size()
    if snake_game.snake.moved is True:
        window = pygame.display.set_mode((w, h))
    else:
        window = pygame.display.set_mode((w, h), pygame.RESIZABLE)

    window.fill(BLACK3)

    if time() - last_time >= 1:
        seconds += 1
        last_time = time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake_game.snake.move_snake(board, 'N')
            if event.key == pygame.K_DOWN:
                snake_game.snake.move_snake(board, 'S')
            if event.key == pygame.K_RIGHT:
                snake_game.snake.move_snake(board, 'E')
            if event.key == pygame.K_LEFT:
                snake_game.snake.move_snake(board, 'W')
        if event.type == pygame.VIDEORESIZE:
            if snake_game.started is False:
                width, height = event.size
                # setting the minimal screen size
                if width < MIN_WIDTH:
                    width = MIN_WIDTH
                if height < MIN_HEIGHT:
                    height = MIN_HEIGHT
                window = pygame.display.set_mode(
                    (width, height), pygame.RESIZABLE)
                board.update_size()
                snake_game.game_logic.update_starting_point_before_start()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if x <= ICON_SIZE[0]:
                if y <= ICON_SIZE[1]:
                    if music is True:
                        music = False
                        pygame.mixer.music.fadeout(2000)
                    else:
                        music = True
                        pygame.mixer.music.play(-1)
    snake_game.printer.draw_rectangles()
    snake_game.printer.draw_score(snake)
    snake_game.printer.draw_time(seconds)
    snake_game.printer.draw_best_score("best_score.txt")
    snake_game.printer.draw_rectangles_taken()
    snake_game.printer.draw_eyes_on_snakes()

    music_icon(window, music)
    best_score_icon(window)
    # snake_game.printer.draw_sprite(YELLOW_COLOUR_IMG, (50, 50))
    # snake_game.printer.draw_sprite(BLACK_COLOUR_IMG, (150, 150))
    # snake_game.printer.draw_sprite(COLOUR_APPLE_IMG, (250, 250))
    # snake_game.printer.draw_sprite(GREEN_COLOUR_IMG, (350, 350))
    pygame.display.update()

pygame.quit()
