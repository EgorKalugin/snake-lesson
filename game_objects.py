from enum import Enum
from typing import Optional

import pygame as pg

vec2 = pg.math.Vector2


class MovingDirections(Enum):
    left = "left"
    right = "right"
    up = "up"
    down = "down"


class Snake:
    def __init__(self, size):
        self.size = size
        self.head = pg.rect.Rect(0, 0, size - 2, size - 2)

        self.direction = vec2(0, 0)
        self.locked_direction: Optional[MovingDirections] = None

        self.length = 1
        self.segments = []

    def move(self):
        self.head.move_ip(self.direction)
        self.segments.append(self.head.copy())
        # обрезаем змейку до ее длины
        self.segments = self.segments[-self.length :]

    def set_position(self, position):
        self.head.center = position

    def get_head_postion(self):
        return self.head

    def get_segments(self):
        return self.segments

    def change_moving_direction(self, new_direction: MovingDirections):
        if self.locked_direction == new_direction:
            return

        if new_direction == MovingDirections.up:
            self.direction = vec2(0, -self.size)
            self.locked_direction = MovingDirections.down
        elif new_direction == MovingDirections.down:
            self.direction = vec2(0, self.size)
            self.locked_direction = MovingDirections.up
        elif new_direction == MovingDirections.left:
            self.direction = vec2(-self.size, 0)
            self.locked_direction = MovingDirections.right
        elif new_direction == MovingDirections.right:
            self.direction = vec2(self.size, 0)
            self.locked_direction = MovingDirections.left

    def increase_snake_length(self):
        self.length += 1


class Food:
    def __init__(self, size):
        self.size = size
        self.body = pg.rect.Rect(0, 0, size - 2, size - 2)

    def get_postion(self):
        return self.body

    def set_position(self, position):
        self.body.center = position
