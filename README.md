# Parkour
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

**NOTE:**
You can press `ESC` at anytime to fully **exit** the game.

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

- `game_components/` : A package containing all the relevant components. Each component is designed to handle a specific aspect of the game, and they work together to create a complete game environment.

	- `character.py`: A module that is responsible for creating the character, character movement and character jump function. It also assigns the keyboard controls for the user to control the character.
	
	- `platform_manager.py`: A class that is responsible for creating the platforms, and setting their behaviour. That includes the random spawn locations, and movement.
	
	 - `mechanics.py`: A class responsible for setting the score, checking the game status and restarting the game.
	
	 - `collision.py`:  Class responsible for assigning what types of collision should happen between the character and platform and deciding how they should interact with each other.
	
	 - `scroll_system.py`: Class responsible for creating the infinite scroll effect in the game. This class handles the scrolling of the game world, including the movement of the camera and the platforms. It also keeps track of the platforms that the character has passed.
	
	 - `walls.py`: Class responsible for creating the walls of the game to prevent the character from going out of bounds from the sides and creates a bounce effect when colliding with the character to boost velocity.

- `game_setup.py`: Class responsible for setting up the game environment. This includes adding the character, platforms, and walls into the **Pymunk** space. 

	 `Spaces are the basic simulation unit in Pymunk. You add bodies, shapes and constraints to a space, and then update the space as a whole. They control how all the rigid bodies, shapes, and constraints interact together.`*([source](http://www.pymunk.org/_/downloads/en/latest/pdf/), see Section 8.2.1)*
	
- `game_manager.py`:  Class is responsible for managing the game state, including the character, platforms, scrolling, and game mechanics. It also handles the rendering of game elements and the game over screen.

- `images.py`: Class responsible for loading all the images.

- `project.py`: This is the main driver of the game. It handles the game's main loop, user inputs, and game states. It also manages the game's main menu and the transition between the menu and the game. The game continues to run until the user chooses to exit.

- `settings.py`: All constant variables that are used in more than one class, function or file is stored here, these are not to be changed. Some extra settings included are the **Pygame** and **Pymunk** settings.

- `scale_objects.py`: All constant variables that are used in different shapes and objects. These are not to be changed. All variables are scaled here in relation to the display size. The way they are scaled is based on the percentage of their width and heights to the current display size.

- `test_project.py`: Description goes here

### Design Choices

The primary libraries used in this project are **Pygame** and **Pymunk**. **Pygame** was chosen due to its simplicity and ease of learning, making it an ideal choice for creating the game's graphical user interface. **Pymunk**, a physics engine, was selected because its capabilities matched the gameplay style envisioned for this project.

The code structure was designed with clarity and modularity in mind. Each class has a distinct role and can function independently, with the exception of the `game_manger` class. This approach makes it easier to understand the purpose of each class and allows for individual testing, development and modification.

Inheritance was intentionally avoided in the design. Although the classes interact with each other, there was no need for a shared variable across all classes. Instead, shared instance variables between two or more classes are stored in `scale_objects.py`.

This design choice led to the use of dependency injection, which further enhances the modularity of the code. It allows each component to be worked on and tested individually using mock objects. This approach not only simplifies the development process but also makes the code more maintainable and easier to debug.

### Built With

- [Python](https://www.python.org) - The main programming language used.
- [Pygame](https://www.pygame.org/news) - A set of Python modules designed for writing video games.
- [Pymunk](https://www.pymunk.org/en/latest/) - A wrapper around the Chipmunk physics library, providing physics simulation functionality.
- [Pytest](https://docs.pytest.org/en/7.4.x/) - A testing framework used to create simple and scalable test cases.
- [Mock](https://docs.python.org/3/library/unittest.mock.html) - A library for testing in Python, allowing you to replace parts of your system under test and make assertions about how they have been used. 

### Tests

The tests for the project were made using **Pytest** and the **Mock** library from **Python**. Automating tests for **Pygame** and **Pymunk** functions can be a little tricky, so the individual class methods were tested in a mock environment of the game. The tests include:
- `main_menu` selection functions are working as needed in the `project.py`
- Collision between the character and platform as specified in `collision.py`.
- Character `movement` and `jump` keys, checks if the character moves correctly when the corresponding keys are pressed.
- Platform movement.
- `Score` based on game state.
- `Game Over` was activating at the correct time.
- Game `Scroll` was working correctly based on both the `Character` position and the auto scroll based on the game state.

To run the `test_project.py` you simply need open the `terminal` of the **ide** of your choice and type:

```
pytest test_project.py
```

When running the test you should run into 2 `warnings`, they are from the `random` library and don't affect the test or the game itself. But if you wish to remove the warning just run **Pytest** like this  in the `terminal` :

```
pytest -p no:warnings test_project.py
```

**NOTE:**
Further details of what each test does can be found in the `test_project.py` file. 
Running the test with no warnings is not recommended.
### License

```
The license your project is under.
```

### Acknowledgments 

- Font used in the project: **ARCADE.TTF** by **Jakob Fischer**. You can find more of their work [here](www.pizzadude.dk). Please note that this font is used for non-commercial purposes in this project.