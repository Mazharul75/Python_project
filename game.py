import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE, CELL_SIZE, TEXT_COLOR, TEXT_BG_COLOR
from entities import Board 

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.board = Board()
        self.player = "X"
        self.game_over = False
        self.font = pygame.font.SysFont('times new roman', 30, bold=True)
        self.message = ""

    def reset_game(self):
        self.board.reset()
        self.player = "X"
        self.game_over = False
        self.message = ""

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

            elif event.key == pygame.K_r:
                self.reset_game()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.game_over:
                return
            mouse_x, mouse_y = event.pos
            clicked_row = mouse_y // CELL_SIZE
            clicked_col = mouse_x // CELL_SIZE
        
            if self.board.available_square(clicked_row, clicked_col):
                self.board.mark_square(clicked_row, clicked_col, self.player)
                winner = self.board.check_winner()
                if winner:
                    self.game_over = True
                    self.message = f" Player {winner} Wins! Press 'R' to Restart "
                elif self.board.is_full():
                    self.game_over = True
                    self.message = " It's a Draw! Press 'R' to Restart "

                else:
                    if self.player == "X":
                        self.player = "O"
                    else:
                        self.player = "X"

    def update(self) -> None:
        pass 

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))
        self.board.draw(self.screen)
        if self.message != "":
            text_surface = self.font.render(self.message, True, TEXT_COLOR, TEXT_BG_COLOR)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                self.handle_events(event)

            self.update()
            self.draw()

        pygame.quit()