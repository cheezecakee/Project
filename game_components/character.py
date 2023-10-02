""" 
The character module is responsible for creating the character body, shape, sensor,
    movement and jump. It also assigns key presses for the user to control the 
    character.
"""

import scale_objects as so
import settings as s
import pymunk, pygame, math
from typing import Callable, Tuple

class Character:
    """Handles character creation and positioning."""

    def __init__(self, space: pymunk.Space) -> None:
        self.space = space
        self.mass: int = so.CHARACTER_MASS
        self.width: int = so.CHARACTER_WIDTH
        self.height: int = so.CHARACTER_HEIGHT
        self.pos_x: float = so.CHARACTER_POS_X
        self.pos_y: float = so.CHARACTER_POS_Y
        self.body: pymunk.Body = self.character_body()
        self.shape: pymunk.Shape = self.character_shape()
        self.sensor_shape: pymunk.Shape= self.character_sensor()
        self.shape.collision_type = 1
        self.sensor_shape.collision_type = 3
    
    def character_body(self) -> pymunk.Body:
        """Create and return a character body."""

        body = pymunk.Body(0, 0)
        body.position = (self.pos_x,self.pos_y)
        return body

    
    def character_shape(self) -> pymunk.Shape:
        """Create and return a character shape."""

        shape = pymunk.Poly.create_box(self.body, (self.width,self.height))
        shape.mass = self.mass
        shape.elasticity = 0.7
        shape.friction = 0.5
        return shape
    
   
    def get_angle(self) -> None:
        """Keep character angle upright."""

        self.body.angle = 0

    
    def set_max_velocity(self) -> None:
        """Set a max velocity for the character."""

        max_velocity_x: int = so.CHARACTER_MAX_VELOCITY_X
        velocity: Tuple[float, float] = self.body.velocity
        speed: float = math.sqrt(velocity.x**2 + velocity.y**2)

        if speed > max_velocity_x:
            scale: float = max_velocity_x / speed
            self.body.velocity = pymunk.Vec2d(velocity.x * scale, velocity.y * scale)

    
    def character_sensor(self) -> pymunk.Shape:
        """Create and return a character sensor shape."""

        sensor_shape = pymunk.Segment(self.body, (-s.WIDTH, self.height), (s.WIDTH, self.height), 0)
        sensor_shape.sensor = True
        return sensor_shape
    
    
    def reset_character(self) -> None:
        """Reset character to starting position and velocity when it's game over."""

        self.body.position = pymunk.Vec2d(self.pos_x,self.pos_y)
        self.body.velocity = pymunk.Vec2d(0, 0)


class Movement:
    """Handle the movement of the character based on user input from the keyboard."""

    def __init__(self, body: pymunk.Body) -> None:
        self.FORCE: int = 2000 
        self.body = body
        self.character_move: Callable[[], None] = self.move

    def left(self) -> None:
        """Applies force to the right side of the character so it moves to the left."""

        self.body.force = pymunk.Vec2d(0, 0)
        self.body.apply_impulse_at_local_point((-5, 0), (0,0))
        self.body.apply_force_at_local_point((-self.FORCE, 0), (0,0))
    
    def right(self) -> None:
        """Applies force to the left side of the character so it moves to the right."""

        self.body.force = pymunk.Vec2d(0, 0)
        self.body.apply_impulse_at_local_point((5, 0), (0,0))
        self.body.apply_force_at_local_point((self.FORCE, 0), (0,0))

    def move(self) -> None:
        """Applies left, right force on key press."""

        key: list[bool] = pygame.key.get_pressed()

        if key[pygame.K_LEFT]: #move left
            self.left()
        if key[pygame.K_RIGHT]: #move right
            self.right()

class Jump:
    """Handle the jump action of the character based on user input from the keyboard."""

    def __init__(self, body: pymunk.Body) -> None:
        self.body = body
        self.character_jump: Callable[[], None] = self.jump_key
    
    def jump(self) -> None:
        """Applies force to the character from the bottom to jump up."""
        
        JUMP_FORCE: int = so.CHARACTER_JUMP_FORCE #stays inside the method so it doesn't stack up
        JUMP_FORCE: float = JUMP_FORCE + abs(self.body.velocity.x) * so.CHARACTER_JUMP_VELOCITY_FACTOR
        self.body.apply_impulse_at_local_point((0, -JUMP_FORCE), (0, 0))

    def jump_key(self) -> None:
        """Applies jump force on key press."""

        key: list[bool] = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            self.jump()
