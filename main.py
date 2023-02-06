import pygame
from constants import FPS, MIN_WIDTH, MIN_HEIGHT, SQUARE_SIZE
from constants import BLACK3, SOUND_EFFECTS, ICON_SIZE
from board import Board
from game import Game
from snake import Snake
from time import time
from other import write_best_score
from other import music_icon, best_score_icon, take_best_score
from snake import SNAKE_COLLISION, COLLISION_WITH_WALL_EVENT
from constants import DELAY_BETWEEN_MOVES
from apples import Apple


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
pygame.mixer.music.load('Sound/old_snake_theme.wav')
if SOUND_EFFECTS == 1:
    music = True
    # pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)
pygame.mixer.Sound.set_volume(collis_with_wall_sound, 0.05)
pygame.mixer.Sound.set_volume(collis_with_snake_sound, 0.05)

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


# Custom event
MOVING_SNAKE_EVERY_SEC_EVENT = pygame.USEREVENT + 1
# every 3 sec this is called
pygame.time.set_timer(
    MOVING_SNAKE_EVERY_SEC_EVENT, DELAY_BETWEEN_MOVES)
EXTRA_SPEED_EVENT = pygame.USEREVENT + 2
NORMAL_SPEED_EVENT = pygame.USEREVENT + 3
END_OF_THE_GAME_EVENT = pygame.USEREVENT + 5
BLACK_APPLE_EVENT = pygame.USEREVENT + 6
pygame.time.set_timer(BLACK_APPLE_EVENT, 5000)


# Button
BUTTON_IMG = pygame.image.load('Images/restart_button.png')


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, window):
        # get mouse possition
        poss = pygame.mouse.get_pos()
        action = False

        # check if mouse if over the button
        if self.rect.collidepoint(poss):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        window.blit(self.image, (
            self.rect.x, self.rect.y))

        return action


def main():
    global window, music

    play = True

    board = Board(window)
    snake = Snake()
    snake_game = Game(window, board, snake)
    green_apple = Apple(GREEN_COLOUR_IMG, 'green', board, snake)
    black_apple = Apple(BLACK_COLOUR_IMG, 'black', board, snake)
    yellow_apple = Apple(YELLOW_COLOUR_IMG, 'yellow', board, snake)
    colour_apple = Apple(COLOUR_APPLE_IMG, 'colour', board, snake)

    last_time = time()
    seconds = 0

    while play:
        clock.tick(FPS)
        snake_game.printer.draw(
            snake, seconds, "best_score.txt")
        music_icon(window, music)
        best_score_icon(window)
        if green_apple.exists is False:
            green_apple.update_random_center_of_rect()
        green_apple.draw(window)
        if black_apple.exists is False:
            black_apple.update_random_center_of_rect()
        black_apple.draw(window)
        if yellow_apple.exists is False:
            yellow_apple.update_random_center_of_rect()
        yellow_apple.draw(window)
        if colour_apple.exists is False:
            colour_apple.update_random_center_of_rect()
        colour_apple.draw(window)

        # check for game over and reset
        if snake_game.end is True:
            possible_best_score = snake_game.snake.length
            best_score_in_file = take_best_score("best_score.txt")

            if possible_best_score > best_score_in_file:
                write_best_score("best_score.txt", possible_best_score)

            button = Button(
                window.get_width() // 2 - 71,
                window.get_height() // 2 - 21,
                BUTTON_IMG
                )
            if button.draw(window) is True:
                pygame.time.set_timer(
                    MOVING_SNAKE_EVERY_SEC_EVENT, DELAY_BETWEEN_MOVES)
                main()
            # play = False
        pygame.display.update()

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
                if snake_game.end is False:
                    if event.key == pygame.K_UP:
                        snake_game.snake.move_snake(board, 'N')
                    if event.key == pygame.K_DOWN:
                        snake_game.snake.move_snake(board, 'S')
                    if event.key == pygame.K_RIGHT:
                        snake_game.snake.move_snake(board, 'E')
                    if event.key == pygame.K_LEFT:
                        snake_game.snake.move_snake(board, 'W')
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
                        if music is True:
                            music = False
                            pygame.mixer.music.fadeout(2000)
                        else:
                            music = True
                            pygame.mixer.music.play(-1)
            if event.type == EXTRA_SPEED_EVENT:
                pygame.time.set_timer(MOVING_SNAKE_EVERY_SEC_EVENT, 100)
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
                pygame.time.set_timer(
                    MOVING_SNAKE_EVERY_SEC_EVENT, 0)
                snake_game.end = True

        # snake_game.printer.draw_sprite(YELLOW_COLOUR_IMG, (50, 50))
        # snake_game.printer.draw_sprite(BLACK_COLOUR_IMG, (150, 150))
        # snake_game.printer.draw_sprite(COLOUR_APPLE_IMG, (250, 250))
        # snake_game.printer.draw_sprite(GREEN_COLOUR_IMG, (350, 350))
        if snake_game.snake.check_for_coll_with_apple(green_apple):
            pygame.event.post(pygame.event.Event(NORMAL_SPEED_EVENT))
        if snake_game.snake.check_for_coll_with_apple(black_apple):
            pygame.event.post(pygame.event.Event(END_OF_THE_GAME_EVENT))
        if snake_game.snake.check_for_coll_with_apple(colour_apple):
            pygame.event.post(pygame.event.Event(EXTRA_SPEED_EVENT))
        if snake_game.snake.check_for_coll_with_apple(yellow_apple):
            pygame.event.post(pygame.event.Event(NORMAL_SPEED_EVENT))

    pygame.quit()


if __name__ == "__main__":
    main()
