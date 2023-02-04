import pygame
from constants import FPS, MIN_WIDTH, MIN_HEIGHT
from constants import BLACK3
from board import Board
from game import Game
from snake import Snake

pygame.init()
pygame.display.set_caption("Snake")
window = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
clock = pygame.time.Clock()

play = True
while play:
    clock.tick(FPS)
    window.fill(BLACK3)

    board = Board(window)
    snake = Snake()
    snake_game = Game(window, board, snake)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
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

    pygame.display.update()

pygame.quit()
