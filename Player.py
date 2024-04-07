import os
import pygame
from os import PathLike
from typing import Callable, Sequence
from debug import debug
from sprite import AnimatedSprite, Sprite
from map import Map

GRAVITY: float = .2
JUMP_HEIGHT = GRAVITY * 45
SPRITES_STILL: PathLike = "./assets/chest_front.png"
SPRITES_RIGHT: PathLike = "./assets/chest_direction_right.png"
DIRECTION_LEFT: int = 1
DIRECTION_RIGHT: int = 2
DIRECTION_STILL: int = 3


class Player(AnimatedSprite):
    _on_ground: bool = False
    _gravity: float = 0
    _jump: float = 0
    _speed_move: float = 0
    _direction: int = DIRECTION_STILL

    def __init__(self, framerate: float, starting_position: pygame.Rect | Sequence[int]) -> None:
        super().__init__([SPRITES_STILL], framerate)
        self.pos = starting_position

    def jump(self) -> None:
        if self.can_jump():
            self._jump += JUMP_HEIGHT

    def _update_on_ground(self, map: Map) -> None:
        rect = pygame.Rect(self.pos[0], self.pos[1] + self.size[1] + 1, self.size[0], 1)
        if len(rect.collidelistall(map.collisions)) != 0:
            debug(rect, "Collision with")
            for i in rect.collidelistall(map.collisions):
                debug(map.collisions[i])
            debug("No more collisions")
            self._on_ground = True
        else:
            self._on_ground = False

    def against_wall(self, reverse: bool, map: Map) -> bool:
        if (reverse):
            rect = pygame.Rect(self.pos[0] - 1, self.pos[1], 1, self.size[1])
        else:
            rect = pygame.Rect(self.pos[0] + self.size[0], self.pos[1], 1, self.size[1])
        if len(rect.collidelistall(map.collisions)) != 0:
            debug(rect, "Collision with")
            for i in rect.collidelistall(map.collisions):
                debug(map.collisions[i])
            debug("No more collisions")
            return True
        return False

    def move(self, map: Map) -> None:
        debug()
        debug()
        debug("Player move() call ")
        self._update_on_ground(map)
        debug(f"{self._on_ground}")
        if self._on_ground and self._jump <= 0:
            self._gravity = 0
            self._jump = 0
        else:
            self._gravity += GRAVITY
            self._jump -= self._gravity
        debug(f"{self._gravity = } {self._jump = } {(self.pos[0], int(self.pos[1] - self._jump)) = }")
        jump: int = int(self._jump)
        while jump > 0:
            self.pos = (self.pos[0], int(self.pos[1] - 1))
            jump -= 1
            self._update_on_ground(map)
        while jump < 0:
            self.pos = (self.pos[0], int(self.pos[1] + 1))
            jump += 1
            self._update_on_ground(map)
            if self._on_ground:
                break
        reverse: bool = self._speed_move < 0
        x = abs(self._speed_move)
        if x > 0:
            if reverse:
                self._direction = DIRECTION_LEFT
            else:
                self._direction = DIRECTION_RIGHT
        else:
            self._direction = DIRECTION_STILL
        debug(f"{reverse = } {x = }")
        while x > 0:
            if self.against_wall(reverse, map):
                break
            self.pos = (self.pos[0] + (-1 if reverse else 1), self.pos[1])
            x -= 1
        debug()
        debug()

    def show(self, show_function: Callable[[pygame.Surface, pygame.Surface, tuple[int, int], tuple[int, int]], None],
             screen: pygame.Surface) -> None:
        debug(f"Showing player at {self.pos = } with {self.size = } and {self._direction = }")
        if self._direction != DIRECTION_STILL:
            self._sprite = pygame.image.load(os.path.join(os.path.dirname(__file__), SPRITES_RIGHT))
            Sprite.show(self, show_function, screen, self._direction == DIRECTION_LEFT)
        else:
            self._sprite = pygame.image.load(os.path.join(os.path.dirname(__file__), SPRITES_STILL))
            Sprite.show(self, show_function, screen)

    def can_jump(self) -> bool:
        return self._on_ground

    @property
    # Speed of the player movement
    def speed(self) -> float:
        return self._speed_move

    @speed.setter
    def speed(self, value: float) -> None:
        self._speed_move = value
