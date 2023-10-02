import project
import pytest
import scale_objects as so
import settings as s
import pymunk

import pygame
from pygame.locals import *

from unittest.mock import patch, Mock
from game_setup import GameSetup
from game_manager import GameManager
from game_components.character import Character
from game_components.character import Movement
from game_components.character import Jump
from game_components.platform_manager import PlatformManager
from game_components.collision import Collision
from game_components.scroll_system import Scroll
from game_components.mechanics import Mechanics 

""" Test the main file functions """
def test_handle_input():
  menu_items = ["start", "exit"]

  selected_item = project.handle_input({pygame.K_DOWN: 1, pygame.K_UP: 0, pygame.K_ESCAPE: 0, pygame.K_RETURN: 0}, 0, menu_items)
  assert selected_item == 1

  selected_item = project.handle_input({pygame.K_UP: 1, pygame.K_DOWN: 0, pygame.K_ESCAPE: 0, pygame.K_RETURN: 0}, 1, menu_items)
  assert selected_item == 0

def test_get_menu_item():
    menu_items = ["start", "exit"]
    menu_item = project.get_menu_item(0, menu_items)
    assert menu_item == "start"

    menu_item = project.get_menu_item(1, menu_items)
    assert menu_item == "exit"

def test_handle_return_key():
    menu_items = ["start", "exit"]

    selected_item = 0
    returned_item = project.handle_return_key({pygame.K_RETURN: 1}, selected_item, menu_items)
    assert returned_item == "start"

    selected_item = 1
    returned_item = project.handle_return_key({pygame.K_RETURN: 1}, selected_item, menu_items)
    assert returned_item == "exit"

""" Test collision """
def test_character_to_platform_collision_up():
    space = pymunk.Space()
    character = Character(space)
    platform_manager = PlatformManager(space)
    platform_body, platform_shape = platform_manager.create_platform()
    platform = (platform_body, platform_shape)
    platforms = [platform]

    collision = Collision(space, character, platforms)
    # Simulate the character moving upwards by applying an upward force
    upward_force = (0, -500)  # Adjust the force as needed
    character.body.apply_impulse_at_local_point(upward_force, (0, 0))

    # Create a mock arbiter, space, and data
    arbiter = Mock()
    space = Mock()
    data = Mock()

    # Call the collide method
    result = collision.collide(arbiter, space, data)

    # Assert that the result is False (collision is prevented)
    assert result is False
    # Assert that the character is not on the ground
    assert collision.on_ground is False

def test_character_to_platform_collision_down():
    space = pymunk.Space()
    character = Character(space)
    platform_manager = PlatformManager(space)
    platform_body, platform_shape = platform_manager.create_platform()
    platform = (platform_body, platform_shape)
    platforms = [platform]

    space.add(character.body, character.shape, platform_body, platform_shape)

    collision = Collision(space, character, platforms)
    collision.add_collision_handlers()

    # Simulate the character moving upwards by applying an upward force
    upward_force = (0, 500)  # Adjust the force as needed
    character.body.apply_impulse_at_local_point(upward_force, (0, 0))

    # Create a mock arbiter, space, and data
    arbiter = Mock()
    space = Mock()
    data = Mock()

    # Call the collide method
    result = collision.collide(arbiter, space, data)

    # Assert that the result is False (collision is prevented)
    assert result is True
    # Assert that the character is not on the ground
    assert collision.on_ground is True

def test_sensor_to_platform_collision():
    # Create a pymunk space
    space = pymunk.Space()

    # Create a character and a platform
    character = Character(space)
    platform_manager = PlatformManager(space)
    platform_body, platform_shape = platform_manager.create_platform()
    platform = (platform_body, platform_shape)
    platforms = [platform]

    # Add the character's sensor and platform to the space
    # space.add(character.body, character.sensor_shape, platform_body, platform_shape)

    # Create a collision object
    collision = Collision(space, character, platforms)

    arbiter = Mock()
    arbiter.shapes = [Mock(), Mock()]
    arbiter.shapes[1].body = platform_body
    space = Mock()
    data = Mock()

    # Set the 'passed' attribute of the platform body to False
    platform_body.passed = False

    # Call the sensor_collide method
    result = collision.sensor_collide(arbiter, space, data)

    # Assert that the result is True (collision is allowed)
    assert result is True

    # Assert that the 'passed' attribute of the platform body is now True
    assert platform_body.passed is True

    # Assert that the counter has been incremented
    assert collision.counter == 0

""" Test character input """

def test_movement():
    # Create a mock body object
    mock_body = pymunk.Body(0, 0)

    # Initialize the Movement class with the mock body
    movement = Movement(mock_body)

    # Simulate a left key press and check if the body's force and impulse are as expected
    with patch('pygame.key.get_pressed', return_value={pygame.K_LEFT: True, pygame.K_RIGHT: False}):
        movement.move()
    assert mock_body.force == pymunk.Vec2d(-2000, 0)
    # Add more assertions here for the impulse and force applied

    # Reset the mock body's force and impulse
    mock_body.force = pymunk.Vec2d(0, 0)
    mock_body.apply_impulse_at_local_point((0, 0), (0,0))

    # Simulate a right key press and check if the body's force and impulse are as expected
    with patch('pygame.key.get_pressed', return_value={pygame.K_LEFT: False, pygame.K_RIGHT: True}):
        movement.move()
    assert mock_body.force == pymunk.Vec2d(2000, 0)

def test_jump():
    mock_body = pymunk.Body(1,1)
    inital_velocity = mock_body.velocity.y

    jump = Jump(mock_body)

    with patch("pygame.key.get_pressed", return_value={pygame.K_SPACE: True}):
        jump.jump_key()
    
    final_velocity = mock_body.velocity.y
    change_in_velocity = final_velocity - inital_velocity

    assert change_in_velocity < 0
    
""" Test camera_movent """
def test_camera_to_player_scroll():
    mock_space = pymunk.Space()
    mock_character_body = pymunk.Body(1,1)
    mock_character_body.position = pymunk.Vec2d(0, s.HEIGHT / 4) # Start characters position less than half of the screen height

    mock_character = Mock()  # Create a mock Character object
    mock_character.body = mock_character_body  # Assign the mock body to the mock Character
    mock_space.add(mock_character_body)
    mock_platforms = [(pymunk.Body(body_type=pymunk.Body.KINEMATIC), pymunk.Segment(pymunk.Body(1,1), (0, 0), (1, 0), 0)) for _ in range(5)]
    for body, _ in mock_platforms:
        mock_space.add(body)
        body.position = pymunk.Vec2d(0, s.HEIGHT) # Start platform at the top of the screen

    scroll = Scroll(mock_space,mock_character, mock_platforms)

    initial_positions = [body.position.y for body, _ in mock_platforms]
    scroll_amount = scroll.move_camera()
    final_positions = [body.position.y for body, _ in mock_platforms]

    for initial, final in zip(initial_positions, final_positions):
        assert final == initial + scroll_amount

def test_auto_scroll():
    mock_space = pymunk.Space()
    mock_character_body = pymunk.Body(1,1)

    mock_character = Mock()  # Create a mock Character object
    mock_character.body = mock_character_body  # Assign the mock body to the mock Character
    mock_space.add(mock_character_body)

    mock_platforms = [(pymunk.Body(body_type=pymunk.Body.KINEMATIC), pymunk.Segment(pymunk.Body(1,1), (0, 0), (1, 0), 0)) for _ in range(5)]
    for body, _ in mock_platforms:
        mock_space.add(body)
        body.position = pymunk.Vec2d(0, s.HEIGHT) # Start platform at the top of the screen    
    scroll = Scroll(mock_space,mock_character, mock_platforms)

    elapsed_time = 60
    initial_positions = [body.position.y for body, _ in mock_platforms]
    scroll_speed = scroll.auto_scroll(elapsed_time)
    final_positions = [body.position.y for body, _ in mock_platforms]

    for initial, final in zip(initial_positions, final_positions):
        assert final == initial + scroll_speed

""" Test platform generation """
def test_plaform_move_to_top():
    mock_space = Mock(spec=pymunk.Space)
    mock_body = Mock(spec=pymunk.Body)
    mock_segment = Mock(spec=pymunk.Segment)
    platforms = []
    platform_manger = PlatformManager(mock_space)
    platforms.append((mock_body, mock_segment))
    platform_manger.platforms = platforms

    mock_body.position.y = s.HEIGHT + 1
    platform_manger.move_platforms()

    assert mock_body.position.y < s.HEIGHT

    assert not mock_body.passed
    
""" Test game outputs """

def test_score():
    mock_counter = 5
    mock_mechanics = Mock(spec=Mechanics)
    mock_mechanics.get_score.return_value = 50
    result = mock_mechanics.get_score(mock_counter)
    assert result == 50

""" Test game events """

def test_game_over():
    mock_mechanic = Mock(spec=Mechanics)
    mock_character_body = pymunk.Body(1,1)
    mock_character_body.position = pymunk.Vec2d(0, s.HEIGHT + 1)# Start characters position less than half of the screen height

    mock_character = Mock()  # Create a mock Character object
    mock_character.body = mock_character_body
    mock_mechanic.check_game_status.return_value = True

    assert mock_mechanic.check_game_status(mock_character) is True