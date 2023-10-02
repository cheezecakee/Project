import pygame
import pymunk
import sys
import os
import settings as s
from game_setup import GameSetup
from game_manager import GameManager

def handle_events(event, key) -> None:
    """ Handle pygame exit events """
    if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    return True

def handle_input(key, selected_item, menu_items) -> str:
    if key[pygame.K_DOWN]:
        selected_item = (selected_item + 1) % len(menu_items)
    elif key[pygame.K_UP]:
        selected_item = (selected_item - 1) % len(menu_items)
    return selected_item

def get_menu_item(selected_item, menu_items) -> str:
    return menu_items[selected_item]

def handle_return_key(key, selected_item, menu_items) -> str:
    if key[pygame.K_RETURN]:
        return get_menu_item(selected_item, menu_items)
    
def main_menu() -> str:
    """ Main menu display """
    pygame.display.set_caption("Menu")
    menu_items = ["start", "exit"]
    selected_item = 0

    run = True
    while run:
        main_menu_bg = pygame.image.load(os.path.join("img","background_main_menu.png")).convert()
        s.screen.blit(main_menu_bg, (0,0))

        for event in pygame.event.get():

            key = pygame.key.get_pressed()

            handle_events(event, key)

            selected_item = handle_input(key, selected_item, menu_items)

            return_item = handle_return_key(key, selected_item, menu_items)
            if return_item:
                return return_item

        game_title = s.font_b.render("PARKOUR", True, s.WHITE)
        s.screen.blit(game_title, (s.WIDTH*0.12,s.HEIGHT*0.40))
        
        for i, item in enumerate(menu_items):
            if i == selected_item:
                text = s.font_a.render(item, True, s.WHITE)
                pygame.draw.rect(s.screen, s.YELLOW, text.get_rect(center=(s.WIDTH*0.20, s.HEIGHT/2 + i * 50)), 2)
            else:
                text = s.font_a.render(item, True,s.GREY)
            s.screen.blit(text, text.get_rect(center=(s.WIDTH*0.20, s.HEIGHT/2 + i * 50)))
        
        # Controls tutorial
        move_keys = s.font_a.render("Press arrow keys to move and space to jump", True, s.WHITE)
        s.screen.blit(move_keys, (s.WIDTH*0.35,s.HEIGHT*0.60))
        jump_key = s.font_a.render("Space", True, s.YELLOW)
        s.screen.blit(jump_key, (s.WIDTH*0.70,s.HEIGHT*0.52))

        # Rendering
        s.clock.tick(s.FPS) 
        pygame.display.update()
    pygame.quit()

def start_game() -> str:
    pygame.display.set_caption("Parkour")
    space = pymunk.Space()
    game_setup = GameSetup(space)
    game_manager = GameManager(game_setup)
    game_manager.update_collision()

    run = True
    while run:
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            handle_events(event, key)
            
        # game running
        game_manager.run_game()

        # Rendering
        s.clock.tick(s.FPS) 
        pygame.display.update()
        # Update physics
        for x in range(1):
            space.step(s.dt)
    pygame.quit()

def main():
    selected_item = main_menu()

    while selected_item != "exit":
        if selected_item == "start":
            start_game()
        elif selected_item == "main_menu":
            selected_item = main_menu()

    pygame.quit()             

if __name__ == "__main__":
    pygame.init()                               
    main()
    sys.exit()