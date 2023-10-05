
from game_components.character import Character
from game_components.platform_manager import PlatformManager
from game_components.walls import Walls
from pymunk import Space
import settings as s


class GameSetup:
    """Class responsible for setting up the game environment.
    This includes adding the character, platforms, and walls into the pymunk space.
    """

    def __init__(self, space: Space) -> None:
        """
        Initialize the space, space settings, bodies and shapes to be add to the space.
        
        Args:
            space (Space): A pymunk.Space object representing the game space.
        """

        self.space = space
        self.space.gravity: tuple = s.GRAVITY
        self.space.damping: float = s.DAMPING
        self.character = Character(self.space)
        self.platform_manager = PlatformManager(self.space)
        self.walls = Walls(self.space)

        # Generate a list of tuples of the body and shapes of the platforms
        self.platform_manager.generate_platform()

        # Add character to the space
        self.space.add(self.character.body, self.character.shape, self.character.sensor_shape)

        # Add platforms to the space
        for body, platform in self.platform_manager.platforms:
            self.space.add(body, platform)

        # Add walls to the space
        left_wall, right_wall = self.walls.create_walls()
        self.space.add(left_wall, right_wall)

    def get_space(self) -> Space:
        """
        Get the pymunk.Space object representing the game space.
        
        Returns:
            A pymunk.Space object representing the game space.
        """

        return self.space
    
    def get_character(self) -> Character:
        """
        Get the Character object representing the game character.

        Returns:
             A Character object representing the game character.
        """

        return self.character
    
    def get_platform_manager(self) -> PlatformManager:
        """
        Get the PlatformManager object responsible for managing the platforms in the game.

        Returns:
            A PlatformManager object responsible for managing the platforms in the game.
        """

        return self.platform_manager
