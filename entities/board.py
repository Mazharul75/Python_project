import pygame
from settings import WIDTH, HEIGHT, ROWS, COLS, CELL_SIZE, LINE_COLOR, LINE_WIDTH, CROSS_COLOR, CIRCLE_COLOR, SPACE

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.winning_line = None 

    def reset(self):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.winning_line = None

    def available_square(self, row, col):
        return self.grid[row][col] is None

    def mark_square(self, row, col, player):
        self.grid[row][col] = player

    def check_winner(self):
        for row in range(ROWS):
            if self.grid[row][0] == self.grid[row][1] == self.grid[row][2] and self.grid[row][0] is not None:
                y = row * CELL_SIZE + CELL_SIZE // 2
                self.winning_line = [(0, y), (WIDTH, y)]
                return self.grid[row][0]

        for col in range(COLS):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] and self.grid[0][col] is not None:
                x = col * CELL_SIZE + CELL_SIZE // 2
                self.winning_line = [(x, 0), (x, HEIGHT)]
                return self.grid[0][col]

        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] and self.grid[0][0] is not None:
            self.winning_line = [(0, 0), (WIDTH, HEIGHT)] 
            return self.grid[0][0]
            
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] and self.grid[0][2] is not None:
            self.winning_line = [(WIDTH, 0), (0, HEIGHT)] 
            return self.grid[0][2]

        return None

    def is_full(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col] is None:
                    return False
        return True

    def draw(self, surface: pygame.Surface) -> None:
        for i in range(1, ROWS):
            y = i * CELL_SIZE
            pygame.draw.line(surface, LINE_COLOR, (0, y), (WIDTH, y), LINE_WIDTH)
            
        for i in range(1, COLS):
            x = i * CELL_SIZE
            pygame.draw.line(surface, LINE_COLOR, (x, 0), (x, HEIGHT), LINE_WIDTH)

        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col] == "O":
                    center_x = col * CELL_SIZE + CELL_SIZE // 2
                    center_y = row * CELL_SIZE + CELL_SIZE // 2
                    pygame.draw.circle(surface, CIRCLE_COLOR, (center_x, center_y), CELL_SIZE // 2 - SPACE, LINE_WIDTH)
                
                elif self.grid[row][col] == "X":
                    start_1 = (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE)
                    end_1 = (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + CELL_SIZE - SPACE)
                    pygame.draw.line(surface, CROSS_COLOR, start_1, end_1, LINE_WIDTH + 5)
                    
                    start_2 = (col * CELL_SIZE + SPACE, row * CELL_SIZE + CELL_SIZE - SPACE)
                    end_2 = (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + SPACE)
                    pygame.draw.line(surface, CROSS_COLOR, start_2, end_2, LINE_WIDTH + 5)
                    
        if self.winning_line:
            red_color = (250, 0, 0)
            pygame.draw.line(surface, red_color, self.winning_line[0], self.winning_line[1], LINE_WIDTH + 10)