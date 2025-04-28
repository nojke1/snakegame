import unittest
import pygame
from snake_game import Snake, Food, Game, HighScoreManager
import os

pygame.init()
pygame.display.set_mode((1, 1))

class TestSnakeGame(unittest.TestCase):

    def setUp(self):
        self.screen_width = 600
        self.screen_height = 480
        self.block_size = 10
        self.game_area_rect_for_test = pygame.Rect(0, 50, self.screen_width, self.screen_height - 50)
        self.snake = Snake((0,0,0), self.block_size, self.screen_width / 2, self.screen_height / 2)
        self.food = Food((0,255,0), self.block_size, self.game_area_rect_for_test)
        self.game = Game(self.screen_width, self.screen_height)
        self.highscore_manager = HighScoreManager("test_highscore.txt")

    def tearDown(self):
        if os.path.exists("test_highscore.txt"):
            os.remove("test_highscore.txt")
        pygame.quit()

    def test_snake_initialization(self):
        self.assertEqual(self.snake.x, self.screen_width / 2)
        self.assertEqual(self.snake.y, self.screen_height / 2)
        self.assertEqual(self.snake.length, 1)
        self.assertEqual(self.snake.x_change, 0)
        self.assertEqual(self.snake.y_change, 0)

    def test_snake_movement(self):
        initial_x = self.snake.x
        initial_y = self.snake.y

        self.snake.change_direction(pygame.K_RIGHT, self.block_size)
        self.snake.update()
        self.assertEqual(self.snake.x, initial_x + self.block_size)
        self.assertEqual(self.snake.y, initial_y)

        self.snake.change_direction(pygame.K_DOWN, self.block_size)
        self.snake.update()
        self.assertEqual(self.snake.x, initial_x + self.block_size)
        self.assertEqual(self.snake.y, initial_y + self.block_size)

    def test_snake_grow(self):
        initial_length = self.snake.length
        self.snake.grow()
        self.assertEqual(self.snake.length, initial_length + 1)

    def test_food_generation(self):
        initial_x = self.food.x
        initial_y = self.food.y
        self.food.generate_new_position()
        self.assertTrue(self.food.x != initial_x or self.food.y != initial_y)
        self.assertTrue(self.game_area_rect_for_test.left <= self.food.x < self.game_area_rect_for_test.right)
        self.assertTrue(self.game_area_rect_for_test.top <= self.food.y < self.game_area_rect_for_test.bottom)

    def test_wall_collision(self):
        game_area = self.game.game_area_rect

        self.snake.x = game_area.left - self.block_size
        self.snake.y = game_area.centery
        self.assertTrue(self.snake.check_collision(game_area))

        self.snake.x = game_area.right
        self.snake.y = game_area.centery
        self.assertTrue(self.snake.check_collision(game_area))

        self.snake.x = game_area.centerx
        self.snake.y = game_area.top - self.block_size
        self.assertTrue(self.snake.check_collision(game_area))

        self.snake.x = game_area.centerx
        self.snake.y = game_area.bottom
        self.assertTrue(self.snake.check_collision(game_area))

    def test_self_collision(self):
        game_area = self.game.game_area_rect
        start_x = game_area.centerx
        start_y = game_area.centery
        self.snake.x = start_x
        self.snake.y = start_y
        self.snake.length = 4
        self.snake.snake_list = [
            [start_x, start_y],
            [start_x - self.block_size, start_y],
            [start_x - 2 * self.block_size, start_y],
            [start_x, start_y]
        ]
        for seg in self.snake.snake_list:
             self.assertTrue(game_area.contains(pygame.Rect(seg[0], seg[1], self.block_size, self.block_size)))

        self.assertTrue(self.snake.check_collision(game_area))

    def test_highscore_manager(self):
        self.assertEqual(self.highscore_manager.load_high_score(), 0)
        self.highscore_manager.save_high_score(123)
        self.assertTrue(os.path.exists("test_highscore.txt"))
        self.assertEqual(self.highscore_manager.load_high_score(), 123)
        self.highscore_manager.save_high_score(456)
        self.assertEqual(self.highscore_manager.load_high_score(), 456)

if __name__ == '__main__':
    unittest.main()
