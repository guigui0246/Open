from typing import Callable, Sequence
import pygame
import os
import time


class Sprite():
    _path: os.PathLike
    _sprite: pygame.Surface
    _pos: tuple[int, int] = (0, 0)
    _size: tuple[int, int]

    def __init__(self, asset: os.PathLike) -> None:
        self._path = asset
        self._sprite = pygame.image.load(os.path.join(os.path.dirname(__file__), self._path))
        self._size = self._sprite.get_size()

    def show(self, show_function: Callable[[pygame.Surface, pygame.Surface, tuple[int, int], tuple[int, int]], None],
             screen: pygame.Surface, reverse: bool = False) -> None:
        sprite = self._sprite
        if reverse:
            sprite = pygame.transform.flip(sprite, 1, 0)
        show_function(screen, sprite, self._pos, self._size)

    @property
    # Size of the sprite
    def size(self) -> tuple[int, int]:
        return self._size

    @size.setter
    def size(self, value: pygame.Rect | Sequence[int]) -> None:
        if isinstance(value, pygame.Rect):
            self._size = value.size
            return
        if isinstance(value, Sequence):
            if len(value) != 2:
                raise IndexError("A Size value must have exactly 2 int values")
            if not (isinstance(value[0], int) and isinstance(value[1], int)):
                raise ValueError("Values are not all int")
            self._size = (value[0], value[1])
            return
        raise ValueError("Cannot parse value")

    @property
    # Position of the sprite
    def pos(self) -> tuple[int, int]:
        return self._pos

    @property
    # Position of the sprite
    def position(self) -> tuple[int, int]:
        return self._pos

    @position.setter
    def position(self, value: pygame.Rect | Sequence[int]) -> None:
        if isinstance(value, pygame.Rect):
            self._pos = (value.x, value.y)
            return
        if isinstance(value, Sequence):
            if len(value) != 2:
                raise IndexError("A Size value must have exactly 2 int values")
            if not (isinstance(value[0], int) and isinstance(value[1], int)):
                raise ValueError("Values are not all int")
            self._pos = (value[0], value[1])
            return
        raise ValueError("Cannot parse value")

    @pos.setter
    def pos(self, value: pygame.Rect | Sequence[int]) -> None:
        if isinstance(value, pygame.Rect):
            self._pos = (value.x, value.y)
            return
        if isinstance(value, Sequence):
            if len(value) != 2:
                raise IndexError("A Size value must have exactly 2 int values")
            if not (isinstance(value[0], int) and isinstance(value[1], int)):
                raise ValueError("Values are not all int")
            self._pos = (value[0], value[1])
            return
        raise ValueError("Cannot parse value")

    def __str__(self) -> str:
        return f"Sprite(file: {self._sprite}, size: {self.size}, pos: {self.pos})"


class AnimatedSprite(Sprite):
    _asset_list: Sequence[os.PathLike]
    _asset_id: int = 0
    _speed: float
    _clock: float = time.time()

    def __init__(self, assets: Sequence[os.PathLike], framerate: float) -> None:
        super().__init__(assets[0])
        self._asset_list = assets
        self._speed = framerate

    def show(self, show_function: Callable[[pygame.Surface, pygame.Surface, tuple[int, int], tuple[int, int]], None],
             screen: pygame.Surface, reverse: bool = False) -> None:
        while (time.time() - self._clock) > len(self._asset_list) * (1 / self._speed):
            self._clock += len(self._asset_list) * (1 / self._speed)
        while (time.time() - self._clock) > (1 / self._speed):
            self._asset_id += 1
            self._clock += (1 / self._speed)
        if len(self._asset_list) >= self._asset_id:
            self._asset_id = 0
        self._sprite = pygame.image.load(os.path.join(os.path.dirname(__file__), self._asset_list[self._asset_id]))
        Sprite.show(self, show_function, screen, reverse)

    @property
    # Speed of the animation in frame per second
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value: float) -> None:
        self._speed = value

    @property
    # Speed of the animation in frame per second
    def frame(self) -> float:
        return self._speed

    @frame.setter
    def frame(self, value: float) -> None:
        self._speed = value

    @property
    # Speed of the animation in frame per second
    def framerate(self) -> float:
        return self._speed

    @framerate.setter
    def framerate(self, value: float) -> None:
        self._speed = value
