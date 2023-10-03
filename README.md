# Parkour v.0.4
#### Video Demo: <>
### Overview

Parkour is a 2D platformer game written in python using **Pygame** and **Pymunk**, it was inspired by the 2001 game *Icy Tower* by Johan Pietz and a favorite childhood game of mine. The game's name and character design are parodies from an episode of the famous TV show, *The Office* (US version), where one of the main characters Micheal Scott was jumping off of furniture and screaming "parkour".  All sprites were made by me, but I do not have ownership of the character design in my game, and was just made for the fun of it. The platforms were designed after the 4 elements: fire, water, earth, and air. 
### Gameplay

The game features the character in a tower-like environment, the goal is to climb as high as you can. The user has to use the directional **left** and **right**  keys to move the character respectively, and the **space** key to jump. The character is able to reach higher platforms by gaining some speed before jumping, and can bounce off of walls . As the player progresses higher the platforms changes *elements*, once reaching the last element the order of elements starts all over again. The game will first begin by following the character as they go up, but after a certain number of platforms have passed, a timer is activated and the screen starts automatically scrolling up, every second gradually scrolls a bit faster until it reaches a max scroll speed. The **score** is calculated by number of platforms the user has passed. 
### Installation

1. Clone the repository to your local machine.
2. Navigate to the **project** directory.
3. Install the necessary libraries by running the following command:
	`pip install -r requirements.txt`

 For more detailed instructions on installing the libraries used in this project, refer to the official guides:

 - [Pygame Installation Guide](https://www.pygame.org/wiki/GettingStarted)
 - [Pymunk Installation Guide](https://www.pymunk.org/en/latest/installation.html)
 - [Pytest Installation Guide](https://docs.pytest.org/en/7.4.x/getting-started.html)

 **NOTE:**
 If you're using Linux or macOS, you might need to use `pip3` instead of `pip`:
 ```
 pip3 install -r requirements.txt
```
 If you're getting an error message about pip, please refer to the [official pip guide](https://pip.pypa.io/en/stable/getting-started/).
 
### How to play

- Use the up **(↑)** and down **(↓)** keys to navigate the ***main menu***.
- Press the return arrow **(↵)** to select a menu item.
- Use the left arrow **(←)** and right arrow **(→)** keys to move your character.
- Press the `Space` key to jump.
- The objective of the game is to climb as **high** as you can.
- Be careful not to **fall**!
### Project Structure

**Here is a brief overview of the structure of the project:**

	project_root/
	├── game_components/
	│   ├── __init__.py
	│   ├── character.py
	│   ├── platform_manager.py
	│   ├── mechanics.py
	│   ├── collision.py
	│   ├── scroll_system.py
	│   └── walls.py
	├── game_setup.py
	├── game_manager.py 
	├── images.py
	├── project.py
	├── settings.py
	├── scale_objects.py
	└── test_project.py

**A description of what each component does:**

- `game_components/` : This directory contains all the game components
	- `character.py`: Description goes here
	- `platform_manager.py`: Description goes here
	- `mechanics.py`: Description goes here
	- `collision.py`: Description goes here
	- `scroll_system.py`: Description goes here
	- `walls.py`: Description goes here
- `game_setup.py`: Description goes here
- `game_manager.py`: Description goes here
- `images.py`: Description goes here
- `project.py`: Description goes here
- `settings.py`: Description goes here
- `scale_objects.py`: Description goes here
- `test_project.py`: Description goes here

### Design Choices

```
What design choices where made and why.
```
### Built With

```
What was used to build the project.
```
### Tests

```
How to run any tests you have for your project.
```
### License

```
The license your project is under.
```
### Acknowledgments 

```
Any credits or acknowledgements you want to give.
```
