"""
All constant variables that are used in more than one class, function or
file is stored here, these are not to be changed. Some extra
settings included are the pygame display, gravity, and physics 
settings.
"""

import pygame

pygame.init()

# Screen settings
WIDTH: int = 1280
HEIGHT: int = 800

# Display settings
FLAGS = pygame.FULLSCREEN
# Fullscreen mode
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=FLAGS)
# Windowed mode
# screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Physics settings
GRAVITY = (0, 2000.0)
DAMPING: float = 0.3

# Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREY = (128,128,128)
YELLOW  = (244, 224, 36)
BURGANDY = (84, 21, 46)

# Other settings
NUMBER_OF_PLATFORMS: int = 100

# Fonts
font_a = pygame.font.Font("fonts/ARCADE.TTF", 36)
font_b = pygame.font.Font("fonts/ARCADE.TTF", 56)
smallfont = pygame.font.SysFont('Corbel',35) 

# Rendering settings
clock = pygame.time.Clock()
FPS: int = 60
dt: float = 1.0/60.0

# Game settings
START_TICKS: int = 0
