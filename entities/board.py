import pygame
from settings import WIDTH, HEIGHT, ROWS, COLS, CELL_SIZE, LINE_COLOR, LINE_WIDTH

class Board:
    def __init__(self):
        pass

    def draw(self, surface: pygame.Surface) -> None:
        for i in range(1, ROWS):
            y = i * CELL_SIZE
            pygame.draw.line(surface, LINE_COLOR, (0, y), (WIDTH, y), LINE_WIDTH)
            
        for i in range(1, COLS):
            x = i * CELL_SIZE
            pygame.draw.line(surface, LINE_COLOR, (x, 0), (x, HEIGHT), LINE_WIDTH)