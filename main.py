import pygame
from constants import FPS, MIN_WIDTH, MIN_HEIGHT, SQUARE_SIZE
from constants import BLACK3, SOUND_EFFECTS, ICON_SIZE
from board import Board
from game import Game
from snake import Snake
from button import Button
from time import time
from other import write_best_score
from other import music_icon, best_score_icon, take_best_score
from snake import SNAKE_COLLISION, COLLISION_WITH_WALL_EVENT
from constants import DELAY_BETWEEN_MOVES
from constants import MOVING_SNAKE_EVERY_SEC_EVENT, EXTRA_SPEED_EVENT
from constants import NORMAL_SPEED_EVENT, END_OF_THE_GAME_EVENT
import sys


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption("Snake")
window = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Sounds
point_sound = pygame.mixer.Sound(
    'Sound/point_sound.wav')
collis_with_wall_sound = pygame.mixer.Sound(
    'Sound/wall_collision.wav')
collis_with_snake_sound = pygame.mixer.Sound(
    'Sound/snake_collision.wav')
click_sound = pygame.mixer.Sound(
    'Sound/click.wav')
pygame.mixer.music.load('Sound/old_snake_theme.wav')
if SOUND_EFFECTS == 1:
    music = True
    pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)
pygame.mixer.Sound.set_volume(collis_with_wall_sound, 0.05)
pygame.mixer.Sound.set_volume(collis_with_snake_sound, 0.05)
pygame.mixer.Sound.set_volume(click_sound, 0.05)

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


# every passed time this is called
# pygame.time.set_timer(
#     MOVING_SNAKE_EVERY_SEC_EVENT, DELAY_BETWEEN_MOVES)

# Button
BUTTON_RESTART_IMG = pygame.image.load('Images/reset.png')
BUTTON_EXIT_IMG = pygame.image.load('Images/exit.png')
BUTTON_PLAT_IMG = pygame.image.load('Images/play.png')
BUTTON_MENU_IMG = pygame.image.load('Images/menu.png')


def main_menu():
    while True:
        clock.tick(FPS)
        window.fill(BLACK3)

        button_play = Button(
            window.get_width() // 2 - 71,
            window.get_height() // 2 - 21,
            BUTTON_PLAT_IMG
            )

        button_exit = Button(
            window.get_width() // 2 - 71,
            window.get_height() // 2 + 30,
            BUTTON_EXIT_IMG
            )

        if button_exit.draw(window) is True:
            click_sound.play(0)
            pygame.time.wait(700)
            pygame.quit()
            sys.exit()
        if button_play.draw(window) is True:
            click_sound.play(0)
            pygame.time.set_timer(
                    MOVING_SNAKE_EVERY_SEC_EVENT, DELAY_BETWEEN_MOVES)
            main()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def main():
    global window, music

    play = True

    board = Board(window)
    snake = Snake()
    snake_game = Game(window, board, snake)
    snake_game.configurate_apples(
        GREEN_COLOUR_IMG, BLACK_COLOUR_IMG,
        YELLOW_COLOUR_IMG, COLOUR_APPLE_IMG)

    last_time = time()
    seconds = 0

    while play:
        clock.tick(FPS)
        music_icon(window, music)
        best_score_icon(window)
        snake_game.update_apples()
        snake_game.printer.draw(
            snake, seconds, "best_score.txt")

        # check for game over and reset
        if snake_game.end is True:
            possible_best_score = snake_game.snake.length
            best_score_in_file = take_best_score("best_score.txt")

            if possible_best_score > best_score_in_file:
                write_best_score("best_score.txt", possible_best_score)

            button_exit = Button(
                window.get_width() // 2 - 71,
                window.get_height() // 2 + 30,
                BUTTON_EXIT_IMG
                )

            if button_exit.draw(window) is True:
                click_sound.play(0)
                pygame.time.wait(700)
                play = False
                pygame.quit()
                sys.exit()

            button_reset = Button(
                window.get_width() // 2 - 71,
                window.get_height() // 2 - 21,
                BUTTON_RESTART_IMG
                )

            button_menu = Button(
                window.get_width() // 2 - 71,
                window.get_height() // 2 - 71,
                BUTTON_MENU_IMG
                )

            if button_menu.draw(window) is True:
                click_sound.play(0)
                main_menu()

            if button_reset.draw(window) is True:
                click_sound.play(0)
                pygame.time.set_timer(
                    MOVING_SNAKE_EVERY_SEC_EVENT, DELAY_BETWEEN_MOVES)
                main()

        pygame.display.update()

        # turning off resizeability after moving the snake
        w, h = window.get_size()
        if snake_game.snake.moved is True:
            window = pygame.display.set_mode((w, h))
        else:
            window = pygame.display.set_mode((w, h), pygame.RESIZABLE)

        window.fill(BLACK3)

        if time() - last_time >= 1:
            if snake_game.end is False:
                seconds += 1
                last_time = time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if snake_game.end is False:
                    if event.key == pygame.K_UP:
                        snake_game.snake.move_snake_player(board, 'N')
                    if event.key == pygame.K_DOWN:
                        snake_game.snake.move_snake_player(board, 'S')
                    if event.key == pygame.K_RIGHT:
                        snake_game.snake.move_snake_player(board, 'E')
                    if event.key == pygame.K_LEFT:
                        snake_game.snake.move_snake_player(board, 'W')
                    if event.key == pygame.K_1:
                        pygame.event.post(pygame.event.Event(
                            EXTRA_SPEED_EVENT))
                    if event.key == pygame.K_2:
                        pygame.event.post(pygame.event.Event(
                            NORMAL_SPEED_EVENT))
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
                        click_sound.play(0)
                        if music is True:
                            music = False
                            pygame.mixer.music.fadeout(2000)
                        else:
                            music = True
                            pygame.mixer.music.play(-1)
            if event.type == EXTRA_SPEED_EVENT:
                pygame.time.set_timer(MOVING_SNAKE_EVERY_SEC_EVENT, 200)
            if event.type == NORMAL_SPEED_EVENT:
                pygame.time.set_timer(
                    MOVING_SNAKE_EVERY_SEC_EVENT, DELAY_BETWEEN_MOVES)
            if event.type == MOVING_SNAKE_EVERY_SEC_EVENT:
                direction_of_sn = snake_game.snake.direction
                snake_game.snake.move_snake(board, direction_of_sn)
            if event.type == SNAKE_COLLISION:
                pygame.time.set_timer(MOVING_SNAKE_EVERY_SEC_EVENT, 0)
                if SOUND_EFFECTS == 1:
                    collis_with_snake_sound.play(0)
                pygame.time.wait(500)
                pygame.event.post(pygame.event.Event(END_OF_THE_GAME_EVENT))
            if event.type == COLLISION_WITH_WALL_EVENT:
                pygame.time.set_timer(MOVING_SNAKE_EVERY_SEC_EVENT, 0)
                if SOUND_EFFECTS == 1:
                    collis_with_wall_sound.play(0)
                pygame.time.wait(500)
                pygame.event.post(pygame.event.Event(END_OF_THE_GAME_EVENT))
            if event.type == END_OF_THE_GAME_EVENT:
                snake_game.end = True
                pygame.time.set_timer(
                    MOVING_SNAKE_EVERY_SEC_EVENT, 0)
        snake_game.check_for_collision_with_apple()


if __name__ == "__main__":
    main_menu()
