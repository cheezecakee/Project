
from game_components.character import Character
from game_components.platform_manager import PlatformManager
from game_components.walls import Walls
from pymunk import Space
import settings as s


class GameSetup:
    """"""
    def __init__(self, space: Space) -> None:
        """"""
        self.space = space
        self.space.gravity :tuple = s.GRAVITY
        self.space.damping :float = s.DAMPING
        self.character = Character(self.space)
        self.platform_manager = PlatformManager(self.space)
        self.walls = Walls(self.space)

        # Generate platforms
        self.platform_manager.generate_platform()

        # Add character to space
        self.space.add(self.character.body, self.character.shape, self.character.sensor_shape)

        # Add platforms to space
        for body, platform in self.platform_manager.platforms:
            self.space.add(body, platform)

        # Add walls to space
        left_wall, right_wall = self.walls.create_walls()
        self.space.add(left_wall, right_wall)

    def get_space(self) -> Space:
        """"""
        return self.space
    
    def get_character(self) -> Character:
        """"""
        return self.character
    
    def get_platform_manager(self) -> PlatformManager:
        """"""
        return self.platform_manager
