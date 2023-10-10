import pymunk
from typing import Tuple, List
from game_components.character import Character

class Collision:
    """
    Class responsible for assigning the collision types to the shapes and deciding how they 
    should interact inside the space.
    """

    def __init__(self, space: pymunk.Space, character: Character, platforms: List[Tuple[pymunk.Body, pymunk.Segment]] ) -> None:
        """
        Initializes the Coliision Class with the given space, character, and platforms.

        Args:
            space (pymunk.Space): The space in which the game objects exists.
            character (Character): The character in the game.
            platforms (List[Tuple[pymunk.Body, pymunk.Segment]]): The platforms in the game. 
        """
        
        self.space = space
        self.character = character
        self.platforms = platforms
        self.on_ground: bool = True
        self.counter: int = -1 #This starts at -1 so that the score starts at 0

    def collide(self, arbiter, space, data) -> None:
        """
        Called when two shapes start touching for the first time.
        Prevents collision if the character is moving upwards.

        Args:
            arbiter (Arbiter): The arbiter for the collision.
            space (Space): The space in which the collision occurred.
            data (Any): Additional data.

        Returns:
            bool: Return True to process the collision normally or False to cause to ignore the 
            collision entirely.
        """
        
        if self.character.body.velocity.y < 0:
            self.on_ground = False
            return False
        elif abs(self.character.body.velocity.y) > 1e-3:
            self.on_ground = True
            return True
        return False
    
    def sensor_collide(self, arbiter, space, data) -> None:
        """
        Called when the character sensor starts touching a platform for the first time.
        Increments a counter everytime this happens.

        Args:
            arbiter (Arbiter): The arbiter for the collision.
            space (Space): The space in which the collision occurred.
            data (Any): Additional data.

        Returns:
            bool: Return True to process the collision normally of False if the body.pass is set
            to True.
        """

        body = arbiter.shapes[1].body
        if not body.passed:
            self.counter += 1
            body.passed = True
        return True

    def add_collision_handlers(self) -> None:
        """
        Add collision handler between the character and platform, and the collision handler
        between the character sensor and the platform.
        """
        
        self.handler = self.space.add_collision_handler(1, 2)
        self.handler.begin = self.collide

        self.sensor_handler = self.space.add_collision_handler(3, 2)
        self.sensor_handler.begin = self.sensor_collide

    def check_in_air(self) -> bool:
        """
        Checks if character is in the air.
        
        Returns:
            bool: True if character is in the  air, False otherwise.
        """
        
        if abs(self.character.body.velocity.y) > 0.01:
            self.on_ground = False
        else:
            self.on_ground = True

    def reset_counter(self) -> None:
        """Resets the counter."""
        self.counter = -1