import scale_objects as so
from typing import Tuple
import pymunk

class Walls:
    """
    Class responsible for creating the walls of the game to prevent the character from going 
    out of bounds from the sides and creates a bounce effect when colliding with the character
    to boost velocity.
    """

    def __init__(self, space: pymunk.Space) -> None:
        """
        Initialize the Walls class with the given space.

        Args:
            space (pymunk.Space): A pymunk.Space object representing the game space.
        """
        
        self.space = space

    def create_walls(self) -> Tuple[pymunk.Segment, pymunk.Segment]:
        """
        Creates and returns static body segments as the wall.

        Returns:
            Tuple[Pymunk.Segment, pymunk.Segment]: A tuple of two pymunk.Segment objects representing the left and right walls of 
            the game.
        """

        LEFT_WALL = pymunk.Segment(self.space.static_body, (0, 0), (0, so.WALL_HEIGHT), so.WALL_THICKNESS)
        LEFT_WALL.elasticity: float = 1
        RIGHT_WALL = pymunk.Segment(self.space.static_body, (so.RIGHT_WALL_WIDTH, so.WALL_HEIGHT), (so.RIGHT_WALL_WIDTH, 0), so.WALL_THICKNESS)
        RIGHT_WALL.elasticity: float = 1
        return LEFT_WALL, RIGHT_WALL
