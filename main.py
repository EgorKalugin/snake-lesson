import sys
from random import randrange

import pygame as pg

from game_objects import Food, MovingDirections, Snake, vec2


class GameSettings:
    def __init__(self):
        self.WINDOW_SIZE = 750  # можно 1000
        self.TILE_SIZE = 50
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()

        self.step_delay = 150  # мсек. Скорость обновления змейки
        self.time = 0


class GameModel(GameSettings):
    def new_game(self):
        self.food = Food(self.TILE_SIZE)
        self.snake = Snake(self.TILE_SIZE)
        self.set_random_snake_position()
        self.set_random_food_position()

    def update_snake(self):
        self.snake.move()

    def delta_time(self):
        """Проверка времени, чтобы змейка двигалась не так быстро"""
        time_now = pg.time.get_ticks()
        if time_now - self.time > self.step_delay:
            self.time = time_now
            return True
        return False

    def change_snake_moving_direction(self, direction: MovingDirections):
        self.snake.change_moving_direction(direction)

    def check_borders(self):
        snake_position = self.snake.get_head_postion()
        if snake_position.left < 0 or snake_position.right > self.WINDOW_SIZE:
            self.new_game()
        elif snake_position.top < 0 or snake_position.bottom > self.WINDOW_SIZE:
            self.new_game()

    def update(self):
        if self.delta_time():
            self.update_snake()
        self.check_food()
        self.check_borders()
        self.check_snake_selfeating()

        pg.display.flip()
        self.clock.tick(60)

    def get_random_position(self):
        return [
            randrange(self.TILE_SIZE // 2, self.WINDOW_SIZE - self.TILE_SIZE // 2, self.TILE_SIZE),
            randrange(self.TILE_SIZE // 2, self.WINDOW_SIZE - self.TILE_SIZE // 2, self.TILE_SIZE),
        ]
        # [625, 325] - пример

    def set_random_food_position(self):
        self.food.set_position(self.get_random_position())

    def set_random_snake_position(self):
        self.snake.set_position(self.get_random_position())

    def check_food(self):
        if self.snake.get_head_postion() == self.food.get_postion():
            self.snake.increase_snake_length()
            self.set_random_food_position()

    def check_snake_selfeating(self):
        body = self.snake.get_segments()[:-1]
        if self.snake.get_head_postion() in body:
            self.new_game()


class GameController(GameSettings):
    def __init__(self, model: GameModel):
        GameSettings.__init__(self)
        self.model = model

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                self.change_snake_direction(event)

    def change_snake_direction(self, event):
        if event.key == pg.K_w:
            self.model.change_snake_moving_direction(MovingDirections.up)
        elif event.key == pg.K_s:
            self.model.change_snake_moving_direction(MovingDirections.down)
        elif event.key == pg.K_a:
            self.model.change_snake_moving_direction(MovingDirections.left)
        elif event.key == pg.K_d:
            self.model.change_snake_moving_direction(MovingDirections.right)


class GameVeiw(GameSettings):
    def __init__(self, model: GameModel, controller: GameController):
        GameSettings.__init__(self)
        self.model = model
        self.controller = controller
        self.model.new_game()

    def draw_grid(self):
        [
            pg.draw.line(self.screen, [50] * 3, (x, 0), (x, self.WINDOW_SIZE))
            for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE)
        ]
        [
            pg.draw.line(self.screen, [50] * 3, (0, y), (self.WINDOW_SIZE, y))
            for y in range(0, self.WINDOW_SIZE, self.TILE_SIZE)
        ]

    def draw(self):
        # рисуеп поле
        self.screen.fill("black")
        self.draw_grid()
        # рисуем змейку
        [
            pg.draw.rect(self.screen, "green", segment)
            for segment in self.model.snake.get_segments()
        ]
        # рисуем еду
        pg.draw.rect(self.screen, "red", self.model.food.get_postion())

    def run_game(self):
        while True:
            self.controller.check_events()
            self.model.update()
            self.draw()


if __name__ == "__main__":
    model = GameModel()
    controller = GameController(model=model)
    view = GameVeiw(model=model, controller=controller)
    view.run_game()
