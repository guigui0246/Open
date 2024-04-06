from typing import Callable, Sequence
import pygame
import os


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
             screen: pygame.Surface) -> None:
        show_function(screen, self._sprite, self._pos, self._size)

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
            self._size = tuple(value)
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
            self._pos = tuple(value)
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
            self._pos = tuple(value)
            return
        raise ValueError("Cannot parse value")

    def __str__(self) -> str:
        return f"Sprite(file: {self._sprite}, size: {self.size}, pos: {self.pos})"
