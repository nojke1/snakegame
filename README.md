# Snake Game

## Description

This is a classic snake game implemented in Python using the Pygame library. The objective of the game is to control the snake to eat the food, growing longer with each piece of food consumed. The game ends when the snake collides with the walls or itself.

## Git and GitHub

To use Git and upload your work to GitHub, follow these steps:

1.  Initialize a Git repository (if you haven't already):
```bash
git init
```
2.  Add the files to the repository:
```bash
git add .
```
3.  Commit the changes:
```bash
git commit -m "Your commit message"
```
4.  Create a repository on GitHub (if you haven't already).
5.  Link the local repository to the remote repository (if you haven't already):
```bash
git remote add origin <repository_url>
```
6.  Push the changes to GitHub:
```bash
git push -u origin master
```
   *  If you are using a different branch name (e.g., main), replace `master` with your branch name.
   *  The `-u` flag sets up tracking between your local branch and the remote branch, so you only need to use `git push` in the future.

To push updates to GitHub after making changes:

1.  Add the changed files to the repository:
```bash
git add .
```
2.  Commit the changes:
```bash
git commit -m "Your commit message"
```
   * Replace "Your commit message" with a descriptive message about the changes you made.
3.  Push the changes to GitHub:
```bash
git push
```

## How to Play

1.  Make sure you have Python installed on your system.
2.  Install the Pygame library: 
```bash
pip install pygame
```
3.  Run the game: 
```bash
python snake_game.py
```
4.  Use the arrow keys to control the snake's movement.

## Features

*   Classic snake gameplay
*   Score tracking
*   Collision detection
*   Simple and intuitive controls

## OOP Pillars

The game demonstrates the four OOP pillars:

*   **Abstraction:** The `GameObject` class is an abstract class that defines the basic properties and methods for all game objects. The `draw` method is an abstract method that must be implemented by subclasses.
*   **Inheritance:** The `Snake` and `Food` classes inherit from the `GameObject` class.
*   **Polymorphism:** The `draw` method is implemented differently in the `Snake` and `Food` classes.
*   **Encapsulation:** The `Snake` and `Food` classes encapsulate their own data and behavior.

## Design Pattern

The `FoodFactory` class implements the Factory design pattern. This pattern is used to create different types of food objects.

## Composition

The `Game` class uses composition to create instances of the `Snake`, `Food`, and `HighScoreManager` classes.

## File Reading/Writing

The `HighScoreManager` class reads and writes the high score to a file named `highscore.txt`.

## Testing

The project includes a testing file, `test_snake_game.py`, which contains unit tests for the game logic. To run the tests, you need to have pytest installed. You can install it using pip:

```bash
pip install pytest
```

Then, you can run the tests using the following command:

```bash
pytest
```

## Code Style

The code follows PEP8 style guidelines.

## License

This project is licensed under the MIT License.
