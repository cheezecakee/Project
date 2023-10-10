import pymunk
import settings as s
from typing import Tuple, List
from game_components.character import Character

class Scroll:
    """
    Class responsible for creating the infinite scroll effect in the game.

    This class handles the scrolling of the game world, including the movement of the camera and
    the platforms. It also keeps track of the platforms that the character has passed.

    Attributes:
        space (pymunk.Space): The space in which the game objects exist.
        character_body (pymunk.Body): The body of the character.
        platforms (list[Tuple[pymunk.Body, pymunk.Segment]]): The platforms in the game.
        platforms_passed (int): The number of platforms that the character has passed.
        speed (float): The current speed of the scrolling.
        max_speed (float): The maximim speed of the scrolling.
        passed_platforms (dict): A dictionary to keep track of the platforms that have been passed.
    """

    def __init__(self, space: pymunk.Space, character: Character, platforms: List[Tuple[pymunk.Body, pymunk.Segment]]) -> None:
        """
        Initializes the Scroll class with the given space, character, and platforms.

        Args:
            space (pymunk.Space): The space in which the game objects exists.
            character (Character): The character in the game.
            platforms (list[Tuple[pymunk.Body, pymunk.Segment]]): The platforms in the game.
        """

        self.space = space
        self.character_body = character.body
        self.platforms = platforms
        self.platforms_passed: int = 0
        self.speed: float = 0
        self.max_speed: float = 3.0
        self.passed_platforms: dict = {}

    def move_camera(self) -> float:
        """
        Move camera based on character's y position.
        
        If the character's y position is less than half of the screen height, the scroll amount 
        is calculated as the difference between half of the screen height and the character's y
        position.
        Then, the y position of all bodies in the space is increased by the scroll amount. Finally,
        the platform counter is updated.

        Returns:
            float: The amount of scrolling.
        """

        follow_height: float = s.HEIGHT / 2
        scroll_amount: int = 0 # Initialize scroll_amount

        if self.character_body.position.y < follow_height:
            scroll_amount: float = follow_height - self.character_body.position.y

        for body in self.space.bodies:
            body.position = pymunk.Vec2d(body.position.x, body.position.y + scroll_amount)        
    
        self.platform_counter()
        return scroll_amount

    def platform_counter(self) -> int:
        """
        Counts the number of platforms that the character has passed.

        This method iterates over all paltforms. If the character's y position is less than the
        platform's y position and the platform have not been passed before, it increments the
        counter and marks the platform as passed.

        If all platforms have been passed, it resets the counter and the passed status of all 
        platforms.

        Returns:
            int: The number of platforms that the character has passed since the last reset.
        """
        
        counter: int = 0
        for body, platform in self.platforms:
            if self.character_body.position.y < body.position.y:
                if body not in self.passed_platforms:
                    self.passed_platforms[platform] = 1
                    counter += 1

        if sum(self.passed_platforms.values()) == len(self.platforms):
            counter: int = 0
            for platform in self.passed_platforms:
                self.passed_platforms[platform] = 0
        return counter

    def auto_scroll(self, elapsed_time) -> float:
        """
        Adjusts the speed of the scrolling based on the elapsed time and moves all bodies in the
        space accordingly.

        This method first calculates the speed by adding 0.5 to the ration of the elaptsed time to 60.
        If the calculated speed exceeds the maxium speed, it is set to the maximum speed.

        Then, it iterates over all bodies in the space and adjusts their y position by adding the
        calculated speed. This creates the effect of scrolling.

        Returns:
            float: The calculated speed of the scrolling.
        """
        
        self.speed: float = 0.5 + elapsed_time / 60
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        for body in self.space.bodies:
            body.position = pymunk.Vec2d(body.position.x, body.position.y + self.speed)
        return self.speed
    