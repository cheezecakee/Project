import pymunk
import random
import settings as s
import scale_objects as so
from typing import Tuple

class PlatformManager:
    """
    Responsible for creating the platform bodies, shapes and adding them to a list.
    Also manages the platform positioning in the space so they can be reused.
    """

    def __init__(self, space: pymunk.Space) -> None:
        self.space = space
        self.platforms: list = []
        self.prev_y: int = so.PREV_Y
        self.friction: float = 1.0
        self.min_platform_size: int = so.MIN_PLATFORM_SIZE
        self.max_platform_size: int = so.MAX_PLATFORM_SIZE
        self.platforms_thickness: int = so.PLATFORM_THICKNESS
        self.platform_distance: int = so.PLATFORM_DISTANCE
        self.n_platforms: int = s.NUMBER_OF_PLATFORMS
        self.passed: bool = False
        self.platform_counter: int = 5

    def create_body(self) -> pymunk.Body:
        """Creates and returns a platform body."""

        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.passed = False
        return body
    
    def create_platform(self) -> Tuple[pymunk.Body, pymunk.Segment]:
        """Creates and returns a platform Tuple which includes the body and segment with a 
        random x size."""

        body = self.create_body()

        platform_size: int = random.randint(so.MIN_PLATFORM_SIZE, so.MAX_PLATFORM_SIZE)
        half_size: float = platform_size / 2

        self.prev_y -= self.platform_distance

        x: int =  random.randint(so.PLATFORM_MIN_X, so.PLATFORM_MAX_X)
        body.position = (x, self.prev_y)
        platform = pymunk.Segment(body, (-half_size,0), (half_size, 0), self.platforms_thickness)
        platform.friction = self.friction
        platform.collision_type = 2

        return body, platform
    
    def create_wide_platform(self) -> Tuple[pymunk.Body, pymunk.Segment]:
        """Creates and returns a wide platform body and segment."""

        body = self.create_body()
        body.position = (s.WIDTH/2, self.prev_y)
        platform = pymunk.Segment(body, (-s.WIDTH/2, 0), (s.WIDTH/2, 0), self.platforms_thickness)
        platform.friction = self.friction
        platform.collision_type = 2

        return body, platform
    
    def generate_platform(self) -> list[Tuple[pymunk.Body, pymunk.Segment]]:
        """
        Generate a list of platforms and bodies.

        This method generates a list of platforms and bodies based on "self.n_platform".
        Every 50th platform is a wide platform, and the rest are regular platforms.

        Returns:
            list: A list of tuples, each containing a "pymunk.Body" and a "pymunk.Segment"
            representing a platform.
        """

        self.platforms = []
        for i in range(self.n_platforms):
            if i % 50 == 0:
                body, platform = self.create_wide_platform()
            else:
                body, platform = self.create_platform()
            self.platforms.append((body, platform))
        self.platforms = list(self.platforms)
        return self.platforms
      
    def move_platforms(self) -> None:
        """
        Move the platforms back to the top of the list and screen height.

        This method iterates over all platforms in "self.platfoms". If a platform's y position is
        greater than "s.HEIGHT", it resets the platform's position. Every 50th platform is moved to
        the center of the screen width, and the rest are moved to a random x position. If a platform's
        y position is less than 10% of "s.HEIGHT", "self.platform_counter" is incremented.
        """

        x: int =  random.randint(so.PLATFORM_MIN_X, so.PLATFORM_MAX_X)
        for i, (body, platform) in enumerate(self.platforms):
            if body.position.y > s.HEIGHT:
                body.passed = False
                if i % 50 == 0:
                    body.position = pymunk.Vec2d(s.WIDTH/2, self.prev_y)
                else:
                    body.position = pymunk.Vec2d(x, self.prev_y)
                
                if body.position.y < s.HEIGHT * 0.10:
                    self.platform_counter += 1

    def reset_platforms(self) -> None:
        """
        Reset the platforms to their starting positions when the game resets.

        This method resets the "prev_y" position to "so.PREV_Y" and repositions each platform in
        "self.platforms". If the platform is every 50th platform, it is moved to the center of the
        screen width. Otherwise, it is moved to a random x position. The "prev_y" position is then
        decremented by "self.plastform_distance", and the "passed" attribute of the body is set to
        False. Finally, "self.platform_counter" is reset to 0.
        """
        self.prev_y = so.PREV_Y
        for i, (body, platform) in enumerate(self.platforms):
            if i % 50 == 0:
                body.position = pymunk.Vec2d(s.WIDTH/2, self.prev_y)
            else:
                platform_size: int = random.randint(so.MIN_PLATFORM_SIZE, so.MAX_PLATFORM_SIZE)
                half_size: float = platform_size / 2
                x: int =  random.randint(so.PLATFORM_MIN_X, so.PLATFORM_MAX_X)
                body.position = pymunk.Vec2d(x, self.prev_y)
            self.prev_y -= self.platform_distance
            body.passed = False

        self.platform_counter = 0