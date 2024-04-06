from os import PathLike
from typing import List, Sequence
from sprite import Sprite
import pygame


class Map(Sprite):
    _collisions: List[pygame.Rect]

    def __init__(self, asset: PathLike) -> None:
        super().__init__(asset)

    @property
    # Speed of the animation in frame per second
    def collisions(self) -> List[pygame.Rect]:
        return self._collisions

    @collisions.setter
    def collisions(self, value: Sequence[pygame.Rect]) -> None:
        if not isinstance(value, Sequence):
            raise ValueError("Cannot parse value")
        for i in value:
            if not isinstance(i, pygame.Rect):
                raise ValueError("Cannot parse value")
        self._collisions = []
        for i in value:
            self._collisions.append(pygame.Rect(i))
