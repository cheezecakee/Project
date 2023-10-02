import pygame
import settings as s
from game_components.character import Character

class Mechanics:
    """Responsible for setting the score, checking the game status and restarting the game."""
    def __init__(self) -> None:
        self.score: int = 0
        self.game_over: bool = False

    def check_game_status(self, character: Character) -> None:
        """Checks if the game is over based on the position of the character."""
        if character.body.position.y > s.HEIGHT:
            self.game_over = True
    
    def get_score(self, counter: int) -> int:
        """Creates the score system based on a counter."""
        self.score = counter * 10
        return self.score

    def restart_key(self) -> None:
        """Responsible for restarting the game on key press."""
        key: list[bool] = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.game_over = False
            self.score = 0