import pygame
import json
import os
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
        
        self.starting_player = "X" 
        self.player = self.starting_player
        self.game_over = False
        
        self.font = pygame.font.SysFont('times new roman', 30, bold=True)
        self.small_font = pygame.font.SysFont('arial', 25, bold=True)
        self.message = ""
        self.state = "MENU"
        
        self.scores_file = "scores.json"
        self.scores = self.load_scores()

    def load_scores(self):
        if os.path.exists(self.scores_file):
            with open(self.scores_file, "r") as file:
                return json.load(file)
        return {"X": 0, "O": 0, "Draws": 0}

    def save_scores(self):
        with open(self.scores_file, "w") as file:
            json.dump(self.scores, file, indent=4)

    def reset_game(self, starting_player=None):
        if starting_player:
            self.starting_player = starting_player
            
        self.board.reset()
        self.player = self.starting_player
        self.game_over = False
        self.message = ""

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                
            elif event.key == pygame.K_x and self.state == "MENU":
                self.state = "PLAYING"
                self.reset_game("X")
            elif event.key == pygame.K_o and self.state == "MENU":
                self.state = "PLAYING"
                self.reset_game("O")
            elif event.key == pygame.K_l and self.state == "MENU":
                self.state = "LEADERBOARD"
                
            elif event.key == pygame.K_r and self.state == "PLAYING":
                self.reset_game()
            elif event.key == pygame.K_m and self.state == "PLAYING":
                self.state = "MENU" 
            elif event.key == pygame.K_l and self.state == "PLAYING":
                self.state = "LEADERBOARD" 
                
            elif event.key == pygame.K_m and self.state == "LEADERBOARD":
                self.state = "MENU"

        elif event.type == pygame.MOUSEBUTTONDOWN and self.state == "PLAYING":
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
                    self.message = f" Player {winner} Wins! 'R' to Restart or 'M' for Menu "
                    self.scores[winner] += 1
                    self.save_scores()
                elif self.board.is_full():
                    self.game_over = True
                    self.message = " Draw! 'R' to Restart or 'M' for Menu "
                    self.scores["Draws"] += 1
                    self.save_scores()
                else:
                    if self.player == "X":
                        self.player = "O"
                    else:
                        self.player = "X"

    def update(self) -> None:
        pass 

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))
        
        if self.state == "MENU":
            title_surf = self.font.render("TIC-TAC-TOE", True, (0, 0, 0))
            title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            self.screen.blit(title_surf, title_rect)
            
            play_surf = self.small_font.render("Press X or O to Start", True, (100, 100, 100))
            play_rect = play_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            self.screen.blit(play_surf, play_rect)
            
            lead_surf = self.small_font.render("Press L for Leaderboard", True, (100, 100, 100))
            lead_rect = lead_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
            self.screen.blit(lead_surf, lead_rect)
            
        elif self.state == "PLAYING":
            self.board.draw(self.screen)
            if self.message != "":
                text_surface = self.font.render(self.message, True, TEXT_COLOR, TEXT_BG_COLOR)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                self.screen.blit(text_surface, text_rect)
                
        elif self.state == "LEADERBOARD":
            lead_title = self.font.render("LEADERBOARD", True, (0, 0, 0))
            lead_rect = lead_title.get_rect(center=(WIDTH // 2, 50))
            self.screen.blit(lead_title, lead_rect)
            
            sorted_scores = sorted(self.scores.items(), key=lambda item: item[1], reverse=True)
            y_offset = 150
            for name, score in sorted_scores:
                if name == "Draws":
                    display_text = f"Total Draws: {score}"
                else:
                    display_text = f"Player {name} Wins: {score}"
                    
                score_surf = self.font.render(display_text, True, (50, 50, 50))
                score_rect = score_surf.get_rect(center=(WIDTH // 2, y_offset))
                self.screen.blit(score_surf, score_rect)
                y_offset += 70
            
            back_surf = self.small_font.render("Press M for Menu", True, (100, 100, 100))
            back_rect = back_surf.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            self.screen.blit(back_surf, back_rect)
            
        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                self.handle_events(event)
            self.update()
            self.draw()

        pygame.quit()