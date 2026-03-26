import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
from entities import Board 

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.board = Board() 

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

    def update(self) -> None:
        pass 

    def draw(self) -> None:
        self.screen.fill((18, 18, 22))
        self.board.draw(self.screen)
        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                self.handle_events(event)

            self.update()
            self.draw()

        pygame.quit()