import os
from typing import List, Sequence
import pygame


class spritesheet():

    """Downloaded from pygame.org
    Updated to follow project policie"""

    def __init__(self, filename: os.PathLike):
        self.sheet = pygame.image.load(os.path.join(os.path.dirname(__file__), filename))

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle: pygame.Rect) -> pygame.Surface:
        "Loads image from x, y, x + offset, y + offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.fill((0, 0, 0, 0))
        image.blit(self.sheet, (0, 0), rect)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects: Sequence[pygame.Rect]) -> List[pygame.Surface]:
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect: pygame.Rect, image_count: int) -> List[pygame.Surface]:
        "Loads a strip of images and returns them as a list"
        tups = [pygame.Rect(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups)
