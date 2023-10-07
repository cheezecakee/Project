import pygame
import os
import settings as s
from game_components.character import Character
from typing import List

class Mechanics:
    """Class responsible for setting the score, checking the game status and restarting the game."""
    
    def __init__(self) -> None:
        """Initializes the Mechanics class."""
        
        self.score: int = 0
        self.game_over: bool = False
        self.high_score_file: str = "highscore.txt"
        if not os.path.exists(self.high_score_file):
            with open(self.high_score_file, "w") as f:
                f.write("0")

    def check_game_status(self, character: Character) -> None:
        """
        Checks if the game is over based on the position of the character.
        
        Args:
            character (Character): The character in the game.
        """
        
        if character.body.position.y > s.HEIGHT:
            s.PARKOUR_SOUND.play()
            self.game_over = True
    
    def get_score(self, counter: int) -> int:
        """
        Creates the score system based on a counter.
        
        Args:
            counter (int): The counter to base the score on.

        Returns:
            int: The calculated score.
        """
        if self.game_over is False:
            self.score = counter * 10
            return self.score
        else:
            self.score = self.score
            return self.score

    def highscore(self) -> int:
        """
        Retrieves the high score, updates it if the current score
        and returns it.

        Returns:
            int: The high score.
        """
        
        highscore = self.get_highscore()
        if self.score > highscore:
            s.PARKOUR_SOUND.play()
            self.save_highscore(self.score)
        return highscore

    def get_highscore(self) -> int:
        """ 
        Reads the high score from a file and returns it.

        Returns:
            int: The high score.
        """
        
        with open(self.high_score_file, "r") as f:
            return int(f.read())

    def save_highscore(self, score) -> None:
        """
        Saves the high score to a file.

        Args:
            score (int): The score to save
        """
        
        with open(self.high_score_file, "w") as f:
            f.write(str(score))

    def restart_key(self) -> None:
        """Responsible for restarting the game on key press."""
        key: List[bool] = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.game_over = False
            self.score = 0
    
