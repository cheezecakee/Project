
import os, pygame
from typing import Tuple

pygame.init()

class Images:
    """Class responsible for loading all the images."""

    def __init__(self) -> None:
        """Initialize the Images class and load all the images."""

        self.character_img, self.character_jumpimg, self.character_gg = self.load_character()
        self.earth_platform, self.lava_platform, self.water_platform, self.air_platform = self.load_platform()
        self.wall_left_img, self.wall_right_img = self.load_wall()
        self.bg, self.bg2 = self.load_background()

    def load_character(self) -> Tuple[pygame.Surface, pygame.Surface, pygame.Surface]:
        """
        Load character images.

        Returns:
            Tuple of character images.
        """

        character_img = pygame.image.load(os.path.join("img", "micheal_scott.png"))
        character_jumpimg = pygame.image.load(os.path.join("img","micheal_scott_jump.png"))
        character_gg = pygame.image.load(os.path.join("img","micheal_scott_gg.png"))
        return character_img, character_jumpimg, character_gg
    
    def load_platform(self) -> Tuple[pygame.Surface, pygame.Surface, pygame.Surface, pygame.Surface]:
        """
        Load platform images.

        Returns:
            Tuple of platform images.
        """

        earth_platform = pygame.image.load(os.path.join("img","earth_platform.png"))
        lava_platform = pygame.image.load(os.path.join("img","lava_platform.png"))
        water_platform = pygame.image.load(os.path.join("img","water_platform.png"))
        air_platform = pygame.image.load(os.path.join("img","air_platform.png"))
        return earth_platform, lava_platform, water_platform, air_platform
    
    def load_wall(self) -> Tuple:
        wall_left_img = pygame.image.load(os.path.join("img","rock_wall_left.png"))
        wall_right_img = pygame.image.load(os.path.join("img","rock_wall_right.png"))
        return wall_left_img, wall_right_img
    
    def load_background(self) -> Tuple[pygame.Surface, pygame.Surface]:
        """
        Load wall images.

        Returns:
            Tuple of images.
        """

        bg = pygame.image.load(os.path.join("img","background1.png")).convert()
        bg2 = pygame.image.load(os.path.join("img","background2.png")).convert()
        return bg, bg2

    def scale_images(self, img: pygame.Surface, img_width: int, img_height: int) -> pygame.Surface:
        """
        Scale images to the given width and height.

        Args:
            img: Image to be scaled
            img_width: Width of the scaled image.
            img_height: Height of the scaled image.

        Returns:
            Scaled image.
        """
        
        img = pygame.transform.scale(img, (img_width, img_height))
        return img
