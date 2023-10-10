"""
All constant variables that are used in more than one class, function or
file is stored here, these are not to be changed. Some extra settings 
included are the pygame display, gravity, and physics settings.
"""

import os
import pygame

pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH: int = 1280
HEIGHT: int = 800

# Display settings
FLAGS = pygame.FULLSCREEN # Sets the display to fullscreen mode
# Fullscreen mode
# screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=FLAGS)
# Windowed mode
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Physics settings
GRAVITY: tuple = (0, 2000.0)
DAMPING: float = 0.3

# Colours in RGB format
BLACK: tuple[int, int, int] = (0,0,0)
WHITE: tuple[int, int, int]  = (255,255,255)
RED: tuple[int, int, int]  = (255,0,0)
GREY: tuple[int, int, int] = (128,128,128)
YELLOW: tuple[int, int, int]   = (244, 224, 36)
BURGANDY: tuple[int, int, int]  = (84, 21, 46)

# Number of platforms that are pre-spawned
NUMBER_OF_PLATFORMS: int = 100

# Fonts
general_font = pygame.font.Font("fonts/ARCADE.TTF", 36)
title_font = pygame.font.Font("fonts/ARCADE.TTF", 56)

# Rendering settings
clock = pygame.time.Clock()
FPS: int = 60 # Frames per second
dt: float = 1.0/60.0 # Delta time

# Game settings
START_TICKS: int = 0 # Starting time in-game

# Sound settings
pygame.mixer.pre_init(42000, -16, 2, 500)
PARKOUR_SOUND = pygame.mixer.Sound(os.path.join("audio", "parkour!.mp3"))
PARKOUR_SOUND.set_volume(10)
ELEVATOR = pygame.mixer.Sound(os.path.join("audio", ("elevator_music.mp3")))
ELEVATOR.set_volume(0.3)