
import sys
import pygame
import settings as s
import scale_objects as so
from images import Images
from game_setup import GameSetup
from game_components.character import Jump
from game_components.character import Movement
from game_components.collision import Collision
from game_components.mechanics import Mechanics 
from game_components.scroll_system import Scroll

class GameManager:
    """"""
    def __init__(self, game_setup: GameSetup) -> None:
        """Responsible for coordinating the interaction between the character and the platform,
        updating the scroll, game state, movement, etc into the game loop"""
        
        # Initialize game setup and related attributes   
        self.game_setup = game_setup
        self.space = game_setup.get_space()        
        self.character = game_setup.get_character()
        self.platform_manager = game_setup.get_platform_manager()
        self.platforms = self.game_setup.get_platform_manager().platforms
        
        # Initialize scroll, mechanics, and images
        self.character_movement = Movement(self.character.body)
        self.character_jump = Jump(self.character.body)
        self.collision = Collision(self.space,self.character, self.platforms)
        
        # Initialize scroll, mechanics, and images
        self.scroll = Scroll(self.space, self.character, self.platforms)
        self.mechanic = Mechanics()
        self.images = Images()

        # Initialize scroll timer
        self.auto_scroll_start_ticks = s.START_TICKS

        # Initialize background image setup for scrolling
        self.background1 = self.images.bg
        self.background2 = self.images.bg2
        self.img_height = self.background1.get_height()
        self.background1_y = 0
        self.background2_y = 0
        self.background_scroll = 0
    
    """ Transform these comments below to docstrings"""
    # Updates collision between character and platform
    def update_collision(self) -> None:
        """"""
        self.collision.add_collision_handlers()
    
    # Updates character movement
    def update_character_movements(self) -> None:
        """"""
        self.character_movement.character_move()

    # Updates character movement jump 
    def update_character_jump(self) -> None:
        """"""
        self.collision.check_in_air()
        if self.collision.on_ground:
            self.character_jump.character_jump()

    # Set the max velocity and keep character upright
    def update_max_velocity_and_angle(self) -> None:
        """"""
        self.character.set_max_velocity()
        self.character.get_angle()
        
    # Moves the platforms back to the top of the screen
    def update_platforms(self) -> None:
        """"""
        self.platform_manager.move_platforms()

    # Update scroll based on character
    def update_scroll(self) -> None:
        """"""
        scroll_amount = self.scroll.move_camera()
        self.background_scroll += scroll_amount

    # Active auto scroll based on time
    def update_auto_scroll(self) -> float:
        """"""
        if self.collision.counter >= 10:
            if self.auto_scroll_start_ticks == 0:
                self.auto_scroll_start_ticks = pygame.time.get_ticks()
            seconds = (pygame.time.get_ticks() - self.auto_scroll_start_ticks) / 1000
            scroll_speed = self.scroll.auto_scroll(seconds)
            self.background_scroll += scroll_speed
            return seconds
        else: 
            return 0.0
    
    # Scrolls the two background images together 
    def scroll_background(self) -> None:
        """"""
        self.background1_y = -s.HEIGHT + self.background_scroll
        self.background2_y = self.background1_y - self.img_height
    
    # Moves background image back to the top of the screen 
    def move_background(self) -> None:
        """"""
        self.scroll_background()
        if self.background1_y > s.HEIGHT:
            self.background1_y = self.background2_y - self.img_height

        if self.background2_y > s.HEIGHT:
            self.background2_y = self.background1_y - self.img_height
            self.background_scroll = 0

    # Updates the score based on the counter
    def update_score(self) -> None:
       """"""
       score = self.mechanic.get_score(self.collision.counter)
       return score
    
    # Updates game state 
    def update_game_status(self) -> None:
        """"""
        self.mechanic.check_game_status(self.character)
    
    # Game Over Screen
    def game_over_display(self) -> None:
        """"""
        s.screen.fill(s.BURGANDY)
        restart = s.font_a.render("Game Over - Press Space to Restart", True, s.WHITE)
        s.screen.blit(restart, (s.WIDTH*0.25,s.HEIGHT/2))
        main_menu = s.font_a.render("Press ESC to Exit", True, s.WHITE)
        s.screen.blit(main_menu, (s.WIDTH*0.37,s.HEIGHT*0.55))
        self.draw_character_game_over()
        self.bg_y = 0
        self.background_scroll = 0
        self.scroll.speed = 1
        self.auto_scroll_start_ticks = s.START_TICKS
        self.character.reset_character()
        self.platform_manager.reset_platforms()
        self.collision.reset_counter()
        self.mechanic.restart_key()

        self.quit_game()

    # Return to main menu
    def quit_game(self) -> str:
        """"""
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    # Display the score and time
    def display_score_time(self):
        """"""
        time = s.font_a.render(f"Time: {self.update_auto_scroll():.2f}s", True, s.WHITE)
        s.screen.blit(time, (s.WIDTH*0.01,s.HEIGHT*0.02))
        score = s.font_a.render(f"Score: {self.update_score()}", True, s.WHITE)
        s.screen.blit(score, (s.WIDTH*0.01,s.HEIGHT*0.07))

    # Draws the wall sprite in the pygame surface
    def draw_wall(self) -> None:
        """"""
        left_wall_img = self.images.wall_left_img
        right_wall_img = self.images.wall_right_img
        s.screen.blit(left_wall_img, (-so.WALL_THICKNESS-(0.50*100),0))
        s.screen.blit(right_wall_img, ((so.RIGHT_WALL_WIDTH-so.WALL_THICKNESS), 0))

    # Draws the character sprite in the pygame surface
    def draw_character(self) -> None:
        """"""
        if not self.collision.on_ground:
            character_img = self.images.character_jumpimg
        else:
            character_img = self.images.character_img
            
        character_img = self.images.scale_images(character_img, self.character.width, self.character.height)
        pos_x = self.character.body.position.x - character_img.get_width() / 2
        pos_y = self.character.body.position.y - character_img.get_height() / 2
        s.screen.blit(character_img, (pos_x, pos_y))

    def draw_character_game_over(self) -> None:
        """"""
        character_img = self.images.character_gg
        # character_img = self.images.scale_images(character_img, self.character.width, self.character.height)
        s.screen.blit(character_img, (s.WIDTH*0.36, s.HEIGHT*0.20))

    # Draws the platform sprite in the pygame surface and updates the sprite
    def draw_platform(self) -> None:
        """"""
        for i, (body, platform) in enumerate(self.platforms):
            platform_img = None

            if self.platform_manager.platform_counter < 100:
                platform_img = self.images.earth_platform
            elif self.platform_manager.platform_counter < 200:
                platform_img = self.images.water_platform
            elif self.platform_manager.platform_counter < 300:
                platform_img = self.images.lava_platform
            elif self.platform_manager.platform_counter < 400:
                platform_img = self.images.air_platform
            else:
                platform_img = self.images.earth_platform
                self.platform_manager.platform_counter = 5

            platform_width = abs(platform.a.x - platform.b.x)
            platform_img = self.images.scale_images(platform_img, platform_width, (so.PLATFORM_THICKNESS*2))

            pos_x = body.position.x - platform_img.get_width() / 2
            pos_y = body.position.y - platform_img.get_height() / 2
            s.screen.blit(platform_img, (pos_x, pos_y))
            
    # Draws the background sprite in the pygame surface
    def draw_background(self) -> None:
        """"""
        # Draw the images at their positions
        s.screen.blit(self.background1, (0, self.background1_y))
        s.screen.blit(self.background2, (0, self.background2_y))

    # Set all the methods in the right order to be placed in the gameloop
    def run_game(self) -> None:
        """"""
        if self.mechanic.game_over is False:  
            self.move_background()
            self.draw_background()
            self.draw_platform()
            self.draw_character()
            self.draw_wall()
            self.update_character_movements() 
            self.update_character_jump()
            self.update_max_velocity_and_angle()
            self.update_platforms()
            self.update_scroll()
            self.update_auto_scroll()
            self.update_score()
            self.display_score_time()
            self.update_game_status()
            self.quit_game()
        else:
            self.game_over_display()
                