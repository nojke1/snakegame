import pygame
import random

class GameObject:
    def __init__(self, x, y, color, size):
        self.x = x
        self.y = y
        self.color = color
        self.size = size

    def draw(self, screen):
        raise NotImplementedError("")

    def update(self):
        pass

class Snake(GameObject):
    def __init__(self, color, size, start_x, start_y):
        super().__init__(start_x, start_y, color, size)
        self.x_change = 0
        self.y_change = 0
        self.snake_list = []
        self.length = 1

    def update(self):
        self.x += self.x_change
        self.y += self.y_change

        snake_head = [self.x, self.y]
        self.snake_list.append(snake_head)
        if len(self.snake_list) > self.length:
            del self.snake_list[0]

    def draw(self, screen):
        for segment in self.snake_list:
            pygame.draw.rect(screen, self.color, [segment[0], segment[1], self.size, self.size])

    def check_collision(self, game_area_rect):
        snake_head_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        if not game_area_rect.contains(snake_head_rect):
            return True

        snake_head = [self.x, self.y]
        for segment in self.snake_list[:-1]:
            if segment == snake_head:
                return True
        return False

    def grow(self):
        self.length += 1

    def change_direction(self, key, block_size):
         if key == pygame.K_LEFT and self.x_change == 0:
            self.x_change = -block_size
            self.y_change = 0
         elif key == pygame.K_RIGHT and self.x_change == 0:
            self.x_change = block_size
            self.y_change = 0
         elif key == pygame.K_UP and self.y_change == 0:
            self.y_change = -block_size
            self.x_change = 0
         elif key == pygame.K_DOWN and self.y_change == 0:
            self.y_change = block_size
            self.x_change = 0

class Food(GameObject):
    def __init__(self, color, size, game_area_rect):
        self.game_area_rect = game_area_rect
        x, y = self._generate_pos_in_rect(size)
        super().__init__(x, y, color, size)

    def _generate_pos_in_rect(self, size):
        rand_x = random.randrange(self.game_area_rect.left, self.game_area_rect.right - size, size)
        rand_y = random.randrange(self.game_area_rect.top, self.game_area_rect.bottom - size, size)
        x = round(rand_x / float(size)) * size
        y = round(rand_y / float(size)) * size
        x = max(self.game_area_rect.left, min(x, self.game_area_rect.right - size))
        y = max(self.game_area_rect.top, min(y, self.game_area_rect.bottom - size))
        return x, y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.size, self.size])

    def generate_new_position(self):
        self.x, self.y = self._generate_pos_in_rect(self.size)

class FoodFactory:
    @staticmethod
    def create_food(food_type, color, size, game_area_rect):
        if food_type == "standard":
            return Food(color, size, game_area_rect)
        else:
            raise ValueError(f"Unknown food type: {food_type}")

class HighScoreManager:
    def __init__(self, filename="highscore.txt"):
        self.filename = filename

    def load_high_score(self):
        try:
            with open(self.filename, 'r') as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self, score):
        try:
            with open(self.filename, 'w') as f:
                f.write(str(score))
        except IOError:
            print(f"Error: Could not save high score to {self.filename}")

class Game:
    def __init__(self, screen_width, screen_height):
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake Game")
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.snake_block = 10
        self.score_font = pygame.font.SysFont("comicsansms", 35)
        self.message_font = pygame.font.SysFont("bahnschrift", 25)
        self.clock = pygame.time.Clock()
        self.top_margin = 50
        self.game_area_rect = pygame.Rect(0, self.top_margin, self.screen_width, self.screen_height - self.top_margin)
        self.game_speed = 15

        start_x = self.game_area_rect.centerx
        start_y = self.game_area_rect.centery
        start_x = round(start_x / self.snake_block) * self.snake_block
        start_y = round(start_y / self.snake_block) * self.snake_block
        start_x = max(self.game_area_rect.left, min(start_x, self.game_area_rect.right - self.snake_block))
        start_y = max(self.game_area_rect.top, min(start_y, self.game_area_rect.bottom - self.snake_block))
        self.snake = Snake(self.black, self.snake_block, start_x, start_y)
        self.food = FoodFactory.create_food("standard", self.green, self.snake_block, self.game_area_rect)
        self.high_score_manager = HighScoreManager()
        self.high_score = self.high_score_manager.load_high_score()

    def display_score(self, score):
        score_text = f"Score: {score}"
        high_score_text = f"High Score: {self.high_score}"
        score_value = self.score_font.render(score_text, True, self.black)
        high_score_value = self.score_font.render(high_score_text, True, self.black)
        self.screen.blit(score_value, [10, 5])
        self.screen.blit(high_score_value, [self.screen_width - high_score_value.get_width() - 10, 5])

    def display_message(self, msg, color):
        mesg = self.message_font.render(msg, True, color)
        mesg_rect = mesg.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
        self.screen.blit(mesg, mesg_rect)

    def game_loop(self):
        game_over = False
        game_close = False

        start_x = self.game_area_rect.centerx
        start_y = self.game_area_rect.centery
        start_x = round(start_x / self.snake_block) * self.snake_block
        start_y = round(start_y / self.snake_block) * self.snake_block
        start_x = max(self.game_area_rect.left, min(start_x, self.game_area_rect.right - self.snake_block))
        start_y = max(self.game_area_rect.top, min(start_y, self.game_area_rect.bottom - self.snake_block))
        self.snake = Snake(self.black, self.snake_block, start_x, start_y)
        self.food.generate_new_position()

        while not game_over:

            while game_close:
                current_score = self.snake.length - 1
                if current_score > self.high_score:
                    self.high_score = current_score
                    self.high_score_manager.save_high_score(self.high_score)

                self.screen.fill(self.white)
                self.display_message("You Lost! Press C-Play Again or Q-Quit", self.red)
                self.display_score(current_score)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            self.game_loop()
                    if event.type == pygame.QUIT:
                        game_over = True
                        game_close = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    self.snake.change_direction(event.key, self.snake_block)

            self.snake.update()

            if self.snake.check_collision(self.game_area_rect):
                game_close = True

            if self.snake.x == self.food.x and self.snake.y == self.food.y:
                self.food.generate_new_position()
                self.snake.grow()

            self.screen.fill(self.white)

            pygame.draw.rect(self.screen, self.blue, self.game_area_rect, 2)

            self.food.draw(self.screen)
            self.snake.draw(self.screen)

            self.display_score(self.snake.length - 1)

            pygame.display.update()
            self.clock.tick(self.game_speed)

        pygame.quit()
        quit()

if __name__ == "__main__":
    game_instance = Game(600, 480)
    game_instance.game_loop()