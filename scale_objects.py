""" 
All constant variables that are used in different shapes and objects. These
are not to be changed. All variables are scaled here in relation to the display
size. The way they are scaled is based on the percentage of their width and 
heights to the current display size.
"""

import settings as s

# Character scale
CHARACTER_WIDTH: int = round(s.WIDTH * 0.047)
CHARACTER_HEIGHT: int = round(s.HEIGHT * 0.094)
CHARACTER_POS_X: float = s.WIDTH / 2
CHARACTER_POS_Y: float = s.HEIGHT - (s.HEIGHT * 0.25)
CHARACTER_MASS: float = 1.2

CHARACTER_MAX_VELOCITY_X: int = 3000

CHARACTER_JUMP_FORCE: int = 1200
# Formula for calculating the jump height based on the characters speed
CHARACTER_JUMP_VELOCITY_FACTOR: float = (8400 - CHARACTER_JUMP_FORCE) / CHARACTER_MAX_VELOCITY_X

# Wall scale
WALL_THICKNESS: int = s.WIDTH * 0.10
WALL_HEIGHT: int = s.HEIGHT
LEFT_WALL_WIDTH: int = 0
RIGHT_WALL_WIDTH: int = s.WIDTH

# Platform scale
MIN_PLATFORM_SIZE: int = round(s.WIDTH * 0.234)
MAX_PLATFORM_SIZE: int = round(s.WIDTH * 0.375)
PLATFORM_THICKNESS: int = s.WIDTH * 0.02
PLATFORM_DISTANCE: float = round(s.HEIGHT / 5)

# The starting y position of the first platform based on the display height
PREV_Y: int = s.HEIGHT

# The formula below is to get the min and max values that the platform x can be created based on the wall thickness so they don't overlap
MAX_HALF_SIZE: int = int(MAX_PLATFORM_SIZE / 2)
PLATFORM_MIN_X: int = WALL_THICKNESS + MAX_HALF_SIZE
PLATFORM_MAX_X: int = s.WIDTH - WALL_THICKNESS - MAX_HALF_SIZE
