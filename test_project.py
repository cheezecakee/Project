"""
This module contains unit tests for the game.

It includes tests for character movement, collision detection, camera scrolling, platform movement, 
and game events.
"""

import pytest
import pymunk
import pygame
from pygame.locals import *
from unittest.mock import patch, Mock

import scale_objects as so
import settings as s

import project
from game_components.character import Character
from game_components.character import Movement
from game_components.character import Jump
from game_components.mechanics import Mechanics 
from game_components.collision import Collision
from game_components.scroll_system import Scroll
from game_components.platform_manager import PlatformManager


def test_handle_input() -> None:

    """
    Test the handle_input function.

    This function tests the handle_input function by simulating different key presses and checking
    the selected menu item.

    Args:
        None

    Returns:
        None
    """

    menu_items = ["start", "exit"]

    selected_item = project.handle_input({pygame.K_DOWN: 1, pygame.K_UP: 0, pygame.K_ESCAPE: 0, pygame.K_RETURN: 0}, 0, menu_items)
    assert selected_item == 1

    selected_item = project.handle_input({pygame.K_UP: 1, pygame.K_DOWN: 0, pygame.K_ESCAPE: 0, pygame.K_RETURN: 0}, 1, menu_items)
    assert selected_item == 0

def test_get_menu_item() -> None:
    """
    Test the get_menu_item function.

    This function tests the get_menu_item function by checking if the correct menu item is returned for
    diffrent indices.

    Args:
        None
    
    Returns:
        None
    """
    
    menu_items = ["start", "exit"]
    menu_item = project.get_menu_item(0, menu_items)
    assert menu_item == "start"

    menu_item = project.get_menu_item(1, menu_items)
    assert menu_item == "exit"

def test_handle_return_key() -> None:
    """
    Test the handle_return_key function.

    This function tests the handle_return_key function by simulating the return key press and checking the
    returned menu item.

    Args:
        None
    
    Returns:
        None
    """
    
    menu_items = ["start", "exit"]

    selected_item = 0
    returned_item = project.handle_return_key({pygame.K_RETURN: 1}, selected_item, menu_items)
    assert returned_item == "start"

    selected_item = 1
    returned_item = project.handle_return_key({pygame.K_RETURN: 1}, selected_item, menu_items)
    assert returned_item == "exit"

def test_character_to_platform_collision_up() -> None:
    """ 
    Test the character to platform upward collision.

    This function tests the upward collision between the character and the platform by creating mock objects
    and simulating the collision.

    Args:
        None

    Returns:
        None
    """

    # Create a mock arbiter, space, and data
    arbiter = Mock()
    space = Mock()
    data = Mock()

    # Create a mock platform
    mock_platform_manager = Mock(spec=PlatformManager)
    body = Mock(spec=pymunk.Body.KINEMATIC)
    segment = Mock(spec=pymunk.Segment)
    mock_platform_manager.create_platform.return_value = (body, segment)
    mock_platform_body, mock_platform_shape = mock_platform_manager.create_platform()
    mock_platform = mock_platform_body, mock_platform_shape
    mock_platforms = [] 
    mock_platforms.append(mock_platform)

    # Create a mock character
    mock_character = Mock(spec=Character)
    mock_character.body = pymunk.Body(1,1)
    mock_character.shape = pymunk.Poly.create_box(mock_character.body)

    # Create a mock collision
    mock_collision = Collision(space, mock_character, mock_platforms)
    
    mock_collision.add_collision_handlers()

    # Apply an upward force to simulate the character jumping
    mock_character.body.apply_impulse_at_local_point((0, -500), (0,0))

    # Now when you call the collide method, it should return False
    assert mock_collision.collide(arbiter, space, data) == False
    assert mock_collision.on_ground is False

def test_character_to_platform_collision_down() -> None:
    """
    Test the character to platform downward collision.

    This function tests the downward collision between the character and the platform by creating mock objects
    and simulating the collision.

    Args:
        None
    
    Returns:
        None
    """
    
    mock_space = Mock(pymunk.Space)
    # Create a mock arbiter, space, and data
    arbiter = Mock()
    space = Mock()
    data = Mock()

    # Create a mock platform
    mock_platform_manager = Mock(spec=PlatformManager)
    body = Mock(spec=pymunk.Body.KINEMATIC)
    segment = Mock(spec=pymunk.Segment)
    mock_platform_manager.create_platform.return_value = (body, segment)
    mock_platform_body, mock_platform_shape = mock_platform_manager.create_platform()
    mock_platform = mock_platform_body, mock_platform_shape
    mock_platforms = [] 
    mock_platforms.append(mock_platform)

    # Create a mock character
    mock_character = Mock(spec=Character)
    mock_character.body = pymunk.Body(1,1)
    mock_character.shape = pymunk.Poly.create_box(mock_character.body)

    # Create a mock collision
    mock_collision = Collision(mock_space, mock_character, mock_platforms)
    
    mock_collision.add_collision_handlers()

    # Apply a downward force to simulate the character moving downward
    mock_character.body.apply_impulse_at_local_point((0, 500), (0,0))

    # Now when you call the collide method, it should return False
    assert mock_collision.collide(arbiter, space, data) == True
    assert mock_collision.on_ground is True

def test_sensor_to_platform_collision() -> None:
    """ 
    Test sensor to platform collision dection.

    This function tests the collision detection between the sensor and the platform by creating mock objects and
    simulating the collision.

    Args:
        None
    
    Returns:
        None
    """

    mock_space = Mock(pymunk.Space)

    # Create a mock character
    mock_character = Mock(spec=Character)
    mock_character.body = pymunk.Body(1,1)
    mock_character_sensor = pymunk.Segment(mock_character.body, (-s.WIDTH, 10), (s.WIDTH, 10), 0)
    mock_character_sensor.sensor = True

    # Create a mock platform
    mock_platform_manager = Mock(spec=PlatformManager)
    body = Mock(spec=pymunk.Body.KINEMATIC)
    segment = Mock(spec=pymunk.Segment)
    mock_platform_manager.create_platform.return_value = (body, segment)
    mock_platform_body, mock_platform_shape = mock_platform_manager.create_platform()
    mock_platform = mock_platform_body, mock_platform_shape
    mock_platforms = [] 
    mock_platforms.append(mock_platform)

    arbiter = Mock()
    arbiter.shapes = [Mock(), Mock()]
    arbiter.shapes[1].body = mock_platform_body
    space = Mock()
    data = Mock()

    # Create a collision object
    mock_collision = Collision(mock_space, mock_character, mock_platforms)

    # Set the 'passed' attribute of the platform body to False
    mock_platform_body.passed = False

    # Call the sensor_collide method
    result = mock_collision.sensor_collide(arbiter, space, data)

    # Assert that the result is True (collision is allowed)
    assert result is True

    # Assert that the 'passed' attribute of the platform body is now True
    assert mock_platform_body.passed is True

    # Assert that the counter has been incremented (collision starts at -1)
    assert mock_collision.counter == 0


def test_movement() -> None:
    """ 
    Test the movement of the character.

    This function tests the movement of the character by simulating key presses and checking the force applied to the
    character's body.

    Args:
        None
    
    Returns:
        None
    """

    # Create a mock body object
    mock_body = pymunk.Body(0, 0)

    # Initialize the Movement class with the mock body
    movement = Movement(mock_body)

    # Simulate a left key press and check if the body's force and impulse are as expected
    with patch('pygame.key.get_pressed', return_value={pygame.K_LEFT: True, pygame.K_RIGHT: False}):
        movement.move()
    assert mock_body.force == pymunk.Vec2d(-2000, 0)

    # Reset the mock body's force and impulse
    mock_body.force = pymunk.Vec2d(0, 0)
    mock_body.apply_impulse_at_local_point((0, 0), (0,0))

    # Simulate a right key press and check if the body's force and impulse are as expected
    with patch('pygame.key.get_pressed', return_value={pygame.K_LEFT: False, pygame.K_RIGHT: True}):
        movement.move()
    assert mock_body.force == pymunk.Vec2d(2000, 0)

def test_jump() -> None:
    """
    Test the jump of the character.

    This function tests the jump of the character by simulating a space key press and checking the change in the 
    character's velocity.

    Args:
        None
    
    Returns:
        None
    """
    
    mock_body = pymunk.Body(1,1)
    inital_velocity = mock_body.velocity.y

    jump = Jump(mock_body)

    with patch("pygame.key.get_pressed", return_value={pygame.K_SPACE: True}):
        jump.jump_key()
    
    final_velocity = mock_body.velocity.y
    change_in_velocity = final_velocity - inital_velocity

    assert change_in_velocity < 0
    

def test_camera_to_player_scroll() -> None:
    """ 
    Test the camera to player scroll.

    This function tests the camera to player scroll by creating mock objects and checking the change in the platform
    positions.

    Args:
        None

    Returns:
        None
    """

    mock_space = pymunk.Space()
    mock_character_body = pymunk.Body(1,1)
    mock_character_body.position = pymunk.Vec2d(0, s.HEIGHT / 4) # Start characters position less than half of the screen height

    mock_character = Mock()  # Create a mock Character object
    mock_character.body = mock_character_body  # Assign the mock body to the mock Character
    mock_space.add(mock_character_body)
    mock_platforms = [(pymunk.Body(body_type=pymunk.Body.KINEMATIC), pymunk.Segment(pymunk.Body(1,1), (0, 0), (1, 0), 0)) for _ in range(5)]
    for body, _ in mock_platforms:
        mock_space.add(body)
        body.position = pymunk.Vec2d(0, 0) # Start platform at the top of the screen

    scroll = Scroll(mock_space,mock_character, mock_platforms)

    initial_positions = [body.position.y for body, _ in mock_platforms]
    scroll_amount = scroll.move_camera()
    final_positions = [body.position.y for body, _ in mock_platforms]

    for initial, final in zip(initial_positions, final_positions):
        assert final == initial + scroll_amount

def test_auto_scroll() -> None:
    """
    Test the auto scroll.

    This function tests the auto scroll by creating mock objects and checking the change in the platform positions after
    a certain elapsed time.

    Args:
        None
    
    Returns:
        None
    """
    
    mock_space = pymunk.Space()
    mock_character_body = pymunk.Body(1,1)

    mock_character = Mock()  # Create a mock Character object
    mock_character.body = mock_character_body  # Assign the mock body to the mock Character
    mock_space.add(mock_character_body)

    mock_platforms = [(pymunk.Body(body_type=pymunk.Body.KINEMATIC), pymunk.Segment(pymunk.Body(1,1), (0, 0), (1, 0), 0)) for _ in range(5)]
    for body, _ in mock_platforms:
        mock_space.add(body)
        body.position = pymunk.Vec2d(0, 0) # Start platform at the top of the screen    
    scroll = Scroll(mock_space,mock_character, mock_platforms)

    elapsed_time = 60
    initial_positions = [body.position.y for body, _ in mock_platforms]
    scroll_speed = scroll.auto_scroll(elapsed_time)
    final_positions = [body.position.y for body, _ in mock_platforms]

    for initial, final in zip(initial_positions, final_positions):
        assert final == initial + scroll_speed


def test_platform_move_to_top() -> None:
    """
    Test the platform move to top.

    This function tests the platform move to top by creating a mock platform and checking its position after calling the 
    move_platforms method.

    Args:
        None
    
    Returns:
        None
    """

    # Create a mock platform
    mock_space = Mock(pymunk.Space)
    platform_manager = PlatformManager(mock_space)
    mock_body = Mock(spec=pymunk.Body)
    mock_segment = Mock(spec=pymunk.Segment)
    mock_body.position.y = s.HEIGHT + 1
    platform_manager.platforms.append((mock_body, mock_segment))

    # Test that platforms with y position > s.HEIGHT are repositioned.
    platform_manager.move_platforms()
    assert mock_body.passed is False
    assert mock_body.position.y < s.HEIGHT


def test_score() -> None:
    """ 
    Test the game score output.

    This function tests the game score output by creating a mock Mechanics object and checking the returned score.

    Args:
        None
    
    Returns:
        None
    """

    mock_counter = 5
    mock_mechanics = Mock(spec=Mechanics)
    mock_mechanics.get_score.return_value = 50
    result = mock_mechanics.get_score(mock_counter)
    assert result == 50


def test_game_over() -> None:
    """ 
    Test the game over event.

    This function tests the game over event by creating mock objects and checking the game status.

    Args:
        None

    Returns:
        None
    """

    mock_mechanic = Mock(spec=Mechanics)
    mock_character_body = pymunk.Body(1,1)
    mock_character_body.position = pymunk.Vec2d(0, s.HEIGHT + 1)# Start characters position less than half of the screen height

    mock_character = Mock()  # Create a mock Character object
    mock_character.body = mock_character_body
    mock_mechanic.check_game_status.return_value = True

    assert mock_mechanic.check_game_status(mock_character) is True